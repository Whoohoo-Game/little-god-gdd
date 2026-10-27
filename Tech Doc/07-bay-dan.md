# 07 · Bầy đàn, lãnh thổ & nhịp sinh sản (GDD 13) → code

> Nguồn: GDD [13 Bầy đàn, lãnh thổ & nhịp sinh sản](../GDD/13-bay-dan-va-sinh-san.md). Tham chiếu: `Docs/GDD/sim/socialsim.py` (dựa trên `biomesim.py`). C# phải khớp **thống kê** với nó, không cần khớp từng bước (02 §7).

## 1. Dữ liệu (`balance.json` → `social`)
- Giữ nguyên mục `social` mà `socialsim.py` đọc; `Balance` (C#) đọc thêm `SocialBalance`. Không chép số sang chỗ khác.
- `social.breedSeason`, `social.breedAbove` **thay** `animalRules.breedSeason`, `animalRules.breedAbove` khi có mục `social` (mục cũ giữ cho `worldsim.py` / `biomesim.py`).
- `social.species.<id>` ghi đè bảng loài lúc dựng `AnimalSpecies`: `cooldownMinutes`, `litter`, `minutesPerCatch` (→ `Need`). Phần còn lại là luật xã hội:

| Khoá | Bầy (`herd`) | Đơn độc (`solitary`) |
|------|--------------|----------------------|
| `speed`, `restMin`, `restMax` | ✓ | ✓ |
| `groupMax`, `splitAt`, `spread`, `herdSpacing`, `anchorStepMinutes` | ✓ | |
| `territory`, `denSpacing`, `searchRange`, `avoid`, `pairs` | | ✓ |

- Loài không có trong `social.species` (Ong) đi như cũ. Không có mục `social` thì cả `World` chạy luật cũ.

## 2. Mô phỏng (`LittleGod.Simulation`)

| Thành phần | Thay đổi |
|------------|----------|
| `SocialRule` (mới, `Balance.cs`) | Một dòng của `social.species`; `IsHerd`, `IsSolitary` |
| `AnimalSpecies.Social` | `SocialRule` hoặc `null` |
| `Herd` (mới, `EcoEntities.cs`) | `Id`, `Species`, `Anchor` (cột), `Pond` (-1 trên cạn), `Members` |
| `Animal` | `Goal` (-1: chưa có), `Rest`, `Den` (-1), `Natal` (hang mẹ, -1), `Herd` |
| `World.Herds` | Danh sách bầy, thứ tự tạo |

### 2.1 Thứ tự trong `StepAnimals` (thay 02 §2 bước Animals, như `socialsim.animals_step`)
1. `BuildAnimalIndex()` như cũ.
2. Con bầy chưa có bầy (vừa tự đến, save cũ) → `HerdFor` (nhập bầy cùng loài, cùng ao, `|anchor − x| ≤ 2 × spread`, chưa đầy; không có thì lập bầy mới tại `x`).
3. Mỗi 30 phút: `ClaimDens()` (GDD 13 §3.3; thú săn chọn chỗ nhiều mồi nhất, Sóc chỉ trên Sồi trưởng thành, cáo ghép vào hang có 1 con).
4. `SteerHerds()`: bầy đói một nửa và đang ở gần nhau thì `Anchor` nhích 1 cột về `BestFood` mỗi `anchorStepMinutes`.
5. Từng con: tuổi, nghỉ lứa, ăn / săn như cũ; Diệc đói đặt `Goal` = cá gần nhất; **`Move`** thay `ForageMove` / `HunterMove` / bước ngẫu nhiên của Sóc với loài có `Social`; chết đói / già như cũ; **`MayBreed`** (GDD 13 §4.1), con non nhận `Herd` và `Natal` của mẹ.
6. Lọc con đã chết khỏi bầy, bỏ bầy rỗng, `SplitHerds()`, nối con mới sinh.

- `CapacityRoom` của con có bầy = `HerdRoom` (bãi = anchor ± (spread + range)), GDD 13 §4.2.
- `Move`: trung tâm = anchor (bầy) hoặc `Den` → `Natal` → `X` (đơn độc); đích ngoài bán kính thì chọn lại; lạc ngoài bán kính + 1 thì bỏ nghỉ; tới đích thì nghỉ `restMin..restMax` và chọn đích mới; đi `speed` cột / phút. Chọn đích tránh con cùng loài khác hang trong `avoid` cột (thử 4 lần).

### 2.2 Vai trò theo vùng sống (GDD 13 §5)
`ComputeRegionStats`: sau khi đếm theo chỗ đứng, mỗi con có `Social` góp `Role` của nó vào mọi đoạn mà `[tâm − bán kính, tâm + bán kính]` chạm tới. `Counts` (tỉ trọng, tỉ lệ mồi : săn) không đổi.

### 2.3 Hiệu năng
`ClaimDens` chạy mỗi 30 phút: mỗi con chưa có hang quét ≤ 81 cột × số hang. `BestFood` quét 25 × (2 spread + 1) cột cho mỗi bầy đói mỗi `anchorStepMinutes`. Với ≤ 10 bầy, ≤ 20 con đơn độc thì dưới 0.05 ms / bước, trong ngân sách 05 §4.

## 3. Lưu game (`LittleGod.Game`)
- `SaveVersion` 4. `WorldState.herds`: `[id, loài, anchor, ao]`; `AnimalState` thêm `goal`, `rest`, `den`, `natal`, `herd` (id bầy hoặc null). `nextHerdId` lưu thẳng như `nextAnimalId`.
- Đọc save v1–v3: không có bầy / hang. Bước đầu tiên tự lập bầy, lần `ClaimDens` kế tiếp chia hang. Không cần chuyển đổi.

## 4. Hiển thị (`AnimalView`)
- Mỗi con đứng **lệch trong cột** theo id (±0.3 cột cho thỏ, sóc; ±0.2 cho thú khác; cá không đổi), để bầy không chồng lên một điểm (GDD 13 §7).
- Đi bộ giữ công thức đuổi theo cột hiện tại; vì mô phỏng nay chỉ bước khi có đích, con vật đứng yên khi nghỉ và không còn giật qua lại.

## 5. Kiểm thử
- Luật nhỏ, tất định: thỏ tới đích thì nghỉ (không đổi cột trong lúc nghỉ); bầy dời anchor về phía cỏ khi đói; bầy 8 con không đẻ thêm; bầy tách khi đủ 8 và có bãi trống cách ≥ 8 cột; cáo làm hang, cặp chung hang, chỉ một con trong cặp sinh, cáo không hang không sinh; mùa Đông không sinh; vai trò của cáo tính cho đoạn kề trong lãnh thổ; lưu–đọc giữ bầy, hang.
- Thống kê (`WorldStatsTests`, 10 seed): kết game, số thỏ / cá, số con chết đói trong biên quanh `socialsim.py survey 16` (GDD 13 §6); thêm chỉ số **số lần quay đầu / con / phút thật** ≤ 5 (Python 2.2).

## 6. Kết quả (2026-10-25)
- 79 EditMode (+1 Explicit) và 3 PlayMode (+1 Explicit) xanh. Thêm `SocialTests` (9 test), `Animals_WalkThenRest_NotJitter`; `WorldStatsTests` nay so với `socialsim.py`.
- `WorldStatsTests` (10 seed, C#) so với `socialsim.py survey 16`:

| Chỉ số | `socialsim.py` | Biên | C# `World` |
|--------|----------------|------|------------|
| Kết game | 16/16, trung vị 1.3 giờ thật (0.6–3.2) | ≥ 7/10, trung vị 0.5–2.5 | 10/10, 0.6–1.5, trung vị ~1.2 |
| Quay đầu / con / phút thật | 2.2 | < 5 | 1.7–2.3 |
| Thỏ / cá trung bình | 10–42 / 14–23 | 10–50 / 10–30 | 15–42 / 17–22 |
| Chết đói / ngày mp | 14–68 | 10–80 | 20–61 |
| Chết đói + bị săn / ngày mp | ~106 | < 160 | 77–140 |

- Khác Python: chia thành viên khi tách bầy xếp theo tuổi rồi theo id (Python giữ thứ tự danh sách), để lưu–đọc ra đúng y.
