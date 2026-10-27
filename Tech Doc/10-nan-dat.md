# 10 · Nắn đất: ao động, đào / lấp từng ô (GDD 16) → code

> Nguồn: GDD [16 Nắn đất](../GDD/16-nan-dat.md) (✅ Q43–Q49). Chưa có mô hình Python cho ao động: kiểm chứng bằng test luật và test thống kê C#.

## 1. Dữ liệu (`balance.json`)
- `powers.digCost` = 150, `powers.fillCost` = 100 (`PowersBalance.DigCost`, `FillCost`).
- `world.pondWaterColumns` (4) chỉ còn dùng để dựng **ba ao ban đầu** theo bố cục vùng.

## 2. Ao động (`LittleGod.Simulation`)
- `Pond { Index, Start, End }`: một dải cột nước liền nhau (gồm cả hai đầu). `World.Ponds` (trái → phải, `Index` = thứ tự) và `World.PondAt(x)`.
- `RebuildPonds()` chạy lúc dựng thế giới, sau `Restore`, và sau mỗi lần đào / lấp:
  1. dò lại các dải nước;
  2. mỗi động vật ở nước (`Habitat == Water`): `Pond` = ao chứa cột của nó (hoặc ao gần nhất);
  3. mỗi bầy cá: neo ở cột đất thì dời về cột nước gần nhất của ao cũ, `Pond` = ao chứa neo; thành viên ở ao khác thì rời bầy (lần sau tự nhập / lập bầy ở ao của nó).
- `Herd.Pond` thành trường đổi được.
- `UpdateBanks()`: `Column.Bank` tính lại cho mọi cột (đất kề nước).
- Thay mọi chỗ coi "ao = vùng":

| Chỗ | Trước | Sau |
|-----|-------|-----|
| `Bounds(a)`, `HerdBounds(h)` | `Zones[a.Pond].WaterStart..WaterEnd` | `Ponds[a.Pond].Start..End` |
| Cá, diệc tự đến (`Arrivals`) | mỗi vùng ao; khoá `Pond × 100 + vùng` | mỗi ao; khoá `Pond × 100 + ao`. Bèo trong ao; lau, liễu trong ao ± 2 cột; diệc đếm trong ao ± 10 cột |
| `Consider(…, pond)` | vùng ao | `Pond`: cá xuất hiện trong ao, diệc ở bờ trái (`Start − 1`) |
| `WakePonds` | vùng ao chưa sống | ao có cột nước chưa sống, kề đất sống |
| Khám phá Sen, Liễu (`DiscoverRule.PondLivingPlants`) | vùng ao | mỗi ao: bèo trong ao, lau trong ao ± 1 cột |
| Khách Rùa (`MomentDirector`) | `zone.IsPond` | vùng có ≥ 2 cột nước sống |
| Cá nhảy, vị trí vẽ cá (`NatureDecor`, `AnimalView`) | vùng ao | `World.Ponds` |

`Zone.WaterStart/WaterEnd/IsPond` chỉ còn cho bố cục ban đầu và việc hồi sinh vùng cũ.

## 3. Đào / lấp (`World.TryReshape(x)`)
`World.ReshapeAt(x)` trả `Dig`, `Fill` hoặc `None` (kèm lý do: đất hoang, Khu Vườn). `ReshapeCommand(x)` gọi `TryReshape` qua `GameSession.Execute`.

**Đào** (cột đất sống, không phải Vườn), giá `digCost`:
1. Cây trên cả 3 tầng chết: cộng `Detritus` của loài vào cột; bỏ hạt trong đất, giun, hành lang.
2. Thú trên cạn đứng ở cột bước sang cột đất sống kề (ưu tiên bên nhiều đất hơn).
3. Cột thành nước: `Ground = Water`, ẩm 100, biome Ao. `RebuildPonds()`, `UpdateBanks()`, `UpdateDistances()`, `LandChanges++`.
4. Môi trường (GDD 16 §4): ao chứa cột ≥ 2 ô thì cột mới có **Bèo** (cây non); nếu cả ao chưa có bèo thì mọi cột nước trống của ao đều có. Hai cột kề nếu là bờ đất sống, tầng bụi trống thì có **Lau sậy** (cây non). Khám phá Bèo, Lau sậy.
5. Sự kiện `Dug`.

