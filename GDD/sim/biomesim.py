"""
Mô hình môi trường sống cho GDD 12: biome theo cột, cỏ phủ lấn đất hoang, thực vật ngoài biome mọc kém / không mọc,
hành lang ≤ 5 ô khi gieo cỏ phủ gần ranh giới, động vật tự đến theo điều kiện sống (không mời, không hồi sinh), Sóc.
Dùng chung luật cây / thú / Sinh khí của worldsim.py; chỉ thay phần vùng, hồi sinh, mời, người chơi mô hình.
Thông số ở balance.json → "biomeModel".

    python3 Docs/GDD/sim/biomesim.py survey [seeds] [pe=300] [idle] [noplayer]
    python3 Docs/GDD/sim/biomesim.py [seed]        # một lần chạy, in dải biome theo thời gian và nhật ký
"""
import sys

import worldsim as ws
from worldsim import Plant, Animal, PLANTS, ANIMALS, NAME, TREE_LAYER, PERIODIC_MINUTES, SIM_PER_REAL, COSTS

BM = ws.B["biomeModel"]

# ---- loài mới (Dương xỉ, Sóc) đăng ký vào bảng của worldsim
for d in BM["plants"]:
    NAME[d["id"]] = d["name"]
    PLANTS[d["name"]] = dict(layer=d["layer"], ground=d["ground"], grow=d["growMinutes"], life=d["lifeMinutes"],
                             moist=tuple(d["moisture"]), fert=d["fertilityMin"], light=d["lightMin"],
                             seeds=d["seedsPerHour"], range=d["seedRange"], water=d["waterUse"],
                             fertuse=d["fertilityUse"], detritus=d["detritus"], essence=d["essence"],
                             regrow=d["regrow"], flower=d["flower"], perennial=d["perennial"],
                             fruit=tuple(NAME[e] for e in d["fruitEaters"]), bank=d["bank"])
    COSTS[d["name"]] = d["sowCost"]
for d in BM["animals"]:
    NAME[d["id"]] = d["name"]
    ANIMALS[d["name"]] = dict(role="ăn cỏ", eats="nuts", life=d["lifeMinutes"], mature=d["matureMinutes"],
                              litter=d["litter"], cooldown=d["cooldownMinutes"], range=d["range"],
                              essence=d["essence"], detritus=d["detritus"], habitat="land", need=0,
                              nut_tree=NAME[d["nutTree"]], min_trees=d["minTrees"], trees_per=d["treesPerAnimal"],
                              fruit=[], bury=d["buryRange"])
ANIMALS["Cáo"]["prey_all"] = ("Thỏ",) + tuple(NAME[i] for i in BM["foxAlsoHunts"])
for n, sp in PLANTS.items():
    sp["name"] = n

BIOMES = {NAME[k]: set(v) for k, v in BM["plantBiomes"].items()}
GROUND = {NAME[k]: v for k, v in BM["groundCover"].items()}        # cỏ phủ → biome nó lan
BORDER = BM["borderColumns"]
BORDER_FACTOR = BM["borderFactor"]
WASTE_SPROUT = BM["wastelandSprout"]
WASTE_FERT = BM["wastelandFertility"]
SOWN_MOIST = BM["sownWastelandMoisture"]
SOW_RANGE = BM["sowRangeOnWasteland"]
CORRIDOR = BM["corridorRange"]
GARDEN_COVER = BM["gardenCover"]
ARRIVE_AFTER = BM["arrival"]["afterMinutes"]
ABSENT_BELOW = BM["arrival"]["absentBelow"]
HAB = BM["habitat"]
SQUIRREL = NAME["squirrel"]
FERN, OAK, APPLE = NAME["fern"], NAME["oak"], NAME["apple"]
BIOME_CHAR = {None: "░", "meadow": "\"", "forest": "♣", "pond": "~"}

_base_suitability = ws.suitability


