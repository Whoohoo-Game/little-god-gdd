"""
Mô hình nhiều vùng cho GDD 08 (hồi sinh đất hoang + biome Ao).
Mọi số cân bằng đọc từ balance.json (nguồn duy nhất, Unity dùng bản sao). ecosim.py giữ nguyên
làm mô hình đồng cỏ của GDD 07 (luật cũ). Chạy ở bước 1 phút như ecosim.py.

    python3 Docs/GDD/sim/worldsim.py [days] [seed]     # bảng theo ngày + nhật ký cho 1 seed
    python3 Docs/GDD/sim/worldsim.py survey [seeds]    # nhiều seed: nhịp hồi sinh, kết game
    python3 Docs/GDD/sim/worldsim.py survey idle       # người chơi không gọi mưa
    python3 Docs/GDD/sim/worldsim.py survey nopred     # không bao giờ mời thú săn (Cáo, Diệc)
    python3 Docs/GDD/sim/worldsim.py survey legacy     # luật 07: sức chứa ×0.7, đói thì bỏ đi (so sánh)
    python3 Docs/GDD/sim/worldsim.py survey hpd=8      # mùa dài 8 giờ mô phỏng (nhịp cũ: 1 mùa = 1 ngày, app mở 8h)
    python3 Docs/GDD/sim/worldsim.py survey notrees    # không có cây tán (so sánh, GDD 11 §2)
    python3 Docs/GDD/sim/worldsim.py survey nodiscount # tắt giảm giá hồi sinh theo Sức khoẻ (so sánh)
    python3 Docs/GDD/sim/worldsim.py survey pe=600     # người chơi ghé mỗi 600 phút mô phỏng (6 phút thật); bội số của 30
    python3 Docs/GDD/sim/worldsim.py meadow            # kiểm tra: 1 đồng cỏ 48 cột, 24h/ngày, so với GDD 07

Thời gian tính bằng **phút mô phỏng** khi app đang mở. Nhịp ×100 (GDD 11 §1): 1 phút thật = 100 phút
mô phỏng, nên "giờ thật" trong bảng = giờ mô phỏng / 100. Mùa đổi theo thời gian mô phỏng (mặc định 3 000 phút,
GDD 11 Q21); tắt app thì thế giới ngủ (không mô phỏng bù). Người chơi mô hình ghé mỗi 300 phút mô phỏng (3 phút thật).
Không phụ thuộc thư viện ngoài.
"""
import bisect
import json
import os
import random
import sys

BALANCE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "balance.json")


def load_balance(path=BALANCE_PATH):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Tham số: đọc từ balance.json, nguồn số duy nhất cho Python và Unity (Tech Doc 03 §1).
# Tên biến giữ như trước; muốn đổi số thì sửa balance.json, không sửa ở đây.
# ---------------------------------------------------------------------------
B = load_balance()
SEASONS = ["Xuân", "Hạ", "Thu", "Đông"]
_by_season = lambda values: dict(zip(SEASONS, values))  # noqa: E731

SIM_PER_REAL = B["time"]["simMinutesPerRealMinute"]  # nhịp ×100 (GDD 11 §1)
HOURS_PER_DAY = B["time"]["seasonMinutes"] // 60     # một "ngày" của mô hình = một mùa (GDD 11 Q21: 50 giờ mp)
MAX_HOURS = 400                                      # giờ mô phỏng tối đa của một lần chạy (= 4 giờ thật)

# Thế giới 144 cột, 14 vùng, thiết kế tay (GDD 05 §3, 08 §3). Loại: start (đã hồi sinh từ đầu),
# meadow (đất thường), pond (có mặt nước ở giữa vùng), garden (Khu Vườn Thiêng, luôn ở đầu phải).
_W = B["world"]
LAYOUT = [(z["name"], z["size"], z["kind"]) for z in _W["layout"]]
GROUP = {"start": "meadow", "meadow": "meadow", "pond": "pond", "garden": "garden"}
POND_WATER = _W["pondWaterColumns"]
START_ESSENCE = _W["startEssence"]
START_GRASS = _W["startGrass"]
WASTE_FERTILITY = _W["wastelandFertility"]
REVIVED = _W["revived"]
BANK_MOIST = REVIVED["bankMoisture"]
STARTERS = _W["starters"]

# Hồi sinh vùng (08 §4)
_R = B["revive"]
REVIVE_HEALTH = _R["healthy"]        # vùng bên cạnh phải "Khoẻ"
BALANCED_HEALTH = _R["balanced"]     # "Cân bằng": điều kiện mở Khu Vườn Thiêng (mọi vùng cùng lúc)
REVIVE_COSTS = _R["costs"]           # theo thứ tự hồi sinh, không theo vùng nào
GARDEN_COST = _R["garden"]           # mời đủ loài đại diện về Vườn (gộp thành một giá)
REVIVE_DISCOUNT = _R["maxDiscount"]  # giảm giá tối đa khi vùng kề Cân bằng

# Quyền năng
PLAYER_RAIN_COST = B["powers"]["rainCost"]
RAIN_RADIUS = B["powers"]["rainRadius"]      # một lần kéo mưa phủ 7 cột

# Môi trường (07 §3)
_E = B["environment"]
EVAPORATION = _by_season(_E["evaporation"])
RAIN_CHANCE_PER_HOUR = _by_season(_E["rainChancePerHour"])
GROWTH_SEASON = _by_season(_E["growthSeason"])
RAIN_AMOUNT = _E["rainAmount"]
SNOWMELT = _E["snowmelt"]
MOIST_DIFFUSION = _E["moistureDiffusion"]
DECOMP_BASE, DECOMP_WORM, DECOMP_YIELD = _E["decompBase"], _E["decompWorm"], _E["decompYield"]
SHADED_LIGHT = 100 - _E["shrubShade"]
# Tầng tán (GDD 11 §2.2)
CANOPY_LIGHT = 100 - _E["canopyShade"]
CANOPY_EVAPORATION = _E["canopyEvaporation"]
CANOPY_RADIUS, CANOPY_SPACING = _E["canopyRadius"], _E["canopySpacing"]
LEAF_RADIUS, LEAF_PER_AUTUMN = _E["leafLitterRadius"], _E["leafLitterPerAutumn"]
TREE_LAYER = 2

# Thực vật (07 §5)
_P = B["plantRules"]
WET_FLOOR = _P["wetFloor"]
HEALTH_RATE, HEALTH_PIVOT = _P["healthRate"], _P["healthPivot"]
DORMANT_WAKE_Q, DORMANT_RECOVER, DORMANT_WAKE_HEALTH = _P["dormantWakeQ"], _P["dormantRecover"], _P["dormantWakeHealth"]
GRASS_FLOOR, GRAZED_HEALTH_LOSS = _P["grassFloor"], _P["grazedHealthLoss"]
SEEDBANK_SPROUT = 1 / _P["seedbankSproutMinutes"]
POLLINATION_BONUS = _P["pollinationBonus"]
REPLANT_Q = _P["replantOnOldAgeQ"]

