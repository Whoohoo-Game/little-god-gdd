"""
Mô hình bầy đàn / đơn độc và nhịp sinh sản cho GDD 13. Dùng chung mọi luật của biomesim.py (GDD 12), chỉ thay
phần động vật: cách di chuyển (đích + nghỉ, theo bầy hoặc theo lãnh thổ), ai được sinh sản, và số liệu sinh sản.
Thông số ở balance.json → "social".

    python3 Docs/GDD/sim/socialsim.py survey [seeds] [old]   # old: luật cũ (đi ngẫu nhiên mỗi phút) để so sánh
    python3 Docs/GDD/sim/socialsim.py survey [seeds] standing  # vai trò tính theo chỗ đứng thay vì vùng sống (GDD 13 §5)
"""
import sys

import worldsim as ws
import biomesim as bs
from worldsim import Animal, ANIMALS, NAME, HUNGRY_BELOW, FORAGE_SIGHT, DORMANT_FOOD, START_HUNGER

SOC = ws.B["social"]
KIND = {NAME[k]: v for k, v in SOC["species"].items()}        # tên loài → luật xã hội ("herd" / "solitary")
BREED_SEASON = ws._by_season(SOC["breedSeason"])
BREED_ABOVE = SOC["breedAbove"]


def use_social_breeding():
    """Nhịp sinh sản mới ghi đè bảng loài (chỉ khi chạy luật mới, để "old" giữ đúng luật cũ)."""
    for _id, sp in SOC["species"].items():
        if "cooldownMinutes" in sp:
            ANIMALS[NAME[_id]]["cooldown"] = sp["cooldownMinutes"]
        if "litter" in sp:
            ANIMALS[NAME[_id]]["litter"] = sp["litter"]
        if "minutesPerCatch" in sp:
            ANIMALS[NAME[_id]]["need"] = 1 / sp["minutesPerCatch"]


ROLES_BY_RANGE = True


class Herd:
    def __init__(self, name, anchor, pond=None):
        self.name, self.anchor, self.pond = name, anchor, pond
        self.members = []


