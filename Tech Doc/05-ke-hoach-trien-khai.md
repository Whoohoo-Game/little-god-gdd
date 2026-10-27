# 05 · Kế hoạch triển khai & kiểm thử (vertical slice)

## 1. Các mốc
Mỗi mốc kết thúc bằng một bản chạy được, test xanh, và cập nhật GDD / Technical Doc nếu có gì làm khác dự định.

| Mốc | Nội dung | Xong khi | Phụ thuộc |
|-----|----------|----------|-----------|
| ✅ **M0 · Nền móng** (xong 2026-10-24) | Tách assembly theo 01 §2; `balance.json` + `worldsim.py` đọc từ đó (T1); PRNG lưu được; define `LITTLEGOD_DEV`; đưa `essenceMultiplier` / `unlimitedEssence` về 1 / false ngoài dev | `worldsim.py survey` ra **đúng y** số cũ khi đọc từ JSON; project build được; test cũ vẫn xanh | — (✅ T1 đã chốt) |
| ✅ **M1 · Mô phỏng slice** (xong 2026-10-24) | `World` 144 cột theo 02: vùng, nền nước, 12 loài, đoạn biome, Sinh khí theo đoạn, Sức khoẻ, hồi sinh có giảm giá, chết đói, tự tìm đến theo đoạn, ong chia đàn, diệc bay về mồi; `ScriptedPlayer` mới bắt chước `worldsim.visit()` | Bộ test thống kê §3.2 xanh; test hiệu năng §4 đạt | M0 |
| ✅ **M2 · Thế giới hiển thị** (xong 2026-10-24, trừ đo CPU) | Camera cố định + `ViewportController`; pool `ColumnView` / `AnimalView`; nút cuộn; Ao, đất hoang, mùa nội suy; hiệu ứng `Starved`, `Hunted`, `Arrived`, `ZoneRevived` | Cuộn mượt qua cả 144 cột; số GameObject không tăng theo kích thước thế giới; CPU trong ngân sách §4 | M1 |
| ✅ **M3 · Phiên chơi & lưu game** (xong 2026-10-24) | `GameSession`, lệnh (01 §3), lịch & mùa theo ngày thật, Sinh khí nghỉ ngơi, lưu/đọc an toàn (03) | Test lịch §3.3 và test lưu–đọc tất định xanh; tắt/mở app giữ đúng trạng thái và vị trí khung nhìn | M1 |
| ✅ **M4 · Khay, công cụ, bản đồ, thẻ** (code xong 2026-10-24, chờ thử tay) | GDD 10 §3–5, §7; chuyển UI sang prefab uGUI (T4); bảng Localization vi/en; phông có dấu | Làm được mọi thao tác của slice không cần nút dev; danh sách kiểm GDD 10 §13 (khay, nút cuộn, mưa kéo) đã thử | M2, M3 |
| ✅ **M4b · Nhịp ×100 & tầng tán** (xong 2026-10-24) | GDD 11: đồng hồ ×100, mùa theo `World.Minute`, Sinh khí nghỉ ngơi trần 10 phút thật, save v2; tầng 2 (Sồi, Táo dại, Liễu) trong `World` + `SliceRunner`; quả theo `fruitEaters`; khám phá cây tán; `ColumnView` vẽ cây tán; nền trời, đất 36 pt | Test thống kê §3.2 theo số mới của `worldsim.py` xanh; save v1 vẫn đọc được; build macOS | M4 |
| ✅ **M4c · Môi trường sống** (xong 2026-10-24) | GDD 12, Tech Doc 06: biome theo cột, cỏ phủ lấn đất hoang, hệ số biome, hành lang, động vật tự đến theo điều kiện sống, Dương xỉ, Sóc, kết game mới; bỏ mời, hồi sinh; save v3; UI bỏ 💌 / 🌿, bản đồ theo biome | Test luật + thống kê khớp `biomesim.py` xanh; save v1, v2 đọc được; build macOS | M4b |
| **M5 · Khoảnh khắc** | `MomentDirector` + `MomentPresenter` đủ 9 loại (GDD 09), chỉ báo ngoài màn hình, chế độ theo dõi; hồi sinh và đặt tên vùng đi qua 🌿 / 🏷️ | Test khoảnh khắc §3.4 xanh, gồm tiêu chí tần suất của GDD 09 §9 | M4 |
| **M6 · Sổ tay, cài đặt, desktop** | Sổ tay 3 tab và Cài đặt bằng cách nới cửa sổ (T2); thức dậy / đi ngủ (GDD 10 §8); chọn màn hình; plugin native tray + autostart (T3); ambient cơ bản | Chạy trên macOS (Apple Silicon + Intel) và Windows 10/11; danh sách kiểm desktop §3.6 đạt | M4, M5 |
| **M7 · Bản chơi thử** | Log chơi thử (§5); build "Playtest" cho cả hai nền tảng; hướng dẫn cài cho người thử | 3–5 người chạy ≥ 5 ngày lịch; thu log; viết báo cáo so với mục tiêu GDD 08 §1, 09 §1 | M6 |

