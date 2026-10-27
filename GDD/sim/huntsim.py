"""
Mô hình hang thỏ, né thú săn và rượt bắt cho GDD 14. Dựa trên socialsim.py (GDD 13), chỉ thay:
- thỏ: mỗi bầy là một gia đình sống quanh một hang; đói lâu thì cả nhà dời đi đào hang mới;
- con mồi tránh chỗ có thú săn, thấy thú săn đang đói lại gần thì chạy về chỗ trú (thỏ: hang, sóc: cây, cá: đầu ao bên kia);
- thú săn đói chọn một con mồi, chạy nhanh tới và vồ; trượt thì mệt, nghỉ một lúc.
Thông số ở balance.json → "hunting".

    python3 Docs/GDD/sim/huntsim.py survey [seeds]     # luật GDD 14
    python3 Docs/GDD/sim/huntsim.py survey [seeds] 13  # luật GDD 13 (bắt mồi theo xác suất, không hang) để so sánh
"""
import sys

import worldsim as ws
import biomesim as bs
import socialsim as ss
from worldsim import ANIMALS, NAME, HUNGRY_BELOW

HUNT = ws.B["hunting"]
BURROW = HUNT["burrow"]
RABBIT = NAME[BURROW["species"]]
PREY = {NAME[k]: v for k, v in HUNT["prey"].items()}
PRED = {NAME[k]: v for k, v in HUNT["predators"].items()}
SLEEP = HUNT.get("sleep", {})
SLEEPERS = {NAME[k]: v for k, v in SLEEP.get("inRefuge", {}).items()}   # loài ngủ trong chỗ trú → [giờ thức, giờ ngủ]
SLEEP_LAG = SLEEP.get("lagHours", 0)
DAY_NIGHT = ws.B["time"]["dayNightMinutes"]
SLEEP_ON = True
AVOID_MARGIN = 2    # GDD 14 §3c: độ trễ của việc né
AVOID_ON = True     # GDD 14 §3c: tránh xa, rình mồi ("noavoid" để so với luật cũ)


def day_hour(minute):
    """Giờ trong ngày của game (GDD 11 §1.5): phút 0 là 6h, một ngày đêm = dayNightMinutes phút mô phỏng."""
    return (6 + 24 * (minute % DAY_NIGHT) / DAY_NIGHT) % 24


def use_hunting():
    ss.use_social_breeding()
    ss.KIND[RABBIT] = dict(ss.KIND[RABBIT], spread=BURROW["spread"])


