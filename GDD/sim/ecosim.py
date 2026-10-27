"""
Mô hình kiểm chứng số liệu cho GDD 07 (hệ sinh thái chi tiết).
Chạy ở bước 1 phút (game thật dùng 1 giây cho sinh vật; kết quả trung bình tương đương).

    python3 Docs/GDD/sim/ecosim.py [hours] [seed]      # bảng theo giờ cho 1 seed
    python3 Docs/GDD/sim/ecosim.py survey              # 20 seed, người chơi bỏ mặc
    python3 Docs/GDD/sim/ecosim.py survey rain         # 20 seed, người chơi ghé 30 phút và gọi mưa khi khô

In ra bảng theo giờ: độ phủ cỏ, số lượng từng loài, Sinh khí/phút, hệ số đa dạng/cân bằng.
Không phụ thuộc thư viện ngoài.
"""
import math
import random
import sys

# ---------------------------------------------------------------------------
# Tham số (giữ đồng bộ với Docs/GDD/07-he-sinh-thai-chi-tiet.md)
# ---------------------------------------------------------------------------
COLUMNS = 48                 # vùng đồng cỏ prototype
START_GRASS = 5

SEASONS = ["Xuân", "Hạ", "Thu", "Đông"]
EVAPORATION = {"Xuân": 0.05, "Hạ": 0.10, "Thu": 0.06, "Đông": 0.02}   # độ ẩm mất/phút
RAIN_CHANCE_PER_HOUR = {"Xuân": 0.30, "Hạ": 0.06, "Thu": 0.15, "Đông": 0.05}
RAIN_AMOUNT = 30
SNOWMELT = 40               # độ ẩm cộng thêm cho mọi cột lúc bắt đầu mùa xuân
DORMANT_FOOD = 0.5         # cỏ ngủ khô vẫn ăn được, giá trị 50%, không mọc lại
PLAYER_RAIN_COST = 30
PLAYER_RAIN_BELOW = 25     # người chơi "ghé 30 phút" gọi mưa khi độ ẩm trung bình dưới mức này
GROWTH_SEASON = {"Xuân": 1.25, "Hạ": 1.0, "Thu": 0.8, "Đông": 0.3}
BREED_SEASON = {"Xuân": 1.5, "Hạ": 1.0, "Thu": 0.7, "Đông": 0.2}

WASTE_FERTILITY = 10
DECOMP_BASE = 0.02           # tỉ lệ Mùn → Đất màu mỗi phút, không có giun
DECOMP_WORM = 0.06           # có giun
DECOMP_YIELD = 0.8
MOIST_DIFFUSION = 0.05

PLANTS = {
    # layer, grow(min), life(min), moisture(min, lo, hi, max), fertility min, light min,
    # seeds/hour, range, uptake water/min, uptake fertility/min, detritus on death, essence/min
    "Cỏ":      dict(layer=0, grow=20,  life=1440, moist=(15, 30, 85, 100), fert=10, light=40,
                    seeds=3.0, range=2, water=0.02, fertuse=0.004, detritus=8,  essence=0.05,
                    regrow=0.6, flower=False, perennial=True),
    "Hoa dại": dict(layer=0, grow=40,  life=1440, moist=(25, 40, 80, 100), fert=25, light=60,
                    seeds=1.5, range=3, water=0.025, fertuse=0.006, detritus=6,  essence=0.10,
                    regrow=0.0, flower=True, perennial=False),
    "Mâm xôi": dict(layer=1, grow=120, life=5760, moist=(30, 45, 85, 100), fert=35, light=40,
                    seeds=0.4, range=2, water=0.04, fertuse=0.008, detritus=20, essence=0.15,
                    regrow=0.0, flower=True, perennial=True),
}

