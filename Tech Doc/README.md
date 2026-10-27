# Little God — Technical Doc

> Phiên bản: **v0.1 (nháp)** · Cập nhật: 2026-10-23
> Phạm vi: **vertical slice** đã đặc tả trong GDD: Đồng cỏ ([07](../GDD/07-he-sinh-thai-chi-tiet.md)), Ao và hồi sinh vùng ([08](../GDD/08-nhieu-vung-va-ao.md)), Khoảnh khắc ([09](../GDD/09-khoanh-khac.md)), Giao diện ([10](../GDD/10-giao-dien.md)).
> Quy trình (✅ GDD README): **GDD → Technical Doc → triển khai.** Tài liệu này chuyển GDD thành quyết định kỹ thuật và kế hoạch làm. Khi GDD đổi, sửa ở đây trước rồi mới sửa code.

## Mục lục
| # | Tài liệu | Nội dung | Trạng thái |
|---|----------|----------|------------|
| 01 | [Kiến trúc](01-kien-truc.md) | Các lớp, assembly, luồng dữ liệu, mô hình thời gian, tất định | 💡 Nháp |
| 02 | [Mô phỏng](02-mo-phong.md) | Mô hình dữ liệu thế giới 144 cột, thứ tự một bước, khoảng cách với `EcoWorld` hiện tại, hiệu năng | 💡 Nháp |
| 03 | [Dữ liệu, thời gian & lưu game](03-du-lieu-thoi-gian-luu-game.md) | Bảng số dùng chung với Python, dữ liệu hình ảnh, lịch & mùa, Sinh khí nghỉ ngơi, định dạng save | 💡 Nháp |
| 04 | [Hiển thị, khoảnh khắc & UI](04-hien-thi-va-ui.md) | Camera & cuộn, chỉ dựng view trong khung nhìn, hệ khoảnh khắc, UI, cửa sổ desktop | 💡 Nháp |
| 05 | [Kế hoạch triển khai & kiểm thử](05-ke-hoach-trien-khai.md) | Các mốc M0–M7, tiêu chí xong, chiến lược test, ngân sách hiệu năng | 💡 Nháp |
| 06 | [Môi trường sống](06-moi-truong-song.md) | GDD 12 → code: biome theo cột, lấn đất hoang, động vật tự đến, Sóc, kết game mới, save v3 | ✅ M4c xong |
| 07 | [Bầy đàn & lãnh thổ](07-bay-dan.md) | GDD 13 → code: bầy, hang, đi tới đích rồi nghỉ, sinh sản chậm lại, vai trò theo vùng sống, save v4 | ✅ Xong |
| 08 | [Hang thỏ & săn mồi](08-hang-va-san-moi.md) | GDD 14 → code: hang thỏ, con mồi né và trốn, thú săn rượt và vồ, bụi cỏ tung lên, save v5 | ✅ Xong code, chờ thử tay |
| 09 | [Sinh động, phản hồi & khoảnh khắc rút gọn](09-sinh-dong-va-phan-hoi.md) | GDD 15 → code: phản hồi tức thì, sinh vật trang trí, hành vi nhỏ, `MomentDirector` 6 loại, `balance.json → moments` mới | ✅ Xong code, chờ thử tay |
| 10 | [Nắn đất](10-nan-dat.md) | GDD 16 → code: ao động (`World.Ponds`), đào / lấp từng ô, môi trường ao tự sinh, công cụ ⛰️, save v6 | ✅ Xong code, chờ thử tay |
| 11 | [Hươu và Sói](11-huou-va-soi.md) | GDD 17 → code: Hươu, Sói, Dương xỉ mọc lại, một cặp thú săn mỗi khu, con lẻ nhập đàn | ✅ Xong code, chờ thử tay |

**Ký hiệu:** dùng chung với GDD (✅ đã chốt · 💡 đề xuất · ❓ cần quyết định). ⚠️ là rủi ro kỹ thuật.