M2 và M3 làm song song được, vì chỉ cùng phụ thuộc M1.

## 2. Thứ tự port luật trong M1
Làm theo thứ tự để mỗi bước có test riêng trước khi chồng bước sau:
1. Cấu trúc vùng, `AliveSpan`, đất hoang, nền nước, khuếch tán trong dải sống. Chạy lại **1 đồng cỏ 48 cột** (Khởi Nguyên) với luật mới, so với `worldsim.py` ở cùng cấu hình.
2. Sức chứa ×1.0 + chết đói.
3. Tự tìm đến theo đoạn biome (gồm luật đoạn kề cho thú săn) + giun lan.
4. Loài Ao: Bèo, Sen, Lau sậy, Cá (theo ao), Diệc (bay về mồi).
5. Ong chia đàn.
6. Đoạn biome, Sinh khí theo đoạn, vai trò mượn, Sức khoẻ.
7. Hồi sinh: giá, giảm giá, mầm khởi đầu, khám phá Bèo/Lau sậy ở ao đầu tiên, điều kiện Vườn.

## 3. Kiểm thử

### 3.1 Loại test
| Loại | Công cụ | Chạy khi |
|------|---------|----------|
| Đơn vị (luật, lịch, khoảnh khắc) | EditMode, NUnit | Mỗi lần commit |
| Thống kê so với `worldsim.py` | EditMode, nhãn `[Category("Slow")]` | Trước khi merge vào nhánh chính; khi đổi `balance.json` |
| Hiệu năng | `Unity.PerformanceTesting` | Mỗi mốc |
| Khói (scene chính chạy 1 ngày mô phỏng ở ×600, không lỗi, số view có giới hạn) | PlayMode | Mỗi mốc |
| Thủ công trên máy thật | Danh sách kiểm §3.6 | M4, M6, M7 |

### 3.2 Thống kê mô phỏng (M1)
10 seed, app mở 8h/ngày, người chơi giả lập gọi mưa và mời đủ loài (giống `worldsim.py survey`). Biên chấp nhận rộng hơn kết quả Python, vì C# và Python không cùng chuỗi số ngẫu nhiên.

| Chỉ số | `worldsim.py` (GDD 08 §10) | Biên cho C# |
|--------|----------------------------|-------------|
| Ngày lịch kết game (trung vị) | 16.8 | 14 – 20 |
| Vùng thứ 9 hồi sinh (trung vị, giờ mở app) | 97 | 80 – 120 |
| Chết đói / ngày lịch, có thú săn | ~7.5 | 3 – 12 |
| Thời gian bị ăn trụi, có thú săn | ~64% | 45% – 80% |
| Có thú săn kết sớm hơn không thú săn | 18% | ≥ 8% |
| 13/13 vùng cùng lúc Cân bằng | 10/10 seed | 10/10 seed |
| Giờ không có con thỏ nào (người chơi chăm) | ≤ 2 | ≤ 6 |
| Cá trung bình trên 3 ao | 15–20 | 8 – 30 |

↻ **M4b (2026-10-24):** nhịp ×100, mùa 2 880 phút mô phỏng, người chơi giả lập ghé mỗi 300 phút mô phỏng (3 phút thật), có cây tán (GDD 11 §1.4). Biên mới cho `WorldStatsTests`, 10 seed:

