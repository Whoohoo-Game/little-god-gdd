# 12 · Thời gian thật (GDD 18) → code

> Nguồn: GDD [18 Thời gian thật & nhịp theo lần liếc](../GDD/18-nhip-theo-lan-liec.md) (✅ Q58–Q62). Tham chiếu số: `Docs/GDD/sim/glancesim.py`.
> Trạng thái: ✅ T6 chốt 2026-10-28 (cách A, §1). Đang làm code.

## 1. Hai nhịp: hành vi và sinh thái (✅ T6)
GDD 18 §2.1 giữ nguyên **hành vi** (đi lại, nghỉ, né, trốn, rình, rượt, vồ, ngủ) như người chơi đang thấy, còn **vòng đời** (lớn, già, đói, sinh, chết, đất, nước, Sinh khí) chậm hơn ~6 lần. Hiện cả hai chạy trong một `World.Step()`, mỗi bước là một "phút mô phỏng" = **0.6 giây thật** (×100).

✅ **Cách A:** tách `World.Step()` thành hai phần.

| | **Tick hành vi** | **Bước sinh thái** |
|---|---|---|
| Mỗi | **0.6 giây** thật (100 tick / phút), như hiện tại | **6 tick** = 3.6 giây (16.7 bước / phút) |
| Đếm bằng | `World.Ticks` (mới) | `World.Minute` (giữ tên, nghĩa mới: số bước sinh thái) |
| Chạy | vị trí, đích, nghỉ, bầy đi lại, né, trốn, rình, rượt, vồ, ngủ / thức | thời tiết, tán, đất / nước, cây, đói no, ăn cỏ / hoa / hạt, quả, già, sinh, chết, `Periodic` (tự đến, hang, biome), Sinh khí |
| Số trong `balance.json` | tính theo **tick**, giữ nguyên số hiện tại | tính theo **bước sinh thái**, giữ nguyên số hiện tại (trừ §2) |

- Vì hành vi vẫn 0.6 giây một tick và số không đổi, con vật đi, nghỉ, rượt, trốn **y như bây giờ**.
- Vì mọi luật sinh thái vẫn đếm theo bước và số không đổi, cân bằng của 07–17 giữ nguyên. Chỉ khác: 1 bước nay là 3.6 giây thay vì 0.6 giây. Đây đúng là thứ `glancesim.py` đo (GDD 18 §5: liếc 15 phút kết trung vị 5.1 giờ thật).
- Mùa = **1 000 bước** = 60 phút. Ngày đêm = **1 000 tick** = 10 phút (số `dayNightMinutes` 1000 giữ nguyên, đổi đơn vị sang tick).

Các cách khác đã xét:
- **B · một bước 3.6 giây cho tất cả:** ít sửa nhất, khớp mô hình Python từng bước. Nhưng hành vi chậm ~6 lần (đi 1 cột mỗi 3.6 giây, nghỉ 1–6 phút, một lần rượt tới 54 giây), trái GDD 18 §2.1.
- **C · một bước 3.6 giây, đổi số hành vi** (tốc độ ×6, thời gian ÷6): con vật nhảy tới 6 cột mỗi bước, số lần vồ / né mỗi lần rượt giảm, làm lệch luật săn của 14.

⚠️ **Khác mô hình Python ở (A):** Python chạy hành vi **một lần** mỗi bước sinh thái, C# chạy **6 lần**. Thú săn có 6 cơ hội rượt / vồ mỗi bước. Lượng mồi bị bắt vẫn bị chặn bởi độ đói (cáo no 15 giờ mp sau mỗi mồi, Tech Doc 08), nhưng có thể nhiều hơn. Thỏ trốn ngắn hơn một bước nên ăn cỏ nhiều hơn. Đo ở §6; nếu lệch thì thêm tick hành vi vào `glancesim.py` để đo lại trước khi chỉnh số.

## 2. Dữ liệu (`balance.json`)
| Mục | Hiện tại | Mới |
|-----|----------|-----|
| `time.simMinutesPerRealMinute` 100 | | **bỏ**; thay bằng `time.ticksPerRealMinute` **100** và `time.ticksPerStep` **6** |
| `time.seasonMinutes` | 3000 | **1000** (bước) = 60 phút (✅ GDD 18 §2.2) |
| `time.dayNightMinutes` | 1000 (phút mp) | 1000, nay là **tick** = 10 phút |
| `growMinutes` tầng Thảm / Bụi (Q58: lớn nhanh ×3) | Cỏ 20 · Hoa dại 40 · Bèo 20 · Dương xỉ 30 · Lau sậy 90 · Mâm xôi 120 · Sen 180 | **7 · 13 · 7 · 10 · 30 · 40 · 60** |
| `moments.lifetimeMinutes` · `fadeLastMinutes` | 8 · 2 | **30 · 5** (Q60) |
| `biomeModel.arrival.newSpeciesGapMinutes` | — | **15** (phút thật, Q59) |
| Mọi số khác | | giữ nguyên |

