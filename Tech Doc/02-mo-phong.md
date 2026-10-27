# 02 · Mô phỏng (`LittleGod.Simulation`)

> Nguồn luật: GDD [07](../GDD/07-he-sinh-thai-chi-tiet.md) (đồng cỏ, đã đổi luật 2026-10-23) và [08](../GDD/08-nhieu-vung-va-ao.md) (nhiều vùng, Ao, cân bằng tự nhiên).
> **Bản tham chiếu:** `Docs/GDD/sim/worldsim.py`. Khi chữ trong GDD và mã Python khác nhau, GDD thắng, và phải sửa Python trước rồi mới viết C#.

## 1. Mô hình dữ liệu
```
World
 ├─ Zones[14]        Zone: Index, Kind {Start, Meadow, Pond, Garden}, Start, End, Alive, Water (đầu, cuối)?
 ├─ Columns[144]     Column: Index, Zone, Ground {Land, Water}, Alive, Moisture, Fertility, Detritus,
 │                           Layers[2] (Plant?), Worms, Seedbank (danh sách có thứ tự)
 ├─ Animals          Animal: Id, Species, X, Age, Hunger, Cooldown, Pond?, Gone
 ├─ Discovered       danh sách có thứ tự các id loài đã khám phá (cả cây lẫn động vật)
 ├─ Essence, EssenceTotal, Minute, Season (đầu vào), RevivalCount
 ├─ AliveSpan        L..R: các cột đã hồi sinh luôn là một dải liền (08 §4.1)
 ├─ ArrivalTimers    (loài, đoạn biome) → phút điều kiện đạt liên tục
 ├─ Rng              PCG32, lưu trong save (01 §5)
 └─ Events           List<EcoEvent> (01 §3)
```

**Đoạn biome** (`Region`, 08 §5.1) **không lưu**, tính lại khi có vùng hồi sinh. Thống kê theo đoạn (đếm loài, vai trò, vai trò mượn, Sinh khí cơ bản, hệ số) tính **một lần mỗi bước** rồi dùng chung cho Sinh khí, Sức khoẻ và UI. Đây là cách `worldsim.py` cache `region_stats()`.

**Tên vùng** là dữ liệu của người chơi, không phải của mô phỏng: lưu ở `LittleGod.Game` (03 §5).

### 1.1 Mở rộng định nghĩa loài
| Trường mới | Kiểu | Ý nghĩa | Thay cho cách làm hiện tại |
|------------|------|---------|----------------------------|
| `PlantSpecies.Ground` | `Land` / `Water` | Bèo, Sen sống trên nước (08 §6.2) | — |
| `PlantSpecies.IgnoresMoisture` | bool | Cây nước: hệ số ẩm luôn = 1 | — |
| `AnimalSpecies.Habitat` | `Land` / `Water` | Cá chỉ đi trong cột nước của ao mình | — |
| `AnimalSpecies.FoodPlant` | id | Thỏ → Cỏ, Cá → Bèo | Mã đang **cứng** `EcoConfig.Grass` trong `Graze`, `ForageMove`, `CapacityRoom` |
| `AnimalSpecies.Prey` | id | Cáo → Thỏ, Diệc → Cá | `Hunt` đang săn **mọi** thú ăn cỏ, nên cáo sẽ ăn cả cá |
| `AnimalSpecies.PreyPerPredator` | float | Cáo 8, Diệc 5 | Hằng `Config.PreyPerPredator` chung |
| ~~`AnimalSpecies.EatsBerries`~~ | — | ↻ Thay bằng `PlantSpecies.FruitEaters` (GDD 11 §2.3): Mâm xôi → cáo, Táo dại → thỏ, cáo | — |
| `PlantSpecies.Bank` | bool | Chỉ mọc ở cột đất kề mặt nước (Liễu) | — |
| `AnimalSpecies.Homing` | bool | Diệc đói bay về phía con mồi gần nhất trong 30 cột | — |
| `AnimalSpecies.LocalRequirement` | điều kiện | Điều kiện để loài tự tìm đến **một đoạn biome** (08 §7.1) | `Requirement` hiện chỉ tính toàn thế giới |