## Hiện trạng code (2026-10-24, sau M0)
| Phần | Ở đâu | Tình trạng so với slice |
|------|-------|-------------------------|
| Mô phỏng thuần C# | `Assets/LittleGod/Scripts/Simulation` (assembly `LittleGod.Simulation`, `noEngineReferences`) | ✅ M1: **`World` 144 cột** theo luật slice (02), đọc `balance.json` qua `Balance`, dùng `Pcg32`. `EcoWorld` cũ đã cất vào `Archive/` ở M2 |
| Test | `Assets/LittleGod/Tests` | ✅ M4c: 68 EditMode (+1 Explicit) và 3 PlayMode (+1 Explicit chụp hình). M4b: 62 EditMode và 2 PlayMode. Trước đó: 54 EditMode (`World`, `Pcg32`, `Viewport`, lịch, Sinh khí nghỉ ngơi, lưu–đọc, đồng bộ `balance.json`, bảng chữ vi/en, glyph phông; 1 test Explicit tạo file mẫu save) + 2 PlayMode smoke (`WorldView`, prefab UI) |
| Hiển thị prototype | `Assets/LittleGod/Scripts/Presentation`, `Scripts/UI` | ✅ M2: `WorldView` chạy `World` 144 cột, camera cố định cuộn theo `Viewport`, pool view theo khung nhìn, Ao / đất hoang / cây khô Khu Vườn, nút cuộn ◀ ▶. ✅ M4: UI là prefab `Assets/LittleGod/UI/PrototypeUI.prefab` (dựng bằng *Little God → Build UI prefab*): khay thần thu gọn / mở rộng, công cụ Gieo / Mưa (`ToolController`), bản đồ mini, thẻ thông tin, chữ qua `Localization` vi/en. 💌 / 🌿 trong khay mời / hồi sinh ngay, tạm cho tới khoảnh khắc ở M5. Sinh khí ×10 / vô hạn chỉ ở chế độ dev |
| Phiên chơi & lưu game | `Assets/LittleGod/Scripts/Game` | ✅ M3: `GameSession` (lịch theo ngày thật, mùa, tuyết tan, Sinh khí nghỉ ngơi, giờ mở app theo ngày), lệnh, `SaveStore` (tmp → đổi tên, `.bak`, cất file hỏng). `WorldView` tự lưu mỗi 5 phút, khi hồi sinh, đổi ngày, thoát; mở lại đúng vị trí khung nhìn |
| Cửa sổ desktop | `Assets/LittleGod/Scripts/Desktop` | Dải trong suốt luôn trên cùng, sát Dock/taskbar, 30 fps, click xuyên qua bằng UniWindowController (`HitTestType.Raycast`) |
| Dựng scene & build | `Assets/LittleGod/Editor/DesktopPrototypeSetup.cs` | Menu *Little God → …* dựng scene `DesktopPrototype` và build macOS |
| Mô hình thiết kế | `Docs/GDD/sim/ecosim.py`, `worldsim.py`, `balance.json` | `worldsim.py` là **tham chiếu cho luật slice** (nhiều vùng, Ao, cân bằng tự nhiên). ✅ M0: đọc mọi số từ `balance.json` |

Công cụ: Unity **6000.6.3f1**, URP 2D, Input System 1.20, uGUI 2.6, Test Framework 1.8, UniWindowController (git, commit `304f9ba`).

## Quyết định kỹ thuật
✅ Đã chốt hết ngày 2026-10-23.