class SocialWorld(bs.BiomeWorld):
    def __init__(self, seed, social=True, **kw):
        super().__init__(seed, **kw)
        self.social = social
        self.herds = []
        self.births, self.oldage = {}, {}
        self.moves = self.reversals = self.animal_minutes = 0
        self.full_herd_minutes = self.floater_minutes = 0
        self.roles_by_range = ROLES_BY_RANGE

    # ---- vị trí trung tâm và bán kính đi lại của một con ---------------------------
    def home_of(self, a):
        k = KIND[a.name]
        if k["social"] == "herd":
            return a.herd.anchor, k["spread"]
        center = a.den if a.den is not None else a.natal if a.natal is not None else a.x
        return center, k["territory"]

    def pick_goal(self, a, center, radius):
        lo, hi = self.bounds(a)
        k = KIND[a.name]
        avoid = k.get("avoid", 0)
        others = [o.x for o in self.by_name.get(a.name, ()) if o is not a and not o.gone and o.den != a.den] if avoid else ()
        goal = center
        for _ in range(4):
            goal = max(lo, min(hi, center + self.rng.randint(-radius, radius)))
            if not any(abs(goal - x) < avoid for x in others):
                break
        return goal

    def move(self, a):
        """Đi tới đích rồi nghỉ một lúc, rồi chọn đích mới quanh trung tâm (anchor của bầy / hang)."""
        k = KIND[a.name]
        center, radius = self.home_of(a)
        if a.goal is None or abs(a.goal - center) > radius:
            a.goal = self.pick_goal(a, center, radius)
        lost = abs(a.x - center) > radius + 1        # tụt khỏi bầy / ra ngoài lãnh thổ: đi về ngay, không nghỉ
        if a.rest > 0 and not lost:
            a.rest -= 1
            return a.x
        if a.x == a.goal:
            a.rest = self.rng.randint(k["restMin"], k["restMax"])
            a.goal = self.pick_goal(a, center, radius)
            return a.x
        step = min(k["speed"], abs(a.goal - a.x))
        return a.x + (step if a.goal > a.x else -step)

    def hungry_hunter_goal(self, a, prey):
        """Diệc đói bay tới bầy cá gần nhất (như worldsim.hunter_move); cáo săn trong lãnh thổ."""
        near = [r.x for r in prey if not r.gone and abs(r.x - a.x) <= ws.HOMING_SIGHT]
        if near:
            a.goal = min(near, key=lambda x: abs(x - a.x))
            a.rest = 0

    # ---- bầy: tạo, gia nhập, dời anchor, tách bầy ----------------------------------
    def herd_for(self, a):
        k = KIND[a.name]
        for h in self.herds:
            if h.name == a.name and h.pond == a.pond and abs(h.anchor - a.x) <= 2 * k["spread"] and len(h.members) < k["groupMax"]:
                return h
        h = Herd(a.name, a.x, a.pond)
        self.herds.append(h)
        return h

    def best_food(self, h, x):
        k = KIND[h.name]
        food = ANIMALS[h.name]["food"]
        lo, hi = self.zones[h.pond].water if h.pond is not None else (self.L, self.R)
        best, best_f = x, -1.0
        for i in range(max(lo, x - FORAGE_SIGHT), min(hi, x + FORAGE_SIGHT) + 1):
            f = 0.0
            for j in range(max(lo, i - k["spread"]), min(hi, i + k["spread"]) + 1):
                g = self.cols[j].layers[0]
                if g and g.name == food and g.mature:
                    f += g.biomass * (DORMANT_FOOD if g.dormant else 1)
            # bầy khác đã ở đó: cỏ coi như ít hơn, nên các bầy giãn ra
            if any(o is not h and o.name == h.name and abs(o.anchor - i) < k["herdSpacing"] for o in self.herds):
                f *= 0.3
            if f > best_f or (f == best_f and abs(i - x) < abs(best - x)):
                best, best_f = i, f
        return best, best_f

    def steer_herds(self):
        for h in self.herds:
            k = KIND[h.name]
            hungry = sum(1 for m in h.members if m.hunger < HUNGRY_BELOW) * 2 >= len(h.members)
            together = all(abs(m.x - h.anchor) <= k["spread"] + 1 for m in h.members)
            if hungry and together and self.minute % k["anchorStepMinutes"] == 0:
                best, _ = self.best_food(h, h.anchor)
                if best != h.anchor:
                    h.anchor += 1 if best > h.anchor else -1

    def herd_room(self, h):
        """0..1: bãi cỏ quanh bầy (anchor ± spread + tầm ăn) còn nuôi thêm được bao nhiêu con."""
        k, sp = KIND[h.name], ANIMALS[h.name]
        lo, hi = self.zones[h.pond].water if h.pond is not None else (self.L, self.R)
        reach = k["spread"] + sp["range"]
        fsp = ws.PLANTS[sp["food"]]
        season = ws.GROWTH_SEASON[self.season]
        food = sum(fsp["regrow"] * bs.suitability(fsp, c) * season * ws.GRAZER_OVERSHOOT
                   for c in self.cols[max(lo, h.anchor - reach):min(hi, h.anchor + reach) + 1]
                   if c.layers[0] and c.layers[0].name == sp["food"] and c.layers[0].living)
        return max(0.0, min(1.0, 1 - len(h.members) / max(food / sp["need"], 0.01)))

    def capacity_room(self, a, count_in):
        if getattr(a, "herd", None) is not None:
            return self.herd_room(a.herd)
        return super().capacity_room(a, count_in)

    def split_herds(self):
        for h in list(self.herds):
            k = KIND[h.name]
            crowded = len(h.members) >= k["splitAt"] and self.herd_room(h) <= 0
            if len(h.members) < k["groupMax"] and not crowded:
                continue
            self.full_herd_minutes += 1
            site, f = self.best_food(h, h.anchor)
            far = all(abs(o.anchor - site) >= k["herdSpacing"] for o in self.herds if o.name == h.name)
            if not far or f <= 0:
                continue                    # không còn chỗ cho bầy mới: bầy giữ nguyên, không đẻ thêm (GDD 13 §3.2)
            adults = sorted((m for m in h.members if m.age >= m.spec["mature"]), key=lambda m: m.age)
            leave = adults[:len(h.members) // 2]
            if len(leave) < 2:
                continue
            new = Herd(h.name, site, h.pond)
            self.herds.append(new)
            for m in leave:
                h.members.remove(m)
                new.members.append(m)
                m.herd, m.goal, m.rest = new, None, 0

    # ---- hang của loài đơn độc ------------------------------------------------------
    def claim_dens(self):
        for name, k in KIND.items():
            if k["social"] != "solitary":
                continue
            animals = [a for a in self.by_name.get(name, ()) if not a.gone]
            dens = {}
            for a in animals:
                if a.den is not None:
                    dens.setdefault(a.den, []).append(a)
            for a in animals:
                if a.den is not None or a.age < a.spec["mature"]:
                    continue
                lo, hi = self.bounds(a)
                # ghép đôi: hang gần nhất mới có một con (loài sống theo cặp)
                single = [d for d, ms in dens.items() if len(ms) == 1 and abs(d - a.x) <= k["searchRange"]] if k.get("pairs") else []
                if single:
                    d = min(single, key=lambda d: abs(d - a.x))
                else:
                    free = [x for x in range(max(lo, a.x - k["searchRange"]), min(hi, a.x + k["searchRange"]) + 1)
                            if self.cols[x].alive and self.cols[x].ground == "land" and self.den_ok(name, x)
                            and all(abs(x - d) >= k["denSpacing"] for d in dens)]
                    if not free:
                        self.floater_minutes += 1
                        continue
                    prey = a.spec.get("prey_all")
                    if prey:
                        # thú săn làm hang nơi có nhiều mồi trong lãnh thổ nhất (gần hơn thì hơn khi bằng nhau)
                        score = {x: sum(1 for n in prey for r in self.by_name.get(n, ()) if abs(r.x - x) <= k["territory"]) for x in free}
                        free = [x for x in free if score[x] > 0]
                        if not free:
                            self.floater_minutes += 1
                            continue
                        d = min(free, key=lambda x: (-score[x], abs(x - a.x), x))
                    else:
                        d = min(free, key=lambda x: (abs(x - a.x), x))
                a.den, a.natal, a.goal, a.rest = d, None, None, 0
                dens.setdefault(d, []).append(a)

    def den_ok(self, name, x):
        if name == bs.SQUIRREL:     # sóc làm tổ trên sồi trưởng thành
            t = self.cols[x].layers[ws.TREE_LAYER]
            return bool(t and t.name == bs.OAK and t.mature)
        return True

    def region_stats(self):
        if self._stats_minute == self.minute:
            return self._regions
        regs = self.regions()
        for r in regs:
            r.update(counts={}, base=0.0, bare=0)
        for c in self.alive_cols():
            k = self.reg_of_col.get(c.i)
            if k is None:
                continue
            r = regs[k]
            cnt = r["counts"]
            if not any(c.layers):
                r["bare"] += 1
            for p in c.layers:
                if p:
                    cnt[p.name] = cnt.get(p.name, 0) + 1
                    if p.living:
                        r["base"] += p.spec["essence"]
            if c.worms:
                cnt["Giun"] = cnt.get("Giun", 0) + 1
                r["base"] += ws.WORM_ESSENCE
        for a in self.animals:
            k = self.reg_of_col.get(a.x)
            if k is None:
                continue
            r = regs[k]
            r["counts"][a.name] = r["counts"].get(a.name, 0) + 1
            if a.age >= a.spec["mature"]:
                r["base"] += a.spec["essence"]
        for r in regs:
            roles = {"sản xuất"} if any(n in ws.PLANTS for n in r["counts"]) else set()
            roles |= {ANIMALS[n]["role"] for n in r["counts"] if n in ANIMALS}
            if "Giun" in r["counts"]:
                roles.add("phân huỷ")
            if self.social and self.roles_by_range:
                # GDD 13 §5: con vật góp vai trò cho mọi đoạn mà vùng sống của nó (lãnh thổ, bãi của bầy) chạm tới
                for a in self.animals:
                    if a.name in KIND and getattr(a, "goal", None) is not None:
                        c, rad = self.home_of(a)
                        if c - rad < r["end"] and c + rad >= r["start"]:
                            roles.add(a.spec["role"])
            r["roles"] = roles
        for k, r in enumerate(regs):
            nbrs = [regs[j] for j in (k - 1, k + 1)
                    if 0 <= j < len(regs) and (regs[j]["end"] == r["start"] or regs[j]["start"] == r["end"])]
            r["nbrs"] = nbrs
            r["borrowed"] = set().union(*(n["roles"] for n in nbrs)) - r["roles"] if nbrs else set()
            r["mult"] = self.multipliers(r, nbrs)
        self._stats_minute = self.minute
        return regs

    # ---- một bước động vật -----------------------------------------------------------
    def animals_step(self, s):
        if not self.social:
            before = {id(a): a.x for a in self.animals}
            super().animals_step(s)
            self.track(before)
            return
        for a in self.animals:
            if not hasattr(a, "goal"):
                a.goal, a.rest, a.den, a.natal, a.herd, a.lastdir = None, 0, None, None, None, 0
        self.by_name = {}
        pos = {}
        for a in self.animals:
            pos.setdefault(a.name, []).append(a.x)
            self.by_name.setdefault(a.name, []).append(a)
        for v in pos.values():
            v.sort()

        def count_in(name, x, r):
            v = pos.get(name, ())
            return ws.bisect.bisect_right(v, x + r) - ws.bisect.bisect_left(v, x - r)

        for a in self.animals:
            if KIND.get(a.name, {}).get("social") == "herd" and a.herd is None:
                a.herd = self.herd_for(a)
                a.herd.members.append(a)
        if self.minute % 30 == 0:
            self.claim_dens()
        self.steer_herds()

        before = {id(a): a.x for a in self.animals}
        born = []
        for a in self.animals:
            if a.gone:
                continue
            sp = a.spec
            a.age += 1
            a.cooldown = max(0, a.cooldown - 1)
            self.animal_minutes += 1
            if sp["eats"] == "grass":
                self.graze(a, s)
            elif sp["eats"] == "rabbit":
                prey_all = self.hunt(a, s)
                if sp.get("homing") and a.hunger < HUNGRY_BELOW:
                    self.hungry_hunter_goal(a, prey_all)
            elif sp["eats"] == "nuts":
                oaks = sum(1 for c in self.near(a.x, sp["range"]) if c.layers[2] and c.layers[2].name == sp["nut_tree"] and c.layers[2].mature)
                a.hunger += ws.POLLINATOR_FED if oaks >= sp["min_trees"] else -ws.POLLINATOR_DRAIN
            elif sp["eats"] == "nectar":
                flowers = sum(1 for c in self.near(a.x, sp["range"]) for p in c.layers if p and p.mature and p.spec["flower"])
                a.hunger += ws.POLLINATOR_FED if flowers >= ws.POLLINATOR_MIN_FLOWERS else -ws.POLLINATOR_DRAIN
            if a.name in KIND:
                a.x = self.move(a)
            a.hunger = max(0, min(100, a.hunger))
            if a.hunger <= ws.LEAVE_HUNGER:
                a.gone = True
                self.cols[a.x].detritus += sp["detritus"]
                self.starved[a.name] = self.starved.get(a.name, 0) + 1
                continue
            if a.age >= sp["life"]:
                a.gone = True
                self.cols[a.x].detritus += sp["detritus"]
                self.oldage[a.name] = self.oldage.get(a.name, 0) + 1
                continue
            if self.may_breed(a, count_in, s):
                a.cooldown = sp["cooldown"]
                for _ in range(sp["litter"]):
                    if a.herd is not None and KIND[a.name].get("capLitter") and len(a.herd.members) >= KIND[a.name]["groupMax"]:
                        break           # hang đầy thì lứa chỉ có số con vừa đủ chỗ (GDD 14 §2.1)
                    x = self.swarm_site(a, pos.get("Ong", [])) if a.name == "Ong" else a.x
                    child = Animal(a.name, x, age=0, pond=a.pond)
                    child.goal, child.rest, child.den, child.natal, child.herd, child.lastdir = None, 0, None, a.den, None, 0
                    if a.herd is not None:
                        child.herd = a.herd
                        a.herd.members.append(child)
                    born.append(child)
                    self.births[a.name] = self.births.get(a.name, 0) + 1
        for h in self.herds:
            h.members = [m for m in h.members if not m.gone]
        self.herds = [h for h in self.herds if h.members]
        self.split_herds()
        self.animals = [a for a in self.animals if not a.gone] + born
        self.track(before)

    def may_breed(self, a, count_in, s):
        sp = a.spec
        if a.hunger <= BREED_ABOVE or a.age < sp["mature"] or a.cooldown:
            return False
        k = KIND.get(a.name)
        if k and k["social"] == "herd":
            mates = sum(1 for m in a.herd.members if m is not a and m.age >= m.spec["mature"])
            if not mates or len(a.herd.members) >= k["groupMax"]:
                return False
        elif k and k["social"] == "solitary":
            if a.den is None:
                return False            # chưa có lãnh thổ thì không sinh sản
            if not k.get("pairs"):
                if count_in(a.name, a.x, sp["range"]) - 1 <= 0:
                    return False
                return self.rng.random() < ws.BREED_CHANCE * BREED_SEASON[s] * self.capacity_room(a, count_in)
            pair = [o for o in self.by_name[a.name] if o.den == a.den and not o.gone]
            if len(pair) < 2 or min(pair, key=lambda o: -o.age) is not a:
                return False            # mỗi hang một lứa: con lớn tuổi hơn trong cặp sinh
        elif count_in(a.name, a.x, sp["range"]) - 1 <= 0:
            return False
        return self.rng.random() < ws.BREED_CHANCE * BREED_SEASON[s] * self.capacity_room(a, count_in)

    def graze(self, a, s):
        sp = a.spec
        need = sp["need"]
        cols = [c for c in self.reach(a, sp["range"])
                if c.layers[0] and c.layers[0].name == sp["food"] and c.layers[0].mature and c.layers[0].biomass > ws.GRASS_FLOOR]
        cols.sort(key=lambda c: -c.layers[0].biomass)
        for c in cols:
            g = c.layers[0]
            value = DORMANT_FOOD if g.dormant else 1.0
            take = min(need / value, g.biomass - ws.GRASS_FLOOR)
            g.biomass -= take
            need -= take * value
            if need <= 0:
                break
        a.hunger += (sp["need"] - need) / sp["need"] * ws.FED_GAIN - ws.STARVE_DRAIN
        if a.hunger < HUNGRY_BELOW and self.near_fruit(a, s):
            a.hunger += ws.FRUIT_GAIN

    def hunt(self, a, s):
        sp = a.spec
        a.hunger -= 100 * sp["need"] * (ws.WINTER_PREDATOR_NEED if s == "Đông" else 1.0)
        prey_all = [r for n in sp["prey_all"] for r in self.by_name.get(n, ())]
        if a.hunger < HUNGRY_BELOW:
            prey = [r for r in prey_all if not r.gone and abs(r.x - a.x) <= sp["range"]]
            if len(prey) > ws.LAST_PAIR:
                r = self.rng.choice(prey)
                shelter = any(c.layers[1] for c in self.near(r.x, 1)) or self.cols[r.x].canopy > 0
                scarcity = min(1.0, len(prey) / ws.PREY_COMFORT)
                if self.rng.random() < ws.CATCH_BASE * scarcity * (ws.SHRUB_ESCAPE if shelter else 1.0):
                    r.gone = True
                    self.cols[r.x].detritus += ws.CATCH_DETRITUS
                    self.hunted[r.name] = self.hunted.get(r.name, 0) + 1
                    a.hunger = 100
            if a.hunger < HUNGRY_BELOW and self.near_fruit(a, s):
                a.hunger += ws.FRUIT_GAIN
        return prey_all

    def track(self, before):
        for a in self.animals:
            x0 = before.get(id(a))
            if x0 is None or x0 == a.x:
                continue
            d = 1 if a.x > x0 else -1
            last = getattr(a, "lastdir", 0)
            self.moves += 1
            if last == -d:
                self.reversals += 1
            a.lastdir = d
        if not self.social:
            self.animal_minutes += len(self.animals)


def survey(seeds=8, social=True):
    print("Luật:", "bầy đàn / đơn độc (GDD 13)" if social else "cũ (đi ngẫu nhiên mỗi phút)", "· giờ là giờ thật (×100)")
    print(f"{'seed':>4} {'Kết':>5} {'thỏ':>4} {'cáo':>4} {'sóc':>4} {'cá':>4} {'diệc':>4} "
          f"{'sinh/ng':>7} {'già/ng':>6} {'đói/ng':>6} {'săn/ng':>6} {'quay đầu':>8} {'đi/phút':>7} {'bầy':>4} {'cỡ bầy':>6} {'hang cáo':>8}")
    ends, rows = [], []
    for seed in range(1, seeds + 1):
        w = SocialWorld(seed, social=social)
        samples = []
        while w.minute < ws.MAX_HOURS * 60 and w.ending is None:
            w.step()
            if w.minute % 600 == 0:
                rabbit_herds = [h for h in w.herds if h.name == "Thỏ"]
                dens = {a.den for a in w.animals if a.name == "Cáo" and getattr(a, "den", None) is not None}
                samples.append([w.count_animal(n) for n in ("Thỏ", "Cáo", bs.SQUIRREL, "Cá", "Diệc")]
                               + [len(rabbit_herds), sum(len(h.members) for h in rabbit_herds) / max(1, len(rabbit_herds)), len(dens)])
        mean = lambda k: sum(s[k] for s in samples) / max(1, len(samples))
        days = max(1.0, w.minute / 1440)
        real_min = w.animal_minutes / ws.SIM_PER_REAL
        missing = [n for n in w.ALL_SPECIES if n not in w.arrived]
        print(f"   phủ kín {bs.real_h(w.filled)} · Vườn {bs.real_h(w.garden_unlocked)} · SK biome thấp nhất {getattr(w, 'min_biome', 0):.0f} "
              f"· chưa đến {missing} · biome {({b: round(v) for b, v in w.biome_health().items()})}")
        print("   bị săn:", {n: round(v / days, 1) for n, v in w.hunted.items()}, "chết đói:", {n: round(v / days, 1) for n, v in w.starved.items()})
        row = dict(births=sum(w.births.values()) / days if social else None, old=sum(w.oldage.values()) / days if social else None,
                   starved=sum(w.starved.values()) / days, hunted=sum(w.hunted.values()) / days,
                   rev=w.reversals / max(1, real_min), mv=w.moves / max(1, real_min))
        rows.append(row)
        print(f"{seed:>4} {bs.real_h(w.ending):>5} {mean(0):>4.0f} {mean(1):>4.0f} {mean(2):>4.0f} {mean(3):>4.0f} {mean(4):>4.0f} "
              f"{(row['births'] or 0):>7.0f} {(row['old'] or 0):>6.0f} {row['starved']:>6.1f} {row['hunted']:>6.1f} "
              f"{row['rev']:>8.1f} {row['mv']:>7.1f} {mean(5):>4.1f} {mean(6):>6.1f} {mean(7):>8.1f}")
        if w.ending:
            ends.append(w.ending / 60 / ws.SIM_PER_REAL)
    ends.sort()
    avg = lambda key: sum(r[key] or 0 for r in rows) / len(rows)
    print(f"\nTrung bình: chết đói {avg('starved'):.1f}/ng · bị săn {avg('hunted'):.1f}/ng · "
          f"quay đầu {avg('rev'):.1f} lần/con/phút thật · bước đi {avg('mv'):.1f} /con/phút thật")
    print(f"Kết game: {len(ends)}/{seeds} seed" + (f", trung vị {ends[len(ends) // 2]:.1f} giờ thật "
                                                   f"(min {ends[0]:.1f}, max {ends[-1]:.1f})" if ends else ""))


if __name__ == "__main__":
    args = sys.argv[1:]
    seeds = next((int(a) for a in args[1:] if a.isdigit()), 8)
    ROLES_BY_RANGE = "standing" not in args
    if "old" not in args:
        use_social_breeding()
    survey(seeds, social="old" not in args)