Phân loại số (để đọc đúng đơn vị):
- **Tick:** `social.species.*.speed`, `restMin` / `restMax`; `hunting.prey.*.fleeSpeed`, `hideMinutes`; `hunting.predators.*.chaseSpeed`, `chaseMaxMinutes`, `tiredMinutes`, `stalkSpeed`; `time.dayNightMinutes`.
- **Phút thật:** `moments.*` (như trước), `restEssence.*`, `biomeModel.arrival.newSpeciesGapMinutes`.
- **Bước sinh thái:** mọi số thời gian còn lại (`social.species.*.anchorStepMinutes` vì bầy chọn chỗ ở phần sinh thái, `moments.giftMinutes` / `newSpeciesGiftMinutes` là số bước thu nhập, `growMinutes`, `lifeMinutes`, `matureMinutes`, `cooldownMinutes`, `minutesPerCatch`, `needPerMinute`, `seedsPerHour`, `rainChancePerHour`, `arrival.afterMinutes`, `loneMinutes`, `burrow.relocateAfterMinutes`, `decayMinutes`, `periodicCheckMinutes`, `seedbankSproutMinutes`, `modelPlayer.visitMinutes`…).

Mỗi khối trong `balance.json` thêm một dòng `_about` ghi đơn vị. Test đồng bộ `balance.json` (Tech Doc 03 §1) giữ nguyên.

## 3. Mô phỏng (`LittleGod.Simulation`)

### 3.1 `World`
- `public int Ticks` (mới): số tick đã chạy. `Minute` giữ nghĩa số bước sinh thái (mọi tuổi, hồi, đồng hồ chờ đang đếm theo nó).
- `public void Tick()` (mới, một tick):
  ```
  live = Ticks % ticksPerStep == 0
  if (live) Weather, Canopy, Environment, StepPlants
  StepAnimals(season, live)               // hành vi mỗi tick, phần sinh thái khi live
  if (live) Periodic (mỗi 30 bước), Sinh khí, Minute++
  Ticks++
  ```
- `public void Step()` giữ cho test và `SliceRunner`: chạy đủ `ticksPerStep` tick (= một bước sinh thái). Test đang gọi `Step()` N lần vẫn hiểu là N bước.
- `Season`, `SeasonAt`: theo `Minute` và `seasonMinutes` mới, không đổi code.
- `DayHour`: tính theo `Ticks` (ngày đêm 1 000 tick). `Asleep()` (thỏ, sóc ngủ trong chỗ trú) đọc `DayHour(Ticks)`.

### 3.2 Tách `StepAnimals`
| Phần | Đi vào | Ghi chú |
|------|--------|---------|
| `BeginHunting` / `EndHunting` (cảnh giác, né, trốn, `HideLeft`) | `Behave` | |
| `Move` (đi tới đích, `Rest`, né / trốn / rượt qua `FleeOrChase`), `HomingGoal` | `Behave` | |
| Nhập bầy cho con chưa có bầy | cả hai | Mỗi tick, để con vừa tự đến có chỗ về ngay |
| `HuntChase`: `Tired`, chọn mồi, rình, rượt, `ChaseLeft`, `Pounce` | `Behave` | Vồ trúng thì cộng no và ghi sự kiện ngay trong tick |
| `HuntChase`: trừ đói `100 × Need` mỗi bước, ăn quả | `Live` | Tách khỏi phần rượt |
| `SteerHerds` (bầy dời chỗ, hang dời khi đói), `Graze`, `Hunt` (thú săn chưa có luật rượt), `ForageMove` / `HunterMove` / sóc đi lại của loài không có luật xã hội, ong / sóc no đói, `Age++`, `Cooldown`, chết đói / già, sinh sản, `ClaimDens`, chia / nhập bầy (`SplitHerds`, `JoinLoneHerds`) | `Live` | |
| `BuildAnimalIndex` | cả hai | Gọi đầu mỗi tick (Behave cần vị trí mới) |

Trong code không tách thành hai hàm: `StepAnimals(s, live)` chạy phần hành vi mỗi tick và bọc phần sinh thái trong `if (live)`, để giữ thứ tự cũ trong một bước. Tick đầu của bước chạy cả hai, 5 tick sau chỉ hành vi. Một bước của mô hình Python tương ứng với `Live` + một lần `Behave`.

### 3.3 Luật nhịp loài mới (Q59)
`Arrivals`: một loài chưa có trong `Arrived` chỉ được đến khi `Minute − lastNewSpeciesMinute ≥ newSpeciesGapMinutes × stepsPerRealMinute` (15 phút = 250 bước). Chưa tới lượt thì không đến và đồng hồ chờ của cặp đó về 0, như `glancesim.GlanceWorld.arrive`. `lastNewSpeciesMinute` lưu trong save.

