"""
Người chơi chỉ liếc mỗi 15–30 phút thật (GDD 18). Dựa trên forestsim.py (bộ luật GDD 17 đã chốt, có Hươu, Sói) cộng
bộ đếm khoảnh khắc của momentsim.py; mọi cây gieo được mở từ đầu (04 §3, 2026-10-28) nên không còn 🌱.
Ở mỗi lần liếc, đo:
- **chuyện lớn** từ lần liếc trước: loài mới, ao thức dậy, rừng thành hình (≥ 3 cột), đất hoang phủ kín, Vườn mở, kết game;
- **đất lan**: số cột đất hoang có sự sống mới từ lần liếc trước;
- bong bóng nhóm A (✨ 🐣) **còn hiện** lúc liếc, và tỉ lệ bong bóng được thấy ít nhất một lần.
Người chơi mô hình như biomesim (mưa vùng khô, gieo theo biome, lấn đất hoang ở hai mép), làm `acts` lượt lấn đất mỗi lần ghé.

Thời gian thật (GDD 18 §2): mô hình vẫn đi từng **bước**; `clock=` là số bước mỗi phút thật, tức tốc độ của mọi vòng đời
sinh thái (balance.json tính theo bước). Không phải tăng tốc thời gian: cùng một thế giới, vòng đời dài ngắn khác nhau.
- `season=` / `day=`: độ dài mùa / ngày đêm tính bằng phút thật (mặc định theo balance.json ở ×100);
- `pgrow=`: cây tầng Thảm và Bụi lớn nhanh gấp N lần (tuổi thọ không đổi);
- `pace=`: loài chưa từng xuất hiện chỉ được đến khi loài mới trước đó đã đến ≥ pace phút thật;
- `life=`: bong bóng sống N phút thật (mặc định 8, GDD 15 §3.3).

    python3 Docs/GDD/sim/glancesim.py survey [seeds] [every=3,15,30] [hours=12] [acts=1] [clock=100] [season=] [day=] [pgrow=1] [pace=0] [life=8]
    python3 Docs/GDD/sim/glancesim.py timeline [seed] [every=15] [...]     # nhật ký từng lần liếc của một seed
"""
import sys
from multiprocessing import Pool

import worldsim as ws
import biomesim as bs
import huntsim as hs
import forestsim as fs
import momentsim as ms

RULES = fs.ALL_RULES + ("skipheron",)       # ✅ bộ luật đã chốt của GDD 17 (Q52–Q57, Q56)
SOWABLE = {n for n in bs.COSTS if n != "rain"}
MILESTONES = ("thức dậy", "đất hoang đã phủ kín", "Khu Vườn Thiêng mở", "Cây Thế Giới nở hoa")
FOREST_FORMED = 3
M = ms.M
GROW = {n: p["grow"] for n, p in ws.PLANTS.items()}     # số gốc, để pgrow không nhân dồn khi Pool dùng lại tiến trình
DEFAULTS = dict(every=15, hours=12, acts=1, clock=ws.SIM_PER_REAL, season=None, day=None, pgrow=1,
                pace=ws.B["biomeModel"]["arrival"]["newSpeciesGapMinutes"], life=None)


def use_options(o):
    """Thời gian của khoảnh khắc tính bằng phút thật; mùa, ngày đêm tính bằng phút thật nếu có."""
    c = o["clock"]
    ms.GAP_A = M["newGiftMinGapMinutes"] * c
    ms.COOLDOWN_BIRTH = M["birthCooldownMinutes"] * c
    ms.COOLDOWN_ARRIVE = M["arriveCooldownMinutes"] * c
    ms.COOLDOWN_DRY = M["droughtCooldownMinutes"] * c
    ms.LIFETIME = (o["life"] or M["lifetimeMinutes"]) * c
    if o["day"]:
        hs.DAY_NIGHT = o["day"] * c         # GDD 11 §1.5
    for n, p in ws.PLANTS.items():
        p["grow"] = GROW[n] if p["layer"] == 2 else max(1, round(GROW[n] / o["pgrow"]))