# Động vật (07 §6, 08 §7)
_A = B["animalRules"]
BREED_SEASON = _by_season(_A["breedSeason"])
START_HUNGER = _A["startHunger"]
FED_GAIN, STARVE_DRAIN = _A["fedGain"], _A["starveDrain"]
HUNGRY_BELOW, BREED_ABOVE, BREED_CHANCE = _A["hungryBelow"], _A["breedAbove"], _A["breedChance"]
LEAVE_HUNGER = _A["starveAt"]                # luật mới: chết đói; luật 07: bỏ đi
DORMANT_FOOD = _A["dormantFood"]             # cỏ ngủ khô vẫn ăn được, giá trị 50%
FORAGE_SIGHT = _A["forageSight"]
GRAZER_OVERSHOOT = _A["grazerCapacity"]      # 08 §7.3: không chừa biên an toàn
CAPACITY_SAFETY = _A["legacyGrazerCapacity"] # luật 07 (survey legacy, meadow)
RETURN_AFTER = _A["arrivalAfterMinutes"]
PERIODIC_MINUTES = _A["periodicCheckMinutes"]  # giun lan, sinh vật tự tìm đến (người chơi mô hình cũng ghé theo nhịp này)
CATCH_BASE, LAST_PAIR, PREY_COMFORT = _A["catchBase"], _A["lastPair"], _A["preyComfort"]
CATCH_DETRITUS = _A["catchDetritus"]
WINTER_PREDATOR_NEED = _A["winterPredatorNeed"]
FRUIT_GAIN, SHRUB_ESCAPE = _A["fruitGain"], _A["shelterEscape"]
POLLINATOR_MIN_FLOWERS, FLOWERS_PER_POLLINATOR = _A["pollinatorMinFlowers"], _A["flowersPerPollinator"]
POLLINATOR_FED, POLLINATOR_DRAIN = _A["pollinatorFedGain"], _A["pollinatorHungryDrain"]
SWARM_RANGE = _A["swarmRange"]               # ong chia đàn: đàn mới bay tới chỗ nhiều hoa trong tầm này
SWARM_SPACING = _A["swarmSpacing"]           # ... nhưng cách đàn khác ít nhất chừng này cột
HOMING_SIGHT = _A["homingSight"]             # diệc đói bay về phía cá trong tầm này
WORM_ESSENCE = B["worm"]["essence"]

# Sinh khí & Sức khoẻ (07 §7.1, 08 §5)
ESS = B["essence"]
HEALTH = B["health"]

# Điều hoà tự nhiên (08 §7.3)
BARE_BIOMASS = B["naturalBalance"]["bareBiomass"]   # cột cỏ/bèo dưới mức này, hoặc ngủ khô, là "trụi"
BARE_REGION = B["naturalBalance"]["bareRegion"]     # đoạn có > 50% cột trụi thì đang "bị ăn trụi"

# Người chơi mô hình (không phải luật game)
PLAYER_RAIN_BELOW = B["modelPlayer"]["rainBelowMoisture"]
REVIVE_RESERVE = B["modelPlayer"]["reviveReserve"]
PLAYER_EVERY = B["modelPlayer"]["visitMinutes"]

# Loài: Python dùng tên hiển thị làm khoá; balance.json dùng id (như C#)
NAME = {sp["id"]: sp["name"] for sp in B["plants"] + B["animals"]}
NAME["worm"] = B["worm"]["name"]
_ROLE = {"herbivore": "ăn cỏ", "predator": "săn mồi", "pollinator": "thụ phấn"}
_DIET = {"plant": "grass", "prey": "rabbit", "nectar": "nectar", "nuts": "nuts"}

PLANTS = {
    sp["name"]: dict(layer=sp["layer"], ground=sp["ground"], grow=sp["growMinutes"], life=sp["lifeMinutes"],
                     moist=tuple(sp["moisture"]) if sp["moisture"] else None, fert=sp["fertilityMin"],
                     light=sp["lightMin"], seeds=sp["seedsPerHour"], range=sp["seedRange"], water=sp["waterUse"],
                     fertuse=sp["fertilityUse"], detritus=sp["detritus"], essence=sp["essence"],
                     regrow=sp["regrow"], flower=sp["flower"], perennial=sp["perennial"],
                     fruit=tuple(NAME[e] for e in sp["fruitEaters"]), bank=sp["bank"])
    for sp in B["plants"]
}
TREES = [n for n, sp in PLANTS.items() if sp["layer"] == TREE_LAYER]


def _animal(sp):
    a = dict(role=_ROLE[sp["role"]], eats=_DIET[sp["diet"]], life=sp["lifeMinutes"], mature=sp["matureMinutes"],
             litter=sp["litter"], cooldown=sp["cooldownMinutes"], range=sp["range"], essence=sp["essence"],
             detritus=sp["detritus"], habitat=sp["habitat"])
    if sp["diet"] == "plant":
        a.update(food=NAME[sp["foodPlant"]], need=sp["needPerMinute"])
    elif sp["diet"] == "prey":
        a.update(prey=NAME[sp["prey"]], need=1 / sp["minutesPerCatch"], prey_per=sp["preyPerPredator"])
        a["prey_all"] = (a["prey"],)      # biomesim.py thêm mồi phụ (Sóc cho Cáo, GDD 12 §3.1)
        if sp["homing"]:
            a["homing"] = True
    else:
        a["need"] = 0
    a["fruit"] = [n for n, p in PLANTS.items() if sp["name"] in p["fruit"]]   # cây có quả loài này ăn được
    return a


ANIMALS = {sp["name"]: _animal(sp) for sp in B["animals"]}


def living_in(cols, names):
    return sum(1 for c in cols for p in c.layers if p and p.name in names and p.living)


def _global_condition(req):
    """Điều kiện mời trên toàn thế giới (07 §6.5, 08 §6.3)."""
    if "animals" in req:
        target = NAME[req["animals"]]
        return lambda w: w.count_animal(target) >= req["count"]
    names = [NAME[i] for i in req["livingPlants"]]
    return lambda w: sum(w.count_living(n) for n in names) >= req["count"]


def _local_condition(req):
    """Điều kiện tại chỗ để loài đã khám phá tự tìm đến một đoạn biome (08 §7.1)."""
    if "animals" in req:
        target = NAME[req["animals"]]
        return lambda w, cols, a, b: w.animals_in(target, a, b) >= req["count"]
    names = tuple(NAME[i] for i in req["livingPlants"])
    return lambda w, cols, a, b: living_in(cols, names) >= req["count"]


# Thứ tự trong balance.json là thứ tự xét lời mời và tự tìm đến
INVITE = {NAME[i["species"]]: dict(cost=i["cost"], cond=_global_condition(i["requires"])) for i in B["invites"]}
LOCAL = {NAME[i["species"]]: _local_condition(i["local"]) for i in B["invites"]}
COSTS = {sp["name"]: sp["sowCost"] for sp in B["plants"] if sp["sowCost"] is not None}


def _discover(rule):
    """Điều kiện khám phá cây tán 🌱 (GDD 11 Q24, 09). Cây cũ (Hoa dại, Mâm xôi, Sen) mô hình gieo luôn như trước."""
    if "zoneLivingPlants" in rule:
        names = [NAME[i] for i in rule["zoneLivingPlants"]]
        return lambda w: any(sum(w.count_living(n, z) for n in names) >= rule["count"] for z in w.zones if z.alive)
    if "pondLivingPlants" in rule:
        names = [NAME[i] for i in rule["pondLivingPlants"]]
        return lambda w: any(sum(w.count_living(n, z) for n in names) >= rule["count"]
                             for z in w.zones if z.alive and z.kind == "pond")
    names = [NAME[i] for i in rule["livingPlants"]]
    animal = NAME[rule["animals"]] if "animals" in rule else None
    return lambda w: (sum(w.count_living(n) for n in names) >= rule["count"]
                      and (animal is None or w.count_animal(animal) >= rule["animalCount"]))


DISCOVER_TREE = {NAME[k]: _discover(v) for k, v in B["moments"]["discover"].items() if NAME[k] in TREES}
COSTS["rain"] = PLAYER_RAIN_COST