class HuntWorld(ss.SocialWorld):
    def __init__(self, seed, **kw):
        super().__init__(seed, **kw)
        self.empty_burrows = []         # [(cột, phút bỏ hang)]: chỉ để vẽ và để gia đình khác dùng lại
        self.pounces = self.misses = 0
        self.hidden_minutes = self.rabbit_minutes = 0
        self.relocations = 0
        self.next_uid = 0

    # ---- trạng thái thêm cho mỗi con ----------------------------------------------
    def init_hunt(self, a):
        if not hasattr(a, "hidden"):
            a.hidden, a.hide_left, a.alarm, a.target, a.chase_left, a.tired = False, 0, None, None, 0, 0
            a.avoid, a.stalking = None, False
            a.sleeping, a.uid = False, self.next_uid
            self.next_uid += 1

    def asleep(self, a):
        """Ngoài giờ thức của loài (mỗi con lệch tới lagHours giờ, như hình ở GDD 11 §1.5)."""
        hours = SLEEPERS.get(a.name)
        if not hours or not SLEEP_ON:
            return False
        lag = (a.uid * 0.618) % 1.0 * SLEEP_LAG
        h = (day_hour(self.minute) - lag) % 24
        awake_from, awake_to = hours
        awake = awake_from <= h < awake_to if awake_from < awake_to else h >= awake_from or h < awake_to
        return not awake

    def home_of(self, a):
        center, radius = super().home_of(a)
        if a.name == RABBIT and a.hunger < HUNGRY_BELOW:
            radius = BURROW["hungrySpread"]     # đói thì đi kiếm ăn xa hang hơn
        return center, radius

    # ---- con mồi: cảnh giác, chạy về chỗ trú -----------------------------------------
    def notice(self, h, p):
        """Tầm con mồi nhận ra thú săn đói (GDD 14 §3c): đang bò rình thì chỉ ≤ stalkNotice cột."""
        k = PRED[h.name]
        return k["stalkNotice"] if getattr(h, "stalking", False) and "stalkNotice" in k else p["alertRange"]

    def alert(self):
        all_hunters = [a for a in self.animals if a.name in PRED and not a.gone]
        hunters = [h for h in all_hunters if h.hunger < HUNGRY_BELOW]
        for a in self.animals:
            self.init_hunt(a)
            p = PREY.get(a.name)
            if not p:
                continue
            near = [h for h in hunters if a.name in h.spec["prey_all"] and abs(h.x - a.x) <= self.notice(h, p)]
            a.alarm = min(near, key=lambda h: abs(h.x - a.x)) if near else None
            # §3c: thú săn no (không rình) trong wary cột thì đi bộ tránh xa
            # đã né thì chỉ thôi né khi thú săn đã rời xa cả chỗ của mình (hang ± bán kính + wary), để không bị kéo về ngay
            # chỗ thú săn rồi lại né, lắc qua lắc lại
            avoiding = getattr(a, "avoid", None) is not None
            center, radius = self.home_of(a) if avoiding else (a.x, 0)
            fed = [h for h in all_hunters if h.hunger >= HUNGRY_BELOW and a.name in h.spec["prey_all"]
                   and (abs(h.x - a.x) < p["wary"] or (avoiding and abs(h.x - center) < radius + p["wary"]))] if p["wary"] and AVOID_ON else []
            a.avoid = min(fed, key=lambda h: abs(h.x - a.x)) if fed and not a.alarm else None
            a.sleeping = self.asleep(a)
            if a.hidden:
                if a.alarm or a.sleeping:       # GDD 14 §3b: ngủ trong hang tới sáng
                    a.hide_left = p["hideMinutes"]
                else:
                    a.hide_left -= 1
                    if a.hide_left <= 0:
                        a.hidden = False
            if a.name == RABBIT:
                self.rabbit_minutes += 1
                self.hidden_minutes += a.hidden

    def den_ok(self, name, x):
        """§3c: thú săn làm hang cách mọi con mồi của nó ≥ fedKeepAway cột (không làm hang giữa bãi mồi)."""
        k = PRED.get(name)
        if k and "fedKeepAway" in k and AVOID_ON and self.by_name.get(name):
            prey = self.by_name[name][0].spec["prey_all"]
            if any(abs(r.x - x) < k["fedKeepAway"] for n in prey for r in self.by_name.get(n, ()) if not r.gone):
                return False
        return super().den_ok(name, x)

    def refuge(self, a):
        """Chỗ trú: thỏ về hang của gia đình, sóc về cây của nó, cá ra đầu ao xa thú săn nhất; None nếu không có."""
        p = PREY[a.name]
        if p["refuge"] == "burrow" and a.herd is not None:
            return a.herd.anchor
        if p["refuge"] == "den" and a.den is not None:
            return a.den
        if p["refuge"] == "far":
            lo, hi = self.bounds(a)
            return lo if abs(a.alarm.x - lo) > abs(a.alarm.x - hi) else hi
        return None

    def move(self, a):
        p = PREY.get(a.name)
        if p:
            if a.hidden:
                return a.x
            if a.sleeping and not a.alarm:
                to = self.refuge(a)
                if to is None:      # chưa có hang / cây: ngủ tại chỗ
                    a.goal, a.rest = None, 0
                    return a.x
                if a.x == to:
                    a.hidden, a.hide_left = True, p["hideMinutes"]
                    a.goal, a.rest = None, 0
                    return a.x
                step = min(ss.KIND[a.name]["speed"], abs(to - a.x))      # đi bộ về ngủ, không chạy
                a.goal, a.rest = None, 0
                return a.x + (step if to > a.x else -step)
            if a.alarm:
                lo, hi = self.bounds(a)
                to = self.refuge(a)
                if to is None:      # không có chỗ trú: chạy ra xa
                    to = lo if a.alarm.x > a.x else hi
                if a.x == to:
                    if p["hideMinutes"] > 0 and p["refuge"] != "far":
                        a.hidden, a.hide_left = True, p["hideMinutes"]
                    a.goal, a.rest = None, 0
                    return a.x
                step = min(p["fleeSpeed"], abs(to - a.x))
                a.goal, a.rest = None, 0
                return a.x + (step if to > a.x else -step)
            if a.avoid is not None:
                # §3c: thú săn no lại gần: đi bộ thẳng tới phía bên kia chỗ của mình (xa thú săn), tới nơi thì nghỉ
                lo, hi = self.bounds(a)
                center, radius = self.home_of(a)
                side = 1 if a.x >= a.avoid.x else -1
                a.goal = max(lo, min(hi, center + side * (radius + AVOID_MARGIN)))
                if a.x == a.goal:
                    a.rest = 0
                    return a.x
                return a.x + (1 if a.goal > a.x else -1) * min(ss.KIND[a.name]["speed"], abs(a.goal - a.x))
        if a.name in PRED and a.target is not None:
            t = a.target
            gap = abs(t.x - a.x)
            k = PRED[a.name]
            # §3c: mồi chưa phát hiện thì bò rình chậm; mồi đã chạy thì rượt
            speed = k["stalkSpeed"] if a.stalking else k["chaseSpeed"]
            step = min(speed, max(0, gap - 1)) if gap > 1 else 0
            a.goal, a.rest = None, 0
            return a.x + (step if t.x > a.x else -step)
        return super().move(a)

    def pick_goal(self, a, center, radius):
        p = PREY.get(a.name)
        k = PRED.get(a.name)
        if k and "fedKeepAway" in k and AVOID_ON and a.hunger >= HUNGRY_BELOW:
            # §3c: thú săn no không đi vào giữa bầy mồi
            lo, hi = self.bounds(a)
            prey = [r.x for n in a.spec["prey_all"] for r in self.by_name.get(n, ()) if not r.gone]
            goal = center
            for _ in range(6):
                goal = max(lo, min(hi, center + self.rng.randint(-radius, radius)))
                if not any(abs(goal - x) < k["fedKeepAway"] for x in prey):
                    break
            return goal
        if not p or not p["wary"]:
            return super().pick_goal(a, center, radius)
        # con mồi tránh chọn chỗ gần thú săn (kể cả thú săn đang no)
        lo, hi = self.bounds(a)
        hunters = [h.x for n in PRED for h in self.by_name.get(n, ()) if not h.gone and a.name in h.spec["prey_all"]]
        goal = center
        for _ in range(4):
            goal = max(lo, min(hi, center + self.rng.randint(-radius, radius)))
            if not any(abs(goal - x) < p["wary"] for x in hunters):
                break
        return goal

    def graze(self, a, s):
        if getattr(a, "hidden", False):
            # trốn trong hang thì không ăn; ngủ thì nằm yên nên đói chậm hơn
            a.hunger -= ws.STARVE_DRAIN * (SLEEP.get("drain", 1.0) if a.sleeping else 1.0)
            return
        super().graze(a, s)

    # ---- thú săn: chọn mồi, rượt, vồ ------------------------------------------------
    def hungry_hunter_goal(self, a, prey):
        pass        # diệc cũng rượt như cáo (hunt)

    def hunt(self, a, s):
        sp, k = a.spec, PRED[a.name]
        self.init_hunt(a)
        a.hunger -= 100 * sp["need"] * (ws.WINTER_PREDATOR_NEED if s == "Đông" else 1.0)
        prey_all = [r for n in sp["prey_all"] for r in self.by_name.get(n, ())]
        if a.tired > 0:
            a.tired -= 1
            a.target = None
            a.stalking = False
        elif a.hunger >= HUNGRY_BELOW:
            a.target = None
            a.stalking = False
        else:
            in_range = [r for r in prey_all if not r.gone and abs(r.x - a.x) <= sp["range"]]
            if len(in_range) <= ws.LAST_PAIR:
                a.target = None     # luật cặp cuối
            else:
                t = a.target
                if t is None or t.gone or getattr(t, "hidden", False) or abs(t.x - a.x) > k["sight"] or a.chase_left <= 0:
                    seen = [r for r in prey_all if not r.gone and not getattr(r, "hidden", False) and abs(r.x - a.x) <= k["sight"]]
                    t = min(seen, key=lambda r: abs(r.x - a.x)) if seen else None
                    a.chase_left = k["chaseMaxMinutes"]
                a.target = t
                a.stalking = t is not None and "stalkSpeed" in k and AVOID_ON and getattr(t, "alarm", None) is not a
                if t is not None:
                    gap = abs(t.x - a.x)
                    if gap <= k["chaseSpeed"] + 1:
                        # tới được trong phút này: lao tới sát mồi rồi vồ luôn (không để mồi chạy thêm một phút)
                        if gap > 1:
                            a.x = t.x + (1 if a.x > t.x else -1)
                        self.pounce(a, t, k, len(in_range))
                    else:
                        a.chase_left -= 1
                        if a.chase_left <= 0:
                            a.target, a.tired = None, k["tiredMinutes"]
        if a.hunger < HUNGRY_BELOW and self.near_fruit(a, s):
            a.hunger += ws.FRUIT_GAIN
        return prey_all

    def pounce(self, a, t, k, prey_count):
        self.pounces += 1
        shelter = any(c.layers[1] for c in self.near(t.x, 1)) or self.cols[t.x].canopy > 0
        scarcity = min(1.0, prey_count / ws.PREY_COMFORT)
        if self.rng.random() < k["pounce"] * scarcity * (ws.SHRUB_ESCAPE if shelter else 1.0):
            t.gone = True
            self.cols[t.x].detritus += ws.CATCH_DETRITUS
            self.hunted[t.name] = self.hunted.get(t.name, 0) + 1
            a.hunger = 100
        else:
            self.misses += 1
            a.tired = k["tiredMinutes"]
        a.target = None

    # ---- hang thỏ ------------------------------------------------------------------
    def steer_herds(self):
        fish = [h for h in self.herds if h.name != RABBIT]
        saved, self.herds = self.herds, fish
        super().steer_herds()           # cá: bầy dời dần như GDD 13
        self.herds = saved
        for h in self.herds:
            if h.name != RABBIT:
                continue
            hungry = sum(1 for m in h.members if m.hunger < HUNGRY_BELOW) * 2 >= len(h.members)
            h.hungry_min = getattr(h, "hungry_min", 0) + 1 if hungry else 0
            if h.hungry_min < BURROW["relocateAfterMinutes"]:
                continue
            h.hungry_min = 0
            best, f = self.best_food(h, h.anchor)
            if f > 0 and abs(best - h.anchor) >= BURROW["relocateMin"]:
                site = self.dig(best)
                if site is None:
                    continue            # quanh bãi cỏ đó không có đất đào hang: ở lại
                self.leave_burrow(h.anchor)
                h.anchor = site
                self.relocations += 1

    def burrow_site(self, x):
        """Miệng hang và buồng ngủ (tới x + 2, mặt cắt GDD 14 §5) đều là đất sống, không phải nước hay đất hoang."""
        return all(0 <= i < len(self.cols) and self.cols[i].alive and self.cols[i].ground == "land" for i in range(x, x + 3))

    def dig(self, x):
        """Dùng lại hang bỏ trống gần đó nếu có, không thì đào hang mới tại x hoặc ở chỗ đào được gần nhất (≤ 8 cột).
        None nếu quanh đó không có đất."""
        for i, (b, _) in enumerate(self.empty_burrows):
            if abs(b - x) <= BURROW["reuseRange"] and self.burrow_site(b):
                del self.empty_burrows[i]
                return b
        for d in range(9):
            for t in (x - d, x + d):
                if self.burrow_site(t):
                    return t
        return None

    def leave_burrow(self, x):
        self.empty_burrows.append((x, self.minute))

    def split_herds(self):
        before = {id(h) for h in self.herds}
        super().split_herds()
        for h in self.herds:
            if id(h) not in before and h.name == RABBIT:
                site = self.dig(h.anchor)
                if site is not None:
                    h.anchor = site

    def animals_step(self, s):
        self.alert()
        before = {id(a) for a in self.animals}
        rabbit_herds = {id(h): h.anchor for h in self.herds if h.name == RABBIT}
        super().animals_step(s)
        # sinh trong hang thì con non cũng ở trong hang
        for a in self.animals:
            if id(a) not in before and a.herd is not None:
                mother = next((m for m in a.herd.members if m is not a and id(m) in before and getattr(m, "hidden", False) and m.x == a.x), None)
                if mother is not None:
                    self.init_hunt(a)
                    a.hidden, a.hide_left = True, mother.hide_left
        alive = {id(h) for h in self.herds}
        for hid, x in rabbit_herds.items():
            if hid not in alive:
                self.leave_burrow(x)       # cả nhà chết hết: hang bỏ trống
        self.empty_burrows = [(x, m) for x, m in self.empty_burrows if self.minute - m < BURROW["decayMinutes"]]