| Chỉ số | `worldsim.py` (8 seed) | Biên cho C# | C# `World` (10 seed) |
|--------|------------------------|-------------|----------------------|
| Giờ thật tới kết game (trung vị) | 1.4 (1.2–2.1) | 1.0 – 2.5 | 1.2 (1.15–1.5) |
| Vùng thứ 9 (giờ mô phỏng) | 80–115 | 70 – 140 | 70–125 |
| Chết đói / ngày mô phỏng | 18–32 | 10 – 40 | 17–28 |
| Thời gian bị ăn trụi | 63–76% | 45% – 85% | 63–78% |
| Có thú săn kết sớm hơn | ~14% | ≥ 3% | ~21% (1.20 so với 1.45 giờ) |
| 13/13 vùng cùng lúc Cân bằng | 8/8 seed | 10/10 seed | 10/10 (đo mỗi 30 phút) |
| Cây tán lúc kết game | ~20 (gồm cây non) | ≥ 10, ≥ 3 trưởng thành | 23–25 |

Test luật mới (tất định): tán phủ 3 cột và che tầng dưới còn 55, mùa Đông không che; dưới tán giữ ẩm hơn, mùa Thu lá rụng gốc ± 2; giữa hai gốc cây tán trống ít nhất 1 ô (trước: > 2 cột); Liễu chỉ mọc ở bờ ao; Táo dại cho thỏ đói +0.3 no/phút mùa Hạ. Lịch: 1 phút thật = 100 bước; mùa đổi mỗi 2 880 bước; tuyết tan đầu Xuân; Sinh khí nghỉ ngơi tối đa 10 phút thật.

Thêm các test luật nhỏ, tất định:
- Cột nước giữ ẩm 100.
- Cây cạn không mọc trên nước.
- Chết đói để lại Mùn.
- Cáo không ăn cá.
- Diệc không bị coi là "vắng" khi đang ở đoạn kề.
- Giá hồi sinh giảm đúng công thức.
- Vườn chỉ mở khi 13 vùng cùng lúc Cân bằng.
- Hạt rơi ngoài dải sống thì mất.

**Kết quả M1 (2026-10-24):** `WorldStatsTests` đạt mọi biên ở trên. 10 seed, trung vị, so với `worldsim.py`:

| Chỉ số | C# `World` | `worldsim.py` |
|--------|------------|---------------|
| Ngày lịch kết game | 17.25 | 16.8 |
| Vùng thứ 9 (giờ mở app) | 102 | 97 |
| Chết đói / ngày lịch | ~8.6 | ~7.5 |
| Thời gian bị ăn trụi | ~68% | ~64% |
| Không thú săn: ngày kết | 19.1 | 19.8 |
| 13/13 vùng Cân bằng · giờ không có thỏ | 10/10 seed · 0 | 10/10 · ≤ 2 |

Một bước mất **0.137 ms** trên thế giới đã hồi sinh hết (90 động vật lúc đo; chưa thử mức 250 con).

**Kết quả M2 (2026-10-24):** PlayMode smoke test `WorldViewSmokeTests` cho thấy: sau 12 ngày mô phỏng với 9 vùng đã hồi sinh và 55 động vật, khung nhìn 47 cột cuộn khắp 144 cột mà chỉ cần **65 `ColumnView`** và **74 `AnimalView`**, không có exception. **Chưa đo** ngân sách CPU §4 trên bản build (cần chạy bản build trên máy thật, xem danh sách kiểm §3.6).

### 3.3 Lịch & lưu game (M3)
- **Lịch:**
  - Qua 0:00 khi app đang chạy.
  - Mở app sau 3 ngày nghỉ: mùa nhảy đúng, Sinh khí nghỉ ngơi chỉ cấp một lần.
  - Đổi giờ máy về quá khứ: không lùi mùa.
  - Hôm trước mở 4h → nhận 2 giờ Sinh khí; mở 9h → nhận 0.
- **Lưu–đọc:**
  - Chạy 2000 bước = lưu ở bước 1000, đọc lại, chạy tiếp 1000 bước, phải ra **đúng y** trạng thái.
  - File hỏng thì dùng `.bak`.
  - Đọc được file mẫu `saveVersion 1` sau mỗi lần đổi cấu trúc.

