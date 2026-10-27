"""
Đếm khoảnh khắc M5 rút gọn (GDD 15 §3) trên mô hình hang thỏ / rượt bắt (huntsim.py, GDD 14).
Chỉ đếm, không đổi luật. Mặc định quà không cộng vào Sinh khí; thêm `rewards` để giả định người chơi click hết
mọi khoảnh khắc ngay khi hiện (tiêu chí 3 của GDD 15 §3.7).
Thông số đọc từ balance.json → moments (GDD 15 §3.3–3.6, Tech Doc 09 §2).
Không mô hình giới hạn "3 trong khung nhìn, 1 mỗi vùng": đó là giới hạn hiển thị, không bỏ khoảnh khắc.

    python3 Docs/GDD/sim/momentsim.py survey [seeds]           # đếm
    python3 Docs/GDD/sim/momentsim.py survey [seeds] rewards   # đếm, và cộng quà như click hết
    python3 Docs/GDD/sim/momentsim.py survey [seeds] gap=90 dry=10   # thử giãn cách nhóm A (giây) / hồi lại 💧 (phút)
"""
import sys

import worldsim as ws
import biomesim as bs
import huntsim as hs

REAL = ws.SIM_PER_REAL                  # phút mô phỏng mỗi phút thật
M = ws.B["moments"]                     # GDD 15 §3; thời gian tính bằng phút thật (Tech Doc 09 §2)
GAP_A = M["newGiftMinGapMinutes"] * REAL                # giãn cách 2 khoảnh khắc nhóm A mới
COOLDOWN_BIRTH = M["birthCooldownMinutes"] * REAL       # 🐣 hồi lại mỗi vùng
COOLDOWN_ARRIVE = M["arriveCooldownMinutes"] * REAL     # ✨ Đến nơi mới hồi lại mỗi vùng
COOLDOWN_DRY = M["droughtCooldownMinutes"] * REAL       # 💧 hồi lại mỗi vùng (Q39)
LIFETIME = M["lifetimeMinutes"] * REAL                  # 💧 tự tắt sau chừng này nếu chưa hết khô
RECOVERING_MAX = M["birthRecoveringMax"]
DRY = M["drought"]
PREDATORS = {"Cáo", "Diệc"}
QUEUED = {"new", "discover"}            # tới sớm hơn giãn cách thì chờ lượt, không bỏ
REWARD_MINUTES = {"arrive": M["giftMinutes"], "birth": M["giftMinutes"], "new": M["newSpeciesGiftMinutes"]}
REWARD_MIN = {"arrive": M["giftMin"], "birth": M["giftMin"], "new": M["newSpeciesGiftMin"]}
KINDS = [("new", "✨Loài"), ("arrive", "✨Đến"), ("birth", "🐣"), ("discover", "🌱"), ("dry", "💧")]


class MomentWorld(hs.HuntWorld):
    def __init__(self, seed, rewards=False, **kw):
        super().__init__(seed, **kw)
        self.rewards = rewards
        self.zone_at = {x: z for z in self.zones for x in range(z.start, z.end)}
        self.moments = []               # (phút, loại)
        self.dropped = {k: 0 for k, _ in KINDS}
        self.queue = []
        self.last_a = -GAP_A
        self.cooldown = {}              # (loại, vùng) → phút được hiện lại
        self.dry_until = {}             # vùng → phút 💧 đang hiện tự tắt
        self.first_births = set()       # (loài, vùng) đã có lần sinh đầu

    # ---- phát khoảnh khắc ---------------------------------------------------------
    def emit(self, kind, z=None):
        if not getattr(self, "ready", False):
            return
        key = (kind, z.i if z is not None else None)
        if z is not None and self.minute < self.cooldown.get(key, -1):
            self.dropped[kind] += 1
            return
        if kind != "dry" and self.minute - self.last_a < GAP_A:
            if kind in QUEUED:
                self.queue.append(kind)
            else:
                self.dropped[kind] += 1
            return
        self.show(kind)
        if z is not None:
            self.cooldown[key] = self.minute + {"birth": COOLDOWN_BIRTH, "arrive": COOLDOWN_ARRIVE}.get(kind, 0)

    def show(self, kind):
        self.moments.append((self.minute, kind, self.season))
        if kind != "dry":
            self.last_a = self.minute
        if self.rewards and kind in REWARD_MINUTES:
            gift = max(REWARD_MIN[kind], self.essence_rate() * REWARD_MINUTES[kind])
            self.essence += gift

    # ---- nguồn sự kiện ------------------------------------------------------------
    def arrive(self, name, x, site):
        first = name not in self.arrived
        super().arrive(name, x, site)
        self.emit("new" if first else "arrive", self.zone_at.get(x))

    def learn(self, name):
        if name not in self.known:
            self.emit("discover")
        super().learn(name)

    def animals_step(self, s):
        before = {id(a) for a in self.animals}
        super().animals_step(s)
        litters = {}
        for a in self.animals:
            if id(a) not in before and a.age == 0:
                litters.setdefault((a.name, a.x), []).append(a)
        for (name, x), kids in litters.items():
            z = self.zone_at.get(x)
            if z is None:
                continue
            first = (name, z.i) not in self.first_births
            self.first_births.add((name, z.i))
            others = self.count_animal(name, z) - len(kids)
            if name in PREDATORS or first or others <= RECOVERING_MAX or name == "Ong":
                self.emit("birth", z)

    def land_zones(self):
        for z in self.zones:
            if z.kind == "garden":
                continue
            land = [c for c in self.zone_cols(z) if c.ground == "land" and c.alive]
            if land:
                yield z, land

    def check_dry(self):
        for z, land in self.land_zones():
            moist = sum(c.moist for c in land) / len(land)
            if z.i in self.dry_until:
                if moist >= DRY["endMoistureAbove"] or self.minute >= self.dry_until[z.i]:
                    del self.dry_until[z.i]
                    self.cooldown[("dry", z.i)] = self.minute + COOLDOWN_DRY
                continue
            if moist >= DRY["moistureBelow"] or self.minute < self.cooldown.get(("dry", z.i), -1):
                continue
            yellow = sum(1 for c in land for p in c.layers if p and p.living and p.health < DRY["yellowHealthBelow"])
            if yellow >= DRY["yellowPlants"]:
                self.dry_until[z.i] = self.minute + LIFETIME
                self.cooldown[("dry", z.i)] = self.dry_until[z.i]
                self.show("dry")

    def step(self):
        if self.queue and self.minute - self.last_a >= GAP_A:
            self.show(self.queue.pop(0))
        if self.minute % 10 == 0:
            self.check_dry()
        super().step()


