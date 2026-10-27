# 03 · Dữ liệu, thời gian & lưu game

## 1. Bảng số cân bằng: một nguồn cho C# và Python
**Vấn đề:** hiện cùng một bảng số được viết tay **ba lần**: `ecosim.py`, `worldsim.py` và `EcoConfig.CreateDefault()`. GDD đòi "đổi số thì sửa cả mô hình và file này" (07 §10). Làm tay như vậy rất dễ lệch.

**✅ Quyết định (T1):** một file **`Docs/GDD/sim/balance.json`** là nguồn duy nhất.
- `worldsim.py` đọc file này thay cho các dict `PLANTS`, `ANIMALS`, `LAYOUT`, `REVIVE_COSTS`… (`ecosim.py` giữ nguyên làm lịch sử của 07).
- Unity dùng một bản sao ở `Assets/LittleGod/Data/balance.json` (TextAsset). Một menu Editor *Little God → Sync balance* chép file và báo lệch.
- Một EditMode test so hai file, **fail nếu khác nhau**, nên không thể quên đồng bộ.

```jsonc
{
  "version": 1,
  "world":   { "hoursPerCalendarDay": 8, "startEssence": 40, "rainCost": 30, "rainRadius": 3, "rainMaxColumns": 21 },
  "layout":  [ { "id": "west_hill", "size": 10, "kind": "meadow", "nameKey": "zone.west_hill" }, ... ],   // 14 vùng, 08 §3
  "revive":  { "costs": [3000, 15000, ...], "garden": 300000, "healthy": 60, "balanced": 85, "maxDiscount": 0.3 },
  "environment": { "evaporation": [0.05, 0.10, 0.06, 0.02], "rainChancePerHour": [...], ... },          // 07 §3
  "plants":  [ { "id": "grass", "layer": 0, "ground": "land", "growMinutes": 20, ... }, ... ],          // 07 §5.5, 08 §6.2
  "animals": [ { "id": "rabbit", "role": "herbivore", "foodPlant": "grass", "need": 1.5, ... }, ... ],  // 07 §6.5, 08 §6.3
  "essence": { "diversityPerSpecies": 0.15, "diversityPerRole": 0.25, "borrowedRole": 0.125, ... },    // 08 §5.2
  "moments": { "lifetimeMinutes": 30, "giftMinutes": 3, "bigGiftMinutes": 20, ... },                   // GDD 09
  "levels":  [ 0, 5000, 50000, 250000 ]                                                              // 07 §7.4
}
```
- Mọi số trong GDD 07–09 đều có một khoá trong file này. Không số cân bằng nào nằm cứng trong code; chỉ hằng kỹ thuật (kích thước bộ đệm, fps) là được viết trong code.
- ✅ **M1:** `World` đọc mọi số từ lớp `Balance` (`Scripts/Simulation/Balance.cs`), nạp `balance.json` bằng Newtonsoft (assembly Simulation tham chiếu `Newtonsoft.Json.dll`, vẫn `noEngineReferences`). Test cũng đọc từ bản sao trong `Assets`. `EcoConfig.CreateDefault()` còn tới M2, chỉ phục vụ `EcoWorld` cũ của prototype.
- ✅ **Đã có từ M0:** `Docs/GDD/sim/balance.json` (sinh từ đúng các giá trị Python lúc đó; `worldsim.py` đọc từ file này và cho output giống hệt bản cũ ở 8 chế độ chạy), bản sao `Assets/LittleGod/Data/balance.json`, menu *Little God → Sync balance.json*, test `BalanceSyncTests`.

## 2. Dữ liệu hình ảnh, âm thanh, chữ
| Dữ liệu | Định dạng | Khoá nối với mô phỏng |
|---------|-----------|------------------------|
| Sprite, hoạt ảnh theo mùa của loài | `SpeciesVisual` (ScriptableObject): sprite theo mùa, trạng thái (non, đói, ngủ khô), lớp vẽ | `speciesId` |
| Biểu tượng khoảnh khắc | `MomentVisual` (ScriptableObject) | `MomentType` |
| Âm thanh | `AmbientSet` (ScriptableObject) theo biome × mùa × ngày/đêm; SFX theo hành động | — |
| Chữ (tên loài, gợi ý sổ tay, dòng gợi ý 🍂, tên vùng gợi ý) | `Localization/vi.json`, `en.json`: bảng khoá → chuỗi | `nameKey`, `hintKey` |