ANIMALS = {
    # need/min = thức ăn cần mỗi phút; life, mature, litter, cooldown (phút); range (cột)
    "Thỏ": dict(role="ăn cỏ",   eats="grass",  need=1.5, life=2880, mature=60,  litter=2,
                cooldown=90,  range=5, essence=0.25, detritus=5),
    "Cáo": dict(role="săn mồi", eats="rabbit", need=1 / 240, life=5760,mature=180, litter=1,
                cooldown=720, range=12, essence=0.60, detritus=10),
    "Ong": dict(role="thụ phấn", eats="nectar", need=0, life=2880, mature=240, litter=1,
                cooldown=480, range=6, essence=0.30, detritus=0),
}
WORM_ESSENCE = 0.04          # mỗi cột có giun
POLLINATION_BONUS = 2.0
FED_GAIN = 0.9             # độ no tăng/phút khi ăn đủ
STARVE_DRAIN = 0.4         # độ no giảm/phút (đói hẳn từ 80 → 0 mất ~3h20)
LEAVE_HUNGER = 10          # đói đến mức này thì bỏ đi (di cư), không chết
FORAGE_SIGHT = 12           # cột: tầm nhìn khi đi tìm thức ăn
CAPACITY_SAFETY = 0.7       # chỉ sinh sản tới 70% sức chứa thực tế
RETURN_AFTER = 120         # loài đã khám phá tự quay lại sau 2 giờ điều kiện đạt liên tục
WET_FLOOR = 0.5
HEALTH_RATE = 1.0           # máu cây đổi (q - 0.35) * HEALTH_RATE mỗi phút
SEEDBANK_SPROUT = 1 / 180   # xác suất/phút nảy mầm từ hạt ngủ (nhân với q)
CATCH_BASE = 0.25           # xác suất bắt/phút khi đang săn
LAST_PAIR = 2
WINTER_PREDATOR_NEED = 0.5  # mùa đông thú săn nằm ổ nhiều, chỉ cần ăn một nửa
PREY_PER_PREDATOR = 8      # cáo chỉ sinh sản khi trong vùng có > 8 thỏ cho mỗi cáo
PREY_COMFORT = 6            # dưới 6 con mồi trong vùng thì xác suất bắt giảm tuyến tính
BERRY_GAIN = 0.3            # cáo ăn quả mâm xôi khi đói (hạ, thu): độ no +0.3/phút
SHRUB_ESCAPE = 0.5           # thỏ cạnh bụi mâm xôi: giảm 50% bị bắt

INVITE = {  # điều kiện + giá
    "Giun": dict(cost=20,  cond=lambda w: w.count_living("Cỏ") >= 6),
    "Thỏ":  dict(cost=60,  cond=lambda w: w.count_living("Cỏ") >= 10),
    "Ong":  dict(cost=80,  cond=lambda w: w.count_living("Hoa dại") >= 4),
    "Cáo":  dict(cost=200, cond=lambda w: w.count_animal("Thỏ") >= 6),
}
START_ESSENCE = 40


def suitability(spec, col):
    lo_min, lo, hi, hi_max = spec["moist"]
    m = col.moist
    if m < lo_min:
        sm = 0.0
    elif m < lo:
        sm = (m - lo_min) / (lo - lo_min)
    elif m > hi:
        # quá ẩm chỉ làm chậm lớn (sàn WET_FLOOR), không giết cây cạn
        sm = max(WET_FLOOR, 1 - (1 - WET_FLOOR) * (m - hi) / (hi_max - hi))
    else:
        sm = 1.0
    sf = min(1.0, max(0.0, (col.fert - spec["fert"] * 0.5) / (spec["fert"] * 0.5)))
    light = col.light(spec["layer"])
    sl = min(1.0, max(0.0, (light - spec["light"] * 0.5) / (spec["light"] * 0.5)))
    return sm * sf * sl


class Plant:
    def __init__(self, name):
        self.name = name
        self.spec = PLANTS[name]
        self.age = 0
        self.growth = 0.0
        self.health = 100.0
        self.biomass = 30.0
        self.dormant = False

    @property
    def mature(self):
        return self.growth >= 1.0