def gaps(times, start, end):
    pts = [start] + [t for t in times if start <= t <= end] + [end]
    return max(b - a for a, b in zip(pts, pts[1:]))


def survey(seeds=8, rewards=False):
    print("Khoảnh khắc M5 rút gọn (GDD 15 §3) trên huntsim · thời gian là phút thật" + (" · cộng quà như click hết" if rewards else ""))
    head = " ".join(f"{label:>6}" for _, label in KINDS)
    print(f"{'seed':>4} {'Kết':>5} {head} {'tổng':>5} {'mỗi':>5} {'trống max':>9} {'đầu tiên':>8} {'10ph đầu':>8} {'trống 10ph':>10}")
    rows, dry_seasons = [], {}
    for seed in range(1, seeds + 1):
        w = MomentWorld(seed, rewards=rewards)
        w.ready = True
        while w.minute < ws.MAX_HOURS * 60 and w.ending is None:
            w.step()
        end = w.ending or w.minute
        times = [t for t, _, _ in w.moments if t <= end]
        count = {k: sum(1 for t, kk, _ in w.moments if kk == k and t <= end) for k, _ in KINDS}
        for t, kk, season in w.moments:
            if kk == "dry" and t <= end:
                dry_seasons[season] = dry_seasons.get(season, 0) + 1
        early = [t for t in times if t <= 10 * REAL]
        row = dict(end=end / 60 / REAL if w.ending else None, total=len(times),
                   every=end / REAL / max(1, len(times)),
                   gap=gaps(times, 10 * REAL, end) / REAL if end > 10 * REAL else 0,
                   first=times[0] / REAL if times else None, early=len(early), early_gap=gaps(times, 0, 10 * REAL) / REAL,
                   **count)
        rows.append(row)
        cells = " ".join(f"{count[k]:>6}" for k, _ in KINDS)
        first = f"{row['first']:.1f}" if row["first"] is not None else "—"
        print(f"{seed:>4} {bs.real_h(w.ending):>5} {cells} {row['total']:>5} {row['every']:>5.1f} {row['gap']:>9.1f} "
              f"{first:>8} {row['early']:>8} {row['early_gap']:>10.1f}")
        first_species = " ".join(f"{n}:{(m / REAL):.0f}ph" for n, m in sorted(w.arrived.items(), key=lambda t: t[1]))
        print(f"     loài đến: {first_species} · bị bỏ vì giãn cách / hồi lại: {({k: v for k, v in w.dropped.items() if v})}")

    def med(key):
        vals = sorted(r[key] for r in rows if r[key] is not None)
        return vals[len(vals) // 2] if vals else None

    ends = sorted(r["end"] for r in rows if r["end"] is not None)
    print(f"\nTrung vị: tổng {med('total')} · mỗi {med('every'):.1f} phút thật một khoảnh khắc · trống dài nhất sau 10 phút đầu "
          f"{med('gap'):.1f} phút (max {max(r['gap'] for r in rows):.1f}) · khoảnh khắc đầu tiên ở phút {med('first'):.1f} · "
          f"{med('early')} khoảnh khắc trong 10 phút đầu, trống dài nhất {med('early_gap'):.1f} phút")
    print("💧 theo mùa (cộng mọi seed):", dry_seasons)
    print("Trung vị mỗi loại:", " · ".join(f"{label} {med(k)}" for k, label in KINDS))
    print(f"Kết game: {len(ends)}/{seeds} seed" + (f", trung vị {ends[len(ends) // 2]:.2f} giờ thật "
                                                   f"(min {ends[0]:.2f}, max {ends[-1]:.2f})" if ends else ""))


if __name__ == "__main__":
    args = sys.argv[1:]
    seeds = next((int(a) for a in args[1:] if a.isdigit()), 8)
    for a in args:
        if a.startswith("gap="):
            GAP_A = REAL * int(a[4:]) // 60
        if a.startswith("dry="):
            COOLDOWN_DRY = REAL * int(a[4:])
    hs.use_hunting()
    print(f"giãn cách nhóm A {GAP_A * 60 // REAL} giây · 💧 hồi lại {COOLDOWN_DRY // REAL} phút")
    survey(seeds, rewards="rewards" in args)