def suitability(sp, col):
    if not col.alive or col.ground != sp["ground"] or (sp["bank"] and not col.bank):
        return 0.0
    if sp["moist"] is None:
        sm = 1.0
    else:
        lo_min, lo, hi, hi_max = sp["moist"]
        m = col.moist
        if m < lo_min:
            sm = 0.0
        elif m < lo:
            sm = (m - lo_min) / (lo - lo_min)
        elif m > hi and hi_max > hi:
            sm = max(WET_FLOOR, 1 - (1 - WET_FLOOR) * (m - hi) / (hi_max - hi))
        else:
            sm = 1.0
    sf = min(1.0, max(0.0, (col.fert - sp["fert"] * 0.5) / (sp["fert"] * 0.5)))
    sl = min(1.0, max(0.0, (col.light(sp["layer"]) - sp["light"] * 0.5) / (sp["light"] * 0.5)))
    return sm * sf * sl


class Plant:
    def __init__(self, name, grown=False):
        self.name = name
        self.spec = PLANTS[name]
        self.age = 0
        self.growth = 1.0 if grown else 0.0
        self.health = 100.0
        self.biomass = 100.0 if grown else 30.0
        self.dormant = False

    @property
    def mature(self):
        return self.growth >= 1.0

    @property
    def living(self):
        return self.mature and not self.dormant


class Column:
    def __init__(self, i, zone):
        self.i = i
        self.zone = zone
        self.ground = "land"
        self.alive = False
        self.moist = 0.0
        self.fert = float(WASTE_FERTILITY)
        self.detritus = 0.0
        self.layers = [None, None, None]
        self.worms = False
        self.seedbank = []
        self.bank = False       # cột đất kề mặt nước (Liễu chỉ mọc ở đây)
        self.canopy = 0         # số tán cây trưởng thành đang phủ cột (cập nhật mỗi bước, mùa Đông = 0)
        self.own_canopy = False # tán phủ cột này chỉ là của chính cây gốc ở đây

    def light(self, layer):
        light = 100
        if layer == 0 and self.layers[1] and self.layers[1].mature:
            light = SHADED_LIGHT
        if self.canopy and (layer < TREE_LAYER or not self.own_canopy):
            light = min(light, CANOPY_LIGHT)    # tán che tầng thảm, tầng bụi, và cây non dưới tán cây khác
        return light

    def revive(self, moist):
        self.alive = True
        self.moist = 100.0 if self.ground == "water" else moist
        self.fert = WASTE_FERTILITY + REVIVED["fertilityBonus"]
        self.detritus = REVIVED["detritus"]


class Zone:
    def __init__(self, i, name, size, kind, start):
        self.i, self.name, self.size, self.kind = i, name, size, kind
        self.start, self.end = start, start + size      # [start, end)
        self.alive = False
        self.water = None                              # (đầu, cuối) cột nước, gồm cả hai đầu
        if kind == "pond":
            w0 = start + (size - POND_WATER) // 2
            self.water = (w0, w0 + POND_WATER - 1)

    @property
    def center(self):
        return (self.start + self.end - 1) // 2


class Animal:
    def __init__(self, name, x, age=None, pond=None):
        self.name = name
        self.spec = ANIMALS[name]
        self.x = x
        self.age = age if age is not None else self.spec["mature"]
        self.hunger = START_HUNGER
        self.cooldown = 0
        self.pond = pond      # cá: vùng ao đang sống
        self.gone = False


