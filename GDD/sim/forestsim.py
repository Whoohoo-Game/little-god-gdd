"""
Mô hình Rừng có Hươu và Sói cho GDD 17. Dựa trên huntsim.py (GDD 14), chỉ thêm:
- 🦌 Hươu: ăn cỏ ở Rừng, gặm Dương xỉ sống như thỏ gặm cỏ; đàn ≤ 4, không hang; thấy Sói đói thì chạy ra xa;
- 🐺 Sói: chỉ bắt Hươu; sống theo cặp chung hang ở Rừng; rình, rượt, vồ như Cáo nhưng vồ trúng ít hơn;
- Dương xỉ mọc lại khi bị gặm (Q51, `regrow`);
- kết game đòi thêm Hươu và Sói (Q53).
Số đọc từ balance.json (Tech Doc 11 §1). Không đổi luật của các file khác.

    python3 Docs/GDD/sim/forestsim.py survey [seeds]                  # ✅ bộ đã chốt (balance.json + Q52–Q57), so với huntsim
    python3 Docs/GDD/sim/forestsim.py survey [seeds] long             # chạy đủ 4 giờ thật, không dừng ở kết game
    python3 Docs/GDD/sim/forestsim.py survey [seeds] draft            # số tạm ban đầu, không luật Q52–Q57 (để so)
    python3 Docs/GDD/sim/forestsim.py survey [seeds] regrow=0         # Dương xỉ không mọc lại (như trước GDD 17)
    python3 Docs/GDD/sim/forestsim.py survey [seeds] no54             # tắt một luật (no52 / no54 / no55 / no57) để so
    python3 Docs/GDD/sim/forestsim.py survey [seeds] present2         # Q54 thử: cần ≥ 2 con (một cặp) trong tầm mới là "đã có"
    python3 Docs/GDD/sim/forestsim.py survey [seeds] heronq54         # Q54 cho cả Diệc (✅ Q56: Diệc giữ luật đến cũ)
    python3 Docs/GDD/sim/forestsim.py survey [seeds] lone=720         # Q57: con lẻ sau bao nhiêu phút mp thì không giữ chỗ
    python3 Docs/GDD/sim/forestsim.py survey [seeds] free             # thêm lần chạy không đòi Hươu+Sói cho kết game
    python3 Docs/GDD/sim/forestsim.py survey [seeds] wolf.pounce=0.8  # thử số khác
    python3 Docs/GDD/sim/forestsim.py forest [seeds]                  # số cột Rừng theo thời gian (huntsim, không Hươu/Sói)
"""
import copy
import sys
from multiprocessing import Pool

import worldsim as ws
import biomesim as bs
import socialsim as ss
import huntsim as hs
from worldsim import NAME, ANIMALS

# ---- số GDD 17 (✅ đã chốt, đọc từ balance.json; Tech Doc 11 §1) --------------------------------------------
_BM = ws.B["biomeModel"]
DEER_ANIMAL = next(d for d in _BM["animals"] if d["id"] == "deer")
WOLF_ANIMAL = next(d for d in _BM["animals"] if d["id"] == "wolf")
HABITAT = {k: _BM["habitat"][k] for k in ("deer", "wolf")}
SOCIAL = {k: ws.B["social"]["species"][k] for k in ("deer", "wolf")}
PREY = {"deer": ws.B["hunting"]["prey"]["deer"]}
PREDATORS = {"wolf": ws.B["hunting"]["predators"]["wolf"]}
FERN_REGROW = next(p for p in _BM["plants"] if p["id"] == "fern")["regrow"]
# Bộ số tạm ban đầu (trước khi đo) để so: "draft". Số đã chỉnh nay nằm sẵn trong balance.json, nên "tuned" không đổi số nữa
DRAFT = {"deer.needPerMinute": 1.0, "deer.fernMin": 12, "wolf.preyPerPredator": 3, "wolf.pounce": 0.6}
TUNED = {}
# Sói thức 15h–9h như Cáo: huntsim không mô hình giấc ngủ của Cáo (chỉ loài ngủ trong chỗ trú) nên Sói cũng không.

