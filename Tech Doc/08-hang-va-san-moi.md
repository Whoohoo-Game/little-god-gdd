# 08 · Hang thỏ, né thú săn & rượt bắt (GDD 14) → code

> Nguồn: GDD [14 Hang thỏ, né thú săn & rượt bắt](../GDD/14-hang-tho-va-san-moi.md). Tham chiếu: `Docs/GDD/sim/huntsim.py` (dựa trên `socialsim.py`, Tech Doc 07). C# khớp **thống kê**, không cần khớp từng bước.

## 1. Dữ liệu (`balance.json` → `hunting`)
- `HuntingBalance` (C#) đọc nguyên mục `hunting`: `burrow` (`BurrowRule`), `prey.<id>` (`PreyRule`), `predators.<id>` (`PredatorRule`). Không chép số sang chỗ khác.
- Lúc dựng loài: `AnimalSpecies.Burrow` (loài có hang: Thỏ), `Fear` (con mồi), `Hunter` (thú săn). Loài có hang dùng **bản sao** `SocialRule` với `spread = burrow.spread`, như `huntsim.use_hunting` ghi đè `KIND`.
- Không có mục `hunting` thì `World` chạy đúng luật GDD 13.

## 2. Mô phỏng (`LittleGod.Simulation`, file `WorldHunting.cs`)

| Thành phần | Thay đổi |
|------------|----------|
| `Animal` | `Hidden`, `HideLeft` (trốn), `Alarm` (thú săn gần nhất đang đe doạ, tính lại mỗi bước, không lưu), `Target` (con mồi đang rượt), `ChaseLeft`, `Tired` |
| `Herd` | `HungryMinutes` (phút liên tục một nửa nhà đói). Với loài có hang, `Anchor` **là hang** |
| `World.EmptyBurrows` | Hang bỏ trống `(X, Since)`; sập sau `decayMinutes` |
| `EcoEvent.OtherId` | `Hunted`: id thú săn đã vồ (-1 nếu bắt theo luật cũ) |
| `EcoEventType.Missed` (mới) | Thú săn vồ trượt: `AnimalId` = thú săn, `X` = chỗ vồ |

### 2.1 Thứ tự trong `StepAnimals` (như `huntsim.animals_step`)
1. **`Alert()`** trước mọi thứ: thú săn đói (độ no < 60) ở đầu bước; mỗi con mồi có `Fear` nhận `Alarm` = thú săn gần nhất ăn được nó trong `alertRange`. Con đang trốn: có `Alarm` thì đặt lại `HideLeft`, không có thì đếm lùi, hết thì ra.
2. Ghi hang của các gia đình thỏ (để biết hang nào bỏ trống cuối bước).
3. Như Tech Doc 07 §2.1. Khác:
   - `SteerHerds`: bầy có hang không dời từng cột; `HungryMinutes ≥ relocateAfterMinutes` thì `BestFood` → nếu cách hang ≥ `relocateMin` và có cỏ: hang cũ thành hang bỏ trống, `Anchor = Dig(best)` (dùng lại hang bỏ trống trong `reuseRange`). Cá dời dần như cũ.
   - `Graze`: con đang trốn không ăn, chỉ mất no.
   - `Hunt` của loài có `Hunter` → **`HuntChase`**: mệt thì nghỉ; không đói thì bỏ mồi; luật cặp cuối; giữ mồi cũ nếu còn thấy (không trốn, trong `sight`, còn `ChaseLeft`), không thì chọn con gần nhất; tới được trong phút này (cách ≤ `chaseSpeed` + 1) thì lao tới sát rồi **`Pounce`**: trúng với `pounce × độ hiếm × nơi trú ẩn`, trượt thì `Tired`. Rượt hết `chaseMaxMinutes` thì bỏ và mệt. Diệc bỏ `HomingGoal`.
   - `Move`: con mồi trốn thì đứng yên; có `Alarm` thì chạy `fleeSpeed` về chỗ trú (hang của nhà, cây của sóc, đầu ao xa thú săn nhất với cá), tới nơi thì trốn (trừ cá). Thú săn có `Target` chạy `chaseSpeed` tới sát mồi. Còn lại như 07.
   - `PickGoal` của con mồi có `wary`: tránh đích cách thú săn (ăn được nó) < `wary` cột.
   - `HomeOf`: thỏ đói đi trong `hungrySpread` quanh hang.
   - Tách bầy có hang: bầy mới `Anchor = Dig(site)`.
4. Cuối bước: bầy có hang biến mất (chết hết) → hang bỏ trống; bỏ hang bỏ trống quá `decayMinutes`.

### 2.2 Hiệu năng
`Alert` duyệt con mồi × thú săn đói (≤ 50 × 15) mỗi bước; `HuntChase` chọn mồi trên danh sách loài mồi. Dưới 0.05 ms / bước.

## 2b. Ngủ trong hang (GDD 14 §3b)
- `hunting.sleep.inRefuge` → `AnimalSpecies.SleepHours` (giờ thức `[từ, tới)`); `World.Asleep(a)`: giờ trong ngày (`DayHour(Minute)`) trừ độ lệch `frac(id × 0.618) × lagHours`, ngoài giờ thức thì ngủ. `AnimalView` dùng **cùng** công thức (không còn bảng giờ riêng cho thỏ, sóc).
- `Animal.Sleeping` tính lại đầu bước trong `BeginHunting` (không lưu). Con đang trốn mà đang ngủ thì `HideLeft` đặt lại như bị đe doạ.
- `FleeOrChase`: ngủ mà không bị đe doạ thì đi bộ (`social.speed`) về chỗ trú, tới nơi thì trốn; không có chỗ trú thì đứng tại chỗ.
- Ăn: con trốn mà đang ngủ mất no `starveDrain × sleep.drain`.

## 3. Lưu game
`SaveVersion` 5. `AnimalState` thêm `hid`, `hideLeft`, `target` (id hoặc null), `chaseLeft`, `tired`; `herds` thêm phần tử thứ tư `hungryMinutes`; `WorldState.emptyBurrows`: `[x, phút]`. Save v4 trở về trước: không có trạng thái săn, đọc như mới.

## 4. Hiển thị
- `BurrowView` (pool trong `WorldView`): ụ đất có lỗ tối ở hang của mỗi gia đình thỏ; hang bỏ trống mờ dần theo tuổi, biến mất khi sập.
- `AnimalView`: thỏ trốn thì mờ đi ở hang, thỉnh thoảng hiện đôi tai; sóc trốn thì leo lên cao (thân cây). Con mồi có `Alarm` nhảy cao, nhanh hơn. Thú săn đang rượt chạy sát đất, không nảy.
- Sự kiện `Hunted` có `OtherId`: thú săn **vồ** (nhảy vòng cung tới chỗ mồi), **`DustPuff`** (bụi cỏ, ở ao là tia nước) tung lên che chỗ đó, con mồi biến mất ngay dưới bụi. Cáo tự đi về hang vì mô phỏng đã cho nó no và bỏ `Target`. Không có `OtherId` (thú săn ngoài khung nhìn, luật cũ): giữ cảnh đuổi ra khỏi màn hình.
- `Missed`: thú săn vồ, bụi nhỏ, con mồi chạy tiếp (mô phỏng).

## 5. Kiểm thử
- Luật nhỏ: thỏ thấy cáo đói thì chạy về hang và trốn, đang trốn thì không ăn; cáo đói chạy 4 cột / phút về phía mồi; cáo vồ trúng thì no 100 và có `Hunted` với `OtherId`; vồ trượt thì mệt; nhà đói 60 phút thì dời hang, hang cũ bỏ trống; hang bỏ trống được dùng lại; lưu–đọc giữ trạng thái trốn, rượt, hang bỏ trống.
- Thống kê (`WorldStatsTests`): so với `huntsim.py survey 16` (GDD 14 §6): kết game, số thỏ, chết đói + bị săn, quay đầu < 8.

## 6. Kết quả (2026-10-25)
- 86 EditMode (+1 Explicit) và 3 PlayMode (+1 Explicit) xanh. Thêm `HuntingTests` (7 test); `SocialTests` đổi bầy thỏ dời từng cột thành dời hang; `WorldStatsTests` so với `huntsim.py`.
- `WorldStatsTests` (10 seed, C#) so với `huntsim.py survey 16`:

| Chỉ số | `huntsim.py` | Biên | C# `World` |
|--------|--------------|------|------------|
| Kết game | 16/16, trung vị 1.1 giờ thật (0.7–2.0) | ≥ 7/10, trung vị 0.5–2.5 | 10/10, 0.7–1.4 |
| Thỏ trung bình | 19–49 | 10–50 | 21–54 |
| Bị săn / ngày mp | 33–62 | trung vị 20–90 | 35–59 |
| Chết đói / ngày mp | 26–100 | trung vị 10–80 | 31–97 |
| Quay đầu / con / phút thật | 3.5 | < 8 | 2.6–4.3 |

- Khác dự kiến ban đầu (đã sửa cả GDD 14 §4 và `huntsim.py`): thú săn **lao tới sát và vồ trong cùng một phút** khi cách ≤ `chaseSpeed` + 1. Bản đầu dừng sát mồi rồi phút sau mới vồ: con mồi chạy trước nên không bao giờ bị bắt khi đang chạy, và số lần vồ trúng phụ thuộc thứ tự danh sách động vật.
- Chưa thử tay: cảnh vồ, bụi cỏ, thỏ trốn / nhú lên, sóc leo cây chỉ mới chạy qua PlayMode smoke test, chưa nhìn trên bản build.

## 7. Hang mặt cắt, gia đình 4 con (GDD 14 §2.1, §5, 2026-10-26)
- `balance.json`: `social.species.rabbit` `groupMax` 4, `splitAt` 4, `herdSpacing` 6, **`capLitter`** true (`SocialRule.CapLitter`): lúc sinh, dừng thêm con khi bầy đã đủ `groupMax`. Cá không bật nên giữ như GDD 13.
- `PixelSprites.BurrowSection()`: mặt cắt 30 × 16 px vẽ trong ô đất (thứ tự vẽ 2: trên đất, dưới cỏ / bụi), gốc đặt ở **miệng hang** (giữa cột của hang, mặt đất); đường hầm dốc sang phải xuống buồng ngủ (đáy buồng sâu 15 px). `PixelSprites.BurrowMound()`: ụ đất đào lên, đặt bên trái miệng hang. `WorldView.SyncBurrows` vẽ cả hai; hang bỏ trống mờ theo tuổi.
- `AnimalView`: thỏ có `Hidden` đi tới miệng hang rồi xuống chỗ nằm của nó trong buồng (`WorldView.BurrowSlot`: thứ tự trong `Herd.Members`, 0–3, tâm chỗ nằm ở 8 / 14 / 20 / 26 px của sprite, miệng hang ở 5.5 px, đáy buồng sâu 15 px); vẫn hiện (bỏ "mờ đi, nhú tai"). Ngủ thì cuộn lại và có "z". Hết `Hidden` thì đi ngược lên miệng hang rồi đi như thường.
- Kết quả: 90 EditMode (+1 Explicit) và 3 PlayMode (+1 Explicit) xanh; thêm `Litter_NeverOverfillsTheBurrow`, test tách nhà đổi sang 4 con. Chưa nhìn hang mặt cắt trên bản build.