class World:
    def __init__(self, seed, layout=LAYOUT, hours_per_day=HOURS_PER_DAY, rains=True, rain_all=False,
                 revive_costs=REVIVE_COSTS, garden_cost=GARDEN_COST, discount=REVIVE_DISCOUNT,
                 natural=True, predators=True, player_every=None, trees=True):
        self.rng = random.Random(seed)
        # người chơi ghé (mời, mưa, hồi sinh, gieo) mỗi bao nhiêu phút mô phỏng; mặc định cùng nhịp kiểm tra định kỳ
        self.player_every = player_every or PLAYER_EVERY
        self.rains, self.rain_all = rains, rain_all
        self.day_len = hours_per_day * 60
        self.revive_costs, self.garden_cost, self.discount = revive_costs, garden_cost, discount
        self.natural, self.predators = natural, predators
        self.starved, self.hunted = {}, {}     # số con chết đói / bị săn, theo loài
        self.graze_checks = self.bare_checks = 0
        self.zones, self.cols = [], []
        x = 0
        for zi, (name, size, kind) in enumerate(layout):
            z = Zone(zi, name, size, kind, x)
            self.zones.append(z)
            for i in range(x, x + size):
                c = Column(i, zi)
                if z.water and z.water[0] <= i <= z.water[1]:
                    c.ground = "water"
                self.cols.append(c)
            x += size
        self.n = x
        for c in self.cols:
            c.bank = c.ground == "land" and any(
                0 <= j < x and self.cols[j].ground == "water" for j in (c.i - 1, c.i + 1))
        self.trees = trees
        self.sown_trees = set()     # cây tán đã khám phá (người chơi mô hình gieo được)
        self.animals = []
        self.essence = START_ESSENCE
        self.essence_total = 0.0
        self.minute = 0
        self.log = []
        self.discovered = set()
        self.return_timer = {}
        self.revivals = []            # (phút, vùng, giá đã trả, tỉ lệ giảm, phút chờ vì thiếu Sinh khí)
        self.ready_since = {}
        self.rain_casts = 0
        self.garden_unlocked = None
        self.ending = None
        self.max_balanced = 0
        self._regions = None
        self._stats_minute = -1
        for z in self.zones:
            if z.kind == "start":
                self.revive_zone(z, starters=False)
        starts = [z for z in self.zones if z.kind == "start"]
        mid = (starts[0].start + starts[-1].end) // 2
        for i in range(mid - START_GRASS // 2, mid + START_GRASS // 2 + 1):
            self.cols[i].layers[0] = Plant("Cỏ", grown=True)
        self.home = mid

    # -- truy vấn -------------------------------------------------------------
    @property
    def day(self):
        return self.minute // self.day_len

    @property
    def season(self):
        return SEASONS[self.day % 4]

    @property
    def hours(self):
        return self.minute / 60

    def alive_cols(self):
        return self.cols[self.L:self.R + 1]

    def count_living(self, name, zone=None):
        cols = self.zone_cols(zone) if zone else self.alive_cols()
        return sum(1 for c in cols for p in c.layers if p and p.name == name and p.living)

    def count_plant(self, name, zone=None):
        cols = self.zone_cols(zone) if zone else self.alive_cols()
        return sum(1 for c in cols for p in c.layers if p and p.name == name)

    def count_animal(self, name, zone=None):
        if zone is None:
            return sum(1 for a in self.animals if a.name == name)
        return sum(1 for a in self.animals if a.name == name and zone.start <= a.x < zone.end)

    def zone_cols(self, z):
        return self.cols[z.start:z.end]

    def near(self, x, r):
        return self.cols[max(self.L, x - r):min(self.R, x + r) + 1]

    def bounds(self, a):
        if a.spec["habitat"] == "water":
            return self.zones[a.pond].water
        return self.L, self.R

    def reach(self, a, r):
        lo, hi = self.bounds(a)
        return self.cols[max(lo, a.x - r):min(hi, a.x + r) + 1]

    # -- hồi sinh -------------------------------------------------------------
    def revive_zone(self, z, starters=True, side=0):
        """side = -1 nếu sự sống tới từ bên trái, +1 nếu từ bên phải."""
        z.alive = True
        for c in self.zone_cols(z):
            c.revive(BANK_MOIST if z.kind == "pond" else REVIVED["moisture"])
        alive = [zz for zz in self.zones if zz.alive]
        self.L, self.R = alive[0].start, alive[-1].end - 1
        self._regions = None
        self._stats_minute = -1
        if not starters:
            return
        # Gió/Gieo hạt đưa sự sống sang: vài mầm ở phía giáp vùng cũ
        order = list(range(z.start, z.end)) if side < 0 else list(range(z.end - 1, z.start - 1, -1))
        land = [i for i in order if self.cols[i].ground == "land"]
        for i in land[:STARTERS["meadowGrass"] if z.kind != "pond" else STARTERS["pondGrass"]]:
            self.cols[i].layers[0] = Plant("Cỏ")
        if z.kind == "pond":
            water = [i for i in order if self.cols[i].ground == "water"]
            for i in water[:STARTERS["pondDuckweed"]]:
                self.cols[i].layers[0] = Plant("Bèo")
            bank = [i for i in land if abs(i - water[0]) == 1]
            for i in bank[:STARTERS["pondReeds"]]:
                self.cols[i].layers[1] = Plant("Lau sậy")

    def revive_discount(self, health):
        """0 khi vùng kề vừa Khoẻ, tăng tuyến tính tới self.discount khi vùng kề Cân bằng."""
        t = (health - REVIVE_HEALTH) / (BALANCED_HEALTH - REVIVE_HEALTH)
        return self.discount * min(1.0, max(0.0, t))

    def revive_cost(self, health=REVIVE_HEALTH):
        k = len(self.revivals)
        base = self.revive_costs[min(k, len(self.revive_costs) - 1)]
        return round(base * (1 - self.revive_discount(health)))

    # -- bước mô phỏng -------------------------------------------------------
    def step(self):
        self._stats_minute = -1     # thống kê đoạn biome chỉ dùng lại trong cùng một bước
        s = self.season
        self.weather(s)
        self.canopy_step(s)
        self.environment(s)
        self.plants(s)
        self.animals_step(s)
        if self.minute % PERIODIC_MINUTES == 0:
            self.visit()
        e = self.essence_rate()
        self.essence += e
        self.essence_total += e
        self.minute += 1

    def weather(self, s):
        if self.minute and self.minute % self.day_len == 0 and s == "Xuân":
            for c in self.alive_cols():
                if c.ground == "land":
                    c.moist = min(100, c.moist + SNOWMELT)
        if self.rng.random() < RAIN_CHANCE_PER_HOUR[s] / 60:
            for c in self.alive_cols():
                if c.ground == "land":
                    c.moist = min(100, c.moist + RAIN_AMOUNT)

    def canopy_step(self, s):
        """Tán cây trưởng thành phủ gốc ± 1 (trừ mùa Đông, rụng lá); mùa Thu lá rụng thành Mùn gốc ± 2."""
        cols = self.alive_cols()
        for c in cols:
            c.canopy, c.own_canopy = 0, True
        litter = LEAF_PER_AUTUMN / self.day_len
        for c in cols:
            t = c.layers[TREE_LAYER]
            if not (t and t.living) or s == "Đông":
                continue
            for n in self.near(c.i, CANOPY_RADIUS):
                n.canopy += 1
                if n is not c:
                    n.own_canopy = False
            if s == "Thu":
                for n in self.near(c.i, LEAF_RADIUS):
                    n.detritus += litter
        for c in cols:
            if c.canopy > 1:
                c.own_canopy = False

    def tree_room(self, x):
        """Gốc cây tán mới phải cách gốc khác hơn CANOPY_SPACING cột."""
        return not any(c.layers[TREE_LAYER] for c in self.near(x, CANOPY_SPACING) if c.i != x)

    def environment(self, s):
        cols = self.alive_cols()
        for c in cols:
            if c.ground == "land":
                c.moist = max(0, c.moist - EVAPORATION[s] * (CANOPY_EVAPORATION if c.canopy else 1.0))
            rate = DECOMP_WORM if c.worms else DECOMP_BASE
            d = c.detritus * rate
            c.detritus -= d
            c.fert = min(100, c.fert + d * DECOMP_YIELD)
        m = [c.moist for c in cols]
        last = len(cols) - 1
        for k, c in enumerate(cols):
            nb = [m[j] for j in (k - 1, k + 1) if 0 <= j <= last]
            c.moist += MOIST_DIFFUSION * (sum(nb) / len(nb) - m[k])
            if c.ground == "water":
                c.moist = 100.0     # mặt nước là nguồn ẩm cố định cho bờ

    def plants(self, s):
        pollinated = set()
        for a in self.animals:
            if a.name == "Ong":
                for c in self.near(a.x, a.spec["range"]):
                    pollinated.add(c.i)
        grow_s = GROWTH_SEASON[s]
        for c in self.alive_cols():
            for layer, p in enumerate(c.layers):
                if not p:
                    for name in c.seedbank:
                        sp = PLANTS[name]
                        if sp["layer"] == layer and (layer != TREE_LAYER or self.tree_room(c.i)) \
                                and self.rng.random() < SEEDBANK_SPROUT * suitability(sp, c):
                            c.layers[layer] = Plant(name)
                            break
                    continue
                sp = p.spec
                if p.mature and p.name not in c.seedbank:
                    c.seedbank.append(p.name)
                q = suitability(sp, c)
                p.age += 1
                if p.dormant:
                    if q >= DORMANT_WAKE_Q:
                        p.health += DORMANT_RECOVER
                        if p.health >= DORMANT_WAKE_HEALTH:
                            p.dormant = False
                    continue
                c.moist = max(0, c.moist - sp["water"] * grow_s)
                c.fert = max(0, c.fert - sp["fertuse"])
                if not p.mature:
                    p.growth += q * grow_s / sp["grow"]
                if sp["regrow"]:
                    p.biomass = min(100, p.biomass + sp["regrow"] * q * grow_s)
                    if p.biomass < GRASS_FLOOR:
                        p.health -= GRAZED_HEALTH_LOSS
                p.health = max(0, min(100, p.health + (q - HEALTH_PIVOT) * HEALTH_RATE))
                # cây trưởng thành sống lâu năm ngủ khô thay vì chết; cây non tầng tán cũng vậy (GDD 11 §2.2)
                if p.health <= 0 and sp["perennial"] and (p.mature or layer == TREE_LAYER) and p.age < sp["life"]:
                    p.dormant = True
                    continue
                if p.health <= 0 or p.age >= sp["life"]:
                    c.layers[layer] = None
                    c.detritus += sp["detritus"]
                    if p.age >= sp["life"] and q > REPLANT_Q and layer != TREE_LAYER:
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
        t = x + self.rng.randint(1, sp["range"]) * self.rng.choice((-1, 1))
        if not self.L <= t <= self.R:
            return
        col = self.cols[t]
        if sp["layer"] == TREE_LAYER and not self.tree_room(t):
            return
        if col.layers[sp["layer"]] is None and self.rng.random() < suitability(sp, col):
            col.layers[sp["layer"]] = Plant(name)

    def animals_step(self, s):
        pos = {}
        by_name = {}
        for a in self.animals:
            pos.setdefault(a.name, []).append(a.x)
            by_name.setdefault(a.name, []).append(a)
        for v in pos.values():
            v.sort()

        def count_in(name, x, r):
            v = pos.get(name, ())
            return bisect.bisect_right(v, x + r) - bisect.bisect_left(v, x - r)

        born = []
        for a in self.animals:
            if a.gone:
                continue
            sp = a.spec
            a.age += 1
            a.cooldown = max(0, a.cooldown - 1)
            if sp["eats"] == "grass":
                food, need = sp["food"], sp["need"]
                cols = [c for c in self.reach(a, sp["range"])
                        if c.layers[0] and c.layers[0].name == food and c.layers[0].mature and c.layers[0].biomass > GRASS_FLOOR]
                cols.sort(key=lambda c: -c.layers[0].biomass)
                for c in cols:
                    g = c.layers[0]
                    value = DORMANT_FOOD if g.dormant else 1.0
                    take = min(need / value, g.biomass - GRASS_FLOOR)
                    g.biomass -= take
                    need -= take * value
                    if need <= 0:
                        break
                a.hunger += (sp["need"] - need) / sp["need"] * FED_GAIN - STARVE_DRAIN
                if a.hunger < HUNGRY_BELOW and self.near_fruit(a, s):
                    a.hunger += FRUIT_GAIN
                a.x = self.forage_move(a, 1)
            elif sp["eats"] == "rabbit":
                a.hunger -= 100 * sp["need"] * (WINTER_PREDATOR_NEED if s == "Đông" else 1.0)
                prey_all = [r for n in sp["prey_all"] for r in by_name.get(n, ())]
                if a.hunger < HUNGRY_BELOW:
                    prey = [r for r in prey_all if not r.gone and abs(r.x - a.x) <= sp["range"]]
                    if len(prey) > LAST_PAIR:
                        r = self.rng.choice(prey)
                        shelter = any(c.layers[1] for c in self.near(r.x, 1)) or self.cols[r.x].canopy > 0
                        scarcity = min(1.0, len(prey) / PREY_COMFORT)
                        if self.rng.random() < CATCH_BASE * scarcity * (SHRUB_ESCAPE if shelter else 1.0):
                            r.gone = True
                            self.cols[r.x].detritus += CATCH_DETRITUS
                            self.hunted[r.name] = self.hunted.get(r.name, 0) + 1
                            a.hunger = 100
                    if a.hunger < HUNGRY_BELOW and self.near_fruit(a, s):
                        a.hunger += FRUIT_GAIN
                a.x = self.hunter_move(a, prey_all)
            elif sp["eats"] == "nuts":
                # Sóc (GDD 12 §3.1): no khi quanh nó có đủ Sồi trưởng thành để kiếm hạt
                oaks = sum(1 for c in self.near(a.x, sp["range"]) if c.layers[2] and c.layers[2].name == sp["nut_tree"] and c.layers[2].mature)
                a.hunger += POLLINATOR_FED if oaks >= sp["min_trees"] else -POLLINATOR_DRAIN
                a.x = max(self.L, min(self.R, a.x + self.rng.choice((-1, 0, 1))))
            elif sp["eats"] == "nectar":
                flowers = sum(1 for c in self.near(a.x, sp["range"]) for p in c.layers
                              if p and p.mature and p.spec["flower"])
                a.hunger += POLLINATOR_FED if flowers >= POLLINATOR_MIN_FLOWERS else -POLLINATOR_DRAIN
            a.hunger = max(0, min(100, a.hunger))
            if a.hunger <= LEAVE_HUNGER:
                a.gone = True
                if self.natural:
                    # chết đói: nằm xuống, mờ dần, để lại mùn (03 §3)
                    self.cols[a.x].detritus += sp["detritus"]
                    self.starved[a.name] = self.starved.get(a.name, 0) + 1
                else:
                    self.log.append((self.minute, f"{a.name} bỏ đi"))
                continue
            if a.age >= sp["life"]:
                a.gone = True
                self.cols[a.x].detritus += sp["detritus"]
                continue
            mates = count_in(a.name, a.x, sp["range"]) - 1
            if (a.hunger > BREED_ABOVE and a.age >= sp["mature"] and a.cooldown == 0 and mates > 0
                    and self.rng.random() < BREED_CHANCE * BREED_SEASON[s] * self.capacity_room(a, count_in)):
                a.cooldown = sp["cooldown"]
                for _ in range(sp["litter"]):
                    x = self.swarm_site(a, pos.get("Ong", [])) if a.name == "Ong" else a.x
                    born.append(Animal(a.name, x, age=0, pond=a.pond))
        self.animals = [a for a in self.animals if not a.gone] + born

    def near_fruit(self, a, s):
        """Quả chín (Hạ, Thu) trong ± 2 cột: Mâm xôi cho cáo, Táo dại cho thỏ và cáo (GDD 11 §2.3)."""
        fruit = a.spec["fruit"]
        return bool(fruit) and s in ("Hạ", "Thu") and any(
            p and p.name in fruit and p.living for c in self.near(a.x, 2) for p in c.layers)

    def forage_move(self, a, step):
        lo, hi = self.bounds(a)
        food = a.spec["food"]
        if a.hunger < HUNGRY_BELOW:
            best, best_food = a.x, -1.0
            for c in self.reach(a, FORAGE_SIGHT):
                g = c.layers[0]
                f = g.biomass * (DORMANT_FOOD if g.dormant else 1) if g and g.name == food and g.mature else 0
                if f > best_food or (f == best_food and abs(c.i - a.x) < abs(best - a.x)):
                    best, best_food = c.i, f
            if best != a.x:
                return a.x + (step if best > a.x else -step)
        return max(lo, min(hi, a.x + self.rng.choice((-step, 0, step))))

    def hunter_move(self, a, prey):
        lo, hi = self.bounds(a)
        if a.spec.get("homing") and a.hunger < HUNGRY_BELOW:
            # diệc đói bay về phía bầy cá gần nhất (cáo thì đi lang thang như GDD 07)
            near = [r.x for r in prey if not r.gone and abs(r.x - a.x) <= HOMING_SIGHT]
            if near:
                target = min(near, key=lambda x: abs(x - a.x))
                if abs(target - a.x) > 1:
                    return a.x + (2 if target > a.x else -2)
        return max(lo, min(hi, a.x + self.rng.choice((-2, -1, 0, 1, 2))))

    def swarm_site(self, a, colonies):
        """Ong chia đàn: đàn mới bay tới chỗ nhiều hoa, cách các đàn khác. Đây là cách ong lan sang ao."""
        best, score = a.x, POLLINATOR_MIN_FLOWERS - 1     # chỗ mới phải có đủ hoa nuôi đàn
        for x in range(max(self.L, a.x - SWARM_RANGE), min(self.R, a.x + SWARM_RANGE) + 1):
            if self.cols[x].ground == "water":
                continue
            k = bisect.bisect_left(colonies, x - SWARM_SPACING + 1)
            if k < len(colonies) and colonies[k] < x + SWARM_SPACING:
                continue
            f = sum(1 for c in self.near(x, a.spec["range"]) for p in c.layers if p and p.mature and p.spec["flower"])
            if f > score:
                best, score = x, f
        return best

    def capacity_room(self, a, count_in):
        sp = a.spec
        same = count_in(a.name, a.x, sp["range"])
        if sp["eats"] == "grass":
            season = GROWTH_SEASON[self.season]
            fsp = PLANTS[sp["food"]]
            safety = GRAZER_OVERSHOOT if self.natural else CAPACITY_SAFETY
            food = sum(fsp["regrow"] * suitability(fsp, c) * season * safety
                       for c in self.reach(a, sp["range"])
                       if c.layers[0] and c.layers[0].name == sp["food"] and c.layers[0].living)
            cap = food / sp["need"]
        elif sp["eats"] == "rabbit":
            cap = sum(count_in(n, a.x, sp["range"]) for n in sp["prey_all"]) / sp["prey_per"]
        elif sp["eats"] == "nuts":
            cap = sum(1 for c in self.near(a.x, sp["range"]) if c.layers[2] and c.layers[2].name == sp["nut_tree"]
                      and c.layers[2].mature) / sp["trees_per"]
        else:
            flowers = sum(1 for c in self.near(a.x, sp["range"]) for p in c.layers if p and p.spec["flower"])
            cap = flowers / FLOWERS_PER_POLLINATOR
        return max(0.0, min(1.0, 1 - same / max(cap, 0.01)))

    # -- vùng sinh thái (biome region), Sinh khí, Sức khoẻ ---------------------
    def regions(self):
        """Các đoạn vùng liền nhau cùng nhóm biome (GDD 03 §5)."""
        if self._regions is None:
            out = []
            for z in self.zones:
                if not z.alive:
                    continue
                g = GROUP[z.kind]
                if out and out[-1]["group"] == g and out[-1]["zones"][-1] == z.i - 1:
                    out[-1]["zones"].append(z.i)
                    out[-1]["end"] = z.end
                else:
                    out.append(dict(group=g, zones=[z.i], start=z.start, end=z.end))
            self.reg_of_zone = {zi: k for k, r in enumerate(out) for zi in r["zones"]}
            self._regions = out
        return self._regions

    def region_stats(self):
        if self._stats_minute == self.minute:
            return self._regions
        regs = self.regions()
        for r in regs:
            r.update(counts={}, base=0.0, bare=0)
        for c in self.alive_cols():
            r = regs[self.reg_of_zone[c.zone]]
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
                r["base"] += WORM_ESSENCE
        for a in self.animals:
            r = regs[self.reg_of_zone[self.cols[a.x].zone]]
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
            r["borrowed"] = set().union(*(n["roles"] for n in nbrs)) - r["roles"] if nbrs else set()
            r["mult"] = self.multipliers(r, nbrs)
        self._stats_minute = self.minute
        return regs

    def multipliers(self, r, nbrs):
        counts = r["counts"]
        local, borrowed = r["roles"], r["borrowed"]
        diversity = (1 + ESS["diversityPerSpecies"] * max(0, len(counts) - 1)
                     + ESS["diversityPerRole"] * max(0, len(local) - 1)
                     + ESS["diversityPerBorrowedRole"] * len(borrowed))   # vai trò mượn từ vùng bên cạnh tính một nửa
        balance = 1.0
        biomass = {n: c * (ESS["animalBiomassWeight"] if n in ANIMALS else 1) for n, c in counts.items()}
        total = sum(biomass.values()) or 1
        top = max(biomass.values()) / total if biomass else 0
        if top > ESS["dominanceLimit"]:
            balance -= (top - ESS["dominanceLimit"]) * ESS["dominancePenalty"]
        for pred in ("Cáo", "Diệc"):
            # thú săn đi lang thang qua nhiều đoạn: đếm cả săn lẫn mồi trên đoạn này + đoạn kề
            if counts.get(pred, 0):
                prey_name = ANIMALS[pred]["prey"]
                f = counts[pred] + sum(n["counts"].get(pred, 0) for n in nbrs)
                prey = counts.get(prey_name, 0) + sum(n["counts"].get(prey_name, 0) for n in nbrs)
                if not ESS["predatorRatioMin"] <= prey / f <= ESS["predatorRatioMax"]:
                    balance -= ESS["penalty"]
                    break
        if r["bare"] / (r["end"] - r["start"]) > ESS["bareLimit"]:
            balance -= ESS["penalty"]
        if len(local | borrowed) >= HEALTH["rolesNeeded"] and balance >= 1.0:
            balance += ESS["bonus"]
        return diversity, max(ESS["balanceMin"], min(ESS["balanceMax"], balance))

    def essence_rate(self):
        return sum(r["base"] * r["mult"][0] * r["mult"][1] for r in self.region_stats())

    def health(self, z):
        """Sức khoẻ vùng 0–100 = độ phủ × (0.4 + 0.3 × vai trò + 0.3 × cân bằng)."""
        if not z.alive:
            return 0.0
        regs = self.region_stats()
        r = regs[self.reg_of_zone[z.i]]
        cols = self.zone_cols(z)
        cover = sum(1 for c in cols if any(p and p.living for p in c.layers)) / len(cols)
        roles = min(1.0, (len(r["roles"]) + HEALTH["borrowedRoleWeight"] * len(r["borrowed"])) / HEALTH["rolesNeeded"])
        lo = ESS["balanceMin"]
        bal = min(1.0, max(0.0, (r["mult"][1] - lo) / (1 - lo)))
        return 100 * cover * (HEALTH["base"] + HEALTH["roles"] * roles + HEALTH["balance"] * bal)

    # -- người chơi mô hình: ghé mỗi 30 phút -----------------------------------
    def visit(self):
        for c in self.alive_cols():
            if not c.worms and c.layers[0] and c.ground == "land" and any(n.worms for n in self.near(c.i, 1)):
                c.worms = True
        self.measure_grazing()
        if self.trees:
            self.discover_trees()
        if self.minute % self.player_every != 0:
            self.arrivals()          # tự tìm đến là luật sinh thái, chạy cả khi người chơi vắng
            return
        self.invites()
        if self.rains:
            self.rain_dry()
        # ghé thưa thì mỗi lần làm bù nhiều việc: hồi sinh liền mấy vùng nếu đủ Sinh khí, gieo nhiều lượt
        for _ in range(max(1, min(10, self.player_every // PERIODIC_MINUTES))):
            if not self.revive_frontier():
                break
        for _ in range(max(1, min(10, self.player_every // PERIODIC_MINUTES))):
            self.sow()
        self.check_garden()

    def invites(self):
        have = {a.name for a in self.animals}
        if any(c.worms for c in self.cols):
            have.add("Giun")
        for name, inv in INVITE.items():
            if name in self.discovered or (not self.predators and ANIMALS.get(name, {}).get("eats") == "rabbit"):
                continue
            if name not in have and inv["cond"](self) and self.essence >= inv["cost"]:
                self.discovered.add(name)
                self.essence -= inv["cost"]
                self.log.append((self.minute, f"mời {name}"))
                if name == "Giun":
                    for c in self.alive_cols():
                        if c.layers[0] and c.ground == "land":
                            c.worms = True
                elif name == "Cá":
                    z = self.best_pond()
                    for _ in range(2):
                        self.animals.append(Animal(name, self.rng.randint(*z.water), pond=z.i))
                elif name == "Diệc":
                    x = self.best_col(name)
                    for _ in range(2):
                        self.animals.append(Animal(name, x))
                else:
                    for _ in range(2):
                        self.animals.append(Animal(name, self.home + self.rng.randint(-3, 3)))
        self.arrivals()

    def arrivals(self):
        """Loài đã khám phá tự tìm đến từng đoạn biome (riêng cá: từng ao). Khi đoạn đó còn < 2 con
        (giun: chưa có cột nào) và đạt điều kiện tại chỗ liên tục 2 giờ, một cặp đi vào từ mép đoạn.
        Thế giới chỉ có 1 đoạn thì đây chính là luật "tự quay lại" của GDD 07 §6.3."""
        regs = self.region_stats()
        for name in INVITE:
            if name not in self.discovered:
                continue
            if name == "Cá":
                sites = [(z.i, z.start, z.end) for z in self.zones if z.kind == "pond" and z.alive]
            else:
                sites = [(r["zones"][0], r["start"], r["end"]) for r in regs]
            for k_site, (key, a, b) in enumerate(sites):
                cols = self.cols[a:b]
                if name == "Giun":
                    absent = not any(c.worms for c in cols)
                elif ANIMALS[name]["eats"] == "rabbit":
                    # thú săn đi lang thang qua đoạn kề: chỉ coi là vắng khi cả đoạn kề cũng vắng
                    lo = sites[max(0, k_site - 1)][1]
                    hi = sites[min(len(sites) - 1, k_site + 1)][2]
                    absent = self.animals_in(name, lo, hi) < 2
                else:
                    absent = self.animals_in(name, a, b) < 2
                k = (name, key)
                if not (absent and LOCAL[name](self, cols, a, b)):
                    self.return_timer[k] = 0
                    continue
                self.return_timer[k] = self.return_timer.get(k, 0) + PERIODIC_MINUTES
                if self.return_timer[k] < RETURN_AFTER:
                    continue
                self.return_timer[k] = 0
                self.log.append((self.minute, f"{name} tới {self.zones[self.cols[a].zone].name}"))
                if name == "Giun":
                    grass = [c for c in cols if c.layers[0] and c.layers[0].name == "Cỏ"]
                    grass[len(grass) // 2].worms = True
                elif name == "Cá":
                    for _ in range(2):
                        self.animals.append(Animal(name, self.rng.randint(*self.zones[key].water), pond=key))
                else:
                    x = self.rng.choice((a, b - 1))     # cả cặp vào từ cùng một mép
                    for _ in range(2):
                        self.animals.append(Animal(name, x))

    def animals_in(self, name, a, b):
        return sum(1 for x in self.animals if x.name == name and a <= x.x < b)

    def best_pond(self):
        ponds = [z for z in self.zones if z.kind == "pond" and z.alive]
        return max(ponds, key=lambda z: self.count_living("Bèo", z))

    def best_col(self, name):
        """Cột có nhiều thức ăn nhất cho loài này."""
        sp = ANIMALS[name]
        if sp["eats"] == "rabbit":
            xs = [a.x for a in self.animals if a.name == sp["prey"]]
            return max(set(xs), key=xs.count) if xs else self.home
        if sp["eats"] == "nectar":
            score = lambda c: sum(1 for p in c.layers if p and p.living and p.spec["flower"])
        else:
            score = lambda c: c.layers[0].biomass if c.layers[0] and c.layers[0].name == sp["food"] and c.layers[0].living else 0
        return max(self.alive_cols(), key=score).i

    def measure_grazing(self):
        """Đếm số lần (đoạn × lần ghé) một đoạn đang bị ăn trụi: > 50% cột cỏ/bèo trụi hoặc ngủ khô."""
        for r in self.regions():
            food = [c.layers[0] for c in self.cols[r["start"]:r["end"]]
                    if c.layers[0] and c.layers[0].name in ("Cỏ", "Bèo") and c.layers[0].mature]
            if len(food) < 4:
                continue
            bare = sum(1 for g in food if g.dormant or g.biomass < BARE_BIOMASS)
            self.graze_checks += 1
            self.bare_checks += bare / len(food) > BARE_REGION

    def rain_dry(self):
        if self.rain_all:     # kiểu GDD 07: một lần mưa phủ cả vùng đồng cỏ
            land = [c for c in self.alive_cols() if c.ground == "land"]
            if self.essence >= COSTS["rain"] and sum(c.moist for c in land) / len(land) < PLAYER_RAIN_BELOW:
                self.essence -= COSTS["rain"]
                self.rain_casts += 1
                for c in land:
                    c.moist = min(100, c.moist + RAIN_AMOUNT)
                self.log.append((self.minute, "gọi mưa"))
            return
        for z in self.zones:
            if not z.alive:
                continue
            land = [c for c in self.zone_cols(z) if c.ground == "land"]
            if self.essence >= COSTS["rain"] and sum(c.moist for c in land) / len(land) < PLAYER_RAIN_BELOW:
                self.essence -= COSTS["rain"]
                self.rain_casts += 1
                for c in self.near(z.center, RAIN_RADIUS):
                    if c.ground == "land":
                        c.moist = min(100, c.moist + RAIN_AMOUNT)

    def frontier(self):
        alive = [z.i for z in self.zones if z.alive]
        out = []
        if alive[0] > 0:
            out.append((self.zones[alive[0] - 1], self.zones[alive[0]], +1))
        if alive[-1] < len(self.zones) - 1:
            out.append((self.zones[alive[-1] + 1], self.zones[alive[-1]], -1))
        return [(z, nb, side) for z, nb, side in out if z.kind != "garden"]

    def revive_frontier(self):
        ready = []
        for z, nb, side in self.frontier():
            h = self.health(nb)
            if h >= REVIVE_HEALTH:
                self.ready_since.setdefault(z.i, self.minute)
                ready.append((h, z, side))
        if not ready:
            return False
        h, z, side = max(ready, key=lambda t: t[0])
        cost = self.revive_cost(h)
        if self.essence >= cost + REVIVE_RESERVE:
            self.essence -= cost
            wait = self.minute - min(self.ready_since[zz.i] for _, zz, _ in ready)
            self.revivals.append((self.minute, z.name, cost, self.revive_discount(h), wait))
            self.log.append((self.minute, f"hồi sinh {z.name} ({cost})"))
            for _, zz, _ in ready:
                self.ready_since.pop(zz.i, None)
            self.revive_zone(z, side=side)
            return True
        return False

    def sow(self):
        for z in self.zones:
            if not z.alive or z.kind == "garden":
                continue
            grass = self.count_plant("Cỏ", z)
            size = z.size - (POND_WATER if z.water else 0)
            if grass >= -(-size * 2 // 10) and self.count_plant("Hoa dại", z) < round(size / 6):
                self.plant_in(z, "Hoa dại")
            if grass >= -(-size * 4 // 10) and self.count_plant("Mâm xôi", z) < round(size / 8):
                self.plant_in(z, "Mâm xôi")
            if z.water and self.count_living("Bèo", z) >= 3 and self.count_plant("Sen", z) < 2:
                self.plant_in(z, "Sen")
            if not self.trees:
                continue
            # cây tán (GDD 11 §2): mỗi đồng cỏ 1 Sồi + 1 Táo dại, mỗi ao 1 Liễu, khi đã khám phá
            for name in TREES:
                if name in self.sown_trees and self.count_plant(name, z) < 1 and (z.water is not None) == PLANTS[name]["bank"]:
                    self.plant_in(z, name)

    def discover_trees(self):
        for name, cond in DISCOVER_TREE.items():
            if name not in self.sown_trees and cond(self):
                self.sown_trees.add(name)
                self.log.append((self.minute, f"khám phá {name}"))

    def plant_in(self, z, name):
        sp = PLANTS[name]
        if self.essence < COSTS[name]:
            return
        options = [c for c in self.zone_cols(z) if c.layers[sp["layer"]] is None and suitability(sp, c) > 0.5
                   and (sp["layer"] != TREE_LAYER or self.tree_room(c.i))]
        if not options:
            return
        self.rng.choice(options).layers[sp["layer"]] = Plant(name)
        self.essence -= COSTS[name]

    def check_garden(self):
        others = [z for z in self.zones if z.kind != "garden"]
        balanced = sum(1 for z in others if self.health(z) >= BALANCED_HEALTH)
        self.max_balanced = max(self.max_balanced, balanced)
        if self.garden_unlocked is None and balanced == len(others):
            self.garden_unlocked = self.minute
            self.log.append((self.minute, "Khu Vườn Thiêng mở"))
        if self.garden_unlocked is not None and self.ending is None and self.essence >= self.garden_cost:
            self.essence -= self.garden_cost
            self.ending = self.minute
            garden = next(z for z in self.zones if z.kind == "garden")
            self.revive_zone(garden, side=-1)
            self.log.append((self.minute, "Cây Thế Giới nở hoa"))

    # -- hiển thị -------------------------------------------------------------
    def strip(self):
        """Mỗi vùng một ký tự: ░ đất hoang, 0–9 = Sức khoẻ/10, ★ = Cân bằng."""
        out = []
        for z in self.zones:
            if not z.alive:
                out.append("░")
            else:
                h = self.health(z)
                out.append("★" if h >= BALANCED_HEALTH else str(min(9, int(h // 10))))
        return "".join(out)


def fmt_h(m):
    return "-" if m is None else f"{m / 60:.0f}h"


def run_one(days, seed):
    w = World(seed)
    names = ["Cỏ", "Hoa dại", "Mâm xôi", "Thỏ", "Cáo", "Ong", "Bèo", "Sen", "Lau sậy", "Cá", "Diệc"] + TREES
    print(f"Thế giới {w.n} cột, {len(w.zones)} vùng, mỗi mùa {w.day_len // 60}h mô phỏng "
          f"({w.day_len / SIM_PER_REAL:.0f} phút thật). "
          f"Dải vùng: ░ hoang, 0–9 Sức khoẻ/10, ★ Cân bằng (≥{BALANCED_HEALTH}).")
    print(f"{'mùa#':>4} {'giờ':>4} {'mùa':5} {'vùng':14} " + " ".join(f"{n[:4]:>4}" for n in names)
          + f" {'SK/ph':>6} {'SK tổng':>9}")
    for d in range(days + 1):
        if d:
            for _ in range(w.day_len):
                w.step()
        print(f"{d:>4} {w.hours:>4.0f} {w.season:5} {w.strip():14} "
              + " ".join(f"{(w.count_plant(n) if n in PLANTS else w.count_animal(n)):>4}" for n in names)
              + f" {w.essence_rate():>6.1f} {w.essence_total:>9.0f}")
        if w.ending is not None:
            break
    print("\nHồi sinh (giờ app mở · vùng · giá đã trả · giảm · chờ vì thiếu Sinh khí):")
    for t, name, cost, disc, wait in w.revivals:
        print(f"  {t / 60:>6.1f}h  ngày {t // w.day_len:>2}  {name:16} {cost:>7}  -{disc:>4.0%}  chờ {wait / 60:>5.1f}h")
    print(f"\nVườn mở: {fmt_h(w.garden_unlocked)} · Kết: {fmt_h(w.ending)} · "
          f"mưa {w.rain_casts} lần · cùng lúc Cân bằng tối đa {w.max_balanced}/13 vùng")
    print("\nSự kiện (trừ bỏ đi/quay lại):")
    for t, e in w.log:
        if "bỏ đi" not in e and "quay lại" not in e:
            print(f"  {t / 60:>6.1f}h  {e}")


def survey(seeds=10, rains=True, hpd=HOURS_PER_DAY, discount=REVIVE_DISCOUNT,
           natural=True, predators=True, player_every=None, trees=True):
    days = MAX_HOURS // hpd
    print("Người chơi:", "gọi mưa vùng khô" if rains else "không gọi mưa", "·",
          "có thú săn" if predators else "KHÔNG mời thú săn", "·",
          "điều hoà tự nhiên" if natural else "luật 07 (sức chứa ×0.7, đói thì bỏ đi)",
          f"· mỗi mùa {hpd}h mô phỏng · giảm giá hồi sinh tối đa {discount:.0%}"
          + f" · người chơi ghé mỗi {player_every or PLAYER_EVERY} phút mô phỏng"
          + ("" if trees else " · KHÔNG có cây tán"))
    print("Giờ là giờ mô phỏng; 'kết thật' = giờ thật ở nhịp ×100. đói/săn tính theo mỗi 24 giờ mô phỏng.")
    print(f"{'seed':>4} {'vùng 5':>7} {'vùng 9':>7} {'Vườn mở':>8} {'Kết':>8} {'kết thật':>8} {'giảm':>5} "
          f"{'thỏ TB/max':>10} {'cá TB/max':>9} {'trụi':>5} {'đói/ng':>7} {'săn/ng':>7} {'thỏ vắng':>8} {'★ max':>5} "
          f"{'cây tán':>7} {'hoa':>4} {'ong':>4}")
    rows = []
    for seed in range(1, seeds + 1):
        w = World(seed, rains=rains, hours_per_day=hpd, discount=discount, natural=natural, predators=predators,
                  player_every=player_every, trees=trees)
        flowers, bees, tree_n = [], [], []
        rabbits, fish, rabbit_gone = [], [], 0
        for m in range(days * w.day_len):
            w.step()
            if m % 60 == 0 and m >= 6 * 60:
                r = w.count_animal("Thỏ")
                rabbits.append(r)
                rabbit_gone += r == 0
                if "Cá" in w.discovered:
                    fish.append(w.count_animal("Cá"))
                flowers.append(w.count_living("Hoa dại"))
                bees.append(w.count_animal("Ong"))
                tree_n.append(sum(w.count_plant(n) for n in TREES))
            if w.ending is not None:
                break
        rv = [t for t, *_ in w.revivals]
        pick = lambda k: fmt_h(rv[k]) if len(rv) > k else "-"
        disc = sum(r[3] for r in w.revivals) / max(1, len(w.revivals))
        end_real = w.ending / 60 / SIM_PER_REAL if w.ending else None
        rows.append((w.garden_unlocked, w.ending, end_real))
        days_run = max(1.0, w.minute / 1440)
        mean = lambda v: sum(v) / len(v) if v else 0
        print(f"{seed:>4} {pick(4):>7} {pick(8):>7} {fmt_h(w.garden_unlocked):>8} {fmt_h(w.ending):>8} "
              f"{(f'{end_real:.1f}h' if end_real else '-'):>8} {disc:>5.0%} "
              f"{mean(rabbits):>5.0f}/{max(rabbits, default=0):<4} {mean(fish):>4.0f}/{max(fish, default=0):<4} "
              f"{w.bare_checks / max(1, w.graze_checks):>5.0%} {sum(w.starved.values()) / days_run:>7.1f} "
              f"{sum(w.hunted.values()) / days_run:>7.1f} {rabbit_gone:>7}h {w.max_balanced:>5} "
              f"{mean(tree_n[len(tree_n) // 2:]):>7.1f} {mean(flowers):>4.0f} {mean(bees):>4.0f}")
    ends = sorted(r[2] for r in rows if r[2])
    if ends:
        print(f"\nKết game: {len(ends)}/{len(rows)} seed, trung vị {ends[len(ends) // 2]:.1f} giờ thật "
              f"(min {ends[0]:.1f}, max {ends[-1]:.1f}) ở nhịp ×{SIM_PER_REAL}")
    else:
        print(f"\nKết game: 0/{len(rows)} seed trong {MAX_HOURS} giờ mô phỏng")


def meadow_check(seeds=20, hours=96):
    """1 vùng đồng cỏ 48 cột, 24h/ngày, mưa kiểu GDD 07: phải ra số gần với ecosim.py survey rain."""
    print("Kiểm tra: đồng cỏ 48 cột như GDD 07 (so với `ecosim.py survey rain`)")
    print(f"{'seed':>4} {'mời thỏ':>8} {'mời cáo':>8} {'thỏ min/max':>11} {'thỏ vắng':>9} {'SK tổng':>9}")
    totals = []
    for seed in range(1, seeds + 1):
        w = World(seed, layout=[("Đồng cỏ", 48, "start")], hours_per_day=24, rain_all=True, natural=False,
                  player_every=PERIODIC_MINUTES, trees=False)
        rabbits = []
        for m in range(hours * 60):
            w.step()
            if m >= 6 * 60 and m % 10 == 0:
                rabbits.append(w.count_animal("Thỏ"))
        first = lambda tag: next((f"{t // 60}h{t % 60:02d}" for t, e in w.log if e == tag), "-")
        totals.append(w.essence_total)
        print(f"{seed:>4} {first('mời Thỏ'):>8} {first('mời Cáo'):>8} {min(rabbits):>5}/{max(rabbits):<5} "
              f"{sum(1 for r in rabbits if r == 0) / 6:>8.1f}h {w.essence_total:>9.0f}")
    print(f"\nSinh khí tổng trung bình: {sum(totals) / len(totals):.0f}")


def main():
    args = sys.argv[1:]
    if args and args[0] == "survey":
        seeds = next((int(a) for a in args[1:] if a.isdigit()), 10)
        hpd = next((int(a[4:]) for a in args[1:] if a.startswith("hpd=")), HOURS_PER_DAY)
        survey(seeds, rains="idle" not in args, hpd=hpd, trees="notrees" not in args,
               discount=0.0 if "nodiscount" in args else REVIVE_DISCOUNT,
               natural="legacy" not in args, predators="nopred" not in args,
               player_every=next((int(a[3:]) for a in args[1:] if a.startswith("pe=")), None))
    elif args and args[0] == "meadow":
        meadow_check()
    else:
        run_one(int(args[0]) if args else MAX_HOURS // HOURS_PER_DAY, int(args[1]) if len(args) > 1 else 1)


if __name__ == "__main__":
    main()