- ✅ GDD 03 §8 nói "dữ liệu loài đặt trong ScriptableObject". Đề xuất tách: **số** ở `balance.json` (để Python đọc được), **hình/tiếng** ở ScriptableObject. Như vậy vẫn đúng tinh thần "cân bằng game mà không phải sửa code".
- Sprite pixel 16 px, Pixels Per Unit = **16**, 1 unit = 1 cột = 32 pt (ảnh 2×, ✅ 01). Thay cho sprite sinh bằng code trong `PixelSprites.cs`; lớp đó được giữ cho tới khi có art.
- Tiếng Việt cần phông có dấu chồng (GDD 10 §11). ✅ M4: uGUI `Text` với phông TTF động (tạm là `LegacyRuntime`), một chỗ đặt phông trong `UiPrefabBuilder.FontPath`; test `FontCoverageTests` kiểm mọi ký tự trong `vi.json` / `en.json` đều có glyph. Phông pixel có dấu sẽ thay vào đó khi chọn xong (TTF, import Font Size đúng lưới, Rendering Mode *Hinted Raster*).
- ✅ M4: `Resources/Localization/vi.json`, `en.json` (khoá phẳng `species.*`, `zone.*`, `state.*`, `tray.*`, `tool.*`, `info.*`…). Ngôn ngữ theo `Application.systemLanguage`, ghi đè bằng PlayerPrefs `littlegod.lang`; thiếu khoá thì rơi về tiếng Việt rồi về chính khoá. Số định dạng theo `vi-VN` / `en-US`.

## 3. Lịch, mùa, ngày đêm
↻ **2026-10-24 (GDD 11 §1):** nhịp ×100 và mùa theo thời gian mô phỏng.
```
simMinutesPerRealMinute = 100        GameSession.Advance: accumulator += giây thật × tốc độ dev × 100
season       = (World.Minute / seasonMinutes) mod 4      seasonMinutes = 3 000 (= 3 × dayNightMinutes; World tự tính mỗi bước)
calendarDay  = (today − startDate).Days                  chỉ còn dùng cho Sinh khí nghỉ ngơi
```
- `GameSession` theo dõi mùa trước / sau mỗi bước để phát `SeasonChanged`, giữ `PreviousSeason` và `seasonBlend` (chuyển dần trong **60 phút mô phỏng** ≈ 36 giây thật).
- `GameSession` vẫn đọc `DateTime.Now` mỗi bước; khi `today` khác `lastDate` thì chỉ cấp **Sinh khí nghỉ ngơi** (§4) và yêu cầu lưu.
- ↻ **Ngày đêm theo thời gian chơi (2026-10-24, GDD 11 §1.5):** `World.DayHour(minute) = 6 + 24 × ((minute mod dayNightMinutes) / dayNightMinutes)`, `time.dayNightMinutes = 1 000` (10 phút thật: ngày 6h–18h, đêm 18h–6h). Không còn đọc `DateTime.Now` cho trời. `GameSession.MinuteFraction` (phần lẻ của bộ tích luỹ, 0..1) cho trời đổi mượt giữa hai bước. Chỉ ảnh hưởng hiển thị và ambient, không lưu gì thêm (suy ra từ `World.Minute`). Cú, đom đóm ngoài slice.
- **Đổi giờ máy về quá khứ:** nếu `today < lastDate` thì giữ `lastDate`, không cấp Sinh khí nghỉ ngơi. **Nhảy tới tương lai** nhiều ngày: Sinh khí nghỉ ngơi chỉ cấp **một lần**; mùa không đổi vì tắt app thì thế giới ngủ.
- Chế độ dev: lịch giả lập "1 ngày lịch = N giờ mở app" (01 §4).

## 4. Sinh khí nghỉ ngơi (✅ Q18, GDD 08 §2)
```
openMinutesByDate: { "2026-10-22": 312, "2026-10-23": 45 }    // chỉ giữ 2 ngày gần nhất
khi sang ngày lịch mới (lúc mở app, hoặc lúc 0:00 nếu app đang chạy):
  yesterday = openMinutesByDate[today − 1]   (không có → 0)
  rest = World.EssenceRate() × 100 × min(10, max(0, 480 − yesterday) × 10 / 480)     ↻ GDD 11 §1.2: trần 10 phút thật
  World.GrantEssence(rest); phát sự kiện RestEssence(rest) cho hiệu ứng thức dậy (GDD 10 §8.1)
```
- `openMinutes` cộng theo **phút mô phỏng đã chạy**, nên khi app bị ẩn tạm vẫn được tính (thế giới vẫn chạy, ✅ Q14). Còn trong chế độ dev ×N thì cộng theo **phút thật**, để test không cấp Sinh khí nghỉ ngơi sai.
- ⚠️ `EssenceRate()` lúc vừa mở app có thể thấp hơn bình thường (đáy mùa Xuân). Chấp nhận được; nếu chơi thử thấy thiệt thì đổi sang trung bình Sinh khí/phút của ngày hôm trước (cần lưu thêm một số).