class GlanceWorld(ms.MomentWorld, fs.ForestWorld):
    def __init__(self, seed, o):
        c = o["clock"]
        kw = {"hours_per_day": o["season"] * c / 60} if o["season"] else {}
        super().__init__(seed, player_every=round(o["every"] * c), **kw)
        self.known = set(SOWABLE)           # 04 §3 (2026-10-28): mọi cây gieo được mở từ đầu
        self.acts = o["acts"]
        self.pace = o["pace"] * c           # loài mới cách nhau ≥ pace bước
        self.last_new = -self.pace
        self.ready = True

    def arrive(self, name, x, site):
        if name not in self.arrived:
            if self.minute - self.last_new < self.pace:
                return                      # chưa tới lượt: đồng hồ chờ 2 giờ của cặp này đã về 0, thử lại sau
            self.last_new = self.minute
        super().arrive(name, x, site)

    def expand(self):
        for _ in range(self.acts):
            super().expand()

    def step(self):
        """biomesim chỉ cho người chơi mô hình ghé ở bước kiểm tra định kỳ (mỗi 30 bước): nhịp ghé không chia hết cho 30 thì
        thực ra ghé thưa hơn. Ở đây người chơi ghé đúng mỗi player_every bước."""
        m = self.minute
        super().step()
        if self.player and m % self.player_every == 0 and m % ws.PERIODIC_MINUTES != 0:
            if self.rains:
                self.rain_dry()
            for _ in range(max(1, min(10, self.player_every // ws.PERIODIC_MINUTES))):
                self.sow()
            self.expand()
            if self.filled is not None:
                self.plant_forest_patch()


def alive_land(w):
    return sum(1 for c in w.cols if c.alive and c.ground == "land")


def run(args):
    seed, o = args
    fs.setup(fs.FERN_REGROW, None, RULES)
    hs.use_hunting()
    use_options(o)
    clock, step = o["clock"], round(o["every"] * o["clock"])
    w = GlanceWorld(seed, o)
    glances, seen_log, land, season, forest = [], 0, alive_land(w), w.season, False
    while w.minute < o["hours"] * 60 * clock:
        w.step()
        if w.minute % step:
            continue                # kết game giữa hai lần liếc: người chơi thấy ở lần liếc kế tiếp
        t = w.minute
        showing = sum(1 for m, k, _ in w.moments if k != "dry" and t - ms.LIFETIME < m <= t)
        big = [e for m, e in w.log[seen_log:] if e.startswith("✨ loài mới") or any(s in e for s in MILESTONES)]
        forest_now = sum(1 for c in w.cols if c.alive and c.biome == "forest") >= FOREST_FORMED
        if forest_now and not forest:
            big.append("rừng thành hình")
        now_land = alive_land(w)
        glances.append(dict(t=t / clock, showing=showing, big=big, spread=now_land - land, season=w.season,
                            new_season=w.season != season))
        seen_log, land, season, forest = len(w.log), now_land, w.season, forest or forest_now
        if w.ending is not None:
            break
    times = [g["t"] * clock for g in glances]
    shown = [m for m, k, _ in w.moments if k != "dry" and m <= (times[-1] if times else 0)]
    caught = sum(1 for m in shown if any(m <= t < m + ms.LIFETIME for t in times))
    days = max(1.0, w.minute / 1440)
    return dict(seed=seed, every=o["every"], ending=w.ending and w.ending / clock,
                garden=w.garden_unlocked and w.garden_unlocked / clock, filled=w.filled and w.filled / clock,
                arrived={n: m / clock for n, m in w.arrived.items()}, glances=glances, moments=len(shown), caught=caught,
                missing=[n for n in w.ALL_SPECIES if n not in w.arrived],
                pop={n: w.count_animal(n) for n in ("Thỏ", "Cáo", bs.SQUIRREL, "Cá", "Diệc", fs.DEER, fs.WOLF, "Ong")},
                starved=sum(w.starved.values()) / days, hunted=sum(w.hunted.values()) / days)


def summarize(r):
    g = r["glances"]
    quiet, streak = 0, 0
    for x in g:     # chuỗi lặng không tính mùa Đông (GDD 18 §3.5)
        streak = 0 if x["big"] or x["season"] == "Đông" else streak + 1
        quiet = max(quiet, streak)
    n = max(1, len(g))
    return dict(n=len(g), crowd=max((len(x["big"]) for x in g), default=0),
                bubble=sum(1 for x in g if x["showing"]) / n, caught=r["caught"] / max(1, r["moments"]),
                big=sum(1 for x in g if x["big"]) / n,
                bigspread=sum(1 for x in g if x["big"] or x["spread"] >= 3) / n,
                quiet=quiet * r["every"], last_new=max(r["arrived"].values(), default=0))


def med(vals):
    v = sorted(x for x in vals if x is not None)
    return v[len(v) // 2] if v else None


def fmt_h(m):
    return "—" if m is None else f"{m / 60:.1f}h"


def describe(o):
    return (f"{o['clock']} bước / phút thật · mùa {o['season'] or 'mặc định'} · ngày đêm {o['day'] or 'mặc định'} · "
            f"Thảm/Bụi lớn nhanh ×{o['pgrow']} · loài mới cách ≥ {o['pace']} phút · bong bóng {o['life'] or M['lifetimeMinutes']} phút · "
            f"lấn đất {o['acts']} lượt mỗi lần ghé · tối đa {o['hours']} giờ thật")


def survey(seeds, everies, o):
    print(describe(o))
    print("liếc = số lần liếc tới kết · lớn = % lần liếc có chuyện lớn · +đất = có chuyện lớn hoặc đất lan ≥ 3 cột · "
          "lặng = chuỗi dài nhất không chuyện lớn, trừ mùa Đông (phút) · dồn = nhiều chuyện lớn nhất trong một lần liếc · "
          "thấy = % ✨/🐣 được thấy ít nhất một lần")
    with Pool() as pool:
        for every in everies:
            res = pool.map(run, [(s, dict(o, every=every)) for s in range(1, seeds + 1)])
            print(f"\n== Liếc mỗi {every} phút ==")
            print(f"{'seed':>4} {'Vườn':>6} {'Kết':>6} {'liếc':>5} {'lớn':>5} {'+đất':>5} {'lặng':>5} {'dồn':>4} {'thấy':>5} "
                  f"{'đói/ng':>6} {'săn/ng':>6}  thiếu / loài đến (phút thật)")
            rows = []
            for r in res:
                s = summarize(r)
                rows.append((r, s))
                arr = " ".join(f"{k}:{v:.0f}" for k, v in sorted(r["arrived"].items(), key=lambda t: t[1]))
                miss = ("thiếu " + ",".join(r["missing"]) + " · ") if r["missing"] else ""
                print(f"{r['seed']:>4} {fmt_h(r['garden']):>6} {fmt_h(r['ending']):>6} {s['n']:>5} {s['big']:>5.0%} {s['bigspread']:>5.0%} "
                      f"{s['quiet']:>5} {s['crowd']:>4} {s['caught']:>5.0%} {r['starved']:>6.0f} {r['hunted']:>6.0f}  {miss}{arr}")
            ends = [r["ending"] for r, _ in rows if r["ending"]]
            m = lambda k: med(s[k] for _, s in rows)
            print(f"Kết {len(ends)}/{seeds}, trung vị {fmt_h(med(ends))} (min {fmt_h(min(ends, default=None))}, max {fmt_h(max(ends, default=None))}) · "
                  f"trung vị: liếc {m('n')} · lớn {m('big'):.0%} · +đất {m('bigspread'):.0%} · lặng {m('quiet')} phút · "
                  f"dồn {m('crowd')} · thấy {m('caught'):.0%}")
            print("Quần thể lúc kết (trung vị): " + " · ".join(f"{n} {med(r['pop'][n] for r, _ in rows)}" for n in rows[0][0]["pop"]))


def timeline(seed, o):
    r = run((seed, o))
    print(describe(o))
    print(f"Seed {seed}, liếc mỗi {o['every']} phút · Vườn mở {fmt_h(r['garden'])} · kết {fmt_h(r['ending'])}")
    for x in r["glances"]:
        print(f"{x['t']:>5.0f}' {x['season'] if x['new_season'] else '':<4} bóng {x['showing']:<2} đất +{x['spread']:<3} "
              + " · ".join(x["big"]))


if __name__ == "__main__":
    args = sys.argv[1:]
    num = next((int(a) for a in args[1:] if a.isdigit()), None)
    o = dict(DEFAULTS)
    everies = [3, 15, 30]
    for a in args:
        if "=" not in a:
            continue
        k, v = a.split("=", 1)
        if k == "every":
            everies = [int(x) for x in v.split(",")]
        elif k in DEFAULTS:
            o[k] = float(v) if k in ("hours", "pgrow", "clock") else int(v)
    if args and args[0] == "timeline":
        timeline(num or 1, dict(o, every=everies[0] if len(everies) == 1 else 15))
    else:
        survey(num or 8, everies, o)