## 4. Phiên chơi, khoảnh khắc, hiển thị

### 4.1 `GameSession`
- `Advance(realSeconds, speed, maxSteps)`: cộng dồn `realSeconds × speed × ticksPerRealMinute` giây-tick rồi gọi `TickOnce()` cho mỗi tick. `maxSteps` tính theo tick. `StepOnce()` giữ cho test và công cụ dev: chạy đủ một bước sinh thái. `MinuteFraction` đổi tên `TickFraction`. Tốc độ dev ×1 / ×10 / ×60 không đổi.
- Báo `SeasonChanged` sau tick có bước sinh thái làm đổi mùa.
- Sinh khí nghỉ ngơi: `EssenceRate() × stepsPerRealMinute × phút` (thay `× simPerReal`), `stepsPerRealMinute = ticksPerRealMinute / ticksPerStep` = 16.7.

### 4.2 `MomentDirector` (Moments.cs)
Mọi thời gian của khoảnh khắc là **phút thật**, nên Director đếm theo **`World.Tick`** thay vì `World.Minute`: `perReal = ticksPerRealMinute` (100, như số cũ). Nhờ vậy `Minutes(real)`, mây 💧 (10 giây chờ, 15 giây mưa, tốc độ cột / phút thật) **giữ nguyên code**, chỉ đổi nguồn phút. `Director.Step` gọi mỗi tick; kiểm tra vùng khô đọc trạng thái thế giới nên gọi tick nào cũng đúng.

### 4.3 Hiển thị và UI
Thay `SimMinutesPerRealMinute` ở mọi chỗ (16 chỗ đọc `World.Minute` trong Presentation / UI cần xem từng chỗ):
- Chỗ đo **thời gian thật** (cầu vồng 5 phút trong `WorldView.RainEnded`, `MomentPresenter` tốc độ mây, `InfoCardView` dòng dev "còn x phút", `NatureDecor` cửa sổ bình minh / chạng vạng) → đọc `World.Tick` và `ticksPerRealMinute`.
- Chỗ đo **mùa / tuổi / lớn** (`NatureDecor` độ dài mùa, `ColumnView` bậc lớn, `TreeSprite`, tuyết phủ / tan) → giữ `World.Minute`.
- `AnimalView` nội suy tới cột mô phỏng như cũ: vị trí vẫn đổi mỗi 0.6 giây nên đi lại không đổi.
- Cây lớn chậm hơn nên `ColumnView` thấy `Growth` đổi mỗi 3.6 giây; bậc lớn của cây tán (GDD 15 §1.2) nay ~17 phút một bậc, không cần sửa code.

## 5. Lưu game: save v7
- `WorldState.tick` (mới), `WorldState.lastNewSpeciesMinute` (mới).
- Đọc save v6: `tick = minute` (ở ×100 một phút mô phỏng là 0.6 giây, đúng bằng một tick, nên giờ trong ngày liền mạch); `minute` giữ nguyên nên tuổi, hồi, đồng hồ chờ giữ nguyên. Mùa tính lại theo 1 000 bước nên có thể **nhảy mùa** khi mở save cũ. Chấp nhận vì mới chỉ có save thử.
- Test đọc save cũ: thêm fixture v6 → v7.

## 6. Kiểm thử
| Test | Nội dung |
|------|----------|
| `TimeTests` (mới) | 100 tick / phút thật, 6 tick / bước; `Step()` = 6 tick; mùa đổi sau 1 000 bước = 60 phút thật; ngày đêm 1 000 tick = 10 phút thật |
| `Behave_KeepsRealTimeSpeeds` | Thỏ đi tới đích với `speed` cột / tick: 10 tick (6 giây) đi được như 10 bước cũ |
| `Live_RunsEverySixthTick` | Tuổi, đói, cây lớn chỉ đổi ở tick chia hết cho 6 |
| `NewSpeciesGap` (Q59) | Hai loài đủ điều kiện cùng lúc: loài thứ hai đến sau ≥ 250 bước |
| `Moments_LiveThirtyRealMinutes` (Q60) | Bong bóng ✨ còn sau 29 phút thật, mất sau 30 |
| Save v6 → v7 | Đọc được; `tick = minute`; lưu–đọc v7 ra y |
| Sửa test cũ | Test luật từng tình huống (`WorldTests`, `SocialTests`, `HuntingTests`, `ForestTests`) dùng `SliceRunner.RuleBalance()`: `ticksPerStep` = 1, mỗi `Step()` là một lần sinh thái + một lần hành vi như mô hình Python; đặt giờ bằng cả `Minute` và `Ticks`. `CalendarTests` (mùa 1 000 bước = 60 phút, Sinh khí nghỉ ngơi × 16.7), `MomentTests` (đếm tick, sống 30 phút). `SliceRunner`: chạy theo tick, mọi cây mở sẵn, người chơi ghé đúng nhịp `playerEvery`, giờ thật = bước ÷ 16.7 |
| **So với `glancesim.py`** (`WorldStatsTests`, Slow, 10 seed) | `SliceRunner` với người chơi mô hình liếc mỗi 250 bước (= 15 phút thật), như `glancesim.py survey 16 every=15` (kết 16/16, trung vị **5.1 giờ** thật, 4.5–7.0; đói 14 / săn 19 con mỗi 1 440 bước): kết trong khoảng tương đương; mọi loài có mặt; **bị săn / ngày** trong ±50% (⚠️ §1). Lệch thì dừng lại báo, không tự chỉnh số |