## 5. Lưu game
**✅ Thư viện (T5):** `com.unity.nuget.newtonsoft-json` (gói chính thức của Unity). `JsonUtility` không đọc/ghi được `Dictionary` và kiểu đa hình.

| Thuộc tính | Giá trị |
|------------|---------|
| Vị trí | `Application.persistentDataPath/save/world.json` · `settings.json` riêng |
| Khi lưu | Mỗi **5 phút**, khi hồi sinh vùng, khi đổi ngày lịch, khi ẩn tạm, khi thoát (✅ 03 §8: không mô phỏng bù nên save chính là trạng thái lúc mở lại) |
| An toàn | Ghi `world.json.tmp` → `fsync` → đổi tên đè. Giữ `world.bak` của lần lưu trước. Đọc lỗi thì thử `.bak`; vẫn lỗi thì **không ghi đè**, đổi tên file hỏng thành `world.broken-<ngày>.json` và báo trong khay |
| Kích thước | ~144 cột × 3 tầng + ~250 động vật → **< 100 KB**, không cần nén |
| Phiên bản | ✅ `"saveVersion": 2` (2026-10-24): cột có 3 tầng, mùa tính lại từ `minute`. Save v1 đọc được: tầng tán để trống, `season` cũ bỏ qua. Test bằng file mẫu v1. ↻ v3: biome theo cột ([06 §3](06-moi-truong-song.md#3-phiên-chơi--lưu-littlegodgame)); v4: bầy, hang, đích của động vật ([07 §3](07-bay-dan.md#3-lưu-game-littlegodgame)) |

**Nội dung `world.json`:**
```jsonc
{
  "saveVersion": 1, "balanceVersion": 1, "createdAt": "2026-10-23",
  "calendar": { "startDate": "2026-10-23", "lastDate": "2026-10-23", "openMinutesByDate": { ... } },
  "world": {
    "minute": 4210, "essence": 1243.5, "essenceTotal": 18320.0, "revivalCount": 2,
    "rng": "9f3c…", "discovered": ["grass", "worm", "rabbit"],
    "zones":   [ { "alive": true }, ... ],
    "columns": [ { "m": 48.2, "f": 36.1, "d": 9.4, "w": true, "seed": ["grass"],
                   "layers": [ { "sp": "grass", "age": 812, "g": 1, "h": 92, "b": 74, "dorm": false }, null ] }, ... ],
    "animals": [ { "id": 311, "sp": "rabbit", "x": 61, "age": 900, "hu": 72, "cd": 0, "pond": null }, ... ],
    "arrivalTimers": [ ["fox", 5, 60], ... ]
  },
  "player": { "zoneNames": { "4": "Ao Sen" }, "viewportX": 52.0, "metVisitors": ["sika_deer"] },
  "moments": { "cooldowns": { "drought:6": 5100, "discoverHint:flower": 4300 } }
}
```
- **Khoảnh khắc đang hiện không được lưu** (✅ GDD 09 §5.2: mở lại không có gì đang chờ). Chỉ lưu thời gian hồi để không hiện lại quá sớm.
- Động vật giữ `id` qua các lần lưu để View khớp lại được. ✅ M3: **lưu thẳng `nextAnimalId`** thay vì tính max + 1, vì con có id lớn nhất có thể đã chết trước khi lưu; tính lại sẽ làm lệch id của con sinh sau và lưu–đọc không còn ra đúng y.
- ✅ M3 thêm vào `world`: `season`, `snowmeltPending`, `gardenUnlocked`, `nextAnimalId`, `firstBirths` (lần sinh đầu theo đoạn, cho 🐣). `arrivalTimers` dùng id loài: `["fox", 5, 60]`. `rng` là `"state:increment"` dạng hex. Cả hai danh sách được sắp xếp khi lưu để bản chụp không phụ thuộc thứ tự duyệt `Dictionary`.
- ✅ M3: chế độ dev có lịch giả lập (1 ngày lịch = 8 giờ mở app) lưu ở thư mục **`save-simcal/`**, tách khỏi save theo ngày thật ở `save/`. Save có `saveVersion` mới hơn app thì không đọc (báo trong khay), file được cất như file hỏng chứ không bị ghi đè.
- ✅ M3: mùa khi sang ngày mới được áp ở bước kế tiếp; tuyết tan cộng khi bước vào **mọi** ngày Xuân mới, kể cả khi nhảy nhiều ngày.
- Test: lưu → đọc → chạy N bước phải ra **đúng y** trạng thái như khi không lưu (nhờ PRNG lưu được, 01 §5).
