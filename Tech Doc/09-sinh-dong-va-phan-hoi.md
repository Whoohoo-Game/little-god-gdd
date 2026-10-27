# 09 · Sinh động, phản hồi & khoảnh khắc rút gọn (GDD 15) → code

> Nguồn: GDD [15 Sinh động & phản hồi](../GDD/15-sinh-dong-va-phan-hoi.md) (✅ Q35–Q42). Tham chiếu tần suất: `Docs/GDD/sim/momentsim.py`.
> Thay phần khoảnh khắc của [04 §4](04-hien-thi-va-ui.md#4-hệ-khoảnh-khắc-littlegodgamemoments) cho bản rút gọn (6 loại). Bản đầy đủ của GDD 09 làm sau.

## 1. Nguyên tắc chung
- **§1 và §2 của GDD 15 chỉ là hình**: nằm trong `LittleGod.Presentation`, chỉ đọc `World`, không ghi gì vào mô phỏng, không lưu. Ngẫu nhiên dùng `UnityEngine.Random` (không đụng `Pcg32` của `World`), nên lưu–đọc và test thống kê không đổi.
- **Khoảnh khắc** (§3) là C# thuần trong `LittleGod.Game` (`MomentDirector`), như 04 §4, để test được. Phần vẽ ở `MomentPresenter` (Presentation).
- **Đơn vị thời gian của khoảnh khắc:** GDD tính bằng phút thật. Code đo bằng **phút mô phỏng ÷ `simMinutesPerRealMinute`**, tức phút thật ở tốc độ ×1. Nhờ vậy khoảnh khắc chạy theo `World.Minute` (tất định, test được), dừng khi tắt app, và tua nhanh ở bản Dev thì khoảnh khắc cũng nhanh theo.
- Hiệu ứng ngắn (lấp lánh, bụi, lá rơi) giữ cách làm hiện có: tạo GameObject rồi tự huỷ, có **trần số lượng** (§5). Sinh vật trang trí sống lâu hơn nên dùng pool.

## 2. Dữ liệu (`balance.json` → `moments`)
Khối `moments` đổi sang số của GDD 15 §3 (đơn vị: phút thật). `momentsim.py` đọc cùng khối này (T1: một nguồn số).

| Khoá | Cũ (GDD 09) | Mới | Dùng cho |
|------|-------------|-----|----------|
| `lifetimeMinutes` | 30 | **8** | Thời gian sống |
| `fadeLastMinutes` | 3 | **2** | Mờ dần cuối đời |
| `retryMinutes` | 120 | **2** | 🌱 bị bỏ qua thì hạt khác tới sau chừng này |
| `newGiftMinGapMinutes` | 10 | **1** | Giãn cách nhóm A |
| `giftMinutes` · `giftMin` | 3 · 5 | **33** · 5 | Quà thường (phút **mô phỏng** thu nhập, GDD 15 §3.6) |
| `newSpeciesGiftMinutes` · `newSpeciesGiftMin` | — | **100** · 10 | Quà vừa (✨ Loài mới) |
| `bigGiftMinutes` · `bigGiftMin` | 20 · 20 | **200** · 20 | Quà lớn (🦋) |
| `birthCooldownMinutes` · `arriveCooldownMinutes` | — | **5** · **5** | Hồi lại mỗi vùng |
| `droughtCooldownMinutes` | — | **30** | 💧 hồi lại mỗi vùng (✅ Q39) |
| `visitorChancePerMinute` | 1/480 | **1/30** | Mỗi vùng đủ điều kiện, mỗi phút thật |
| `visitorMinGapMinutes` | 240 | **12** | Toàn thế giới |
| `visitorDurationMinutes` | 10 | **2** | Khách đi ngang |
| `visitorMinHealth` | — | **60** | Vùng Khoẻ (✅ Q41) |
| `maxInView` · `maxPerZone` | 3 · 1 | 3 · 1 | Giới hạn hiển thị |

`GameBalance.MomentsBalance` thêm các trường mới. Các khoá chỉ dùng cho bản đầy đủ (`overgrazedCooldownMinutes`, `giftSeedGapMinutes`, `overgrazed`) giữ nguyên.

## 3. Khoảnh khắc (`LittleGod.Game`, file `Moments.cs`)

### 3.1 Kiểu dữ liệu
```
enum MomentKind { NewSpecies, Arrival, Birth, Discover, Visitor, Drought }
class Moment { Id, Kind, Zone, Column, SpeciesId, AnimalId, VisitorId, Born (phút mp), Expires (phút mp), Direction }
```
Nhóm A là mọi loại trừ `Drought` (nhóm B).

### 3.2 `MomentDirector`
Tạo trong `GameSession`, gọi sau mỗi `World.Step()` với các sự kiện **của đúng bước đó** (`World.Events` từ chỉ số trước bước tới cuối). `WorldView` vẫn xoá `World.Events` mỗi khung như cũ.

| Nguồn | Cách bắt | Lọc |
|-------|----------|-----|
| ✨ Loài mới | `Discovered` với id là **động vật** | Xếp hàng nếu chưa hết giãn cách. Bám theo con đầu tiên của cặp (`Arrived` cùng bước) |
| ✨ Đến nơi mới | `Arrived` của loài **đã biết từ trước bước này** | Một cặp / ba cá cùng bước, cùng loài, cùng vùng → một khoảnh khắc. Hồi 5 phút mỗi vùng |
| 🐣 Con non | `Born` | Như GDD 09: loài có `Hunter` (Cáo, Diệc), hoặc `First`, hoặc `Count ≤ birthRecoveringMax`, hoặc ong (`SwarmFounded`). Một lứa (cùng bước, cùng loài, cùng cột) → một. Hồi 5 phút mỗi vùng |
| 🌱 Hạt lạ | Mỗi `periodicCheckMinutes`: loài cây chưa khám phá có `DiscoverRule.IsMet` | Chọn cột trống hợp (`CanGrowAt`) gần chỗ đạt điều kiện; không có thì thử lần sau. Xếp hàng nếu chưa hết giãn cách. Bỏ qua (hết hạn) thì chờ `retryMinutes` |
| 🦋 Khách lạ | Mỗi phút thật: từng vùng sống có `Health ≥ visitorMinHealth` | Hươu sao: đồng cỏ, 6h–18h · Cú mèo: rừng, 19h–5h · Rùa đầm: ao, mọi giờ (biome của vùng = biome chiếm nhiều cột đất nhất; vùng ao = ao). Xác suất `visitorChancePerMinute`, cách nhau ≥ `visitorMinGapMinutes`. Sống đúng `visitorDurationMinutes`, đi từ mép này sang mép kia của vùng |
| 💧 Vùng khô | Mỗi 10 phút mp: từng vùng có cột đất sống | Như GDD 09 (`moments.drought`). Hết khi ẩm ≥ 40 hoặc hết `lifetimeMinutes`; sau đó hồi `droughtCooldownMinutes`. Không chịu giãn cách |

- **Giãn cách nhóm A:** khoảnh khắc A mới tới sớm hơn `newGiftMinGapMinutes` sau cái trước thì **bỏ**, trừ ✨ Loài mới và 🌱 (vào hàng đợi, ra khi tới lượt).
- **Hết hạn:** `Expires = Born + lifetimeMinutes × simPerReal`. `Hold(id)` (chuột đang rê trên bong bóng) cộng thêm 1 phút mp mỗi bước, nên thời gian sống dừng lại. Bong bóng bám con vật: con vật chết / rời thế giới thì khoảnh khắc mất.
- **Ngẫu nhiên** (khách lạ, chọn cột cho hạt) dùng `System.Random` riêng của director, seed từ seed thế giới; không đụng `Pcg32` của `World`.
- **Lưu:** chỉ lưu hồi lại (`SaveData.MomentsData.Cooldowns`, khoá `"loại:vùng"` → phút mp) và phút của khoảnh khắc A gần nhất. Khoảnh khắc đang hiện, hàng đợi và khách đang đi **không lưu** (GDD 09 §5.2). Không đổi `SaveVersion`: trường mới tự rỗng khi đọc save cũ.

### 3.3 Nhận khoảnh khắc
`CollectMomentCommand(id)` qua `GameSession.Execute` (như mọi lệnh khác):

| Loại | Kết quả |
|------|---------|
| ✨ Đến nơi mới · 🐣 | `GrantEssence(max(giftMin, EssenceRate × giftMinutes))` |
| ✨ Loài mới | Quà vừa |
| 🦋 | Quà lớn; thêm `VisitorId` vào `Player.MetVisitors` |
| 🌱 | `World.Discover(id)` + `TryPlant(id, cột, free: true)` |
| 💧 | `TryRain(tâm − rainRadius, tâm + rainRadius)` giá thường; thiếu Sinh khí thì lệnh trả false, bong bóng ở lại |

Nhận xong (trừ 💧 thất bại) thì khoảnh khắc biến mất. 💧 thành công cũng biến mất (rồi hồi 30 phút).

### 3.4 Thay phần tạm thời
`WorldView.DiscoverStraySeeds` (tự khám phá cây khi đạt ngưỡng) bỏ đi: 🌱 đi qua khoảnh khắc. `SliceRunner` (test) vẫn tự khám phá như cũ.

### 3.5 Hiển thị (`MomentPresenter`, Presentation)
- Bong bóng là `SpriteRenderer` (pool), sprite pixel 12 × 12 vẽ bằng `PixelSprites` (khung tròn trắng + biểu tượng), ở tỉ lệ thế giới 16 px/đơn vị (tức 2× như GDD). Nổi lên xuống 1 px, chu kỳ 2 giây. Hiện dần 1 giây; mờ 100% → 40% trong `fadeLastMinutes` cuối.
- Vị trí: trên đầu con vật nếu khoảnh khắc bám con vật và view của nó đang có; không thì trên cột của khoảnh khắc. 🌱: hạt nằm trên đất ở cột đó, bong bóng ở trên. 🦋: `VisitorView` đi ngang vùng, bong bóng trên đầu khách.
- Chọn bong bóng: tối đa `maxInView` trong khung nhìn, `maxPerZone` mỗi vùng, theo thứ tự ưu tiên của GDD 15 §3.3; thừa thì ẩn, cái khác mất thì cái bị ẩn hiện lại.
- **Rê chuột:** vùng bắt ≥ 20 × 20 pt (0.625 đơn vị). `WorldView.Hover` thêm `HoverKind.Moment` (`AnimalId` = id khoảnh khắc); thẻ thông tin hiện tên + việc / quà. Presenter gọi `Hold(id)`.
- **Click:** `CollectMomentCommand`. Thành công: lấp lánh, rồi 5 chấm sáng bay về khay thần (góc phải dưới của dải) trong 0.6 giây. 🌱 thì mầm nhú (theo §4.2), 💧 thì mưa (sự kiện `Rain` sẵn có).
- **Chỉ báo ngoài màn hình:** `ScrollButton` tự tạo một `Image` nhỏ (biểu tượng 8 × 8) phía trên mũi tên khi có khoảnh khắc nhóm A/B ở phía đó ngoài khung nhìn, kèm chấm nếu ≥ 2. Bản đồ mini dùng `markers` / `markerTemplate` có sẵn trong prefab: một chấm 2 pt mỗi khoảnh khắc. Không cần dựng lại prefab.

## 4. Phản hồi tức thì (GDD 15 §1, Presentation)

### 4.1 Mưa
- `ColumnView.Bounce(delay)`: cỏ, hoa, bụi co 0.92 rồi dãn 1.04 rồi về 1 trong 0.4 giây, sau `delay` 0–0.3 giây. `WorldView` gọi cho mọi cột trong khung nhìn bị sự kiện `Rain` phủ.
- **Đất ướt:** màu đất đã theo độ ẩm (04 §3). Đổi thang cho đúng GDD: ≥ 60 sẫm hẳn, 40–60 sẫm vừa, < 40 như thường (khô vàng dưới 30 giữ như cũ).
- **Vũng nước:** `Puddle` (sprite 6 × 2 px), 1–2 vũng mỗi 7 cột trên cột đất có tầng Thảm trống, 20 giây co lại rồi mất. Không có mùa Đông.
- **Hồi sức:** `ColumnView` nhớ máu của cây ở lần đọc trước (mỗi 1 giây). Trong 30 giây sau mưa, cây có máu < 100 và máu đang tăng thì bay lên một chấm lá xanh, mỗi cây tối đa 1 chấm mỗi 3 giây; tối đa 8 chấm cùng lúc.
- **Cầu vồng:** `Rainbow` (vòng cung 7 dải màu vẽ bằng code, độ đục ≤ 35%, sau cây). Khi một `RainEffect` tắt lúc 7h–17h, không phải Đông: xác suất 25%, toàn thế giới tối đa 1 lần mỗi 5 phút thật. Hiện 2 giây, giữ 15, mờ 3.

### 4.2 Gieo và cây lớn
- **Mầm nhú:** `ColumnView` nhận ra cây mới (đối tượng `Plant` khác lần trước) khi cột đang được vẽ (không phải lúc `Bind`): cây phóng từ 0 lên cỡ hiện tại trong 0.5 giây, kèm `DustPuff` nhỏ (0.3).
- **Bậc lớn của cây tán:** bậc = `Growth` qua các mốc 0 · 0.2 · 0.4 · 0.6 · 0.8 · 1. Bậc 0–1 (Mầm 2 lá, Cây con) vẽ bằng sprite riêng (`PixelSprites.Sapling(bậc)`) có **cọc và dây buộc**; từ bậc 2 vẽ cây như hiện tại. Lên bậc: nhún 1 → 1.08 → 1 trong 0.4 giây và 3 chấm lá bay lên. Mâm xôi: mốc 0.5 và 1. Hoa dại vừa trưởng thành (nở): nhún và 2 cánh hoa bay lên.
- Cột vừa vào khung nhìn (`Bind`) ghi nhận bậc hiện tại, không diễn.

### 4.3 Đất được lấn
- `ColumnView`: cột vừa có sự sống chuyển màu đất trong **2 giây** (trước 1.5), rồi **lấm tấm chấm sáng** trên ngọn cỏ (mỗi 4–8 giây một chấm) trong **60 giây**. ⚠️ Khác GDD 15 §1.3 ("viền cỏ sáng hơn 15%"): màu của `SpriteRenderer` chỉ nhân được xuống, không làm sprite sáng hơn màu gốc; muốn đúng nghĩa đen phải thêm material cộng sáng.
- Lần đầu một đoạn Rừng ≥ 3 cột (sự kiện `BiomeFormed` của dương xỉ, đọc `World.Regions()`): lấp lánh chạy dọc cả đoạn trong 1.5 giây. Ao thức dậy giữ lấp lánh như hiện tại.

### 4.4 Ong, click con vật
- Ong đang bay trên cột có Hoa dại: mỗi 1.5–3 giây rơi 2–3 chấm phấn vàng.
- Click con vật (không cầm công cụ): `AnimalView.React()`, 1 giây; con đang ngủ chỉ trở mình.

### 4.5 Chưa làm ở vòng này
- **Chấm vàng trên hoa đã thụ phấn:** mô phỏng không theo dõi thụ phấn từng hoa, chỉ có hệ số theo số ong. Làm khi mô phỏng có thông tin đó.
- **Quả chín dần từ xanh sang đỏ:** cần thêm một bộ sprite tán "quả xanh" cho Mâm xôi và Táo dại. Để vòng sau.

## 5. Sinh vật trang trí & hành vi nhỏ (GDD 15 §2, Presentation)

### 5.1 `NatureDecor`
MonoBehaviour do `WorldView` tạo. Mỗi 0.5 giây đọc trạng thái trong khung nhìn ± 4 cột rồi sinh / bỏ sinh vật trang trí theo bảng GDD 15 §2.1. Pool riêng mỗi loại.

| Loại | Lớp | Ghi chú cài đặt |
|------|-----|-----------------|
| Bướm, chuồn chuồn | `Flyer` | Lượn theo nhiễu, đích là hoa / ngọn lau gần nhất; đậu thì đứng yên 3–8 / 4–10 giây. Né con trỏ (< 40 pt = 1.25 đơn vị). Gió đẩy lệch |
| Đom đóm | `Firefly` | Độ đục theo sin, chu kỳ 2–4 giây; sorting trên cây |
| Đàn chim | `BirdFlock` | 3–7 sprite chim 3 × 2 px, bay ngang trời sau cây (sorting giữa trời và cây xa), vỗ cánh đổi 2 sprite |
| Chim sẻ | `Sparrow` | Gắn với một cột cây tán; nhảy giữa các điểm trên tán (lấy từ `PixelSprites.TreeCanopyCenter` × cỡ cây) |
| Cá nhảy | `NatureDecor` gọi `AnimalView.Leap()` cho một con cá đang hiện; vòng sóng `Ripple` |
| Nấm | `Mushroom` | Sinh khi `WorldView` nhận `Starved` / `Died` / `Hunted` trong khung nhìn (sau 20 giây), hoặc cột Rừng mùn ≥ 40 mùa Thu trong 10 phút sau mưa. Sống 3 phút, teo 10 giây |
| Ụ đất giun | `WormMound` | Thay `PeekWorms` cũ (con giun nhú lên mỗi 4–9 giây): ụ đất đùn lên kèm con giun, mỗi 30–60 giây, sống 20 giây |
| Cánh hoa | `FallingLeaf` màu hồng | Táo dại đang có hoa (mùa Xuân) trong khung nhìn |

- **Gió** (`Wind`, static): mỗi 40–90 giây một cơn, hướng ngẫu nhiên, mặt gió chạy 8 cột/giây. `Wind.Bend(x)` trả độ nghiêng 0..1 ở cột x; `ColumnView` xoay cỏ / hoa / dương xỉ / lau tối đa 15°, cây tán 3° (sprite cả cây xoay quanh gốc; 5° trong GDD trông như cây đổ khi cả cây là một sprite). Đông × 1.5; đang mưa thì không có cơn mới.
- **Ngân sách:** trang trí ≤ 24, chấm hiệu ứng ≤ 40 (đếm trong `Effects`, static), thừa thì không sinh.
- **Cài đặt** (GDD 15 §2.5): chưa có màn Cài đặt (M6), nên đọc `PlayerPrefs "littlegod.nature"` (2 Đầy đủ · 1 Ít · 0 Tắt, mặc định 2). Ít: trần còn một nửa, không cầu vồng, không gió. Chưa có nút đổi trong game; đổi bằng `defaults write` / PlayerPrefs cho tới M6.

### 5.2 Hành vi nhỏ (`AnimalView`)
- Trạng thái mới `Idle`: con vật thức, không trốn, không chạy trốn / rượt, đã tới cột (|dx| < 0.02). Chọn động tác theo **trọng số** trong bảng GDD 15 §2.2, chỉ trong các động tác hợp điều kiện, không lặp động tác vừa làm. Động tác 1–3 giây, nghỉ 1.5–4 giây có hoạt ảnh thở (co dãn dọc ±3%, chu kỳ 2 giây). Bắt đầu đi thì cắt động tác.
- Động tác làm bằng **sprite tư thế** nhỏ trong `PixelSprites` (thỏ đứng hai chân, thỏ cúi gặm, thỏ nằm duỗi, thỏ rửa mặt; cáo ngồi, cáo nằm, cáo vươn vai; sóc ngồi; diệc một chân, diệc xoè cánh) cộng biến hình (nghiêng, nhún, co dãn, lật hướng). Không vẽ khung hình chuyển động cho từng động tác ở vòng này.
- Điều kiện đọc từ mô phỏng: cột có cỏ (gặm), độ no ≥ 80 (nằm duỗi), thú săn thức gần trong 12 cột (đứng ngó, quay về phía nó), con non (`!Adult`), mùa Thu (sóc), cột có cây tán (sóc leo), bướm trang trí gần trong 2 cột (cáo con vồ bướm, hỏi `NatureDecor`).
- Cá: "cả bầy quay đầu" dùng một bảng static `herdId → thời điểm quay`; mỗi bầy tối đa 1 lần mỗi 10 giây.
- Con đang ngủ: mỗi 10–20 giây trở mình (lật hướng) hoặc giật tai (co dãn) 0.5 giây.
- **Bộ đếm khoảng lặng** (chỉ Dev): `WorldView.QuietSeconds` = số giây kể từ lần gần nhất có con vật trong khung nhìn bắt đầu động tác hoặc di chuyển; hiện trong dòng dev của khay cùng số trang trí.

## 6. Kiểm thử
- **EditMode (`LittleGod.Game.Tests`, `MomentTests`):** Loài mới tạo khoảnh khắc và được xếp hàng khi chưa hết giãn cách; Đến nơi mới gộp cả cặp; 🐣 lọc đúng (thỏ đông không ra, cáo ra) và hồi 5 phút; 💧 xuất hiện khi khô + cây vàng, tắt khi ẩm ≥ 40, hồi 30 phút; 🦋 chỉ ở vùng Khoẻ và đúng giờ; hết hạn sau 8 phút, `Hold` giữ lại; nhận quà cộng đúng Sinh khí; nhận 🌱 khám phá và gieo miễn phí; 💧 thiếu Sinh khí thì ở lại; lưu–đọc giữ hồi lại.
- **Thống kê:** `MomentTests` chạy 3 seed tới kết game bằng người chơi giả lập của `TestSupport`, kiểm tra trung bình ≥ 1 khoảnh khắc mỗi 4 phút thật (tiêu chí GDD 15 §3.7). `momentsim.py` vẫn là tham chiếu số.
- **PlayMode smoke:** chạy `WorldView` 1 ngày mp ở tốc độ cao không lỗi, số sinh vật trang trí ≤ 24, có ít nhất một bong bóng được tạo.
- **Thử tay:** danh sách GDD 15 §4.

## 7. Kết quả (2026-10-27)
- **Test:** 100 EditMode (+1 Explicit) và 4 PlayMode (+2 Explicit) xanh. Thêm `MomentTests` (10 test: lọc 🐣, gộp lứa, giãn cách và hàng đợi ✨, hồi 5 phút, hết hạn và giữ khi rê chuột, nhận quà, 💧 xuất hiện / thiếu Sinh khí / hết khô / hồi 30 phút, 🌱 khám phá và gieo miễn phí, hồi lại qua lưu–đọc, tần suất), và `Liveliness_DecorBoundedAndMomentsShowAndCollect` (PlayMode).
- `SaveTests.SaveLoadContinue…` giờ so sánh save **trừ khối `moments`**: khoảnh khắc đang hiện / đang chờ không lưu (GDD 09 §5.2) nên thời gian hồi sau khi đọc lại có thể khác; thế giới, người chơi, lịch vẫn phải y hệt.
- **Tần suất** (`MomentTests.Frequency…`, người chơi giả lập của `TestSupport`, không nhặt khoảnh khắc nào, 60 phút thật): 41–50 khoảnh khắc mỗi seed (🌱 18–20 vì hạt bị bỏ qua quay lại sau 2 phút, 💧 10–11, 🐣 5–10, ✨ Đến 3–4, ✨ Loài mới 3, 🦋 1–2). Đạt tiêu chí ≥ 1 mỗi 4 phút.
- **Ảnh** (`CaptureLiveliness`, Explicit, ra `Logs/life-*.png`): cây non có cọc, thỏ gặm cỏ / đứng / nằm, bướm, mưa, cầu vồng. Lần chụp đầu cầu vồng quá to và quá đậm, còn hiện khi trời tối: đổi sprite thành 160 × 80 px không phóng to, độ đục tối đa 0.25, tắt sớm khi sau 17h.
- **Chưa thử tay:** toàn bộ danh sách GDD 15 §4, đặc biệt cảm giác rối / không rối ở mức Đầy đủ, và CPU.

## 8. Sửa sau thử tay (2026-10-27)
- **Rừng phía xa trống giữa cặp cây già:** `ForestBackdrop` cho cây xa chết theo tuổi thọ loài và không bao giờ mọc lại, trong khi cây chính quá tuổi vẫn sống (save thử: ba sồi 58 000–62 000 phút mp, tuổi thọ cây xa 34 560–43 200). Nay mỗi chỗ cây xa có **thế hệ**: `thế hệ = ⌊tuổi / tuổi thọ⌋`, cây non thế hệ sau lớn theo `growMinutes` của loài, hash theo thế hệ để dáng khác cây cũ, hiện dần trong 2% đầu đời. GDD 11 §2.6 đã ghi. Thêm kiểm tra vào `ForestBackdrop_GrowsBetweenClosePairs…`.
- **Cầu vồng kéo sang tối:** thời gian tính bằng giây thật nên ở tốc độ dev ×60 kéo dài vài giờ trong game. Nay `Rainbow` chạy theo `TreeSprite.TimeScale` (tốc độ chơi), chỉ sinh lúc 7h–16h, độ đục nhân với `clamp01(17 − giờ)` nên luôn tắt trước 17h.

## 9. Mây mưa thay bong bóng 💧 (GDD 15 §3.4b, 2026-10-27)
- `balance.json → moments.rainCloud`: `speedColumnsPerRealMinute` 90 (1.5 cột/giây), `drift` 4 (cột thêm mỗi bên vùng khi trôi chờ).
- **Mô phỏng:** `World.TrySpend(cost)` và `World.Drizzle(x)` (cộng `rainAmount` cho một cột đất sống, không sự kiện, không tốn gì).
- **`MomentDirector`:** cột của 💧 lúc chờ = `DroughtColumn(m, phút)`, trôi đều từ `zone.Start − drift` tới `zone.End − 1 + drift` (hoặc ngược lại) trong thời gian sống. Nhận: `TrySpend(rainCost)`, khoảnh khắc thành `RainCloud { Id, X, Direction }` (danh sách `Clouds`, không lưu); mỗi bước mô phỏng mây đi `speed / simPerReal` cột, `Drizzle` mọi cột nó vừa đi qua; ra khỏi `[0, 143]` thì tan. Hồi 30 phút như cũ.
- **Hiển thị:** `MomentPresenter` không vẽ bong bóng cho 💧 (không tính vào giới hạn 3 bong bóng); `CloudView` vẽ mây (sprite 24 × 9 px) ở `Top − 0.55`, vùng bắt chuột theo khung mây. Mây đang mưa: bề ngang 1 → 2.5 và màu trắng → xám trong 1 giây, hạt mưa / tuyết rơi dưới mây tới mặt đất, `WorldView.RainPassed(x)` cho cột vừa được mưa (cây nhún, vũng, hồi sức). Chỉ báo ngoài màn hình và chấm bản đồ mini giữ như cũ.

### 9.1 Mây lan 10 ô (sau thử tay, 2026-10-27)
- `moments.rainCloud.width` = 10 (cột). Mây mưa phủ các cột `[⌊tâm − 5⌋, ⌊tâm + 5⌋ − 1]` (tâm = cột mây + 0.5). Nhận: `Drizzle` cả 10 cột ngay. Mỗi bước: mép trước đi tới đâu thì `Drizzle` các cột mới; mép sau ra khỏi `[0, 143]` thì mây tan.
- `CloudView` đang mưa: 9 cụm (sprite mây 24 × 9 px, không kéo giãn) tản từ tâm ra đều trên 10 đơn vị trong 1 giây, so le cao thấp, màu xám; hạt mưa / tuyết rơi trong suốt bề ngang ±5 đơn vị. Báo `WorldView.RainPassed` cho 10 cột lúc lan ra và cho từng cột mép trước đi qua.

### 9.2 Mây mưa trôi chậm như lúc chờ (sau thử tay, 2026-10-27)
- Bỏ `rainCloud.speedColumnsPerRealMinute`. `RainCloud.Speed` = `MomentDirector.DriftSpeed(m)` = `(zone.Size − 1 + 2 × drift) / thời gian sống (phút mp)`, đúng tốc độ trôi lúc chờ; `CloudView` nội suy bằng chính tốc độ đó.
- Màu mây mưa đậm hơn: (0.38, 0.40, 0.47) thay (0.62, 0.66, 0.72).
- `DroughtCloud_RainsOnEveryColumnOnItsWayToTheEdge` kiểm tra thêm tốc độ bằng tốc độ trôi lúc chờ.

### 9.3 Bản Dev: luôn có mây mưa (2026-10-27)
- Chỉ để thử: mây 💧 hiện ít (cần vùng khô + ≥ 3 cây vàng, hồi 30 phút) nên khó thử. `MomentDirector.AlwaysCloud` (mặc định tắt) bật bởi `WorldView` khi `DevMode.Enabled`: mỗi lần xét 💧 (10 phút mp) mà không có đám mây đang chờ thì tạo một đám ở vùng sống có độ ẩm trung bình thấp nhất, bỏ qua điều kiện cây vàng và thời gian hồi; đám mây này (`Moment.Forced`) không tắt vì đất ẩm, chỉ hết khi hết thời gian sống. Bản thường và test EditMode giữ luật GDD 15. Test: `DevAlwaysCloud_KeepsOneWaitingCloud`.

### 9.4 Mây trôi gấp 5 lần mây nền (sau thử tay, 2026-10-27)
- `rainCloud.columnsPerRealMinute` = 12 (= 5 × mây nền của `SkyView`, 0.04 cột/giây); bỏ `drift`. `MomentDirector.CloudSpeed` = 12 / `simPerReal` cột mỗi phút mp, dùng cho cả mây chờ và mây mưa (`DriftSpeed` trả đúng giá trị này).
- Mây chờ có vị trí riêng `Moment.X`, mỗi bước cộng `CloudSpeed`, luôn trôi sang phải như mây nền (kể cả khi chuột đang rê, xem §9.7). Xuất phát ở `tâm vùng − CloudSpeed × thời gian sống / 2` để bay qua giữa vùng khô đúng nửa đời; ra khỏi bản đồ thì tắt (hồi 30 phút như khi hết hạn).
- Mây nền đếm giây thật, mây 💧 đếm phút mô phỏng: ở ×1 đúng gấp 5; tua nhanh ở bản Dev thì mây 💧 nhanh theo tốc độ chơi.

### 9.5 Mây nhanh hơn, mây chờ sống 10 giây (sau thử tay, 2026-10-27)
- `rainCloud.columnsPerRealMinute` = 60 (25 × mây nền), `rainCloud.lifetimeSeconds` = 10. `MomentDirector.CloudLifetime` = 10 / 60 × `simPerReal` phút mp (17); `Show` dùng nó cho 💧 thay `lifetimeMinutes`. `FadeOf` của 💧 mờ trong 30% cuối đời. Xuất phát ở `tâm vùng − CloudSpeed × CloudLifetime / 2`.
- `AlwaysCloud` (bản Dev) xét mỗi bước thay vì mỗi 10 phút mp, nên mây cũ tan là có đám mới ngay.
- ⚠️ Bản thường: mây chờ sống 10 giây nhưng hồi 30 phút mỗi vùng khi tan; cần xem lại sau khi thử bản thường (GDD 15 §3.4b).

### 9.6 Mây mưa 15 giây rồi co rút (sau thử tay, 2026-10-27)
- `rainCloud.rainSeconds` = 15. `RainCloud.Ends` = phút click + `CloudRainMinutes` (15 / 60 × `simPerReal` = 25 phút mp). `MoveClouds(now)`: tới `Ends` thì bỏ mây (không mưa thêm); mép trước chạm mép bản đồ thì cũng bỏ ngay.
- `CloudView.Vanish()` với mây đang mưa: các cụm dồn về giữa và mờ trong 1 giây (`ShrinkSeconds`), màu đen giữ nguyên, hạt mưa không sinh thêm, mây tự trôi tiếp với vận tốc cũ (mô phỏng đã bỏ nó).
- Ở 1 cột/giây, một lần gọi mây mưa khoảng 25 cột. Test: `DroughtCloud_RainsFifteenSeconds_OncePerColumn_ThenShrinks`; ảnh `Logs/life-cloud-shrink.png`.

### 9.7 Con trỏ không chặn chuyển động (2026-10-27)
- Lỗi thử tay: con trỏ để yên trên đường bay thì mây chờ dừng mãi và giật lùi. Nguyên nhân: luật "rê chuột thì mây dừng" (Claude tự thêm, không có trong yêu cầu) cộng phần vẽ vẫn nội suy tới trước trong lúc mô phỏng giữ nguyên vị trí.
- Sửa: `MomentDirector.Step` luôn cộng `CloudSpeed` cho mây chờ; `Hold` chỉ giữ thời gian sống (GDD 09 §5.1). ✅ Luật chung của người chơi: **con trỏ chuột không được chặn bất cứ chuyển động nào**.

## 10. Bỏ Khách lạ (2026-10-28)
- Người chơi không cần cơ chế này: bỏ `MomentKind.Visitor`, `CheckVisitors` / `VisitorFor` / `VisitorColumn`, vẽ khách (`SyncVisitors`, sprite Hươu sao / Rùa đầm / Cú mèo, bong bóng 🦋), chữ `moment.Visitor`, `visitor.*`, và các khoá `visitor*`, `bigGift*` trong `balance.json → moments`. `momentsim.py` bỏ theo.
- `PlayerData.MetVisitors` (có từ GDD 09) giữ trong save để không đổi định dạng; không còn ai ghi vào.
