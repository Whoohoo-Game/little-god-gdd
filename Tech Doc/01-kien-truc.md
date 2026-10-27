# 01 · Kiến trúc

## 1. Nguyên tắc
| Nguyên tắc | Lý do (GDD) | Hệ quả kỹ thuật |
|------------|-------------|-----------------|
| **Mô phỏng tách khỏi hiển thị** | ✅ 03 §8: phần lớn thế giới nằm ngoài khung nhìn nhưng vẫn phải chạy; dễ test | Logic game là C# thuần, không tham chiếu `UnityEngine`. Unity chỉ đọc trạng thái và gửi lệnh |
| **Luật được kiểm chứng trước bằng Python** | ✅ quy trình GDD | Mọi luật có số liệu đều có bản tham chiếu trong `worldsim.py`; C# phải cho kết quả thống kê khớp (05 §3) |
| **Tất định theo seed** | Test lặp lại được; save/load không đổi kết quả | Một bộ sinh số ngẫu nhiên có trạng thái lưu được; không dùng `UnityEngine.Random` trong logic |
| **Rẻ khi chạy nền cả ngày** | ✅ 01: ≤ 2% CPU, 30 fps | Bước mô phỏng 1 lần/phút; chỉ dựng đối tượng hiển thị cho phần đang thấy; UI cập nhật 4 lần/giây |
| **Không có gì modal, không gì tự phát âm** | ✅ trụ cột 3 | Lớp UI không có hộp thoại chặn; âm thanh chỉ phát từ thao tác của người chơi (trừ ambient) |

## 2. Các lớp & assembly
```
┌───────────────────────────────────────────────────────────────────────────┐
│ LittleGod.App (Unity)          điểm khởi động, ghép các phần, vòng lặp chính │
└──────┬───────────────┬────────────────┬──────────────────┬────────────────┘
       │               │                │                  │
┌──────▼──────┐ ┌──────▼───────┐ ┌──────▼───────┐ ┌────────▼─────────┐
│ Presentation│ │ UI           │ │ Desktop      │ │ Audio            │   ← Unity
│ view thế giới│ │ khay, sổ tay │ │ cửa sổ dải,  │ │ ambient, SFX     │
│ bong bóng   │ │ cài đặt      │ │ native plugin│ │                  │
└──────┬──────┘ └──────┬───────┘ └──────────────┘ └──────────────────┘
       │ đọc trạng thái, nghe sự kiện, gửi lệnh
┌──────▼───────────────▼────────────────────────────────────────────────────┐
│ LittleGod.Game (C# thuần)   phiên chơi: đồng hồ & lịch, khoảnh khắc, cấp thần,│
│                             Sinh khí nghỉ ngơi, lệnh của người chơi, save   │
└──────┬────────────────────────────────────────────────────────────────────┘
┌──────▼────────────────────────────────────────────────────────────────────┐
│ LittleGod.Simulation (C# thuần)   thế giới 144 cột, vùng, cây, động vật,    │
│                                   Sinh khí, hồi sinh, sự kiện               │
└───────────────────────────────────────────────────────────────────────────┘
```