def survey(seeds=8, hunting=True):
    print("Luật:", "hang thỏ, né, rượt và vồ (GDD 14)" if hunting else "GDD 13", "· giờ là giờ thật (×100)")
    print(f"{'seed':>4} {'Kết':>5} {'thỏ':>4} {'cáo':>4} {'sóc':>4} {'cá':>4} {'diệc':>4} {'hang':>4} "
          f"{'đói/ng':>6} {'săn/ng':>6} {'vồ trúng':>8} {'trốn%':>5} {'dời/ng':>6} {'quay đầu':>8}")
    ends, rows = [], []
    for seed in range(1, seeds + 1):
        w = HuntWorld(seed) if hunting else ss.SocialWorld(seed)
        samples = []
        while w.minute < ws.MAX_HOURS * 60 and w.ending is None:
            w.step()
            if w.minute % 600 == 0:
                samples.append([w.count_animal(n) for n in ("Thỏ", "Cáo", bs.SQUIRREL, "Cá", "Diệc")]
                               + [sum(1 for h in w.herds if h.name == RABBIT)])
        mean = lambda k: sum(s[k] for s in samples) / max(1, len(samples))
        days = max(1.0, w.minute / 1440)
        real_min = w.animal_minutes / ws.SIM_PER_REAL
        hunted = {n: round(v / days, 1) for n, v in w.hunted.items()}
        starved = {n: round(v / days, 1) for n, v in w.starved.items()}
        pounces = getattr(w, "pounces", 0)
        hit = (pounces - w.misses) / pounces if hunting and pounces else 0
        hidden = w.hidden_minutes / max(1, w.rabbit_minutes) if hunting else 0
        reloc = getattr(w, "relocations", 0) / days
        row = dict(starved=sum(w.starved.values()) / days, hunted=sum(w.hunted.values()) / days, rev=w.reversals / max(1, real_min),
                   fox_starved=w.starved.get("Cáo", 0) / days)
        rows.append(row)
        print(f"   bị săn {hunted} · chết đói {starved} · chưa đến {[n for n in w.ALL_SPECIES if n not in w.arrived]}")
        print(f"{seed:>4} {bs.real_h(w.ending):>5} {mean(0):>4.0f} {mean(1):>4.0f} {mean(2):>4.0f} {mean(3):>4.0f} {mean(4):>4.0f} "
              f"{mean(5):>4.1f} {row['starved']:>6.1f} {row['hunted']:>6.1f} {hit:>8.0%} {hidden:>5.0%} {reloc:>6.1f} {row['rev']:>8.1f}")
        if w.ending:
            ends.append(w.ending / 60 / ws.SIM_PER_REAL)
    ends.sort()
    avg = lambda key: sum(r[key] for r in rows) / len(rows)
    print(f"\nTrung bình: chết đói {avg('starved'):.1f}/ng (cáo {avg('fox_starved'):.1f}) · bị săn {avg('hunted'):.1f}/ng · "
          f"quay đầu {avg('rev'):.1f} lần/con/phút thật")
    print(f"Kết game: {len(ends)}/{seeds} seed" + (f", trung vị {ends[len(ends) // 2]:.1f} giờ thật "
                                                   f"(min {ends[0]:.1f}, max {ends[-1]:.1f})" if ends else ""))


if __name__ == "__main__":
    args = sys.argv[1:]
    seeds = next((int(a) for a in args[1:] if a.isdigit() and a != "13"), 8)
    hunting = "13" not in args[1:]
    SLEEP_ON = "nosleep" not in args
    AVOID_ON = "noavoid" not in args
    if hunting:
        use_hunting()
    else:
        ss.use_social_breeding()
    survey(seeds, hunting)
