# 11 · Hươu và Sói (GDD 17) → code

> Nguồn: GDD [17 Hươu và Sói](../GDD/17-huou-va-soi.md). Tham chiếu: `Docs/GDD/sim/forestsim.py` (dựa trên `huntsim.py`, Tech Doc 08). C# khớp **thống kê**, không cần khớp từng bước.

## 1. Dữ liệu (`balance.json`)
Số đã chốt (GDD 17 §2–§3, bản đã chỉnh) chuyển từ đầu `forestsim.py` vào `balance.json`; `forestsim.py` đọc lại từ đó, không giữ bản sao.

| Mục | Thêm |
|-----|------|
| `biomeModel.animals` | `deer` (ăn cỏ, `diet: plant`, `foodPlant: fern`, `needPerMinute` 0.5) và `wolf` (`diet: prey`, `prey: deer`, `preyFallback: ["squirrel"]`, `preyPerPredator` 5), nối sau Sóc |
| `biomeModel.plants[fern].regrow` | 0 → **0.4** (Q51) |
| `biomeModel.habitat` | `deer`: `fernMin` 8, `canopyMin` 2; `wolf`: `preyMin` 6, `denMin` 3 |
| `biomeModel.arrival` | `presentInTerritory: ["fox", "wolf"]` (Q54, Q56), `loneMinutes` 1440 (Q57) |
| `social` | `species.deer` (bầy ≤ 4), `species.wolf` (đơn độc, theo cặp, `denBiome: "forest"`); `joinLoneHerds: true` (Q55) |
| `hunting` | `prey.deer` (`refuge: "none"`: chạy ra xa, không trốn), `predators.wolf` (`pounce` 0.4) |

- `biomesim.py`: loài trong `biomeModel.animals` không ăn hạt thì dựng bằng `worldsim._animal` (trước đây coi mọi loài ở đó là Sóc). Các mô hình cũ không có luật tự đến cho Hươu, Sói nên không đổi, trừ Dương xỉ mọc lại.
- C#: `AnimalDef.PreyFallback`, `HabitatRule.FernMin / CanopyMin`, `HabitatBalance.Deer / Wolf`, `ArrivalBalance.PresentInTerritory / LoneMinutes`, `SocialBalance.JoinLoneHerds`, `SocialRule.DenBiome`.

## 2. Mô phỏng (`LittleGod.Simulation`)

| Luật | Chỗ | Cách làm |
|------|-----|----------|
| Hươu ăn | `Graze` (đã chung cho `Diet.Grass`) | Gặm `FoodPlant` = Dương xỉ; bầy, chọn bãi, sức chứa theo `regrow` như Thỏ |
| Hươu né Sói | `Alert`, `FleeOrChase` | `Fear` có `refuge: none`: `Refuge()` trả mép xa thú săn, không trốn (`hideMinutes` 0) |
| Sói săn | `HuntChase`, `PreyWithin` | Như Cáo. **Q52:** `AnimalSpecies.PreyFallback`: không có Hươu trong `range` thì `PreyWithin` xét thêm Sóc. Sức chứa và chọn hang chỉ tính Hươu |
| Hang Sói | `FreeDenSite` → `DenOk` | `SocialRule.DenBiome`: hang chỉ ở cột có biome đó (Rừng) |
| Tự đến | `Arrivals` | Hươu: đoạn Rừng, vắng (< 2 trong đoạn), ≥ `fernMin` Dương xỉ sống, ≥ `canopyMin` cây tán, không mùa Đông. Sói: đoạn Rừng, ≥ `preyMin` Hươu trong đoạn + đoạn kề, ≥ `denMin` cây tán, không mùa Đông |
| **Q54** "đã có mặt" | `PredatorPresent(sp, lo, hi)` | Loài trong `presentInTerritory` (Cáo, Sói): đã có mặt nếu còn ≥ 1 con (không tính con "được thả" của Q57) trong [đoạn + đoạn kề] nới thêm `social.territory` mỗi bên. Diệc giữ luật cũ (Q56) |
| **Q57** con lẻ | `UpdateLone()` đầu `Arrivals` | Mỗi 30 phút: Cáo, Sói không có con trưởng thành cùng loài trong `territory` thì `Animal.Alone += 30`, có thì về 0. `Alone ≥ loneMinutes` thì không tính "đã có mặt". Cặp mới có thể nhận hang chỉ có 1 con (luật cặp sẵn có của `ClaimDens`) |
| **Q55** nhập đàn | `JoinLoneHerds()` sau `SplitHerds` | Bầy chỉ còn 1 con: nhập bầy cùng loài (cùng ao với cá) gần nhất còn chỗ (`< groupMax`); con đó `Goal = -1`, tự đi bộ về chỗ bầy mới. Thỏ: hang cũ thành hang bỏ trống |
| Kết game | `AllSpecies` | Thêm `deer`, `wolf` (Q53) |

- `Animal.Alone` lưu trong save (`AnimalState.alone`, mặc định 0): save cũ đọc được, **không** tăng phiên bản save.
- Sói không ngủ trong chỗ trú (như Cáo): giờ thức 15h–9h chỉ là hình (`AnimalView.AwakeHours`).

## 3. Hiển thị (`LittleGod.Presentation`)
- `PixelSprites.Deer()`, `Wolf()` theo tỉ lệ thật (Cáo 14 px ≈ 105 cm): Hươu ~16 px dài, gạc nhỏ; Sói ~16 px, xám. Màu mới trong bảng màu: lông hươu.
- `AnimalView`: chọn sprite; giờ thức (Hươu như Thỏ, Sói như Cáo); hành vi nhỏ: Hươu gặm, vểnh tai, đứng nhìn khi có Sói; Sói như Cáo (liếm, ngáp, đánh hơi, nhìn về phía Hươu), con non chơi. Sói rượt chạy sát đất như Cáo.
- `WorldView`: cảnh vồ (bụi tung, thú săn về hang) nhận cả Sói.
- Chữ: `species.deer`, `species.wolf` (vi, en).

## 4. Kiểm thử
- EditMode: Hươu đến khi đủ Dương xỉ + cây tán; Sói chỉ đến khi đủ Hươu; Sói bắt Sóc chỉ khi vắng Hươu (Q52); Q54 chặn cặp Cáo thứ hai trong lãnh thổ; Q57 con lẻ 1 ngày thì cho cặp mới; Q55 con lẻ nhập bầy gần nhất; hang Sói chỉ trong Rừng; save giữ `Alone`.
- Thống kê (`Slow`): `SliceRunner` 8 seed như `forestsim.py survey 8 tuned`: Hươu có mặt ≥ 90% nửa sau, Sói ≥ 70%, kết game đủ 8 seed.