| Assembly | Phụ thuộc | Nội dung | Hiện có? |
|----------|-----------|----------|----------|
| `LittleGod.Simulation` | — (`noEngineReferences`) | Luật hệ sinh thái (02) | ✅ có, cần mở rộng |
| `LittleGod.Game` | Simulation, Newtonsoft (`noEngineReferences`) | Phiên chơi, khoảnh khắc, lịch, save model (03, 04 §4) | ✅ có từ M3: `GameSession`, lệnh, đồng hồ (thật / giả lập / giả cho test), `SaveData`, `SaveStore`, `GameBalance`, `DevMode` |
| `LittleGod.Presentation` | Game, Simulation, Unity | View cột/cây/động vật, camera, hiệu ứng, bong bóng | ✅ có từ M2: `WorldView`, `Viewport`, `ColumnView`, `AnimalView`, hiệu ứng |
| `LittleGod.UI` | Game, Presentation, Desktop, Unity, uGUI | Khay thần, bản đồ mini, sổ tay, cài đặt, thẻ thông tin | ✅ có từ M2: nút cuộn ◀ ▶, `PrototypeUI`, khay **tạm** (`GodTray` dựng bằng code, thay ở M4) |
| `LittleGod.Desktop` | Unity, UniWindowController | Cửa sổ dải, work area, đa màn hình, plugin native (tray, autostart) | ✅ có từ M0 |
| `LittleGod.Audio` | Game, Unity | Ambient theo biome/mùa/ngày đêm, SFX khi click | Mới (nhỏ) |
| `LittleGod.App` | tất cả | `Bootstrap` MonoBehaviour, composition root | Mới |
| `LittleGod.Editor` | Desktop, Prototype, URP, UniWindowController | Dựng scene, build (thường / Dev), đồng bộ `balance.json` | ✅ có từ M0 |
| `LittleGod.Simulation.Tests` · `LittleGod.Game.Tests` | | EditMode | ✅ một phần |
| `LittleGod.PlayMode.Tests` · `LittleGod.Presentation.Tests` | | Kiểm tra khói (smoke) cảnh chính · logic `Viewport` | ✅ có từ M2 |

Thư mục đích:
```
Assets/LittleGod/
  Scripts/Simulation/   Scripts/Game/   Scripts/Presentation/   Scripts/UI/
  Scripts/Desktop/      Scripts/Audio/  Scripts/App/
  Data/        balance.json (bản sao từ Docs, xem 03 §1), SpeciesVisuals/*.asset, Localization/*.json
  Art/  Audio/  Fonts/  Scenes/Main.unity
  Plugins/macOS/LittleGodNative.bundle   Plugins/Windows/LittleGodNative.dll
  Tests/EditMode/  Tests/PlayMode/
  Editor/      menu dựng scene, build, công cụ dev
```
✅ M2: `Scripts/Prototype/`, `EcoWorld`, `EcoConfig` và test của chúng đã chuyển sang `Archive/prototype-ecoworld/` ở gốc project (ngoài `Assets`, không biên dịch). Project không có git, nên cất thay vì xoá.

## 3. Luồng dữ liệu
```
          ┌───────────── mỗi khung hình (30 fps) ─────────────┐
 đồng hồ  │  GameSession.Tick(realDeltaSeconds)               │
 thật ───►│    ├─ tích luỹ thời gian mở app                    │
          │    ├─ đổi ngày lịch? → mùa mới, Sinh khí nghỉ ngơi  │
          │    ├─ đủ 60 s → World.Step()  (1 phút mô phỏng)     │
          │    └─ MomentDirector.Update(events, world)         │
          │  View: đọc World + Session, xử lý Events, nội suy  │
          │  UI:   4 lần/giây đọc Session (Sinh khí, cấp…)     │
          └───────────────────────────────────────────────────┘
 chuột ──► UI / View ──► GameSession.Execute(Command) ──► World / Moments
```
- **Lệnh** (`PlantCommand`, `RainCommand`, `InviteCommand`, `ReviveCommand`, `CollectMomentCommand`, `RenameZoneCommand`) đi qua `GameSession` để có một chỗ duy nhất kiểm tra giá, ghi log playtest (05 §5) và đánh dấu "có thay đổi cần lưu".
- **Sự kiện** (`EcoEvent`) do mô phỏng ghi vào một danh sách. Mỗi khung hình, `GameSession` chuyển chúng cho `MomentDirector` rồi cho View, sau đó xoá. Giữ cơ chế hiện có của `EcoWorld.Events`; thêm các loại mới ở 02 §5.
- View và UI **không bao giờ sửa** trạng thái mô phỏng trực tiếp.