## 7. Python (`Docs/GDD/sim`)
- `worldsim.SIM_PER_REAL` = `ticksPerRealMinute / ticksPerStep` (16.7, số thực): các mô hình cũ in "giờ thật" theo nhịp mới. Số đã ghi trong GDD 07–17 là của ×100, giữ nguyên làm lịch sử.
- `glancesim.py`: mặc định đọc nhịp, mùa, `growMinutes` từ `balance.json` mới; bỏ `pgrow`, `season`, `day` khỏi mặc định (vẫn giữ để thử).
- Chưa có tick hành vi trong Python (§1 ⚠️).

## 8. Việc làm
1. `balance.json` + `Balance.cs` (§2), Python đọc lại (§7), test đồng bộ xanh.
2. `World.Tick()`, tách `StepAnimals` (§3.1–3.2), `Step()` = 6 tick. Test cũ xanh với số mới.
3. Luật nhịp loài mới (§3.3).
4. `GameSession`, `MomentDirector`, hiển thị (§4).
5. Save v7 (§5).
6. So `SliceRunner` với `glancesim.py` (§6), ghi kết quả vào §9.
7. Build macOS Dev, thử tay: con vật đi / rượt / trốn như trước; gieo cỏ thấy lớn trong ~25 giây; mùa đổi sau 1 giờ.

## 9. Kết quả (2026-10-28)
Code xong theo §8 bước 1–5. Đo `WorldStatsTests` (10 seed, người chơi mô hình liếc mỗi 250 bước = 15 phút thật) so với `glancesim.py survey 16 every=15`:

| | C# | Python | |
|---|---|---|---|
| Kết game: trung vị (ngắn – dài) | **5.3 giờ** (4.8–7.0), 10/10 | 5.1 giờ (4.5–7.0), 16/16 | ✅ |
| Đất hoang phủ kín | 2.8 giờ (2.5–4.2) | 2.5 giờ (2.2–4.1) | ✅ |
| Loài đến (trung vị) | Ong 0.4 · Cá 0.9 · Thỏ 1.0 · Diệc 1.5 · Hươu 1.7 · Cáo 2.0 · Sói 2.6 · Giun 4.4 · Sóc 4.8 giờ | Ong 0.4 · Cá 0.7 · Thỏ 1.0 · Diệc 1.6 · Hươu 1.6 · Cáo 1.8 · Sói 2.6 · Giun 4.5 · Sóc 4.7 giờ | ✅ |
| Chết đói / 1 440 bước | ~12 | ~14 | ✅ |
| **Bị săn / 1 440 bước** | **~35** (30–56) | ~19 (12–26) | ⚠️ +85%, ngoài ±50% |
| Sói có mặt (nửa sau) | 100% ở 7/10 seed, còn lại 32–69% | | |

- ⚠️ Bị săn nhiều hơn đúng như §1 đã lường: hành vi chạy 6 lần mỗi bước sinh thái nên thú săn có 6 lần rượt / vồ. Quần thể vẫn đứng (thỏ trung bình 16–29, mọi loài có mặt, kết game như Python). Theo §6 **chưa chỉnh số**, chờ quyết định.
- Ngân sách: ~1.1 ms mỗi bước sinh thái (6 tick) ≈ 18 ms mỗi phút thật, dưới 50 ms (0.5 ms × 100 bước của ×100). Test ngân sách đổi sang tính theo phút thật.
- Test luật từng tình huống chạy với `ticksPerStep` = 1 và không giãn loài mới (`SliceRunner.RuleBalance()`); nhịp tick và luật Q59 kiểm ở `TimeTests`.
- Lỗi đo đã sửa: người chơi mô hình của `biomesim.py` / `SliceRunner` chỉ ghé ở bước kiểm tra định kỳ (mỗi 30 bước). `glancesim.py` và `SliceRunner` nay ghé đúng nhịp (GDD 18 §5).