Giun vẫn là thuộc tính của cột (07 §6.5), không phải `AnimalSpecies`.

## 2. Thứ tự một bước (1 phút)
Giữ đúng thứ tự của `worldsim.py` `World.step()`. Đổi thứ tự sẽ làm lệch kết quả so với bản tham chiếu.

| # | Giai đoạn | Nội dung | GDD |
|---|-----------|----------|-----|
| 0 | `Season` | ✅ Mùa = `(Minute / seasonMinutes) mod 4` | GDD 11 §1.1 |
| 1 | `Weather` | Tuyết tan ở phút đầu của mỗi mùa Xuân (`Minute > 0 && Minute % seasonMinutes == 0`); mưa tự nhiên phủ **mọi cột đất đã hồi sinh** | 07 §3.1 |
| 1b | `Canopy` | ✅ Tán cây trưởng thành phủ gốc ± 1 (trừ Đông): `Column.Canopy` (số tán), `OwnCanopy`; mùa Thu rải Mùn lá gốc ± 2 | GDD 11 §2.2 |
| 2 | `Environment` | Bốc hơi (bỏ qua cột nước; dưới tán ×0.5), phân huỷ Mùn, khuếch tán ẩm **chỉ trong dải đã hồi sinh**; cột nước đặt lại 100 | 07 §3, 08 §6.1 |
| 3 | `Plants` | Thụ phấn theo vị trí ong; hạt ngủ trong đất; lớn, hút nước, ngủ khô, chết, gieo hạt. Hạt rơi ra ngoài dải đã hồi sinh thì mất. ✅ Tầng 2 (tán): giữa hai gốc phải trống ít nhất `canopySpacing` = 1 ô; cây tán chết già không tự mọc lại tại chỗ; cây non tầng tán cạn sức khoẻ thì ngủ khô như cây trưởng thành | 07 §5, GDD 11 §2 |
| 4 | `Animals` | Ăn (theo `FoodPlant` / `Prey`; ✅ quả theo `fruitEaters` của loài cây, Hạ–Thu, ± 2 cột; trú ẩn cạnh bụi **hoặc dưới tán**), di chuyển, **chết đói** khi độ no ≤ 10, chết già, sinh sản với sức chứa **×1.0** cho thú ăn cỏ, ong chia đàn | 07 §6, 08 §7.2–7.3 |
| 5 | `Periodic` (mỗi 30 phút) | Giun lan sang cột đất có cỏ; **sinh vật tự tìm đến đoạn biome** (cá: theo ao; thú săn: xét cả đoạn kề) | 08 §7.1 |
| 6 | `Essence` | Thống kê theo đoạn → Sinh khí/phút = Σ đoạn (cơ bản × Đa dạng × Cân bằng) | 08 §5.2 |
| 7 | `Minute++` | | |

**Không còn trong mô phỏng** (chuyển sang `LittleGod.Game` hoặc lệnh người chơi): mời loài, gọi mưa, gieo, hồi sinh, giảm giá hồi sinh, cấp thần, Sinh khí nghỉ ngơi, khoảnh khắc. Mô phỏng chỉ cung cấp API (§4).