def biome_factor(sp, col):
    """GDD 12 §2.3: × 1 trong biome của loài, × 0.5 giáp ranh (≤ 5 ô) hoặc hành lang, × 0 sâu trong biome khác."""
    homes = BIOMES.get(sp["name"])
    if not homes:                       # cây bờ ao: chỉ cần cột kề nước
        return 1.0
    if col.corridor is not None:
        if col.corridor in homes:
            return 1.0 if sp["name"] in GROUND else BORDER_FACTOR
        if col.biome in homes:
            return BORDER_FACTOR        # cây của biome đang bị lấn
    if col.biome in homes:
        return 1.0
    d = min(col.dist.get(b, 999) for b in homes)
    if d <= BORDER or sp["name"] in GROUND:
        return BORDER_FACTOR            # cỏ phủ là cây tiên phong: gieo đâu cũng mọc, ít nhất nửa sức (GDD 12 §2.3)
    return 0.0


def suitability(sp, col):
    q = _base_suitability(sp, col)
    return q * biome_factor(sp, col) if q > 0 else 0.0


ws.suitability = suitability            # mọi chỗ worldsim gọi suitability đều tính biome


class BiomeWorld(ws.World):
    def __init__(self, seed, player=True, **kw):
        super().__init__(seed, trees=True, **kw)
        self.player = player
        for c in self.cols:
            c.biome = "meadow" if c.alive and c.ground == "land" else None
            c.corridor = None
            c.dist = {}
            if not c.alive:
                c.fert = WASTE_FERT
        for z in self.zones:            # ao trong Khởi Nguyên (không có) / ao thức dậy theo đất kề
            if z.kind == "pond":
                z.alive = False
        self.known = {"Cỏ"}             # cây người chơi gieo được (khám phá 🌱)
        self.arrived = {}               # loài → phút xuất hiện lần đầu
        self.timers = {}
        self.filled = None              # phút mọi cột (trừ Vườn) đã có sự sống
        self.biome_changes = 0
        self.expand_side = {}
        self.update_bounds()
        self.update_distances()

    # ---- biome, khoảng cách, ranh giới ---------------------------------------
    def update_bounds(self):
        alive = [c.i for c in self.cols if c.alive]
        self.L, self.R = alive[0], alive[-1]
        self._regions = None
        self._stats_minute = -1

    def update_distances(self):
        n = self.n
        for b in ("meadow", "forest", "pond"):
            d = [999] * n
            last = -999
            for x in range(n):
                if self.cols[x].alive and self.cols[x].biome == b:
                    last = x
                d[x] = x - last
            last = 10 ** 6
            for x in range(n - 1, -1, -1):
                if self.cols[x].alive and self.cols[x].biome == b:
                    last = x
                d[x] = min(d[x], last - x)
            for x in range(n):
                self.cols[x].dist[b] = d[x]

    def canopy_step(self, s):
        super().canopy_step(s)
        self.update_distances()

    def update_biomes(self):
        changed = False
        for c in self.alive_cols():
            if c.ground != "land":
                continue
            p = c.layers[0]
            if p and p.mature and p.name in GROUND:
                b = GROUND[p.name]
                if b != c.biome:
                    c.biome = b
                    changed = True
                    self.biome_changes += 1
                if c.corridor == b:
                    c.corridor = None
        if changed:
            self._regions = None

    def can_colonize(self, t):
        c = self.cols[t]
        if c.ground != "land" or c.alive:
            return False
        return self.zones[c.zone].kind != "garden" or self.garden_unlocked is not None

    def colonize(self, t, name, moist):
        c = self.cols[t]
        c.alive = True
        c.biome = GROUND[name]
        c.moist = max(c.moist, moist)
        c.fert = max(c.fert, WASTE_FERT)
        c.layers[0] = Plant(name)
        self.zones[c.zone].alive = True
        self.update_bounds()
        self.wake_ponds()

    def wake_ponds(self):
        """Ao (nước) thức dậy khi một cột đất kề nó có sự sống: 2 cụm bèo, 1 lau sậy ở bờ sống, bờ bên kia mọc cỏ (GDD 12 §2)."""
        for z in self.zones:
            if z.kind != "pond" or z.water is None or self.cols[z.water[0]].alive:
                continue
            banks = [i for i in (z.water[0] - 1, z.water[1] + 1) if self.cols[i].alive]
            if not banks:
                continue
            for i in range(z.water[0], z.water[1] + 1):
                w = self.cols[i]
                w.alive, w.biome, w.moist, w.fert = True, "pond", 100.0, WASTE_FERT + 15
            for i in (z.water[0], z.water[1])[:ws.STARTERS["pondDuckweed"]]:
                self.cols[i].layers[0] = Plant("Bèo")
            self.cols[banks[0]].layers[1] = Plant("Lau sậy")
            # nước mang hạt sang bờ bên kia: bờ đối diện mọc cỏ phủ của biome đã chạm tới ao (GDD 12 §2)
            near = self.cols[banks[0]]
            cover = next((n for n, b in GROUND.items() if b == near.biome), "Cỏ")
            for i in (z.water[0] - 1, z.water[1] + 1):
                if self.can_colonize(i):
                    self.colonize(i, cover, 70.0)
            z.alive = True
            self.update_bounds()
            self.log.append((self.minute, f"{z.name} thức dậy"))

    # ---- hạt: lấn đất hoang, sóc chôn hạt --------------------------------------
    def drop_seed(self, name, x):
        sp = PLANTS[name]
        reach = sp["range"]
        if name == OAK and any(a.name == SQUIRREL and abs(a.x - x) <= ANIMALS[SQUIRREL]["range"] for a in self.animals):
            reach = ANIMALS[SQUIRREL]["bury"]      # sóc chôn hạt xa hơn (GDD 12 §3.1)
        t = x + self.rng.randint(1, reach) * self.rng.choice((-1, 1))
        if not 0 <= t < self.n:
            return
        col = self.cols[t]
        if not col.alive:
            if name in GROUND and self.can_colonize(t):
                src = self.cols[x]
                if self.rng.random() < WASTE_SPROUT * suitability(sp, src):
                    self.colonize(t, name, src.moist * 0.8)
            return
        if sp["layer"] == TREE_LAYER and not self.tree_room(t):
            return
        if col.layers[sp["layer"]] is None and self.rng.random() < suitability(sp, col):
            col.layers[sp["layer"]] = Plant(name)

    # ---- đoạn biome theo cột ----------------------------------------------------
    def regions(self):
        if self._regions is None:
            out = []
            self.reg_of_col = {}
            for x in range(self.L, self.R + 1):
                c = self.cols[x]
                if not c.alive or c.biome is None:
                    continue
                if out and out[-1]["group"] == c.biome and out[-1]["end"] == x:
                    out[-1]["end"] = x + 1
                else:
                    out.append(dict(group=c.biome, start=x, end=x + 1))
                self.reg_of_col[x] = len(out) - 1
            self._regions = out
        return self._regions

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
            roles = {"sản xuất"} if any(n in PLANTS for n in r["counts"]) else set()
            roles |= {ANIMALS[n]["role"] for n in r["counts"] if n in ANIMALS}
            if "Giun" in r["counts"]:
                roles.add("phân huỷ")
            r["roles"] = roles
        for k, r in enumerate(regs):
            nbrs = [regs[j] for j in (k - 1, k + 1)
                    if 0 <= j < len(regs) and (regs[j]["end"] == r["start"] or regs[j]["start"] == r["end"])]
            r["nbrs"] = nbrs
            r["borrowed"] = set().union(*(n["roles"] for n in nbrs)) - r["roles"] if nbrs else set()
            r["mult"] = self.multipliers(r, nbrs)
        self._stats_minute = self.minute
        return regs

    def health(self, z):
        """Sức khoẻ vùng (08 §5.3), vùng có thể gồm nhiều đoạn biome (ao + bờ): vai trò và cân bằng lấy trung bình
        theo số cột của từng đoạn trong vùng."""
        cols = self.zone_cols(z)
        regs = self.region_stats()
        ks = [self.reg_of_col[c.i] for c in cols if c.alive and c.i in self.reg_of_col]
        if not ks:
            return 0.0
        cover = sum(1 for c in cols if any(p and p.living for p in c.layers)) / len(cols)
        lo = ws.ESS["balanceMin"]
        roles = bal = 0.0
        for k in ks:
            r = regs[k]
            roles += min(1.0, (len(r["roles"]) + ws.HEALTH["borrowedRoleWeight"] * len(r["borrowed"])) / ws.HEALTH["rolesNeeded"])
            bal += min(1.0, max(0.0, (r["mult"][1] - lo) / (1 - lo)))
        roles, bal = roles / len(ks), bal / len(ks)
        return 100 * cover * (ws.HEALTH["base"] + ws.HEALTH["roles"] * roles + ws.HEALTH["balance"] * bal)

    # ---- động vật tự đến theo điều kiện sống (GDD 12 §3) ------------------------
    def arrivals(self):
        regs = self.region_stats()
        winter = self.season == "Đông"
        season_i = ws.SEASONS.index(self.season)

        def cols(r):
            return self.cols[r["start"]:r["end"]]

        def living(cs, names):
            return sum(1 for c in cs for p in c.layers if p and p.living and p.name in names)

        def count(name, a, b):
            return sum(1 for x in self.animals if x.name == name and a <= x.x < b)

        def span(r):
            lo = min([r["start"]] + [n["start"] for n in r["nbrs"]])
            hi = max([r["end"]] + [n["end"] for n in r["nbrs"]])
            return lo, hi

        flowers = {n for n, p in PLANTS.items() if p["flower"]}
        for name, sites in (("Giun", regs), ("Ong", regs), ("Thỏ", regs), ("Cáo", regs), (SQUIRREL, regs),
                            ("Cá", [z for z in self.zones if z.kind == "pond" and z.alive]),
                            ("Diệc", [z for z in self.zones if z.kind == "pond" and z.alive])):
            for site in sites:
                ok, spawn_x, key = False, None, None
                if isinstance(site, dict):
                    r = site
                    cs = cols(r)
                    key = (name, r["group"], self.cols[(r["start"] + r["end"] - 1) // 2].zone)
                    h = HAB[{"Giun": "worm", "Ong": "bee", "Thỏ": "rabbit", "Cáo": "fox"}.get(name, "squirrel")]
                    b = r["group"]
                    if name == "Giun":
                        absent = not any(c.worms for c in cs)
                        spots = [c for c in cs if c.layers[0] and c.layers[0].living and c.detritus >= h["detritusMin"]
                                 and c.moist >= h["moistureMin"]]
                        ok = absent and b in h["biomes"] and bool(spots)
                        spawn_x = spots[len(spots) // 2].i if spots else None
                    elif name == "Ong":
                        absent = count("Ong", r["start"], r["end"]) < 1
                        shelter = sum(1 for c in cs if c.layers[1] or c.layers[2])
                        ok = (absent and b in h["biomes"] and season_i in h["seasons"]
                              and living(cs, flowers) >= h["flowersMin"] and shelter >= h["shelterMin"])
                    elif name == "Thỏ":
                        absent = count("Thỏ", r["start"], r["end"]) < ABSENT_BELOW
                        shelter = sum(1 for c in cs if c.layers[1] or c.layers[2])
                        ok = (absent and not winter and b in h["biomes"] and living(cs, {"Cỏ"}) >= h["grassMin"]
                              and shelter >= h["shelterMin"])
                    elif name == "Cáo":
                        lo, hi = span(r)
                        absent = count("Cáo", lo, hi) < ABSENT_BELOW
                        prey = sum(count(p, lo, hi) for p in ANIMALS["Cáo"]["prey_all"])
                        den = sum(1 for c in cs if c.layers[2] or (c.layers[1] and c.layers[1].name == "Mâm xôi"))
                        ok = (absent and not winter and b in h["biomes"] and prey >= h["preyMin"]
                              and den >= h["denMin"] and hi - lo >= h["rangeMin"])
                    else:   # Sóc
                        absent = count(SQUIRREL, r["start"], r["end"]) < ABSENT_BELOW
                        oaks = sum(1 for c in cs if c.layers[2] and c.layers[2].name == OAK and c.layers[2].mature)
                        ok = absent and not winter and b in h["biomes"] and oaks >= h["matureOaksMin"]
                    if spawn_x is None:
                        spawn_x = self.rng.choice((r["start"], r["end"] - 1))
                else:
                    z = site
                    key = (name, "pond", z.i)
                    water = self.cols[z.water[0]:z.water[1] + 1]
                    if name == "Cá":
                        absent = sum(1 for a in self.animals if a.name == "Cá" and a.pond == z.i) < ABSENT_BELOW
                        ok = absent and not winter and living(water, {"Bèo"}) >= HAB["fish"]["duckweedMin"]
                    else:
                        lo = self.zones[max(0, z.i - 1)].start
                        hi = self.zones[min(len(self.zones) - 1, z.i + 1)].end
                        absent = count("Diệc", lo, hi) < ABSENT_BELOW
                        fish = sum(1 for a in self.animals if a.name == "Cá" and a.pond == z.i)
                        zc = self.zone_cols(z)
                        perch = (living(zc, {"Lau sậy"}) >= HAB["heron"]["reedsMin"]
                                 or living(zc, {"Liễu"}) >= HAB["heron"]["willowMin"])
                        ok = absent and not winter and fish >= HAB["heron"]["fishMin"] and perch
                    spawn_x = self.rng.randint(*z.water) if name == "Cá" else z.water[0] - 1
                if not ok:
                    self.timers[key] = 0
                    continue
                self.timers[key] = self.timers.get(key, 0) + PERIODIC_MINUTES
                if self.timers[key] < ARRIVE_AFTER:
                    continue
                self.timers[key] = 0
                self.arrive(name, spawn_x, site)

    def arrive(self, name, x, site):
        if name not in self.arrived:
            self.arrived[name] = self.minute
            self.log.append((self.minute, f"✨ loài mới: {name}"))
        self.discovered.add(name)
        if name == "Giun":
            self.cols[x].worms = True
        elif name == "Cá":
            for _ in range(3):
                self.animals.append(Animal(name, self.rng.randint(*site.water), pond=site.i))
        else:
            for _ in range(2):
                self.animals.append(Animal(name, x))

    # ---- khám phá cây 🌱 (người chơi nhặt ngay) ------------------------------------
    def discover(self):
        w = self
        if w.count_living("Cỏ") >= 10:
            self.learn("Hoa dại")
        if w.count_living("Cỏ") >= 20:
            self.learn("Mâm xôi")
        for z in w.zones:
            if not z.alive:
                continue
            if z.kind == "pond" and w.count_living("Bèo", z) >= 3:
                self.learn("Sen")
            if z.kind == "pond" and w.count_living("Lau sậy", z) >= 2:
                self.learn("Liễu")
            if w.count_living("Mâm xôi", z) >= 4:
                self.learn(FERN)
        if w.count_living(FERN) >= BM["discover"]["oak"]["count"]:
            self.learn(OAK)
        if w.count_animal("Ong") >= 1 and any(c.alive and c.biome == "forest" for c in w.cols):
            self.learn(APPLE)

    def learn(self, name):
        if name not in self.known:
            self.known.add(name)
            self.log.append((self.minute, f"🌱 khám phá {name}"))

    # ---- nhịp chung + người chơi mô hình ------------------------------------------
    def step(self):
        super().step()
        if self.minute % PERIODIC_MINUTES == 0:
            self.update_biomes()

    def visit(self):
        for c in self.alive_cols():
            if not c.worms and c.layers[0] and c.ground == "land" and any(n.worms for n in self.near(c.i, 1)):
                c.worms = True
        self.measure_grazing()
        self.discover()
        self.arrivals()
        self.check_garden()
        if self.filled is None and all(c.alive for c in self.cols
                                      if c.ground == "land" and self.zones[c.zone].kind != "garden"):
            self.filled = self.minute
            self.log.append((self.minute, "đất hoang đã phủ kín"))
        if not self.player or self.minute % self.player_every != 0:
            return
        if self.rains:
            self.rain_dry()
        for _ in range(max(1, min(10, self.player_every // PERIODIC_MINUTES))):
            self.sow()
        self.expand()
        if self.filled is not None:
            self.plant_forest_patch()

    def plant_in(self, z, name):
        if name not in self.known:
            return
        super().plant_in(z, name)

    def zone_biome(self, z):
        land = [c.biome for c in self.zone_cols(z) if c.alive and c.ground == "land"]
        return max(set(land), key=land.count) if land else None

    def sow(self):
        for z in self.zones:
            if z.kind == "garden":
                continue
            land = [c for c in self.zone_cols(z) if c.ground == "land"]
            if sum(1 for c in land if c.alive) < len(land) / 2:
                continue
            b = self.zone_biome(z)
            size = len(land)
            grass = self.count_plant("Cỏ", z)
            if b == "meadow":
                if grass >= -(-size * 2 // 10) and self.count_plant("Hoa dại", z) < round(size / 6):
                    self.plant_in(z, "Hoa dại")
                if grass >= -(-size * 4 // 10) and self.count_plant("Mâm xôi", z) < round(size / 8):
                    self.plant_in(z, "Mâm xôi")
            if sum(1 for c in land if c.alive and c.biome == "forest") >= 3:     # có mảng rừng: trồng cây rừng
                for name, want in ((OAK, 3), (APPLE, 2)):
                    if self.count_plant(name, z) < want:
                        self.plant_in(z, name)
                if self.count_plant("Mâm xôi", z) < 4:          # bụi ra hoa nuôi ong, chỗ trốn, hang cáo
                    self.plant_in(z, "Mâm xôi")
            if z.water and self.count_living("Bèo", z) >= 3 and self.count_plant("Sen", z) < 2:
                self.plant_in(z, "Sen")
            if z.water and self.count_plant("Liễu", z) < 1:
                self.plant_in(z, "Liễu")

    def plant_forest_patch(self):
        """Đất đã kín mà rừng chưa thành hình (< 6 cột): gieo một mảng Dương xỉ giữa đồng cỏ (cây tiên phong mọc nửa sức), mưa ở đó."""
        if FERN not in self.known or sum(1 for c in self.cols if c.alive and c.biome == "forest") >= 6:
            return
        z = next((z for z in self.zones if z.kind == "meadow" and self.zone_biome(z) == "meadow"), None)
        if z is None or self.essence < 6 * COSTS[FERN] + COSTS["rain"]:
            return
        for c in self.zone_cols(z)[2:8]:
            if c.layers[0] is None or c.layers[0].name != FERN:
                c.layers[0] = Plant(FERN)
                self.essence -= COSTS[FERN]
            c.moist = min(100, c.moist + ws.RAIN_AMOUNT)
        self.essence -= COSTS["rain"]

    def expand(self):
        """Người chơi đẩy đất sống ra: gieo cỏ phủ lên đất hoang cách mép 3 ô (≤ 5), mưa ở đó.
        Bên trái phủ Dương xỉ khi đã khám phá (tạo rừng), bên phải phủ Cỏ."""
        for side in (-1, 1):
            edge = self.L if side < 0 else self.R
            t = edge + side * 3
            if not 0 <= t < self.n or not self.can_colonize(t):
                t = next((edge + side * k for k in (1, 2) if 0 <= edge + side * k < self.n
                          and self.can_colonize(edge + side * k)), None)
                if t is None:
                    continue
            cover = FERN if side < 0 and FERN in self.known else "Cỏ"
            if self.essence < COSTS[cover] + BM["modelPlayerExpandReserve"]:     # trồng hoa, cây trước, dư mới lấn đất
                continue
            self.essence -= COSTS[cover]
            self.colonize(t, cover, SOWN_MOIST)
            self.cols[t].moist = SOWN_MOIST
            if self.essence >= COSTS["rain"] + BM["modelPlayerExpandReserve"]:
                self.essence -= COSTS["rain"]
                self.rain_casts += 1
                for c in self.cols[max(0, t - 3):min(self.n, t + 4)]:
                    if c.ground == "land":
                        c.moist = min(100, c.moist + ws.RAIN_AMOUNT)

    ALL_SPECIES = ("Giun", "Ong", "Thỏ", "Cáo", "Cá", "Diệc", SQUIRREL)

    def biome_health(self):
        """Sức khoẻ từng biome (GDD 12 §5): mỗi đoạn tính như Sức khoẻ vùng (08 §5.3) trên cột của đoạn,
        rồi lấy trung bình theo số cột của mọi đoạn cùng biome."""
        regs = self.region_stats()
        lo = ws.ESS["balanceMin"]
        total, size = {}, {}
        for r in regs:
            cs = self.cols[r["start"]:r["end"]]
            cover = sum(1 for c in cs if any(p and p.living for p in c.layers)) / len(cs)
            roles = min(1.0, (len(r["roles"]) + ws.HEALTH["borrowedRoleWeight"] * len(r["borrowed"])) / ws.HEALTH["rolesNeeded"])
            bal = min(1.0, max(0.0, (r["mult"][1] - lo) / (1 - lo)))
            h = 100 * cover * (ws.HEALTH["base"] + ws.HEALTH["roles"] * roles + ws.HEALTH["balance"] * bal)
            n = r["end"] - r["start"]
            total[r["group"]] = total.get(r["group"], 0) + h * n
            size[r["group"]] = size.get(r["group"], 0) + n
        return {b: total[b] / size[b] for b in total}

    def check_garden(self):
        """GDD 12 §5 (✅ Q30): Vườn mở khi đất hoang phủ kín, mọi loài đã từng xuất hiện, mọi biome đang có đều Khoẻ."""
        bh = self.biome_health()
        self.min_biome = min(bh.values()) if bh else 0
        self.max_balanced = max(self.max_balanced, sum(1 for v in bh.values() if v >= ws.REVIVE_HEALTH))
        if (self.garden_unlocked is None and self.filled is not None
                and all(n in self.arrived for n in self.ALL_SPECIES)
                and bh and min(bh.values()) >= ws.REVIVE_HEALTH):
            self.garden_unlocked = self.minute
            self.log.append((self.minute, "Khu Vườn Thiêng mở"))
        if self.garden_unlocked is not None and self.ending is None:
            garden = next(z for z in self.zones if z.kind == "garden")
            cols = self.zone_cols(garden)
            if sum(1 for c in cols if c.alive) >= GARDEN_COVER * len(cols):
                self.ending = self.minute
                self.log.append((self.minute, "Cây Thế Giới nở hoa"))

    def strip(self):
        return "".join(BIOME_CHAR[c.biome] if c.alive else "░" for c in self.cols)


def real_h(m):
    return "-" if m is None else f"{m / 60 / SIM_PER_REAL:.1f}h"


def survey(seeds=8, player=True, rains=True, player_every=None, sprout=None):
    global WASTE_SPROUT
    if sprout is not None:
        WASTE_SPROUT = sprout
    print(f"hạt nảy trên đất hoang × {WASTE_SPROUT}", "·", "Người chơi:", ("mô hình, ghé mỗi " + str(player_every or ws.PLAYER_EVERY) + " phút mp") if player else "KHÔNG gieo, không mưa",
          "· giờ là giờ thật (×100)")
    print(f"{'seed':>4} {'phủ kín':>7} {'Vườn mở':>8} {'Kết':>6} {'SKbiome':>7} {'rừng%':>5} {'thỏ':>4} {'cáo':>4} {'sóc':>4} "
          f"{'cá':>4} {'ong':>4} {'đói/ng':>6} {'săn/ng':>6} {'đổi biome':>9}  lần đầu xuất hiện (giờ thật)")
    ends = []
    for seed in range(1, seeds + 1):
        w = BiomeWorld(seed, player=player, rains=rains, player_every=player_every)
        samples = []
        while w.minute < ws.MAX_HOURS * 60 and w.ending is None:
            w.step()
            if w.minute % 600 == 0:
                samples.append([w.count_animal(n) for n in ("Thỏ", "Cáo", SQUIRREL, "Cá", "Ong")])
        mean = lambda k: sum(s[k] for s in samples) / max(1, len(samples))
        land = [c for c in w.cols if c.ground == "land" and c.alive]
        forest = sum(1 for c in land if c.biome == "forest") / max(1, len(land))
        days = max(1.0, w.minute / 1440)
        first = " ".join(f"{n}:{real_h(m)}" for n, m in sorted(w.arrived.items(), key=lambda t: t[1]))
        print(f"{seed:>4} {real_h(w.filled):>7} {real_h(w.garden_unlocked):>8} {real_h(w.ending):>6} {min(w.biome_health().values()):>7.0f} "
              f"{forest:>5.0%} {mean(0):>4.0f} {mean(1):>4.0f} {mean(2):>4.0f} {mean(3):>4.0f} {mean(4):>4.0f} "
              f"{sum(w.starved.values()) / days:>6.1f} {sum(w.hunted.values()) / days:>6.1f} {w.biome_changes:>9}  {first}")
        if w.ending:
            ends.append(w.ending / 60 / SIM_PER_REAL)
    ends.sort()
    print(f"\nKết game: {len(ends)}/{seeds} seed" + (f", trung vị {ends[len(ends) // 2]:.1f} giờ thật "
                                                   f"(min {ends[0]:.1f}, max {ends[-1]:.1f})" if ends else
                                                   f" trong {ws.MAX_HOURS / SIM_PER_REAL:.0f} giờ thật"))


def run_one(seed):
    w = BiomeWorld(seed)
    print(f"Dải 144 cột: ░ đất hoang, \" đồng cỏ, ♣ rừng, ~ ao. Mỗi dòng = 30 phút thật.")
    while w.minute < ws.MAX_HOURS * 60 and w.ending is None:
        w.step()
        if w.minute % 3000 == 0:
            print(f"{real_h(w.minute):>5} {w.strip()}  SK {w.essence:>7.0f}")
    print("\nNhật ký:")
    for t, e in w.log:
        if "bỏ đi" not in e:
            print(f"  {real_h(t):>6}  {e}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "survey":
        seeds = next((int(a) for a in args[1:] if a.isdigit()), 8)
        pe = next((int(a[3:]) for a in args[1:] if a.startswith("pe=")), None)
        sprout = next((float(a[7:]) for a in args[1:] if a.startswith("sprout=")), None)
        survey(seeds, player="noplayer" not in args, rains="idle" not in args, player_every=pe, sprout=sprout)
    else:
        run_one(int(args[0]) if args else 1)