class Column:
    def __init__(self, i):
        self.i = i
        self.moist = 50.0
        self.fert = WASTE_FERTILITY + 25.0   # vùng đã hồi sinh có sẵn chút đất màu
        self.detritus = 10.0
        self.layers = [None, None]           # 0 thảm, 1 bụi (prototype chưa có tầng tán)
        self.worms = False
        self.seedbank = set()               # loài từng sống ở đây: hạt ngủ trong đất

    def light(self, layer):
        shade = 0
        if layer == 0 and self.layers[1] and self.layers[1].mature:
            shade = 30
        return 100 - shade


class Animal:
    def __init__(self, name, x, age=None):
        self.name = name
        self.spec = ANIMALS[name]
        self.x = x
        self.age = age if age is not None else self.spec["mature"]
        self.hunger = 80.0
        self.cooldown = 0


class World:
    def __init__(self, seed, rains=False):
        self.rng = random.Random(seed)
        self.rains = rains
        self.cols = [Column(i) for i in range(COLUMNS)]
        self.animals = []
        self.essence = START_ESSENCE
        self.essence_total = 0.0
        self.minute = 0
        self.log = []
        self.discovered = set()
        self.return_timer = {}
        mid = COLUMNS // 2
        for i in range(mid - START_GRASS // 2, mid + START_GRASS // 2 + 1):
            p = Plant("Cỏ")
            p.growth = 1.0
            p.biomass = 100
            self.cols[i].layers[0] = p

    # -- truy vấn -------------------------------------------------------------
    @property
    def season(self):
        return SEASONS[(self.minute // 1440) % 4]

    def count_plant(self, name):
        return sum(1 for c in self.cols for p in c.layers if p and p.name == name)

    def count_living(self, name):
        """Cây trưởng thành, không ngủ khô: dùng cho điều kiện mời/quay lại."""
        return sum(1 for c in self.cols for p in c.layers
                   if p and p.name == name and p.mature and not p.dormant)

    def count_animal(self, name):
        return sum(1 for a in self.animals if a.name == name)

    def near(self, x, r):
        return self.cols[max(0, x - r):min(COLUMNS, x + r + 1)]

    # -- bước mô phỏng -------------------------------------------------------
    def step(self):
        s = self.season
        self.weather(s)
        self.environment(s)
        self.plants(s)
        self.animals_step(s)
        self.player()
        e = self.essence_rate()
        self.essence += e
        self.essence_total += e
        self.minute += 1

    def weather(self, s):
        if self.minute % 1440 == 0 and s == "Xuân" and self.minute:
            for c in self.cols:
                c.moist = min(100, c.moist + SNOWMELT)
        if self.rng.random() < RAIN_CHANCE_PER_HOUR[s] / 60:
            for c in self.cols:
                c.moist = min(100, c.moist + RAIN_AMOUNT)

    def environment(self, s):
        for c in self.cols:
            c.moist = max(0, c.moist - EVAPORATION[s])
            rate = DECOMP_WORM if c.worms else DECOMP_BASE
            d = c.detritus * rate
            c.detritus -= d
            c.fert = min(100, c.fert + d * DECOMP_YIELD)
        # khuếch tán độ ẩm sang cột bên cạnh
        m = [c.moist for c in self.cols]
        for i, c in enumerate(self.cols):
            nb = [m[j] for j in (i - 1, i + 1) if 0 <= j < COLUMNS]
            c.moist += MOIST_DIFFUSION * (sum(nb) / len(nb) - m[i])

    def plants(self, s):
        pollinated = set()
        for a in self.animals:
            if a.name == "Ong":
                for c in self.near(a.x, a.spec["range"]):
                    pollinated.add(c.i)
        for c in self.cols:
            for layer, p in enumerate(c.layers):
                if not p:
                    for name in c.seedbank:
                        sp = PLANTS[name]
                        if sp["layer"] == layer and self.rng.random() < SEEDBANK_SPROUT * suitability(sp, c):
                            c.layers[layer] = Plant(name)
                            break
                    continue
                sp = p.spec
                if p.mature:
                    c.seedbank.add(p.name)
                q = suitability(sp, c)
                p.age += 1
                if p.dormant:
                    # ngủ khô: không hút nước, không lớn, không sinh khí; tỉnh lại khi điều kiện tốt
                    if q >= 0.5:
                        p.health += 0.5
                        if p.health >= 30:
                            p.dormant = False
                    continue
                c.moist = max(0, c.moist - sp["water"] * GROWTH_SEASON[s])
                c.fert = max(0, c.fert - sp["fertuse"])
                if not p.mature:
                    p.growth += q * GROWTH_SEASON[s] / sp["grow"]
                if sp["regrow"]:
                    p.biomass = min(100, p.biomass + sp["regrow"] * q * GROWTH_SEASON[s])
                    if p.biomass < 10:
                        p.health -= 4
                p.health = max(0, min(100, p.health + (q - 0.35) * HEALTH_RATE))
                if p.health <= 0 and sp["perennial"] and p.mature and p.age < sp["life"]:
                    p.dormant = True
                    continue
                if p.health <= 0 or p.age >= sp["life"]:
                    c.layers[layer] = None
                    c.detritus += sp["detritus"]
                    # cây chết già thả hạt tại chỗ: thảm cỏ không biến mất hàng loạt
                    if p.age >= sp["life"] and q > 0.3:
                        c.layers[layer] = Plant(p.name)
                    continue
                if p.mature and s != "Đông":
                    rate = sp["seeds"] / 60 * q
                    if sp["flower"] and c.i in pollinated:
                        rate *= POLLINATION_BONUS
                    if self.rng.random() < rate:
                        self.drop_seed(p.name, c.i)

    def drop_seed(self, name, x):
        sp = PLANTS[name]
        off = self.rng.randint(1, sp["range"]) * self.rng.choice((-1, 1))
        t = x + off
        if not 0 <= t < COLUMNS:
            return
        col = self.cols[t]
        if col.layers[sp["layer"]] is None and self.rng.random() < suitability(sp, col):
            col.layers[sp["layer"]] = Plant(name)

    def animals_step(self, s):
        born = []
        rabbits = [a for a in self.animals if a.name == "Thỏ"]
        for a in list(self.animals):
            if a not in self.animals:   # đã bị săn trong bước này
                continue
            sp = a.spec
            a.age += 1
            a.cooldown = max(0, a.cooldown - 1)
            if sp["eats"] == "grass":
                need = sp["need"]
                for c in sorted(self.near(a.x, sp["range"]), key=lambda c: -(c.layers[0].biomass if c.layers[0] and c.layers[0].name == "Cỏ" else 0)):
                    g = c.layers[0]
                    if g and g.name == "Cỏ" and g.mature and g.biomass > 10:
                        value = DORMANT_FOOD if g.dormant else 1.0
                        take = min(need / value, g.biomass - 10)
                        g.biomass -= take
                        need -= take * value
                        if need <= 0:
                            break
                a.hunger += (sp["need"] - need) / sp["need"] * FED_GAIN - STARVE_DRAIN
                a.x = self.forage_move(a, 1)
            elif sp["eats"] == "rabbit":
                a.hunger -= 100 * sp["need"] * (WINTER_PREDATOR_NEED if s == "Đông" else 1.0)
                if a.hunger < 60:
                    prey = [r for r in rabbits if r in self.animals and abs(r.x - a.x) <= sp["range"]]
                    # luật cặp cuối: không săn khi con mồi chỉ còn <= LAST_PAIR con trong vùng
                    if len(prey) > LAST_PAIR:
                        r = self.rng.choice(prey)
                        shrub = any(c.layers[1] for c in self.near(r.x, 1))
                        scarcity = min(1.0, len(prey) / PREY_COMFORT)   # mồi hiếm thì khó bắt
                        catch = CATCH_BASE * scarcity * (SHRUB_ESCAPE if shrub else 1.0)
                        if self.rng.random() < catch:
                            self.animals.remove(r)
                            self.cols[r.x].detritus += 2
                            a.hunger = 100
                    if a.hunger < 60 and s in ("Hạ", "Thu") and any(
                            c.layers[1] and c.layers[1].mature and not c.layers[1].dormant
                            for c in self.near(a.x, 2)):
                        a.hunger += BERRY_GAIN
                a.x = max(0, min(COLUMNS - 1, a.x + self.rng.choice((-2, -1, 0, 1, 2))))
            elif sp["eats"] == "nectar":
                flowers = sum(1 for c in self.near(a.x, sp["range"]) for p in c.layers
                              if p and p.mature and p.spec["flower"])
                a.hunger += 1.0 if flowers >= 3 else -0.5
            a.hunger = max(0, min(100, a.hunger))
            if a.hunger <= LEAVE_HUNGER:
                self.animals.remove(a)
                self.log.append((self.minute, f"{a.name} bỏ đi"))
                continue
            dead = a.age >= sp["life"]
            if dead:
                if a in self.animals:
                    self.animals.remove(a)
                    self.cols[a.x].detritus += sp["detritus"]
                continue
            # sinh sản: đủ no, đủ tuổi, hết thời gian chờ, có bạn cùng loài trong vùng
            mates = sum(1 for b in self.animals if b.name == a.name and b is not a and abs(b.x - a.x) <= sp["range"])
            if (a.hunger > 70 and a.age >= sp["mature"] and a.cooldown == 0 and mates
                    and self.rng.random() < 0.5 * BREED_SEASON[s] * self.capacity_room(a)):
                a.cooldown = sp["cooldown"]
                for _ in range(sp["litter"]):
                    born.append(Animal(a.name, a.x, age=0))
        self.animals.extend(born)

    def forage_move(self, a, step):
        """Đói (< 60) thì đi về phía cột có nhiều thức ăn nhất trong tầm nhìn; no thì đi lang thang."""
        if a.hunger < 60:
            best, best_food = a.x, -1.0
            for c in self.near(a.x, FORAGE_SIGHT):
                g = c.layers[0]
                food = g.biomass * (DORMANT_FOOD if g.dormant else 1) if g and g.name == "Cỏ" and g.mature else 0
                if food > best_food or (food == best_food and abs(c.i - a.x) < abs(best - a.x)):
                    best, best_food = c.i, food
            if best != a.x:
                return a.x + (step if best > a.x else -step)
        return max(0, min(COLUMNS - 1, a.x + self.rng.choice((-step, 0, step))))

    def capacity_room(self, a):
        """0..1: còn bao nhiêu chỗ trong vùng sống (theo thức ăn)."""
        sp = a.spec
        same = sum(1 for b in self.animals if b.name == a.name and abs(b.x - a.x) <= sp["range"])
        if sp["eats"] == "grass":
            season = GROWTH_SEASON[self.season]
            food = sum(PLANTS["Cỏ"]["regrow"] * suitability(PLANTS["Cỏ"], c) * season * CAPACITY_SAFETY
                       for c in self.near(a.x, sp["range"])
                       if c.layers[0] and c.layers[0].name == "Cỏ" and c.layers[0].mature and not c.layers[0].dormant)
            cap = food / sp["need"]
        elif sp["eats"] == "rabbit":
            prey = sum(1 for b in self.animals if b.name == "Thỏ" and abs(b.x - a.x) <= sp["range"])
            cap = prey / PREY_PER_PREDATOR
        else:
            flowers = sum(1 for c in self.near(a.x, sp["range"]) for p in c.layers if p and p.spec["flower"])
            cap = flowers / 6
        return max(0.0, min(1.0, 1 - same / max(cap, 0.01)))

    # -- sinh khí ------------------------------------------------------------
    def species_counts(self):
        counts = {}
        for c in self.cols:
            for p in c.layers:
                if p:
                    counts[p.name] = counts.get(p.name, 0) + 1
        for a in self.animals:
            counts[a.name] = counts.get(a.name, 0) + 1
        worms = sum(1 for c in self.cols if c.worms)
        if worms:
            counts["Giun"] = worms
        return counts

    def multipliers(self):
        counts = self.species_counts()
        roles = {"sản xuất"} if any(n in PLANTS for n in counts) else set()
        for n in counts:
            if n in ANIMALS:
                roles.add(ANIMALS[n]["role"])
        if "Giun" in counts:
            roles.add("phân huỷ")
        species = len(counts)
        diversity = 1 + 0.15 * max(0, species - 1) + 0.25 * max(0, len(roles) - 1)

        balance = 1.0
        biomass = {n: c * (3 if n in ANIMALS else 1) for n, c in counts.items()}
        total = sum(biomass.values()) or 1
        top = max(biomass.values()) / total if biomass else 0
        if top > 0.4:
            balance -= (top - 0.4) * 1.5
        r, f = counts.get("Thỏ", 0), counts.get("Cáo", 0)
        if f and not (4 <= r / f <= 10):
            balance -= 0.2
        bare = sum(1 for c in self.cols if not any(c.layers)) / COLUMNS
        if bare > 0.3:
            balance -= 0.2
        if len(roles) >= 5 and balance >= 1.0:
            balance += 0.2
        return diversity, max(0.3, min(1.2, balance))

    def essence_rate(self):
        base = 0.0
        for c in self.cols:
            for p in c.layers:
                if p and p.mature and not p.dormant:
                    base += p.spec["essence"]
            if c.worms:
                base += WORM_ESSENCE
        for a in self.animals:
            if a.age >= a.spec["mature"]:
                base += a.spec["essence"]
        d, b = self.multipliers()
        return base * d * b

    # -- người chơi "lười": mời loài khi đủ điều kiện, thỉnh thoảng gieo hoa/bụi --
    def player(self):
        if self.minute % 30:
            return
        have = {a.name for a in self.animals}
        if any(c.worms for c in self.cols):
            have.add("Giun")
        for name, inv in INVITE.items():
            if name in self.discovered:
                # loài đã khám phá: tự quay lại miễn phí khi điều kiện đạt đủ lâu
                lonely = name in ANIMALS and self.count_animal(name) < 2
                if (name not in have or lonely) and inv["cond"](self):
                    self.return_timer[name] = self.return_timer.get(name, 0) + 30
                    if self.return_timer[name] >= RETURN_AFTER:
                        self.return_timer[name] = 0
                        self.log.append((self.minute, f"{name} quay lại"))
                        edge = self.rng.choice((0, COLUMNS - 1))   # cả cặp vào từ cùng một mép
                        for _ in range(2):
                            self.animals.append(Animal(name, edge))
                else:
                    self.return_timer[name] = 0
                continue
            if name not in have and inv["cond"](self) and self.essence >= inv["cost"]:
                self.discovered.add(name)
                self.essence -= inv["cost"]
                self.log.append((self.minute, f"mời {name}"))
                if name == "Giun":
                    for c in self.cols:
                        if c.layers[0]:
                            c.worms = True
                else:
                    x = COLUMNS // 2
                    n = 2
                    for _ in range(n):
                        self.animals.append(Animal(name, x + self.rng.randint(-3, 3)))
        # giun tự lan sang cột có cỏ
        for c in self.cols:
            if not c.worms and c.layers[0] and any(n.worms for n in self.near(c.i, 1)):
                c.worms = True
        if self.rains and self.essence >= PLAYER_RAIN_COST \
                and sum(c.moist for c in self.cols) / COLUMNS < PLAYER_RAIN_BELOW:
            self.essence -= PLAYER_RAIN_COST
            for c in self.cols:
                c.moist = min(100, c.moist + RAIN_AMOUNT)
            self.log.append((self.minute, "gọi mưa"))
        # gieo: hoa (10) khi có ≥ 10 cỏ, mâm xôi (25) khi có ≥ 20 cỏ
        if self.count_plant("Cỏ") >= 10 and self.count_plant("Hoa dại") < 8 and self.essence >= 10:
            self.try_plant("Hoa dại", 10)
        if self.count_plant("Cỏ") >= 20 and self.count_plant("Mâm xôi") < 6 and self.essence >= 25:
            self.try_plant("Mâm xôi", 25)

    def try_plant(self, name, cost):
        sp = PLANTS[name]
        options = [c for c in self.cols if c.layers[sp["layer"]] is None and suitability(sp, c) > 0.5
                   and (sp["layer"] == 1 or True)]
        if name == "Hoa dại":
            options = [c for c in self.cols if c.layers[0] is None and suitability(sp, c) > 0.5]
        if not options:
            return
        col = self.rng.choice(options)
        col.layers[sp["layer"]] = Plant(name)
        self.essence -= cost
        self.log.append((self.minute, f"gieo {name}"))


def survey(hours=96, seeds=20, rains=False):
    """Chạy nhiều seed, báo cáo các chỉ số ổn định."""
    print("Người chơi:", "ghé mỗi 30 phút, gọi mưa khi khô" if rains else "lười tuyệt đối (không gọi mưa)")
    print(f"{'seed':>4} {'cỏ@4h':>6} {'mời thỏ':>8} {'mời cáo':>8} {'thỏ min/max':>9} {'thỏ vắng':>9} {'thỏ về':>7} {'cáo vắng':>9} {'SK/ph@24h':>10} {'SK tổng':>9}")
    for seed in range(1, seeds + 1):
        w = World(seed, rains)
        rabbits, fox_gone, rate24, grass4 = [], 0, 0, 0
        fox_seen = False
        for m in range(hours * 60):
            w.step()
            if m == 4 * 60:
                grass4 = w.count_plant("Cỏ")
            if m == 24 * 60:
                rate24 = w.essence_rate()
            if m >= 6 * 60 and m % 10 == 0:
                rabbits.append(w.count_animal("Thỏ"))
                f = w.count_animal("Cáo")
                if f:
                    fox_seen = True
                elif fox_seen:
                    fox_gone += 1
                    fox_seen = False
        first = lambda tag: next((f"{t // 60}h{t % 60:02d}" for t, e in w.log if e == tag), "-")
        zero_h = sum(1 for r in rabbits if r == 0) / 6
        leaves = sum(1 for _, e in w.log if e == "Thỏ quay lại")
        print(f"{seed:>4} {grass4:>6} {first('mời Thỏ'):>8} {first('mời Cáo'):>8} {min(rabbits):>4}/{max(rabbits):<4} {zero_h:>8.1f}h {leaves:>7} {fox_gone:>9} {rate24:>10.1f} {w.essence_total:>9.0f}")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "survey":
        survey(rains="rain" in sys.argv)
        return
    hours = int(sys.argv[1]) if len(sys.argv) > 1 else 96
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    w = World(seed)
    print(f"{'giờ':>4} {'mùa':5} {'cỏ/khô':>6} {'hoa':>3} {'xôi':>3} {'giun':>4} {'thỏ':>4} {'cáo':>3} {'ong':>3} "
          f"{'ẩm':>4} {'màu':>4} {'SK/ph':>6} {'đa':>4} {'cb':>4} {'SK tổng':>8}")
    for h in range(hours + 1):
        if h:
            for _ in range(60):
                w.step()
        cnt = w.species_counts()
        d, b = w.multipliers()
        m = sum(c.moist for c in w.cols) / COLUMNS
        cnt["Cỏ"] = f"{cnt.get('Cỏ', 0)}" + (f"/{sum(1 for c in w.cols if c.layers[0] and c.layers[0].dormant)}k" if any(c.layers[0] and c.layers[0].dormant for c in w.cols) else "")
        f = sum(c.fert for c in w.cols) / COLUMNS
        if h % 2 == 0 or h < 8:
            print(f"{h:>4} {w.season:5} {cnt.get('Cỏ', 0):>6} {cnt.get('Hoa dại', 0):>3} {cnt.get('Mâm xôi', 0):>3} "
                  f"{cnt.get('Giun', 0):>4} {cnt.get('Thỏ', 0):>4} {cnt.get('Cáo', 0):>3} {cnt.get('Ong', 0):>3} "
                  f"{m:>4.0f} {f:>4.0f} {w.essence_rate():>6.2f} {d:>4.2f} {b:>4.2f} {w.essence_total:>8.0f}")
    print("\nSự kiện người chơi:")
    for t, e in w.log[:20]:
        print(f"  {t // 60:>3}h{t % 60:02d}  {e}")


if __name__ == "__main__":
    main()