## 3. Khoảng cách với `EcoWorld` hiện tại
| Hạng mục | Hiện tại | Cần cho slice | Mức |
|----------|----------|---------------|-----|
| Kích thước | 48 cột, 1 vùng | 144 cột, 14 vùng, đất hoang, `AliveSpan` | Lớn |
| Nền cột | Chỉ đất | Đất / nước; cây và thú theo nền | Lớn |
| Loài | 3 cây + 3 thú + giun | +Bèo, Sen, Lau sậy, Cá, Diệc | Vừa |
| Sức chứa thú ăn cỏ | ×0.7 (`CapacitySafety`) | ×1.0 | Nhỏ |
| Đói | Bỏ đi (`EcoEventType.Left`) | Chết đói, để lại Mùn (`Starved`) | Nhỏ |
| Quay lại | Toàn thế giới, vào ở mép thế giới | Theo đoạn biome, vào ở mép đoạn; thú săn xét đoạn kề; cá theo ao | Vừa |
| Ong | Đứng yên | Chia đàn tới chỗ nhiều hoa | Nhỏ |
| Sinh khí | Một hệ số cho cả thế giới | Theo đoạn biome, có vai trò mượn | Vừa |
| Sức khoẻ vùng | Không có | Công thức 08 §5.3 | Vừa |
| Hồi sinh | Không có | `ReviveCost` (giảm giá theo Sức khoẻ vùng kề), `TryRevive`, mầm khởi đầu (08 §4) | Vừa |
| Mùa | `Minute / 1440` | Đầu vào từ lịch (01 §4) | Nhỏ |
| Ngẫu nhiên | `System.Random` | PCG32 lưu được | Nhỏ |
| Khám phá cây | Gieo được mọi loài | Chỉ gieo loài đã khám phá; `Discover(plant)` gọi từ khoảnh khắc 🌱 (GDD 09 §3.2) | Nhỏ |
| Mưa người chơi | Bán kính cố định | Theo bề rộng kéo: `30 × ⌈n/7⌉`, tối đa 21 cột (GDD 10 §3.3) | Nhỏ |
| Hiệu năng | `Animals.Contains`, `List` mới mỗi lần ăn, `IEnumerable` có `yield` | Không cấp phát trong vòng lặp nóng (§6) | Vừa |

✅ **Đã làm ở M1** (2026-10-24): `World` viết mới trong `Scripts/Simulation/World.cs`, đọc số từ `Balance` (`Balance.cs`, nạp `balance.json` bằng Newtonsoft). Dùng lại `Plant`, `Column`, `Animal`, `PlantSpecies`, `AnimalSpecies` (thêm trường ở §1.1). `EcoWorld` + `EcoConfig` **giữ nguyên tới M2** vì prototype còn chạy trên chúng, rồi xoá cùng `Scripts/Prototype/`.

## 4. API công khai
```csharp
public sealed class World
{
    // trạng thái chỉ đọc
    IReadOnlyList<Zone> Zones; IReadOnlyList<Column> Columns; IReadOnlyList<Animal> Animals;
    float Essence, EssenceTotal; int Minute; Season Season; (int L, int R) AliveSpan;
    List<EcoEvent> Events;

    void Step();
    void SetSeason(Season s, bool isFirstMinuteOfSpringDay);

    // truy vấn cho UI / khoảnh khắc
    float EssenceRate();                       // Sinh khí/phút hiện tại
    double Health(int zone);                   // 0–100, 08 §5.3
    ZoneState State(int zone);                 // Wasteland, Recovering, Healthy, Balanced
    RegionStats RegionOf(int zone);            // đếm loài, vai trò, hệ số; cache theo bước
    float Suitability(string plant, int x);    // q, cho công cụ Gieo (GDD 10 §3.3)
    bool IsInvitable(string animal);           // chỗ đứng của con vật 💌 tính ở Moments (M5)
    int  ReviveCost(int zone, out float discount);
    bool CanRevive(int zone);                  // kề dải đã hồi sinh, vùng kề ≥ 60

    // lệnh (gọi qua GameSession)
    bool TryPlant(string plant, int x, bool free = false);
    bool TryRain(int fromX, int toX);          // giá 30 × ⌈n/7⌉, n ≤ 21
    bool TryInvite(string animal);
    bool TryRevive(int zone, int side);        // trả giá, mở cột, gieo mầm khởi đầu
    void Discover(string species);             // khoảnh khắc 🌱, hồi sinh ao đầu tiên
    void GrantEssence(float amount);           // quà khoảnh khắc, Sinh khí nghỉ ngơi
}
```
- `TryRevive` cho **Khu Vườn Thiêng** dùng điều kiện riêng (mọi vùng khác Cân bằng cùng lúc, 08 §8) và giá 300k không giảm. Phần "mời loài đại diện" không có trong slice.
- Mọi lệnh trả `bool` và không ném ngoại lệ khi không đủ điều kiện; UI hỏi `Can…` trước để hiện trạng thái nút.