DEER, WOLF, FERN = "Hươu", "Sói", bs.FERN
BASE_SPECIES = bs.BiomeWorld.ALL_SPECIES
FERN_REGROW_NOW = 0.0          # trước GDD 17 Dương xỉ không mọc lại: huntsim "gốc" chạy với số này để so
_BASE = dict(deer=DEER_ANIMAL, wolf=WOLF_ANIMAL, habitat=HABITAT, social=SOCIAL, prey=PREY, pred=PREDATORS)
HAB = HABITAT
# Luật mới (✅ Q52, Q54, Q55, Q56, Q57, 2026-10-28); bật cùng "tuned", tắt từng luật bằng no52 / no54 / no55 / no57
ALL_RULES = ("q52", "q54", "q55", "q57")
RULES = set()
PRESENT_RANGE = {"Cáo": "territory", "Diệc": "territory", "Sói": "territory"}   # Q54: tầm đi lại = lãnh thổ (social.species)
WOLF_FALLBACK = None
PRESENT_MIN = 1                 # Q54: số con trong tầm đi lại thì coi là "đã có" (thử: present2 = cần một cặp)
LONE = {"minutes": _BM["arrival"]["loneMinutes"], "species": ("Cáo", "Sói")}  # Q57: con lẻ (không con trưởng thành cùng loài trong lãnh thổ) ≥ 1 ngày mp thì không tính "đã có"
Q54_SPECIES = {"Cáo", "Diệc", "Sói"}    # thử: skipheron / skipfox = giữ luật cũ cho loài đó


def setup(regrow=FERN_REGROW, overrides=None, rules=()):
    """Đăng ký Hươu, Sói vào các bảng của worldsim / socialsim / huntsim. overrides: {"deer.litter": 2, "wolf.pounce": 0.8, ...}
    (deer./wolf. đổi khoá đó ở mọi mục animals, social.species, hunting, habitat có nó)."""
    global HAB, RULES, WOLF_FALLBACK, PRESENT_MIN, Q54_SPECIES
    RULES = set(rules)
    PRESENT_MIN = 2 if "present2" in RULES else 1
    LONE["minutes"] = next((int(r[5:]) for r in RULES if r.startswith("lone=")), _BM["arrival"]["loneMinutes"])
    Q54_SPECIES = {"Cáo", "Diệc", "Sói"} - ({"Diệc"} if "skipheron" in RULES else set()) - ({"Cáo"} if "skipfox" in RULES else set())
    t = copy.deepcopy(_BASE)
    for key, v in (overrides or {}).items():
        who, field = key.split(".", 1)
        hit = [d for d in ((t["deer"] if who == "deer" else t["wolf"]), t["social"][who],
                           (t["prey"].get(who) or t["pred"].get(who)), t["habitat"][who]) if field in d]
        if not hit:
            raise KeyError(key)
        for d in hit:           # cùng khoá ở nhiều mục (cooldownMinutes, litter, minutesPerCatch): đổi hết
            d[field] = v
    HAB = t["habitat"]
    NAME["deer"], NAME["wolf"] = DEER, WOLF
    ANIMALS[DEER] = ws._animal(t["deer"])
    ANIMALS[WOLF] = ws._animal(t["wolf"])
    ss.KIND[DEER], ss.KIND[WOLF] = t["social"]["deer"], t["social"]["wolf"]
    for name, sp in ((DEER, t["social"]["deer"]), (WOLF, t["social"]["wolf"])):   # như ss.use_social_breeding
        if "cooldownMinutes" in sp:
            ANIMALS[name]["cooldown"] = sp["cooldownMinutes"]
        if "litter" in sp:
            ANIMALS[name]["litter"] = sp["litter"]
        if "minutesPerCatch" in sp:
            ANIMALS[name]["need"] = 1 / sp["minutesPerCatch"]
    hs.PREY[DEER] = t["prey"]["deer"]
    hs.PRED[WOLF] = t["pred"]["wolf"]
    ws.PLANTS[FERN]["regrow"] = regrow
    # Q52: không có Hươu trong tầm săn thì Sói bắt Sóc
    WOLF_FALLBACK = dict(ANIMALS[WOLF], prey_all=(DEER, bs.SQUIRREL))