| # | Câu hỏi | Quyết định | Chi tiết |
|---|---------|------------|----------|
| ✅ T1 | Bảng số cân bằng để ở đâu cho cả C# và Python cùng đọc? | Một file `balance.json` dùng chung; Python đọc thay cho bảng viết tay | [03 §1](03-du-lieu-thoi-gian-luu-game.md#1-bảng-số-cân-bằng-một-nguồn-cho-c-và-python) |
| ✅ T2 | Sổ tay và Cài đặt là "cửa sổ riêng" (GDD 10 §6): làm thế nào khi Unity chỉ có một cửa sổ? | Tạm **nới cao** cửa sổ dải đất khi mở panel; phần trống vẫn trong suốt và click xuyên qua | [04 §6.2](04-hien-thi-va-ui.md#62-sổ-tay--cài-đặt-như-cửa-sổ-riêng) |
| ✅ T3 | Biểu tượng menu bar / system tray và khởi động cùng máy cần plugin native | Plugin native `LittleGodNative` cho macOS và Windows, làm ở **mốc M6**; trước đó dùng nút Ẩn/Thoát tạm | [04 §6.3](04-hien-thi-va-ui.md#63-menu-hệ-thống--khởi-động-cùng-máy) |
| ✅ T4 | Giữ uGUI hay chuyển UI Toolkit? | **Giữ uGUI**, chuyển UI sang prefab | [04 §5](04-hien-thi-va-ui.md#5-ui) |
| ✅ T5 | Thư viện JSON cho save | `com.unity.nuget.newtonsoft-json` | [03 §5](03-du-lieu-thoi-gian-luu-game.md#5-lưu-game) |

## Nhật ký quyết định
| Ngày | Quyết định |
|------|------------|
| 2026-10-23 | ✅ Technical Doc viết cho vertical slice, dựa trên GDD 07–10 |
| 2026-10-23 | ✅ **T1:** `Docs/GDD/sim/balance.json` là nguồn số cân bằng duy nhất; `worldsim.py` và Unity cùng đọc; test fail nếu bản sao trong `Assets/LittleGod/Data` lệch |
| 2026-10-23 | ✅ **T2:** Sổ tay và Cài đặt làm bằng cách tạm nới cao cửa sổ dải đất khi mở panel (cách A, 04 §6.2) |
| 2026-10-23 | ✅ **T3:** Plugin native `LittleGodNative` (menu bar / system tray, khởi động cùng máy) làm ở mốc M6 |
| 2026-10-23 | ✅ **T4:** Giữ uGUI, chuyển UI từ dựng bằng code sang prefab |
| 2026-10-23 | ✅ **T5:** Save dùng `com.unity.nuget.newtonsoft-json` |
| 2026-10-24 | ✅ **M0 xong** (05 §1): assembly Desktop / Game / Prototype / Editor; `balance.json` + `worldsim.py` đọc từ đó (output giống hệt bản cũ); `Pcg32`; `DevMode` + build Dev (`LITTLEGOD_DEV`); Sinh khí ×10, vô hạn và nút tốc độ chỉ còn ở chế độ dev. 17/17 test EditMode xanh, build macOS thường và Dev thành công |
| 2026-10-24 | Test `AttentivePlayer…`: ngưỡng cáo tối đa nới từ ≤ 4 lên ≤ 6 theo phân bố của `ecosim.py` trên 60 seed (2–6). Ngưỡng cũ chỉ dựa trên 20 seed nên đỏ khi đổi bộ sinh số |
| 2026-10-24 | ✅ **M1 xong** (05 §1): `World` 144 cột + `Balance` (Newtonsoft), `SliceRunner`, 19 test mới; thống kê khớp `worldsim.py` (05 §3.2); 0.137 ms/bước. 36/36 test xanh, build macOS Dev thành công |
| 2026-10-24 | Khác `worldsim.py`: phải **khám phá** Hoa dại / Mâm xôi / Sen trước khi gieo (theo khoảnh khắc 🌱, GDD 09). `SliceRunner` khám phá ngay khi đạt ngưỡng nên nhịp không đổi |
| 2026-10-24 | ✅ **M2 xong, trừ đo CPU** (05 §1): assembly `Presentation` + `UI`; `WorldView` / `Viewport` / pool view; sprite Ao, đất hoang, Khu Vườn; hiệu ứng `Starved` (nằm xuống, để lại ụ mùn), `Hunted` (chạy khỏi khung nhìn, thú săn đuổi theo), `Arrived` (đi vào từ mép), `ZoneRevived` (lấp lánh, đất xanh dần); nút cuộn ◀ ▶ đủ click / giữ / double-click. Code cũ cất vào `Archive/prototype-ecoworld/`. 30 EditMode + 1 PlayMode xanh, build macOS thường và Dev thành công |
| 2026-10-24 | Tạm thời tới M5: khám phá cây theo ngưỡng 🌱 tự động trong `WorldView`; khay có nút "Hồi sinh" thay cho 🌿. Tối đa 16 hoạt ảnh rời đi cùng lúc (ở tốc độ dev nhiều con chết trong một khung hình) |
| 2026-10-24 | ✅ **M3 xong** (05 §1): `GameSession` + lệnh + đồng hồ thật / giả lập; `SaveData` + `SaveStore`; `World.Capture/Restore`; khay tạm dùng lệnh, có nút dev "Thế giới mới"; tuyết phủ / tan dần trong 60 phút. 47 EditMode (+1 Explicit) và 1 PlayMode xanh, build macOS thường và Dev thành công |
| 2026-10-24 | Lưu `nextAnimalId` thẳng vào save (khác 03 §5 cũ ghi max + 1), để lưu–đọc ra đúng y |
| 2026-10-24 | ✅ **M4 xong phần code, chờ thử tay** (05 §1): prefab UI dựng bằng `UiPrefabBuilder`; `GodTrayView` (mở 150 ms / đóng 600 ms, cấp, quyền năng khoá "Sắp có", chú thích, chấm báo), `ToolController` (Gieo tô cột theo tỉ lệ nảy mầm, Mưa click 7 cột hoặc kéo tới 21 cột, giá 30 × ⌈n/7⌉), `MiniMapView` (Texture2D 144 × 1, khung nhìn, mép hồi sinh được, click / kéo), `InfoCardView` (300 ms, ghim 4 giây, dòng dev); `Localization` + `vi.json` / `en.json` (88 khoá, ngôn ngữ theo hệ thống, ghi đè bằng PlayerPrefs `littlegod.lang`). 53 EditMode (+1 Explicit) + 2 PlayMode xanh, build macOS thường và Dev thành công. **Chưa** thử tay danh sách GDD 10 §13 trên máy thật |
| 2026-10-24 | Khác 04 §5: phông dùng **uGUI `Text` + TTF động** (LegacyRuntime, đủ 53 ký tự có dấu đang dùng, có test glyph) thay cho TextMeshPro bitmap, vì T4 giữ uGUI cũ và TTF động không cần dựng atlas. Phông pixel có dấu: **chờ chọn** (đổi một chỗ `UiPrefabBuilder.FontPath`). Không có `GodTrayModel` riêng: `GodTrayView` đọc `World` 4 lần/giây; thẻ thông tin là Screen Space cạnh con trỏ thay vì World Space. Icon vẫn sinh bằng code (`PixelIcon` gắn lúc chạy) tới khi có art |
| 2026-10-24 | ✅ **GDD 11 → kỹ thuật:** đồng hồ ×100 trong `GameSession.Advance`; `World` tự tính mùa từ `Minute` (bỏ `SetSeason`, lịch chỉ còn cho Sinh khí nghỉ ngơi); Sinh khí nghỉ ngơi = tốc độ × 100 × tối đa 10 phút; save v2 (3 tầng, đọc được v1); tầng tán là `Layers[2]`, cột có `Canopy` / `OwnCanopy` / `Bank`; quả theo `PlantSpecies.FruitEaters` thay `EatsBerries`; khám phá cây tán thêm luật `zoneLivingPlants` và `animals` trong `moments.discover`. Mốc mới **M4b** (05 §1) |
| 2026-10-24 | Hình: `SkyView` (nền trời + collider phủ dải), đất 36 pt, cá bơi trong các cột nước của ao (04 §1) |
| 2026-10-24 | Sửa lỗi: dải che menu chuột phải của Dock trên macOS. Hạ tầng cửa sổ từ 101 (tầng menu, do UniWindowController đặt) về 3 (floating) bằng `MacWindowLevel` (04 §6.1) |
| 2026-10-24 | Hình cây tán: chiều cao ngẫu nhiên theo loài (hash cột + phút nảy mầm), cây lớn thêm sau trưởng thành; `ForestBackdrop` vẽ 3–5 cây mờ phía xa cho mỗi cặp cây tán cách nhau ≤ 3 cột, tàn lụi khi mất một cây chính; chỉ là hình, không lưu (GDD 11 §2.6, 04 §3) |
| 2026-10-24 | **Sửa lỗi nghiêm trọng:** `WorldState.ColumnState.Layers` cố định 2 phần tử nên `World.Capture` ném `IndexOutOfRange` khi có cây tán: tự lưu hỏng mỗi khung hình và nút Thoát không thoát (thoát gọi lưu trước). Mảng nay theo `Column.LayerCount`; `WorldView.Save` bắt lỗi (báo trong khay, không chặn); nút Thoát luôn thoát. Test `CanopyTrees_SaveAndLoad` |
| 2026-10-24 | UI (GDD 10 §3): danh sách bật lên xổ ngang; khay ẩn khi cầm công cụ; hình xem trước khi gieo |
| 2026-10-24 | Cân bằng (GDD 11 §2.2–2.3): cây non tầng tán ngủ khô thay vì chết (`World.StepPlants`, `worldsim.plants`); Sồi lớn 1 440 phút, ẩm 15/30, màu 20. Sồi gieo lớn được 7% → 98%. Test `TreeSapling_GoesDormantInDrought_InsteadOfDying` |
| 2026-10-24 | Rừng phía xa: cặp hình thành ngay khi có hai cây tán (kể cả cây non) cách ≤ 3 cột; cây xa lớn theo `Growth`/`Age` của cây chính trẻ hơn, rải đều giữa hai gốc, trơ cành khi cây chính cùng loài ngủ khô (GDD 11 §2.6) |
| 2026-10-24 | Lá mọc / rụng dần (GDD 11 §2.6): `PixelSprites` tách thân + cành và tán lá; `TreeSprite` (cây chính và cây xa) mọc lá 6 s, rụng 4 s kèm `FallingLeaf`, đổi màu tán mờ dần 3 s; tán đặt gần camera hơn thân 0.01 để luôn che cành |
| 2026-10-24 | `TreeSprite`: lúc ổn định vẽ một sprite ghép (thân + tán), chỉ tách hai lớp khi đang chuyển, để cây mờ không lộ thân qua lá; thời gian mọc / rụng / đổi màu nhân `TreeSprite.TimeScale` (= tốc độ chơi, WorldView đặt mỗi khung) |
| 2026-10-24 | Rừng (GDD 11 §2.2, §2.6): `canopySpacing` 2 → 1 (giữa hai gốc trống ít nhất 1 ô); `ForestBackdrop` ghép cặp cây tán liền nhau cách ≤ 7 cột (trước ≤ 3) |
| 2026-10-24 | Mùa Đông (GDD 11 §2.6): lớp tuyết trên đất (cả đất hoang), băng trên ao (cá mờ bên dưới), cỏ / bụi màu rơm phủ tuyết, `PixelSprites.TreeSnow` đọng trên cành (cây chính và cây xa), mưa mùa Đông vẽ thành tuyết rơi, `SkyView` thêm tối đa 60 bông tuyết lất phất theo `WorldView.Snow` |
| 2026-10-24 | ✅ **GDD 12 → kỹ thuật** ([06](06-moi-truong-song.md)): `Biome` theo cột, `biomeModel` trong `balance.json` dùng chung với `biomesim.py`, bỏ mời / hồi sinh, save v3, mốc **M4c** |
| 2026-10-24 | ✅ **M4c xong:** `World` biome theo cột, lấn đất hoang, ao thức dậy, hành lang, động vật tự đến theo `biomeModel.habitat`, Dương xỉ, Sóc, Vườn / kết game theo GDD 12 §5; bỏ mời, hồi sinh; save v3; `SliceRunner` theo người chơi mô hình của `biomesim.py`; thống kê C# khớp (06 §6) |
| 2026-10-24 | Thú vẽ theo tỉ lệ thật, chuẩn Cáo 14 px ≈ 105 cm (GDD 03 §3): Thỏ 6×5, Sóc 7×5, Diệc 9×13, Cá 5×2; Ong, Giun cỡ nhỏ nhất còn thấy; `AnimalView` collider tối thiểu 0.5 đơn vị |
| 2026-10-24 | ✅ **GDD 11 §1.5 → kỹ thuật:** ngày đêm theo `World.Minute` (`time.dayNightMinutes = 1000`, `World.DayHour`), bỏ `DateTime.Now` khỏi `SkyView`; `AnimalView` có nếp ngủ / thức theo loài, chỉ là hình (03 §3, 04 §2) |
| 2026-10-24 | `time.seasonMinutes` 2 880 → **3 000** (1 mùa = 30 phút thật = 3 ngày đêm, GDD 11 §1.1); `CalendarTests` theo số mới. 70 EditMode xanh |
| 2026-10-25 | ✅ **GDD 13 → code** ([07](07-bay-dan.md)): mục `social` trong `balance.json`; `WorldSocial.cs` (bầy, hang, đi tới đích rồi nghỉ, ai được sinh, vai trò theo vùng sống); `AnimalView` đứng lệch trong cột; save v4 (bầy, hang, đích). Thống kê C# khớp `socialsim.py`; quay đầu 33 → ~2 lần/con/phút thật. 79 EditMode + 3 PlayMode xanh |
| 2026-10-25 | ✅ **GDD 14 → code** ([08](08-hang-va-san-moi.md)): mục `hunting`; `WorldHunting.cs` (hang thỏ, dời hang, hang bỏ trống, con mồi cảnh giác / chạy về chỗ trú / trốn, thú săn rượt rồi lao tới vồ); `AnimalView` trốn, chạy, vồ; `DustPuff`; hang vẽ trong `WorldView`; save v5. Thống kê C# khớp `huntsim.py`. 86 EditMode + 3 PlayMode xanh |
| 2026-10-25 | ✅ Thỏ ngủ trong hang, sóc trên cây là luật mô phỏng ([08 §2b](08-hang-va-san-moi.md)): `hunting.sleep`, `World.Asleep`, `Animal.Sleeping`; thỏ con sinh trong hang ở trong hang; `AnimalView` theo giờ ngủ của mô phỏng cho thỏ, sóc; cáo thức 15h–9h; cáo no 15 giờ mp. 89 EditMode + 3 PlayMode xanh |
| 2026-10-26 | ✅ Hang thỏ mặt cắt + gia đình 4 con ([08 §7](08-hang-va-san-moi.md)): `SocialRule.CapLitter`; `PixelSprites.BurrowSection` / `BurrowMound`; `WorldView.BurrowSlot`; thỏ trốn / ngủ nằm trong buồng, vẫn nhìn thấy. 90 EditMode + 3 PlayMode xanh |
| 2026-10-28 | ✅ **Mở hết cây gieo được** (GDD 04 §3): `World.KnowSowablePlants()` khi tạo thế giới và khi đọc save cũ; bỏ nguồn 🌱 trong `MomentDirector`. Test mới: `NoSeedDiscoveryMoments`, `OldSave_UnlocksAllSowablePlants` |
| 2026-10-28 | ✅ Nút **🌍 Phủ đất** (GDD 10 §2): `UiPrefabBuilder` thêm `coverButton` trước Gieo (Gieo, Mưa, ô khoá dời phải 68 pt); `GodTrayView` có `PopupKind.Cover` chỉ liệt kê cây `IsCover`, Gieo bỏ cây phủ |
| 2026-10-28 | ✅ **GDD 17 → code** ([11](11-huou-va-soi.md)): Hươu, Sói trong `biomeModel.animals`; Dương xỉ `regrow` 0.4; luật Q52 (`PreyFallback`), Q54 (`PredatorPresent`), Q55 (`JoinLoneHerds`), Q57 (`UpdateLone`, `Animal.Alone` trong save); hang Sói chỉ trong Rừng (`denBiome`); `PixelSprites.Deer/Wolf`, hành vi trong `AnimalView`. `forestsim.py` đọc số từ `balance.json`. Thống kê C# 10 seed: Hươu có mặt 100%, Sói 100% ở 8/10 seed, kết 0.6–1.2 giờ thật. 124 EditMode + 4 PlayMode xanh |
