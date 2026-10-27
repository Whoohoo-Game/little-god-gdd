# 04 · Hiển thị, khoảnh khắc & UI

> Nguồn: GDD [09 Khoảnh khắc](../GDD/09-khoanh-khac.md), [10 Giao diện](../GDD/10-giao-dien.md), [01 Ràng buộc](../GDD/01-tong-quan.md#ràng-buộc-từ-hình-thức-dải-đáy-màn-hình).

## 1. Camera & khung nhìn
- Camera orthographic, **1 unit = 1 cột = 32 pt**. Chiều cao dải 180 pt = 5.625 unit; ✅ mặt đất **36 pt = 1.125 unit** (ô 16 × 18 px), đủ sâu cho cá bơi trong ao.
- ✅ **Nền trời** (`SkyView`) phủ cả dải sau thế giới: dải màu đỉnh trời → chân trời theo mùa (nội suy `seasonBlend`), sáng tối theo giờ trong ngày của game (`WorldView.DayHour`, 03 §3; sáng 7h–17h, tối 19h–5h, ráng quanh 6h và 18h; sao khi đêm), mây trôi có thị sai. Có `BoxCollider2D` phủ cả dải nên hit-test `Raycast` của UniWindowController luôn coi con trỏ trong dải là "trên game": click hụt mặt đất không rơi xuống desktop. `WorldView.Pick` bỏ qua collider này khi tìm vật dưới con trỏ (con vật > cây > đất).
- Thế giới rộng 144 unit. Khung nhìn rộng `screenWidthPt / 32` cột (màn 1512 pt thấy ~47 cột). Camera **không co** cả thế giới vào màn hình như prototype (`FitCamera`). Kích thước camera cố định theo chiều cao dải, còn vị trí X là `viewportX`.
- `ViewportController` giữ `viewportX`, kẹp trong `[0, 144 − viewWidth]`, lưu vào save (03 §5). Nút cuộn, bản đồ mini, sổ tay và chế độ theo dõi đều chỉ đặt **đích**; controller trượt tới đích với easing (GDD 10 §4–5).
- Pixel perfect: dùng **Pixel Perfect Camera** của URP 2D với Assets PPU 16. Kiểm tra trên màn Retina (1 pt = 2 px) và màn thường 1×.

## 2. Chỉ dựng view trong khung nhìn
✅ GDD 03 §8: chỉ tạo GameObject cho phần đang thấy cộng một đoạn đệm.

| Thành phần | Cách làm |
|------------|----------|
| `ColumnView` | Pool cố định `viewWidth + 2 × 8` (đệm 8 cột mỗi bên). Khi cuộn, view trôi khỏi một bên được gán lại cho cột mới ở bên kia |
| `AnimalView` | Pool. Chỉ gán cho động vật có `X` trong khung nhìn ± 8. Động vật đi ra ngoài thì trả view về pool. Nhờ vậy cảnh "đuổi ra khỏi màn hình" và "đi vào từ mép" (✅ 03 §3) diễn ra ở mép **khung nhìn**, không phải mép thế giới |
| Hiệu ứng (mưa, lấp lánh, ụ mùn) | Pool theo loại. Sự kiện xảy ra ngoài khung nhìn thì **bỏ** hiệu ứng |
| Đất hoang | Một dải sprite lặp + lớp sương mờ; không cần view theo cột |

- Mỗi khung hình chỉ `Refresh` các `ColumnView` đang hoạt động (~63 cột), thay cho cả thế giới.
- Động vật nội suy vị trí giữa hai bước (mô phỏng di chuyển theo cột, mỗi phút một lần), như `AnimalView` hiện tại.
- ✅ **Nếp sinh hoạt (GDD 11 §1.5, chỉ là hình):** `AnimalView` đọc `WorldView.DayHour` mỗi khung, so với khoảng thức của loài (bảng trong `AnimalView.AwakeHours`, Cáo khoảng vắt qua nửa đêm), lệch riêng mỗi con 0–0.7 giờ theo `Id`. Lúc ngủ: đứng yên tại chỗ (bỏ qua `SetColumn`), sprite thấp xuống 15%, một sprite "z" con bay lên mờ dần; Ong hạ xuống sát cỏ; Cá bơi chậm, sát đáy. Thức dậy: đi bộ tới cột mô phỏng, tốc độ tối đa 4 unit/s. `Exit` / `Chase` / `Die` đánh thức con vật. `WorldView.SyncAnimals` giữ view đang ngủ khi chỗ nó nằm còn trong khung nhìn, dù cột mô phỏng đã ra ngoài; `NearestPredator` ưu tiên thú săn đang thức.

## 3. Thể hiện trạng thái (đọc bằng một cái liếc)
| Trạng thái mô phỏng | Thể hiện | GDD |
|---------------------|----------|-----|
| Độ ẩm cột | Màu đất (khô vàng ↔ ẩm xám xanh) | 07 §3.1 |
| Máu cây < 60 / < 30 / ngủ khô | Ngả vàng / vàng úa rũ / nâu | 07 §5.2 |
| Sinh khối cỏ | Chiều cao cỏ | 08 §7.3 (cỏ trụi) |
| Thú đói (độ no < 60) | Gầy hơn, đi chậm hơn | 08 §7.3 |
| Chết đói / chết già | Nằm xuống, mờ dần 1.5 s, để lại ụ mùn hoặc bông hoa nhỏ | ✅ 03 §3 |
| Bị săn | Con mồi chạy khỏi mép khung nhìn, thú săn đuổi theo rồi quay lại | ✅ 03 §3 |
| Mùa | Bảng màu và lớp phủ (tuyết, lá) nội suy theo `seasonBlend` (03 §3). ✅ Mùa Đông (GDD 11 §2.6): `ColumnView` thêm lớp tuyết trên mặt đất (sprite phủ mép cỏ, độ đục = lượng tuyết) và lớp băng trên cột nước (trên cá); cây thấp ngả trắng 60%; `TreeSprite` thêm lớp tuyết đọng trên cành (`PixelSprites.TreeSnow`); `RainEffect` vẽ bông tuyết khi mùa Đông; `SkyView` thêm tuyết bay lất phất theo lượng tuyết | ✅ 03 §7 |
| Cây tán (tầng 2) | Sprite vẽ bằng code theo loài (cao nhất: Sồi ~4.4 unit, Liễu ~3.6, Táo dại ~2.8; GDD 11 §2.6), vẽ sau tầng bụi. Lớn 15% → 80% theo `Growth`, rồi → 100% sau thêm 2 × `GrowMinutes` tuổi. Chiều cao riêng mỗi cây = hash(cột, phút nảy mầm = `Minute − Age`) → hệ số trong khoảng của loài; không cần lưu. **Rừng phía xa:** `ForestBackdrop` (Presentation) mỗi khung tìm các cặp cây tán liền nhau (kể cả cây non) cách nhau ≤ 7 cột quanh khung nhìn; mỗi cặp sinh 3–5 sprite mờ (độ đục 0.35–0.6, ngả lam, sorting sau cây chính, không collider), rải đều giữa hai gốc; tuổi thọ, chiều cao, loài lấy từ hash(cặp, phút cặp hình thành = phút nảy mầm của cây trẻ hơn). Độ lớn theo `Growth`/`Age` của cây chính trẻ hơn; dáng theo mùa, trơ cành khi cây chính cùng loài ngủ khô. Cặp biến mất thì sprite mờ dần 2 giây rồi trả về pool. Không đụng `World`, không lưu. **Lá:** `TreeSprite` gồm sprite thân + cành (luôn có) và sprite tán (pivot ở giữa tán) với `leafAmount` 0..1 tiến dần về đích (có lá / trơ cành): mọc 6 s (phóng to), rụng 4 s (mờ, sinh `FallingLeaf` theo lượng giảm, tối đa 240 lá cùng lúc), đổi màu tán bằng sprite tán thứ hai mờ dần 3 s; gắn lại cột thì đặt ngay, không diễn | Cây non lớn dần theo `Growth`; Thu lá cam, Đông trơ cành; Táo dại hoa Xuân, quả Hạ–Thu; Liễu rủ cành. Collider ở thân để thẻ thông tin chọn được | GDD 11 §2.6 |
| Vùng Cân bằng | Vài đốm sáng nhỏ trôi chậm | GDD 10 §5 |
| Kích cỡ thú | Sprite vẽ theo tỉ lệ thật, chuẩn là Cáo 14 px ≈ 105 cm (GDD 03 §3); `AnimalView` cho collider tối thiểu 0.5 × 0.5 đơn vị để thú nhỏ vẫn chọn được | GDD 03 §3 |

## 4. Hệ khoảnh khắc (`LittleGod.Game.Moments`)
Logic khoảnh khắc là **C# thuần** trong `LittleGod.Game`, để test được và để sau này có thể mô phỏng song song trong Python (GDD 09 §9). Unity chỉ vẽ.

```
MomentDirector.Update(world, events, viewport, nowMinute)
  1. nguồn sự kiện   : Arrived → ✨, Born/SwarmFounded (đã lọc) → 🐣, ZoneRevived → 🏷️
  2. nguồn trạng thái (mỗi 30 phút mô phỏng, lệch pha theo vùng):
                       hạt khám phá/hạt quà → 🌱, khách lạ → 🦋, lời mời → 💌,
                       vùng khô → 💧, sẵn sàng hồi sinh → 🌿, ăn trụi → 🍂
  3. luật chặn       : tối đa 1 mỗi vùng; nhóm A mới cách nhau ≥ 10 phút (bỏ, không xếp hàng,
                       trừ 🌱 khám phá); thời gian hồi theo (loại, vùng)
  4. hết hạn         : 30 phút (dừng đếm khi chuột đang rê trên bong bóng)
  → ActiveMoments: danh sách { id, type, zone, x, createdAt, expiresAt, payload }
```
- **Hiển thị:** `MomentPresenter` (Presentation) chọn tối đa **3** bong bóng trong khung nhìn theo thứ tự ưu tiên của GDD 09 §5.2, đẩy bong bóng ra khỏi vùng khay, và vẽ chỉ báo trên nút cuộn (GDD 09 §7).
- **Click:** gửi `CollectMomentCommand(id)` → `MomentDirector` áp kết quả qua API mô phỏng: `GrantEssence` (quà), `Discover` + `TryPlant(free)` (🌱), `TryRain` (💧), `TryInvite` (💌), `TryRevive` (🌿).
- **Khách lạ** là đối tượng của `Moments`, không phải `Animal` của mô phỏng (không ăn, không bị săn; GDD 09 §3.2). View vẽ nó như một con vật đi ngang.
- Hằng số (thời gian sống, hồi, quà ×3 / ×20, tỉ lệ khách lạ) đọc từ `balance.json → moments` (03 §1).

## 5. UI
**✅ Quyết định (T4): giữ uGUI**, chuyển từ dựng bằng code (`GodTray.Build`) sang **prefab**:
- Dự án đã dùng uGUI, và hit-test `Raycast` của UniWindowController đã chạy với nó.
- Bong bóng và thẻ thông tin nằm trong thế giới, dễ làm bằng canvas World Space.
- UI Toolkit mạnh hơn về layout nhưng kém ở phần UI trong thế giới, và chưa được thử với cách click xuyên qua của UniWindowController.

| Thành phần (GDD 10) | Lớp | Ghi chú |
|---------------------|-----|---------|
| Khay thần thu gọn / mở rộng (§3) | `GodTrayView` | ✅ M4: đọc `World` 4 lần/giây (không tách Model, khay chỉ đọc). Độ trễ mở 150 ms / đóng 600 ms đặt trong Inspector để chỉnh khi chơi thử |
| Công cụ Gieo / Mưa (§3.3) | `ToolController` | Trạng thái: `None` (mặc định), `Sow(id)`, `Rain`. Huỷ bằng chuột phải / Esc / 20 giây không dùng. Lớp tô cột theo `World.Suitability`; ✅ hình mờ xem trước (`ghost`, sprite của loài, cây tán theo mùa); `GodTrayView` ẩn cả khay bằng `CanvasGroup` khi `Tools.Kind != None` |
| Nút cuộn (§4) | `ScrollButton` | Độ đục theo khoảng cách con trỏ (§6.1) |
| Bản đồ mini (§5) | `MiniMapView` | Một `Texture2D` 144 × 1 cập nhật mỗi 5 giây (màu vùng), cộng một lớp overlay cho khung nhìn và chấm khoảnh khắc. Không cần một GameObject cho mỗi cột |
| Sổ tay (§6), Cài đặt (§9) | `NotebookView`, `SettingsView` | Xem §6.2 |
| Thẻ thông tin (§7) | `InfoCardView` | ✅ M4: Screen Space cạnh con trỏ (một canvas cho cả UI), đọc `WorldView.Hover` |
| Thức dậy / đi ngủ (§8) | `WakeSequence` | Timeline nhỏ bằng code (coroutine), không khoá input |

Văn bản đi qua bảng `Localization` (03 §2). ✅ M4: prefab `Assets/LittleGod/UI/PrototypeUI.prefab` dựng lại bằng *Little God → Build UI prefab* (`UiPrefabBuilder`, cũng chạy trong *Setup Desktop Prototype*); `PrototypeUI` tạo prefab và gọi `Init(WorldView)` cho khay, thẻ, nút cuộn. Chỉnh tay prefab thì đừng chạy lại menu đó.

## 6. Cửa sổ desktop (`LittleGod.Desktop`)

### 6.1 Click xuyên qua & con trỏ
- Giữ `UniWindowController.hitTestType = Raycast` (đang dùng): điểm dưới con trỏ có UI hoặc collider thì cửa sổ nhận click, còn lại thì xuyên qua.
- Vùng nhận click phải **nhỏ** (✅ 01). Collider cây/động vật lấy theo bounds sprite; nút cuộn 16 × 48; khay thu gọn 64 × 22.
- **Rê chuột gần nút cuộn / lên khay** khi con trỏ đang ở vùng xuyên qua: cửa sổ không nhận sự kiện chuột ở đó, nên đọc vị trí con trỏ toàn cục bằng `UniWindowController.GetCursorPosition()` (có sẵn trong gói) rồi đổi sang toạ độ dải.
- ✅ **Tầng cửa sổ (2026-10-24):** trên macOS, UniWindowController bật topmost bằng `NSPopUpMenuWindowLevel` (101), bằng tầng menu chuột phải hệ thống, nên dải che menu ngữ cảnh của Dock. `MacWindowLevel` (Desktop) hạ cửa sổ về `NSFloatingWindowLevel` (3): vẫn trên mọi app thường, nhưng dưới Dock (20; Dock phóng to icon cũng đè lên dải) và dưới mọi menu bật lên. `DesktopStrip` kiểm tra lại mỗi giây vì plugin đặt lại 101 khi gắn lại cửa sổ. Windows: plugin dùng `HWND_TOPMOST`; menu taskbar / jump list là cửa sổ topmost mở sau nên sẽ nằm trên dải, **chưa thử trên máy Windows**.
- ⚠️ Con lăn chuột trên mặt đất / sinh vật vẫn bị cửa sổ game giữ lại (GDD 04 §1, giới hạn đã biết). Không xử lý trong slice; ghi nhận khi chơi thử.

### 6.2 Sổ tay & Cài đặt như "cửa sổ riêng"
GDD 10 §6 muốn sổ tay là một cửa sổ nổi phía trên dải đất. Unity standalone chỉ có **một** cửa sổ.

| Cách | Ưu | Nhược |
|------|----|-------|
| **A · Nới cao cửa sổ dải** khi mở panel (180 → 180 + 340 pt), panel vẽ ở phần trên; phần trống trong suốt và click xuyên qua như bầu trời | Dùng được ngay với UniWindowController (`windowSize`, `windowPosition`); không cần plugin | Lúc nới cao, phần trong suốt phía trên vẫn là cửa sổ "luôn trên cùng" (không sao vì click xuyên qua). Phải đổi kích thước camera / canvas khi nới |
| B · Cửa sổ native thứ hai (plugin) | Đúng nghĩa cửa sổ riêng | Tốn công cho cả macOS và Windows; dựng UI bằng công nghệ khác |

**✅ Quyết định (T2): cách A.** Camera thế giới giữ nguyên ở 180 pt dưới cùng (viewport rect theo pixel). Canvas sổ tay/cài đặt chỉ nằm ở phần nới thêm. Đóng panel thì thu lại 180 pt.

### 6.3 Menu hệ thống & khởi động cùng máy
UniWindowController không có biểu tượng menu bar / system tray và không có autostart.

| Tính năng | macOS | Windows |
|-----------|-------|---------|
| Biểu tượng + menu (GDD 10 §10) | `NSStatusItem` + `NSMenu` (plugin Objective-C `.bundle`) | `Shell_NotifyIcon` + menu chuột phải (plugin C++ `.dll`, hoặc P/Invoke từ C#) |
| Ẩn dải đất (thế giới vẫn chạy) | Ẩn cửa sổ (`orderOut`), giảm fps xuống 1 | `ShowWindow(SW_HIDE)`, giảm fps |
| Khởi động cùng máy (✅ Q14) | `SMAppService.mainApp` (macOS 13+) | Khoá `HKCU\…\Run` |

**✅ Quyết định (T3):** gói thành một plugin `LittleGodNative` với API C# chung (`ITrayIcon`, `IAutostart`), làm ở **mốc M6** (05). Trước đó, nút "Ẩn" trên khay tạm thời thu nhỏ dải còn 8 pt, và nút "Thoát" **vẫn nằm trên khay ở mọi bản build** (nếu chỉ để ở chế độ dev thì bản chơi thử không có cách thoát).

### 6.4 Đa màn hình (✅ Q9)
- Đã có: `DesktopStrip.Fit()` đặt dải ở màn hình **0** và nghe `OnMonitorChanged`.
- Cần thêm: chọn màn hình theo cài đặt (`UniWindowController.GetMonitorRect(i)`, `GetMonitorCount()`). Màn đã chọn bị rút ra thì về màn chính. `ScreenWorkArea.GetBottomInset()` hiện chỉ đọc **màn chính**, cần nhận chỉ số màn hình.
- Đổi độ rộng màn hình thì tính lại `viewWidth` và pool `ColumnView`.

### 6.5 Ngân sách khung hình
- 30 fps khi dải đang hiện (`Application.targetFrameRate`, đã có trong `DesktopStrip`).
- Không có gì chuyển động trong khung nhìn → vẫn 30 fps (con vật luôn động nhẹ). Ẩn tạm → **1 fps** và tắt camera thế giới.
- Ngân sách tổng: **≤ 2% CPU** trung bình (✅ 01), đo theo 05 §4.