**Lấp** (mọi cột nước), giá `fillCost`:
1. Cây nước chết: cộng `Detritus`.
2. Cá ở cột bơi sang cột nước gần nhất của cùng ao. Ao chỉ còn ô này: cá **rời đi** (bỏ khỏi thế giới, sự kiện `Departed`, không tính chết), diệc trong ao ± 10 cột mà không còn ao nào trong 20 cột cũng rời đi (✅ Q47).
3. Cột thành đất: ẩm 80, biome của cột đất sống kề (không có thì Đồng cỏ); cột nước chưa sống thì thành đất hoang. `RebuildPonds()`, `UpdateBanks()`, `UpdateDistances()`, `LandChanges++`.
4. Sự kiện `Filled`.

Hang thỏ đè lên cột vừa đào: luật "hang chỉ trên đất" (Tech Doc 08 §8) tự dời nhà ở bước kế. Liễu mất bờ: yếu dần theo độ phù hợp (Liễu cần bờ).

## 4. Lưu game
`SaveVersion` 6. `ColumnState.water` (true / false) lưu nền của mọi cột; save v5 trở về trước không có thì lấy theo bố cục vùng. `AnimalState.pond` và `herds[2]` vẫn lưu, nhưng sau khi đọc `RebuildPonds()` tính lại theo vị trí nên save cũ (`pond` = chỉ số vùng) đọc đúng.

## 5. Hiển thị & UI
- **Khay:** biểu tượng khoá thứ ba (⛰️, `LockedPowers` "shape") thành **nút công cụ** khi mở (✅ Q44: mở ngay): thêm `Button` lúc `Init`, không cần dựng lại prefab. Gợi ý: "Nắn đất: đào / lấp từng ô".
- **`ToolController`:** `ToolKind.Shape`, `SelectShape()`. Rê: cột tô xanh nước (sẽ đào), nâu (sẽ lấp), đỏ (không được); thẻ: "Đào ao · 150" / "Lấp ao · 100" / lý do. Click: `ReshapeCommand`; chỉ từng ô (✅ Q49), không kéo.
- **`WorldView`:** `Dug` / `Filled` → `DustPuff` (đào: bụi đất + tia nước; lấp: bụi đất). `Departed` → view con vật mờ đi tại chỗ (như cá bị bắt, không để lại gì).
- `ColumnView` đã vẽ theo `Column.Ground` mỗi khung nên tự đổi ô đất / nước; băng mùa Đông theo cột.

## 6. Kiểm thử
- **Luật (`ReshapeTests`):** đào giữa đồng cỏ → ao mới 1 ô, trừ 150, bờ hai bên; đào kề ao → ao rộng thêm; đào ô ngăn hai ao → nhập; lấp giữa ao → tách hai, cá ở cột lấp bơi sang ô kề; lấp ô cuối → ao mất, cá rời đi (không tính chết); không đào đất hoang / Vườn; thiếu Sinh khí thì không làm; ao 2 ô có bèo, bờ mới có lau; hang trên cột vừa đào dời lên đất; lưu–đọc giữ nền đã đổi.
- **Thống kê:** `WorldStatsTests` giữ nguyên (không đào gì thì thế giới như cũ). Thêm một chạy có đào: đào 6 ô cạnh mỗi ao lúc đầu, chạy tới kết game, kiểm tra cá có nhiều hơn và không lỗi.
- **PlayMode:** công cụ ⛰️ chọn được, đào / lấp qua lệnh, khung hình không lỗi.

## 7. Kết quả (2026-10-27)
- 111 EditMode (+1 Explicit) và 4 PlayMode (+2 Explicit) xanh. Thêm `ReshapeTests` (8 test: ba ao ban đầu; đào ao 1 ô có bờ và lau; đào kề thì rộng ra và có bèo; nhập / tách ao, cá bơi sang ô kề; lấp ô cuối thì cá rời đi, không tính chết; thú trên cạn bước sang bên; không nắn đất hoang / Vườn / thiếu Sinh khí; lưu–đọc giữ nền), `ReshapeSessionTests.DugPond_GrowsDuckweed_AndFishFindIt` (ao 6 ô đào giữa đồng cỏ có bèo, cá tự tìm đến), PlayMode: công cụ ⛰️ đào rồi lấp qua lệnh.
- `WorldStatsTests` (không đào gì) vẫn trong biên: ao động không đổi thế giới khi người chơi không nắn đất.
- `WorldTests` cũ gán cá vào ao bằng chỉ số vùng (`Pond = zone.Index`); đổi sang `PondAt(...).Index` vì `Animal.Pond` giờ là chỉ số ao.
- **Chưa làm:** đo cân bằng khi người chơi đào nhiều (chưa có mô hình Python cho ao động); chưa thử tay công cụ ⛰️ trên bản build.