**Kết quả M3 (2026-10-24):** 17 test mới trong `LittleGod.Game.Tests` xanh, phủ mọi mục ở trên: qua 0:00, mở lại sau 3 ngày, chỉnh giờ lùi, hôm trước mở 4h / 7h / 8h / 9h, tuyết tan khi vào Xuân, chỉ giữ 2 ngày giờ mở app, đặt tên vùng, chạy 2000 bước = lưu ở 1000 + đọc + chạy tiếp (so cả chuỗi JSON), `.bak`, file hỏng được cất, save phiên bản mới hơn không bị đọc, file mẫu `Tests/Game/Fixtures/world-v1.json`. Save của thế giới đã hồi sinh hết (149 động vật) nặng **34.9 KB**.

### 3.4 Khoảnh khắc (M5)
- **Luật chặn:**
  - Tối đa 1 bong bóng mỗi vùng, 3 trong khung nhìn.
  - Hai quà mới cách nhau ≥ 10 phút.
  - Thời gian hồi đúng.
  - Không hiện 🍂 vào mùa Đông.
  - Lọc 🐣 đúng 4 điều kiện.
- **Tần suất** (GDD 09 §9), chạy cùng người chơi giả lập:
  - Trung bình ≥ 1.5 khoảnh khắc mỗi giờ sau ngày 2.
  - Không có khoảng 45 phút nào trống hoàn toàn khi thế giới đã có ≥ 3 vùng.
  - Click hết thì kết game sớm hơn **≤ 10%**.

### 3.5 Hiệu năng (M1, M2)
Xem §4.

### 3.6 Danh sách kiểm thủ công (M4, M6, M7)
- **Click xuyên qua:** trên macOS và Windows, bấm được vào cửa sổ bên dưới ở bầu trời, giữa hai nút cuộn, và ngay trên khay khi khay đang thu gọn ở chỗ trống.
- **Dock / taskbar:**
  - Dải đất nằm sát trên Dock / taskbar.
  - Ẩn hoặc hiện Dock và đổi vị trí taskbar thì dải tự đặt lại.
  - Kéo chuột vào Dock không làm khay mở nhầm (GDD 10 §13).
- **Đa màn hình:** chọn màn phụ; rút màn phụ thì dải về màn chính.
- **Panel nới cửa sổ:** mở/đóng sổ tay nhiều lần, khung nhìn không bị giật và vẫn click xuyên qua phía trên được (T2).
- **Mọi mục của GDD 10 §13 và 09 §9** (phần chơi thử).

## 4. Ngân sách hiệu năng
| Hạng mục | Ngân sách | Đo bằng |
|----------|-----------|---------|
| `World.Step()` (144 cột, ~250 động vật) | ≤ 0.5 ms | Performance test, 30 ngày mô phỏng |
| Khung hình khi dải đang hiện | ≤ 4 ms CPU ở 30 fps | Unity Profiler, bản build |
| CPU trung bình cả tiến trình, 30 phút để yên | **≤ 2%** (✅ 01) trên Apple M1 và một laptop Windows tầm trung | Activity Monitor / Task Manager, ghi lại mỗi mốc |
| Bộ nhớ | ≤ 300 MB | Profiler |
| Lưu game | ≤ 20 ms, không giật khung hình | Profiler |
| GameObject đang hoạt động | Không tăng theo số cột thế giới (chỉ theo khung nhìn) | PlayMode smoke |

## 5. Log chơi thử (M7)
- File CSV **cục bộ** trong `persistentDataPath/playtest/`, chỉ có ở build "Playtest". Không gửi đi đâu: game bán một lần trên Steam, không có telemetry (✅ README GDD).
- **Mỗi giờ mở app một dòng:** ngày lịch, giờ mở app, Sinh khí, Sinh khí/phút, số vùng và trạng thái từng vùng, số mỗi loài, số chết đói / bị săn.
- **Mỗi khoảnh khắc một dòng:** loại, vùng, hiện lúc, click hay hết hạn.
- **Mỗi lệnh của người chơi một dòng:** gieo, mưa, mời, hồi sinh.
- Một công cụ nhỏ (Python, trong `Docs/GDD/sim/`) đọc log để so với mục tiêu GDD 08 §1 và 09 §1.