## 4. Mô hình thời gian
| Khái niệm | Định nghĩa | Dùng cho |
|-----------|------------|----------|
| **Phút mô phỏng** | Một lần `World.Step()`. ✅ Nhịp ×100 (GDD 11 §1): **1 phút thật app mở = 100 phút mô phỏng** (`time.simMinutesPerRealMinute`) | Mọi tốc độ, tuổi thọ, thời gian lớn (07 §2) |
| **Ngày mô phỏng** | 1440 phút mô phỏng | Tuổi thọ ghi "ngày" trong 07/08 |
| **Ngày lịch** | Ngày theo giờ máy (`DateTime.Now.Date`), đổi lúc 0:00 | Mùa (✅ 03 §7), Sinh khí nghỉ ngơi (✅ Q18), ngày hồi sinh hiển thị trong sổ tay |
| **Mùa** | ✅ GDD 11 Q21: `(World.Minute / seasonMinutes) mod 4`, `seasonMinutes` = 3 000 (30 phút thật, 3 ngày đêm); save mới bắt đầu Xuân | Tham số theo mùa của mô phỏng; hình ảnh chuyển dần trong 60 phút mô phỏng (03 §3) |
| **Khung hình** | 1/30 giây | Nội suy chuyển động, hiệu ứng |

- Tắt app thì không có phút mô phỏng nào (✅ Q2). Mở lại thì `GameSession` so ngày lịch với lần lưu cuối để biết mùa hiện tại và có cấp Sinh khí nghỉ ngơi hay không (03 §3–4).
- ↻ **2026-10-24:** mùa không còn đến từ lịch. `World` tự tính mùa từ `Minute` (vẫn thuần, tất định); `World.SetSeason` bị bỏ. Ngày lịch chỉ còn dùng cho Sinh khí nghỉ ngơi và sổ tay.
- **Nhịp thật** ×100 ≈ 1.7 `Step()` mỗi giây. **Tốc độ dev** (×1, ×10, ×60 trên nền ×100): chạy nhiều `Step()` trong một khung hình, tối đa 20 bước/khung. Ở chế độ này lịch cũng được giả lập: "1 ngày lịch = N giờ mở app" (mặc định 8, giống `worldsim.py`).

## 5. Tất định & số ngẫu nhiên
- Mô phỏng dùng một PRNG riêng (**PCG32** hoặc **xoshiro128\*\***) có trạng thái 64–128 bit **lưu vào save**, thay cho `System.Random` (không lưu được trạng thái).
- Tách luồng ngẫu nhiên: `World.Rng` (sinh thái), `Moments.Rng` (khoảnh khắc, khách lạ). Như vậy thêm/bớt khoảnh khắc không làm đổi diễn biến sinh thái của cùng seed.
- Hiển thị (nhún nhảy, vị trí lệch nhẹ) dùng `UnityEngine.Random`, không ảnh hưởng mô phỏng.
- Không dùng `Dictionary`/`HashSet` để **duyệt** khi thứ tự ảnh hưởng kết quả. Duyệt theo mảng/danh sách có thứ tự (`Seedbank` hiện đã giữ thứ tự, xem `EcoEntities.cs`).

## 6. Chế độ dev
- Bật bằng scripting define `LITTLEGOD_DEV` (mặc định bật trong Editor và bản build "Dev"), tắt trong bản phát hành.
- Gồm: tốc độ thời gian, nhân Sinh khí, Sinh khí vô hạn (đang có trong `EcoConfig.EssenceMultiplier` / `UnlimitedEssence`), lớp phủ debug (hệ số Đa dạng/Cân bằng, Sức khoẻ từng vùng), nhảy ngày lịch, xuất log playtest.
- ⚠️ Prototype hiện để `essenceMultiplier = 10` và `unlimitedEssence = true` trong `EcosystemView`. Bản chơi thử slice **phải** về 1 / false, nếu không mọi đánh giá về nhịp đều sai.