class ForestWorld(hs.HuntWorld):
    def __init__(self, seed, require=True, **kw):
        super().__init__(seed, **kw)
        self.ALL_SPECIES = BASE_SPECIES + ((DEER, WOLF) if require else ())
        self.wolf_squirrels = 0
        self.joins = 0
        self.releases = 0           # Q57: số lần một cặp được đến nhờ con lẻ không còn tính là "đã có"

    # ---- Q54: thú săn "đã có mặt" nếu còn bất kỳ con nào trong tầm đi lại quanh đoạn / ao ----------------------
    def site_span(self, name, site):
        if isinstance(site, dict):
            lo = min([site["start"]] + [n["start"] for n in site.get("nbrs", ())])
            hi = max([site["end"]] + [n["end"] for n in site.get("nbrs", ())])
        else:
            lo = self.zones[max(0, site.i - 1)].start
            hi = self.zones[min(len(self.zones) - 1, site.i + 1)].end
        t = ss.KIND[name][PRESENT_RANGE[name]]
        return lo - t, hi + t

    def predator_near(self, name, site):
        lo, hi = self.site_span(name, site)
        if name not in Q54_SPECIES:     # luật cũ: < 2 con trong đoạn + đoạn kề (ao: vùng ao ± 1)
            lo, hi = self.site_span(name, site)
            t = ss.KIND[name][PRESENT_RANGE[name]]
            lo, hi = lo + t, hi - t
            return sum(1 for a in self.animals if a.name == name and not a.gone and lo <= a.x < hi) >= bs.ABSENT_BELOW
        return sum(1 for a in self.animals if a.name == name and not a.gone and lo <= a.x < hi
                   and not self.released(a)) >= PRESENT_MIN

    # ---- Q57: con lẻ lâu ngày thì không giữ chỗ -----------------------------------------------------------------
    def released(self, a):
        return "q57" in RULES and a.name in LONE["species"] and getattr(a, "alone", 0) >= LONE["minutes"]

    def update_lone(self):
        for name in LONE["species"]:
            t = ss.KIND[name]["territory"]
            group = [a for a in self.animals if a.name == name and not a.gone]
            for a in group:
                mate = any(o is not a and o.age >= o.spec["mature"] and abs(o.x - a.x) <= t for o in group)
                a.alone = 0 if mate else getattr(a, "alone", 0) + ws.PERIODIC_MINUTES

    def count_release(self, name, site):
        lo, hi = self.site_span(name, site)
        if any(a.name == name and not a.gone and lo <= a.x < hi and self.released(a) for a in self.animals):
            self.releases += 1

    def arrivals(self):
        if "q57" in RULES:
            self.update_lone()
        if "q54" in RULES:
            regs = self.region_stats()
            ponds = [z for z in self.zones if z.kind == "pond" and z.alive]
            blocked = [((n, r["group"], self.cols[(r["start"] + r["end"] - 1) // 2].zone)) for n in ("Cáo",) for r in regs
                       if self.predator_near(n, r)] + [("Diệc", "pond", z.i) for z in ponds if self.predator_near("Diệc", z)]
            real = self.arrive

            def arrive(name, x, site):
                if name in ("Cáo", "Diệc") and self.predator_near(name, site):
                    return
                if name == "Cáo":
                    self.count_release(name, site)
                real(name, x, site)
            self.arrive = arrive
            try:
                super().arrivals()
            finally:
                del self.arrive
            for k in blocked:
                self.timers[k] = 0          # đang có mặt: đồng hồ 2 giờ không chạy
        else:
            super().arrivals()
        regs = self.region_stats()
        if self.season == "Đông":
            for k in [k for k in self.timers if k[0] in (DEER, WOLF)]:
                self.timers[k] = 0
            return

        def count(name, a, b):
            return sum(1 for x in self.animals if x.name == name and a <= x.x < b and not x.gone)

        for name in (DEER, WOLF):
            for r in regs:
                cs = self.cols[r["start"]:r["end"]]
                key = (name, r["group"], self.cols[(r["start"] + r["end"] - 1) // 2].zone)
                trees = sum(1 for c in cs if c.layers[2])
                if name == DEER:
                    h = HAB["deer"]
                    ferns = sum(1 for c in cs if c.layers[0] and c.layers[0].name == FERN and c.layers[0].living)
                    ok = (r["group"] in h["biomes"] and count(DEER, r["start"], r["end"]) < bs.ABSENT_BELOW
                          and ferns >= h["fernMin"] and trees >= h["canopyMin"])
                else:
                    h = HAB["wolf"]
                    lo = min([r["start"]] + [n["start"] for n in r["nbrs"]])
                    hi = max([r["end"]] + [n["end"] for n in r["nbrs"]])
                    absent = not self.predator_near(WOLF, r) if "q54" in RULES else count(WOLF, lo, hi) < bs.ABSENT_BELOW
                    ok = (r["group"] in h["biomes"] and absent
                          and count(DEER, lo, hi) >= h["preyMin"] and trees >= h["denMin"])
                if not ok:
                    self.timers[key] = 0
                    continue
                self.timers[key] = self.timers.get(key, 0) + ws.PERIODIC_MINUTES
                if self.timers[key] < bs.ARRIVE_AFTER:
                    continue
                self.timers[key] = 0
                if name == WOLF and "q54" in RULES:
                    self.count_release(WOLF, r)
                self.arrive(name, self.rng.choice((r["start"], r["end"] - 1)), r)

    # ---- Q52: Sói bắt Sóc khi không có Hươu trong tầm săn ----------------------------------------------------
    def hunt(self, a, s):
        if a.name == WOLF:
            deer = any(not r.gone and abs(r.x - a.x) <= ANIMALS[WOLF]["range"] for r in self.by_name.get(DEER, ()))
            a.spec = WOLF_FALLBACK if "q52" in RULES and not deer else ANIMALS[WOLF]
        return super().hunt(a, s)

    def pounce(self, a, t, k, prey_count):
        was = t.gone
        super().pounce(a, t, k, prey_count)
        if a.name == WOLF and t.name == bs.SQUIRREL and t.gone and not was:
            self.wolf_squirrels += 1

    # ---- Q55: con lẻ một mình nhập bầy cùng loài gần nhất còn chỗ ---------------------------------------------
    def animals_step(self, s):
        super().animals_step(s)
        if "q55" not in RULES:
            return
        for h in list(self.herds):
            if len(h.members) != 1:
                continue
            m = h.members[0]
            k = ss.KIND[h.name]
            room = [o for o in self.herds if o is not h and o.name == h.name and o.pond == h.pond
                    and 0 < len(o.members) < k["groupMax"]]
            if not room:
                continue
            o = min(room, key=lambda o: abs(o.anchor - m.x))
            h.members = []
            o.members.append(m)
            m.herd, m.goal, m.rest = o, None, 0         # move() thấy "lạc bầy": đi bộ về anchor (hang) mới
            self.joins += 1
            if h.name == hs.RABBIT:
                self.leave_burrow(h.anchor)             # thỏ vào hang của gia đình kia, hang cũ bỏ trống
        self.herds = [h for h in self.herds if h.members]

    def den_ok(self, name, x):
        if name == WOLF and self.cols[x].biome != "forest":
            return False        # Sói làm hang trong Rừng
        return super().den_ok(name, x)


# ---- đo ------------------------------------------------------------------------------------------------------
TRACK = ("Thỏ", "Cáo", bs.SQUIRREL, "Cá", "Diệc", DEER, WOLF)


def run(args):
    seed, mode, regrow, overrides, long_run, rules = args
    setup(FERN_REGROW_NOW if mode == "base" else regrow, overrides, () if mode in ("base", "prev") else rules)
    hs.use_hunting()
    if mode == "base":
        w = hs.HuntWorld(seed)
    else:
        w = ForestWorld(seed, require=(mode != "free"))
    samples = []
    while w.minute < ws.MAX_HOURS * 60 and (w.ending is None or long_run):
        w.step()
        if w.minute % 600 == 0:
            forest = sum(1 for c in w.cols if c.alive and c.biome == "forest")
            ferns = sum(1 for c in w.cols if c.layers[0] and c.layers[0].name == FERN and c.layers[0].living)
            fregs = sum(1 for r in w.regions() if r["group"] == "forest" and r["end"] - r["start"] >= 5)
            dens = len({a.den for a in w.animals if a.name == WOLF and getattr(a, "den", None) is not None})
            samples.append((w.minute, forest, ferns, [w.count_animal(n) for n in TRACK], fregs, dens))
    days = max(1.0, w.minute / 1440)
    return dict(seed=seed, mode=mode, ending=w.ending, garden=w.garden_unlocked, minute=w.minute, samples=samples,
                arrived=dict(w.arrived), hunted={n: v / days for n, v in w.hunted.items()},
                starved={n: v / days for n, v in w.starved.items()},
                missing=[n for n in w.ALL_SPECIES if n not in w.arrived],
                wolf_sq=getattr(w, "wolf_squirrels", 0) / days, releases=getattr(w, "releases", 0) / days, joins=getattr(w, "joins", 0) / days)


def late(r):
    """Nửa sau của lần chạy."""
    s = r["samples"]
    return s[len(s) // 2:] or s


def stats(r):
    s, L = r["samples"], late(r)
    mean = lambda k: sum(x[3][k] for x in s) / max(1, len(s))
    k_d, k_w = TRACK.index(DEER), TRACK.index(WOLF)
    out = dict(forest_mean=sum(x[1] for x in L) / len(L), forest_min=min(x[1] for x in L),
               fern=sum(x[2] for x in L) / len(L), means=[mean(k) for k in range(len(TRACK))])
    for name, k in (("deer", k_d), ("wolf", k_w)):
        out[name] = dict(mean=sum(x[3][k] for x in L) / len(L), min=min(x[3][k] for x in L),
                         present=sum(1 for x in L if x[3][k] > 0) / len(L))
    out["fregs"] = sum(x[4] for x in L) / len(L)
    out["dens"] = sum(x[5] for x in L) / len(L)
    out["wolf_per_forest"] = sum(x[3][k_w] / max(1, x[4]) for x in L) / len(L)
    return out


def rh(m):
    return bs.real_h(m)


def survey(seeds=8, regrow=FERN_REGROW, overrides=None, long_run=False, rules=ALL_RULES, free=False):
    modes = ("req", "prev", "base") + (("free",) if free else ())
    jobs = [(s, m, regrow, overrides, long_run, tuple(rules)) for s in range(1, seeds + 1) for m in modes]
    with Pool() as p:
        res = p.map(run, jobs)
    by = {(r["seed"], r["mode"]): r for r in res}
    print(f"GDD 17 · Dương xỉ regrow {regrow} · thay số {overrides or '—'} · luật {sorted(rules) or '—'} · "
          f"{'chạy đủ 4 giờ thật' if long_run else 'dừng ở kết game'} · giờ là giờ thật (×100); số con / cột: nửa sau lần chạy")
    print("cột: mới (luật mới) / trước (cùng số, không luật mới) / gốc (huntsim)")
    print(f"{'seed':>4} {'Kết mới/trước/gốc':>17} | {'rừng':>4} {'đoạn':>4} | {'hươu tb/min/%/đến':>20} {'sói tb/min/%/đến':>20} "
          f"{'hang':>4} {'sói/đoạn':>8} {'sói→sóc':>7} {'nhập':>4} | {'thỏ':>11} {'cáo':>11} {'sóc':>11} {'cá':>11} {'diệc':>11}")
    tot = {m: [] for m in modes}
    agg = []
    for seed in range(1, seeds + 1):
        rq, pv, bs_ = by[(seed, "req")], by[(seed, "prev")], by[(seed, "base")]
        a, p_, b = stats(rq), stats(pv), stats(bs_)
        agg.append((a, p_, b, rq, pv))
        for m in modes:
            if by[(seed, m)]["ending"]:
                tot[m].append(by[(seed, m)]["ending"] / 60 / ws.SIM_PER_REAL)
        cell = lambda d, r, name: f"{d['mean']:>4.1f}/{d['min']:>2}/{d['present']:>4.0%}/{rh(r['arrived'].get(name)):>5}"
        an = " ".join(f"{a['means'][k]:>3.0f}/{p_['means'][k]:>3.0f}/{b['means'][k]:<3.0f}" for k in range(5))
        print(f"{seed:>4} {rh(rq['ending']):>5}/{rh(pv['ending']):>5}/{rh(bs_['ending']):>5} | {a['forest_mean']:>4.0f} {a['fregs']:>4.1f} | "
              f"{cell(a['deer'], rq, DEER):>20} {cell(a['wolf'], rq, WOLF):>20} {a['dens']:>4.1f} {a['wolf_per_forest']:>8.1f} "
              f"{rq['wolf_sq']:>7.1f} {rq['joins']:>4.0f} | {an}")
        print(f"     trước: hươu {cell(p_['deer'], pv, DEER)} sói {cell(p_['wolf'], pv, WOLF)} hang {p_['dens']:.1f} · "
              f"mới: bị săn/ng {({n: round(v, 1) for n, v in rq['hunted'].items()})} · chết đói/ng "
              f"{({n: round(v, 1) for n, v in rq['starved'].items()})} · chưa đến {rq['missing']}")
    n = len(agg)
    avg = lambda f: sum(f(x) for x in agg) / n
    for i, label in ((0, "mới"), (1, "trước")):
        print(f"\nTrung bình {label}: hươu {avg(lambda x: x[i]['deer']['mean']):.1f} con, có mặt {avg(lambda x: x[i]['deer']['present']):.0%} · "
              f"sói {avg(lambda x: x[i]['wolf']['mean']):.1f} con, có mặt {avg(lambda x: x[i]['wolf']['present']):.0%}, "
              f"{avg(lambda x: x[i]['dens']):.1f} hang, {avg(lambda x: x[i]['wolf_per_forest']):.1f} sói / đoạn Rừng "
              f"(đoạn ≥ 5 cột: {avg(lambda x: x[i]['fregs']):.1f}) · rừng {avg(lambda x: x[i]['forest_mean']):.0f} cột, "
              f"Dương xỉ {avg(lambda x: x[i]['fern']):.0f}", end="")
    print(f"\nSói bắt Sóc: {avg(lambda x: x[3]['wolf_sq']):.2f} con/ngày mp · con lẻ nhập bầy {avg(lambda x: x[3]['joins']):.1f} lần/ngày mp · "
          f"Q57 cho cặp mới đến {avg(lambda x: x[3]['releases']):.2f} lần/ngày mp")
    print("Trung bình cả lần chạy mới / trước / gốc:",
          " · ".join(f"{TRACK[k]} {avg(lambda x: x[0]['means'][k]):.1f}/{avg(lambda x: x[1]['means'][k]):.1f}/{avg(lambda x: x[2]['means'][k]):.1f}"
                     for k in range(5)))
    for m, label in (("req", "mới"), ("prev", "trước"), ("base", "huntsim gốc"), ("free", "mới, không đòi Hươu+Sói")):
        if m in tot:
            e = sorted(tot[m])
            print(f"Kết game ({label}): {len(e)}/{seeds} seed" + (f", trung vị {e[len(e) // 2]:.1f} giờ thật (min {e[0]:.1f}, max {e[-1]:.1f})" if e else ""))


def forest_timeline(seeds=8):
    """Số cột Rừng của người chơi mô hình (huntsim gốc) theo giờ thật."""
    res = Pool().map(run, [(s, "base", 0.0, None, True, ()) for s in range(1, seeds + 1)])
    marks = [h * 60 * ws.SIM_PER_REAL for h in (0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0)]
    print("Cột Rừng / Dương xỉ sống theo giờ thật, huntsim gốc, chạy đủ 4 giờ:")
    print(f"{'seed':>4} " + " ".join(f"{m / 60 / ws.SIM_PER_REAL:>8.2f}h" for m in marks) + "   Kết")
    for r in res:
        at = {x[0]: x for x in r["samples"]}
        cells = []
        for m in marks:
            x = at.get(m - m % 600) or r["samples"][-1]
            cells.append(f"{x[1]:>4}/{x[2]:<4}")
        print(f"{r['seed']:>4} " + " ".join(f"{c:>9}" for c in cells) + f"   {rh(r['ending'])}")


def _num(v):
    try:
        return int(v)
    except ValueError:
        return float(v)


if __name__ == "__main__":
    args = sys.argv[1:]
    seeds = next((int(a) for a in args[1:] if a.isdigit()), 8)
    regrow = next((float(a[7:]) for a in args if a.startswith("regrow=")), FERN_REGROW)
    overrides = dict(DRAFT) if "draft" in args else {}
    overrides |= {a.split("=")[0]: _num(a.split("=")[1]) for a in args if "=" in a and a.split(".")[0] in ("deer", "wolf")}
    if args and args[0] == "forest":
        forest_timeline(seeds)
    else:
        rules = [r for r in ALL_RULES if "draft" not in args and "no" + r[1:] not in args]   # ✅ luật đã chốt: bật mặc định
        rules += [a for a in args if a in ("present2", "skipheron", "skipfox") or a.startswith("lone=")]
        if "draft" not in args and "heronq54" not in args and "skipheron" not in rules:
            rules.append("skipheron")       # ✅ Q56: Diệc giữ luật đến cũ
        survey(seeds, regrow, overrides or None, long_run="long" in args, rules=rules, free="free" in args)