## 5. Sự kiện
| Loại | Khi nào | Ai dùng |
|------|---------|---------|
| `Planted` | Gieo (cả miễn phí) | View: mầm nhú, lấp lánh |
| `Rain` | Mưa tự nhiên / người chơi (kèm khoảng cột) | View: mây, mưa |
| `Invited` | Mời thành công | View, Sổ tay |
| `Born` | Sinh nở. Kèm **số con cùng loài trong đoạn trước lần sinh** và cờ "lần sinh đầu trong đoạn" | Khoảnh khắc 🐣 (lọc ở GDD 09 §3.2) |
| `SwarmFounded` | Ong chia đàn tới chỗ mới | Khoảnh khắc 🐣 |
| `Arrived` | Một cặp tự tìm đến đoạn biome (kèm đoạn, mép) | Khoảnh khắc ✨, View: đi vào từ mép |
| `Hunted` | Bị săn | View: đuổi chạy khỏi màn hình (✅ 03 §3) |
| `Starved` | Chết đói | View: nằm xuống, mờ dần, để lại ụ mùn |
| `Died` | Chết già | View: như trên |
| `ZoneRevived` | Hồi sinh xong | View: hiệu ứng lan; khoảnh khắc 🏷️; Sổ tay |
| `Discovered` | Loài mới vào danh sách đã khám phá | UI: nút gieo, Sổ tay |

Bỏ `Left` và `Returned` (thay bằng `Starved` và `Arrived`). Bỏ `SeasonChanged` khỏi mô phỏng vì mùa đến từ `GameSession`.

## 6. Hiệu năng
Ngân sách: **≤ 0.5 ms cho một `Step()`** trên máy Apple M1 / laptop Windows tầm trung, với 144 cột và ~250 động vật (gấp ~1.5 lần mức cao nhất đo được trong `worldsim.py`). Ở tốc độ ×1, mỗi phút chỉ có một bước, nên chi phí trung bình gần như bằng 0. Ngân sách này để chế độ dev ×600 (tối đa 20 bước/khung) vẫn mượt.

| Kỹ thuật | Thay cho |
|----------|----------|
| Cờ `Gone` trên `Animal`, lọc một lần cuối bước (như `worldsim.py`) | `Animals.Contains` / `Remove` trong vòng lặp (O(n²)) |
| Mảng đếm theo cột cho từng loài, dựng lại đầu mỗi bước (counting sort trên 144 cột). Đếm trong khoảng `[x−r, x+r]` bằng tổng tiền tố | Duyệt toàn bộ `Animals` trong `HasMate`, `CapacityRoom` |
| Duyệt cột bằng vòng `for` trên chỉ số | `IEnumerable<Column> Near()` có `yield` (cấp phát mỗi lần gọi) |
| Bộ đệm `List` dùng lại cho chỗ ăn | `new List<Column>` trong `Graze` mỗi phút mỗi con |
| Thống kê đoạn biome tính một lần mỗi bước | Tính lại trong mỗi lời gọi `Health` / `EssenceRate` |

Đo bằng một EditMode test hiệu năng (`Unity.PerformanceTesting` đã có trong project) chạy 30 ngày mô phỏng ở thế giới đã hồi sinh hết.

## 7. Đồng bộ với `worldsim.py`
- Mỗi luật trong C# có chú thích trỏ tới mục GDD và hàm Python tương ứng (ví dụ `// GDD 08 §7.1 · worldsim.arrivals`).
- C# và Python **không cần khớp từng bước** (bộ sinh số khác nhau), mà phải khớp **thống kê** trên nhiều seed (05 §3). Đây cũng là cách test hiện tại so với `ecosim.py`.
- Khi đổi số: đổi `balance.json` (03 §1) → chạy `worldsim.py survey` → cập nhật GDD → chạy test C#.
