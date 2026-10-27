# 08 · Nhiều vùng & biome Ao: đặc tả chi tiết

> Phạm vi: **toàn thế giới 144 cột, 14 vùng** (thuộc vertical slice): hồi sinh đất hoang, biome thứ hai **Ao**, Khu Vườn Thiêng ở mức tối giản.
> Mọi con số dưới đây đã chạy qua mô hình [`sim/worldsim.py`](sim/worldsim.py) (10 seed × tới khi kết game). Mọi số đọc từ [`sim/balance.json`](sim/balance.json), nguồn duy nhất cho cả Python và Unity; đổi số thì sửa file đó. `ecosim.py` được giữ nguyên làm mô hình đồng cỏ của 07 (luật cũ), vì C# hiện vẫn khớp với nó.
> Trạng thái: 💡 đề xuất đã kiểm chứng bằng mô hình, chờ duyệt rồi mới port sang C#.

## 1. Mục tiêu nhịp chơi & kết quả

| Mục tiêu | Kết quả mô hình (app mở 8h/ngày, người chơi ghé mỗi 30 phút) |
|----------|--------------------------------------------------------------|
| Hồi sinh vùng đầu tiên ngay trong ngày chơi đầu | Seed 1: **13 giờ** (bản trước: trung vị 9.5 giờ), chậm hơn vì thỏ ăn trụi Khởi Nguyên trước khi có cáo. Khảo sát mới chưa đo cột này |
| Kết chính trong **2–4 tuần** (05 §5) | Trung vị **ngày lịch 16.8** (15.2–17.7), tức ~133 giờ app mở |
| Hồi sinh đều đặn, giãn dần | 5 vùng đầu trong ~45 giờ (ngày 6), đủ 9 vùng ở ~97 giờ (ngày 12) |
| Ao tự đứng được sau khi mời | Cá trung bình 15–20 con, tối đa 29–40 trên 3 ao; diệc giữ cá không vượt quá sức chứa của bèo |
| Không có vòng xoáy chết ở quy mô thế giới | 13/13 vùng đạt Cân bằng cùng lúc ở mọi seed. Thỏ có thể chết đói hết ở một nơi, nhưng luôn quay lại (tối đa 2 giờ không có con thỏ nào khi người chơi chăm, 17 giờ khi bỏ mặc và không có thú săn) |
| Sinh khí có chỗ tiêu | Gần như toàn bộ Sinh khí được tiêu vào hồi sinh và Vườn |
| Hệ sinh thái tự cân bằng như tự nhiên | ✅ Thú ăn cỏ đông quá thì ăn trụi cỏ và chết đói; thú săn giữ chúng ở mức vừa. Có thú săn: chết đói **giảm ~3 lần**, cỏ bị ăn trụi ít hơn, kết game **sớm hơn 18%** (§7.3) |
| Chăm sóc được thưởng rõ ràng | 💡 Có, nhưng vừa phải: gọi mưa giúp kết sớm hơn ~8%. Đòn bẩy lớn nhất của người chơi là **mời và giữ thú săn** |

## 2. Thời gian: giờ app mở & mùa theo ngày lịch
- Mô hình chạy theo **giờ app mở**. Mặc định app mở **8 giờ mỗi ngày lịch**.
- Mỗi **ngày lịch** là một mùa (✅ 03 §7), nên một mùa chỉ dài bằng số giờ app mở hôm đó. Tuyết tan +40 độ ẩm ở phút đầu tiên của mỗi ngày Xuân.
- Tuổi thọ, thời gian lớn… vẫn tính bằng phút app mở như 07. Một con thỏ sống 2 ngày *mô phỏng* (48 giờ mở app) tương đương ~6 ngày lịch.
- ✅ **Sinh khí nghỉ ngơi** (Q18): mỗi ngày lịch, lần đầu thế giới thức dậy (mở app, hoặc lúc 0:00 nếu app đang chạy), người chơi nhận:
  ```
  Sinh khí nghỉ ngơi = Sinh khí/phút hiện tại × min(120, max(0, 480 − số phút app mở trong ngày lịch hôm trước))

  ↻ **Đổi 2026-10-24:** ở nhịp ×100 trần là **10 phút thật** thu nhập, công thức mới ở [11 §1.2](11-nhip-va-tang-tan.md#12-sinh-khí-nghỉ-ngơi--q22-giữ-trần-10-phút-thật).
  ```
  Tức là bù phần còn thiếu so với 8 giờ, tối đa 2 giờ Sinh khí. Người mở app ≥ 8h/ngày không nhận gì; người mở 4h/ngày nhận đủ 2 giờ.
  - 🎨 Hiện như một phần của hiệu ứng thức dậy (02): một làn sáng nhỏ bay về khay thần. Không có bảng tóm tắt, không có chữ.
  - Không phải mô phỏng bù: chỉ cộng Sinh khí, thế giới không chạy thêm (✅ Q2).
  - 💡 Ước tính (chưa chạy mô hình): người mở 4h/ngày kết ở ~22 ngày thay vì ~33. Vì tiến trình chủ yếu bị giới hạn bởi Sinh khí (§11 mục 4), cộng 2 giờ Sinh khí gần tương đương mở app thêm 2 giờ.
- Mô hình 07 coi 1 mùa = 24 giờ chạy liên tục. Lệnh `worldsim.py meadow` chạy lại đúng kịch bản đó (1 đồng cỏ 48 cột, 24h/ngày) và cho Sinh khí tổng **~200k**, khớp 07 (~197k).

## 3. Bố cục thế giới
💡 14 vùng **thiết kế tay** (05 §3). 4 vùng giữa (48 cột, ≈ 1 màn hình) là **Đồng cỏ Khởi Nguyên**: đã hồi sinh từ đầu nhưng chỉ có 5 cỏ ở chính giữa, đúng như kịch bản của 07.

```
cột:  0         10        20        30       39       48                                      96        106       116       126       136    143
      │Đồi Tây  │Ao Sậy   │Bãi Gió  │Đồng Xa │Ao Sen  │ Khởi Nguyên 1 · 2 · 3 · 4 (48 cột)     │Đồi Đông │Ao Đông  │Đồng Đông│Thềm Đá  │Vườn  │
      │ đồng cỏ │  ≈≈≈≈   │ đồng cỏ │đồng cỏ │  ≈≈≈≈  │   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    │ đồng cỏ │  ≈≈≈≈   │ đồng cỏ │ đồng cỏ │Thiêng│
                                                    └──── bắt đầu ở đây, lan ra hai phía ────┘
```

| Loại vùng | Số vùng | Kích thước | Ghi chú |
|-----------|---------|------------|---------|
| Khởi Nguyên | 4 | 12 cột | Đã hồi sinh từ đầu |
| Đồng cỏ | 6 | 9–10 cột | 💡 Tạm thay cho Rừng, Thảo nguyên khô, Đồi đá (chưa mô hình hoá) |
| Ao | 3 | 9–10 cột | **4 cột nước** ở giữa vùng, bờ hai bên |
| Khu Vườn Thiêng | 1 | 8 cột | Luôn ở đầu phải (✅ 05 §5) |

Cột đất hoang: Đất màu 10, Độ ẩm 0, không có gì mọc được, sinh vật không đi vào được. Mưa và khuếch tán ẩm chỉ áp dụng cho cột đã hồi sinh.

## 4. Hồi sinh một vùng
> ↻ **2026-10-24:** Hồi sinh vùng, giá và giảm giá hồi sinh được thay bằng [12 · Môi trường sống](12-moi-truong-song.md): không còn lệnh hồi sinh; Vườn mở theo 12 §5.


### 4.1 Điều kiện & giá
- Chỉ vùng **kề với vùng đã hồi sinh** mới hồi sinh được, nên phần đã hồi sinh luôn là một dải liền.
- Vùng kề phải **Khoẻ**: Sức khoẻ ≥ **60** (xem §5).
- Người chơi trả Sinh khí theo **thứ tự** hồi sinh, không theo vùng nào. Nhờ vậy người chơi tự do chọn trái hay phải mà không bị phạt.
- ✅ **Giảm giá theo Sức khoẻ vùng kề** (Q17): giảm 0% khi vùng kề vừa Khoẻ (60), tăng tuyến tính tới **30%** khi vùng kề Cân bằng (85):
  ```
  giá = giá gốc × (1 − 0.3 × kẹp((Sức khoẻ vùng kề − 60) / 25, 0, 1))
  ```
  🎨 Khay thần hiện giá đã giảm, kèm biểu tượng lá nhỏ, để người chơi thấy "chăm vùng này thì mở vùng sau rẻ hơn".

| Lần hồi sinh | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | Khu Vườn |
|---|---|---|---|---|---|---|---|---|---|---|
| Giá gốc | 3,000 | 15,000 | 30,000 | 48,000 | 66,000 | 84,000 | 102,000 | 120,000 | 145,000 | 300,000 (không giảm) |
| Thời điểm (trung vị, giờ mở app) | ~10–13h | | | | 45h | | | | 97h | 133h |

> Tổng giá gốc: 613k cho 9 vùng + 300k cho Vườn. Trong mô hình, người chơi được giảm trung bình 23–28%, nên thực trả ~450k cho 9 vùng. Bảng giá gốc được chỉnh **trước khi có giảm giá**. ✅ Giữ bảng giá này (Q17): game kết ở ~17 ngày (8h/ngày), vẫn trong 2–4 tuần. Sẽ chỉnh lại sau khi chơi thử vertical slice. Tham khảo: bản chưa có cân bằng tự nhiên đo được nhân ×1.35 thì kết ở ~21 ngày.

### 4.2 Khi vùng hồi sinh
- Mọi cột của vùng: Đất màu 35, Mùn 10, Độ ẩm 50 (bờ ao 70, cột nước luôn 100).
- **Gió/Gieo hạt đưa sự sống sang**: 3 mầm cỏ ở 3 cột giáp vùng cũ. Vùng ao có 2 mầm cỏ, 2 mầm bèo ở 2 cột nước gần nhất, và 1 bụi lau sậy non ở bờ.
- Thực vật Ao (Bèo, Lau sậy) được **khám phá khi hồi sinh ao đầu tiên** (✅ 04 §3: "khi một vùng mới được hồi sinh"). Riêng Sen phải được người chơi gieo.

## 5. Đoạn biome, Sinh khí & Sức khoẻ

### 5.1 Đoạn biome
**Đoạn biome** là các vùng **liền nhau, cùng nhóm biome** (03 §5). Khởi Nguyên và Đồng cỏ cùng nhóm "đồng cỏ"; mỗi ao là một đoạn riêng. Ví dụ, khi Đồng Xa hồi sinh, nó nhập vào đoạn Khởi Nguyên thành một đoạn đồng cỏ 57 cột.

### 5.2 Sinh khí theo đoạn
Công thức 07 §7.1 được tính **riêng cho từng đoạn** rồi cộng lại:

```
Sinh khí/phút = Σ_đoạn ( Σ cơ bản × Đa dạng × Cân bằng )

Đa dạng  = 1 + 0.15 × (số loài − 1) + 0.25 × (vai trò tại chỗ − 1) + 0.125 × (vai trò mượn)
           vai trò mượn = vai trò có ở đoạn kề nhưng không có tại chỗ (tính một nửa)
Cân bằng = như 07, với hai thay đổi:
           − tỉ lệ mồi:săn đếm trên đoạn + đoạn kề (thú săn đi lang thang qua nhiều đoạn)
           − thưởng +0.2 khi đủ 5 vai trò, tính cả vai trò mượn
```

Khi thế giới chỉ có một đoạn, công thức này giống hệt 07.

### 5.3 Sức khoẻ vùng (0–100)
```
Sức khoẻ = 100 × Độ phủ × (0.4 + 0.3 × Vai trò + 0.3 × Cân bằng')

Độ phủ     = tỉ lệ cột của vùng có ít nhất một cây trưởng thành, không ngủ khô
Vai trò    = min(1, (vai trò tại chỗ + 0.5 × vai trò mượn) / 5)     ← tính trên đoạn chứa vùng
Cân bằng'  = (hệ số Cân bằng của đoạn − 0.3) / 0.7, kẹp [0, 1]
```
- **Khoẻ** ≥ 60: mở hồi sinh vùng kề. **Cân bằng** ≥ 85: điều kiện mở Vườn.
- Độ phủ là **nhân tử**, nên một vùng vừa hồi sinh luôn bắt đầu từ 0 dù cả đoạn đang khoẻ. Nếu dùng công thức cộng, vùng mới sẽ lập tức đạt ~60 nhờ "hưởng" Vai trò và Cân bằng của cả đoạn, và người chơi mở được vùng tiếp theo ngay. (Đây là suy luận khi thiết kế, chưa chạy so sánh.)
- 🎨 Bản đồ mini tô màu vùng theo Sức khoẻ; vùng Cân bằng có ánh lấp lánh nhẹ.

## 6. Biome Ao

### 6.1 Mặt nước
- Cột nước có **Độ ẩm cố định 100**, không bốc hơi, không nhận mưa. Qua khuếch tán (5%/phút), bờ ao luôn ẩm (~70–95). Đây là cách Ao tạo ra **dải ven nước** mà không cần luật riêng.
- Cột nước chỉ trồng được **thực vật thuỷ sinh**; cây cạn không mọc trên nước và ngược lại.
- Cá chỉ di chuyển trong các cột nước của ao mình. Diệc, thỏ, cáo đi qua được.

### 6.2 Thực vật
| | Bèo | Sen | Lau sậy |
|---|---|---|---|
| Nền · tầng | Nước · Thảm | Nước · Bụi (lá nổi) | Đất · Bụi |
| Thời gian lớn | 20 phút | 3 giờ | 1.5 giờ |
| Tuổi thọ | 1 ngày | 4 ngày | 3 ngày |
| Lâu năm (ngủ khô)? | Có | Có | Có |
| Độ ẩm min / lo / hi / max | — (luôn đủ nước) | — | 50 / 65 / 100 / 100 |
| Đất màu · ánh sáng tối thiểu | 10 · 40 | 30 · 60 | 20 · 40 |
| Hạt/giờ · tầm hạt | 3.0 · 2 cột | 0.3 · 2 cột | 0.6 · 1 cột |
| Hút nước · đất màu (/phút) | 0 · 0.004 | 0 · 0.008 | 0.03 · 0.006 |
| Mùn khi chết | 4 | 15 | 15 |
| Có hoa (cần thụ phấn) | Không | **Có** | Không |
| Sinh khí/phút | 0.05 | 0.25 | 0.12 |
| Đặc biệt | Thức ăn của cá: sinh khối mọc lại 1.0 × q × mùa /phút | Thức ăn cho ong, nên **ong mượn từ đồng cỏ kế bên** | Chỉ sống sát nước. Cá cạnh lau sậy hoặc sen thì khó bị bắt (×0.5) |

### 6.3 Động vật
| | Cá | Diệc |
|---|---|---|
| Vai trò | Ăn cỏ (ăn bèo) | Săn mồi (ăn cá) |
| Ăn | Bèo 0.5/phút | 1 cá / 5 giờ |
| Vùng sống · tầm kiếm ăn | 3 · 12 cột (chỉ trong ao) | 15 cột · bay về phía cá gần nhất trong 30 cột khi đói |
| Trưởng thành | 2 giờ | 4 giờ |
| Tuổi thọ | 2 ngày | 4 ngày |
| Mỗi lứa · nghỉ giữa 2 lứa | 3 · 3 giờ | 1 · 15 giờ |
| Sức chứa | Theo bèo, như thỏ (07 §6.2) | Số cá trong vùng sống ÷ **5** |
| Sinh khí/phút (khi trưởng thành) | 0.20 | 0.60 |
| Mùn khi chết | 3 | 8 |
| Mời: điều kiện · giá | ≥ **4** bèo sống (một ao phủ kín) · 120 | ≥ 6 cá · 300 |

Diệc dùng chung luật săn của cáo (07 §6.4): luật cặp cuối, độ hiếm, nơi trú ẩn, nghỉ đông. Diệc không có nguồn ăn phụ.

### 6.4 Chuỗi thức ăn
```
   💧 mặt nước ──► bờ ẩm
        │             │
       Bèo           Lau sậy, Cỏ
        │   Sen ◄──── Ong (mượn từ đồng cỏ kế bên)
        ▼
       Cá ──► Diệc
        │ (chết)
        ▼
   🍂 Mùn ──► Giun (ở bờ) ──► 🌱 Đất màu
```
Ao **không có loài thụ phấn riêng**. Đây là ví dụ đầu tiên cho luật "mượn vai trò" (03 §4b): một ao kẹp giữa hai đồng cỏ có hoa sẽ có ong. Nếu ao nằm cạnh vùng thiếu hoa, Sen ra ít hạt hơn và ao chỉ được tính nửa vai trò thụ phấn.

## 7. Sinh vật: lan sang vùng mới & cân bằng tự nhiên

### 7.1 Loài tự tìm đến đoạn biome mới
> ↻ **2026-10-24:** Lời mời + tự tìm đến được thay bằng [12 · Môi trường sống](12-moi-truong-song.md): mọi loài tự đến theo bảng điều kiện sống ở 12 §3, kể cả lần đầu.

💡 Luật "tự quay lại" của 07 §6.3 được làm tổng quát thành luật **theo từng đoạn biome** (riêng cá: theo từng ao):
- Loài **đã khám phá**, ở đoạn đang có **< 2 con** (giun: chưa có cột nào), và đoạn đó đạt **điều kiện tại chỗ liên tục 2 giờ**, thì **một cặp** đi vào từ một mép của đoạn.
- Điều kiện tại chỗ dùng cùng ngưỡng với lời mời, nhưng đếm trong đoạn: Giun ≥ 6 cỏ; Thỏ ≥ 10 cỏ; Ong ≥ 4 hoa (hoa dại + sen); Cáo ≥ 6 thỏ; Cá ≥ 3 bèo trong ao; Diệc ≥ 6 cá.
- Riêng thú săn: chỉ coi là "vắng" khi **cả đoạn kề** cũng vắng, vì cáo và diệc đi lang thang qua nhiều đoạn. Nếu không có điều này, các cặp diệc mới liên tục được thả vào và diệc lên tới 16–18 con trong khi chỉ có ~25 cá.
- Khi thế giới chỉ có một đoạn, luật này chính là luật quay lại của 07.

> Kết quả: khoảng **2 lần/ngày lịch** có một cặp sinh vật tự đến một vùng (seed 1: 34 lần trong 16 ngày). Mỗi lần là một **khoảnh khắc** ✨ (đặc tả ở [09](09-khoanh-khac.md)). Click để đón thì được thưởng một ít Sinh khí, bỏ qua thì con vật vẫn ở lại.

### 7.2 Ong chia đàn
Khi một đàn ong sinh sản, đàn mới bay tới cột có **nhiều hoa nhất trong 12 cột** và cách các đàn khác **≥ 4 cột** (nếu không có chỗ nào có ≥ 3 hoa thì ở lại chỗ cũ). Đây là cách ong lan dần ra khỏi Khởi Nguyên và tới được sen ở ao.

### 7.3 Cân bằng tự nhiên: ăn trụi, chết đói, thú săn
✅ Không có dịch bệnh. Số lượng thú ăn cỏ được điều hoà bằng **chuỗi thức ăn**, như trong tự nhiên:

```
 cỏ nhiều ──► thỏ đẻ nhiều ──► thỏ ăn nhanh hơn cỏ mọc ──► cỏ trụi, vàng, ngủ khô
     ▲                                                          │
     │                                                          ▼
 cỏ mọc lại ◄── còn ít thỏ ◄──────────────────────────── thỏ đói rồi chết đói
                    ▲
                    └── cáo ăn bớt thỏ từ sớm, nên vòng trên hiếm khi xảy ra
```

**Thay đổi so với 07** (chỉ trong `worldsim.py`; `ecosim.py` và C# vẫn theo 07):

| Luật | 07 | 08 |
|------|----|----|
| Sức chứa thú ăn cỏ (07 §6.2) | Lượng thức ăn mọc lại × **0.7**, nên không bao giờ vượt | × **1.0**: đẻ tới đúng lượng cỏ mọc lại *lúc đó*. Khi sang Đông (cỏ mọc ×0.3) hoặc gặp hạn, đàn thỏ đang có sẽ thành **quá đông** so với lượng cỏ |
| Đói (07 §6.3) | Độ no ≤ 10 thì **bỏ đi**, không để lại gì | Độ no ≤ 10 thì **chết đói**: nằm xuống, mờ dần, để lại Mùn (✅ 03 §3) |
| Áp dụng cho | | Mọi loài: thỏ, cá, cả cáo và diệc khi hết mồi |

**Giữ nguyên từ 07** để không có vòng xoáy chết:
- Cỏ lâu năm **ngủ khô** khi bị ăn trụi chứ không chết hẳn; hạt ngủ trong đất.
- **Luật cặp cuối** của thú săn: không săn khi trong vùng chỉ còn ≤ 2 con mồi.
- Loài đã khám phá **tự tìm đến lại** khi cỏ hồi phục (§7.1), nên thỏ chết đói hết ở một nơi thì vài giờ sau một cặp mới lại vào.

🎨 Người chơi đọc được cả chu kỳ bằng một cái liếc: cỏ thưa và vàng → thỏ gầy, đi chậm → vài con nằm xuống, để lại ụ mùn → cỏ xanh lại. Khi có cáo, cảnh "đuổi ra khỏi màn hình" (✅ 03 §3) thay cho phần lớn các cái chết đói.

**Kết quả** (8h/ngày, 10 seed, người chơi gọi mưa; "trụi" = đoạn có > 50% cột cỏ/bèo dưới 20 sinh khối hoặc đang ngủ khô):

| | Có thú săn | Không mời thú săn (`nopred`) | Luật 07 (`legacy`) |
|---|---|---|---|
| Kết game (ngày lịch) | **16.8** (15.2–17.7) | 19.8 (17.6–21.6) | 17.9 (16.0–18.9) |
| Thỏ trung bình · cao nhất | 22 · 61–85 | 30 · 65–102 | 17 · 35–67 |
| Thời gian bị ăn trụi | **~64%** | ~84% | ~27% |
| Chết đói / ngày lịch (mọi loài) | **~7.5** | ~20 | 0 (nhưng có con bỏ đi) |
| Bị săn / ngày lịch | ~42 | 0 | ~26 |

- **Thú săn làm đúng vai trò của nó:** giảm chết đói ~3 lần, bớt ăn trụi, và vì Cân bằng cao hơn nên kết game sớm hơn 3 ngày. Đây là phần thưởng cho việc mời cáo và diệc.
- Thỏ dao động mạnh theo mùa (seed 1: 5–10 con mỗi mùa Xuân, 58–84 con mỗi mùa Hạ từ ngày 9). Đây là chu kỳ "bùng nổ – ăn trụi – chết đói" mong muốn: theo mùa, đoán được, không phải thảm hoạ.
- ~64% thời gian "trụi" nghe nhiều, nhưng phần lớn rơi vào **Đông và đầu Xuân**, khi cỏ mọc chỉ bằng 0.3 lần bình thường. Ngay cả luật 07 cũng có ~27%.
- Mức chết đói ~7.5 con/ngày lịch là trên **cả thế giới 144 cột** (~3 màn hình), tức người chơi thấy khoảng 1 con mỗi 3 giờ trên màn hình đang nhìn. Cần thử cảm giác trong prototype.

## 8. Khu Vườn Thiêng (mức tối giản)
- **Mở** khi 13 vùng còn lại đều đã hồi sinh và **cùng lúc đạt Cân bằng** (≥ 85). Trong mô hình, điều này xảy ra 2–42 giờ sau lần hồi sinh cuối, thường vào mùa Hạ hoặc Thu, khi thỏ và cá đã hồi lại sau mùa Đông.
- **Kết chính**: mời đủ loài đại diện về Vườn. Mô hình gộp phần này thành **một giá 300k Sinh khí**, mất **0–32 giờ app mở** sau khi Vườn mở (tới 4 ngày lịch ở 8h/ngày; nếu chờ Vườn mở lâu thì đã tích đủ tiền từ trước). Như vậy dài hơn "1–2 phiên" của 05 §5. Muốn đúng 1–2 phiên thì hạ giá xuống ~150k, và kết game sẽ sớm hơn khoảng 1 ngày lịch.

## 9. Người chơi trong mô hình
Ghé mỗi 30 phút, mỗi lần làm theo thứ tự:
1. Mời loài mới khi đủ điều kiện và đủ Sinh khí.
2. **Gọi mưa**: mỗi vùng có độ ẩm trung bình < 25 thì kéo một lần mưa ở giữa vùng (phủ 7 cột, 30 Sinh khí).
3. **Hồi sinh** vùng kề có vùng bên cạnh khoẻ nhất, ngay khi đủ Sinh khí với giá (đã giảm) lúc đó (giữ lại 50 để còn gọi mưa). Người chơi mô hình **không cố chờ** vùng kề Cân bằng để được giảm tối đa.
4. **Gieo**: mỗi vùng giữ khoảng 1 hoa dại / 6 cột và 1 mâm xôi / 8 cột (cùng mật độ với 07), và 2 sen mỗi ao.
5. Kiểm tra điều kiện mở Vườn.

"Người bỏ mặc" (`survey idle`) bỏ bước 2 (không gọi mưa), các bước khác giữ nguyên, kể cả việc mời thú săn. Kịch bản `nopred` thì không bao giờ mời Cáo và Diệc.

## 10. Kết quả kiểm chứng
10 seed mỗi kịch bản.

**Luật hiện tại (giảm giá theo Sức khoẻ + cân bằng tự nhiên):**

| Kịch bản | Vùng 5 | Vùng 9 | Vườn mở | Kết (giờ mở app) | **Kết (ngày lịch)** | Thỏ TB | Ăn trụi | Chết đói/ngày | Gọi mưa |
|----------|--------|--------|---------|------------------|---------------------|--------|---------|---------------|----------|
| Chăm (gọi mưa), có thú săn, 8h/ngày | 45h | 97h | 109h | 133h | **16.8** (15.2–17.7) | 22 | 64% | 7.5 | có |
| Chăm, có thú săn, 4h/ngày | 45h | 97h | 118h | 130h | **33.0** (27.8–38.9) | 24 | 67% | 4.6 | có |
| Chăm, có thú săn, 12h/ngày | 44h | 99h | 112h | 134h | **11.1** (10.4–12.2) | 24 | 66% | 10 | có |
| Không gọi mưa, có thú săn | 48h | 108h | 132h | 146h | **18.2** (16.8–20.8) | 21 | 60% | 8 | không |
| Gọi mưa, không thú săn | 51h | 112h | 133h | 156h | **19.8** (17.6–21.6) | 31 | 84% | 20 | có |
| Không gọi mưa, không thú săn | 54h | 118h | 133h | 165h | **20.4** (18.6–28.6) | 25 | 80% | 21 | không |

**Đòn bẩy của người chơi** (ngày lịch kết game, 8h/ngày):

| | Có thú săn | Không thú săn | Thú săn giúp |
|---|---|---|---|
| Gọi mưa | **16.8** | 19.8 | **18%** |
| Không gọi mưa | 18.2 | 20.4 | 12% |
| **Mưa giúp** | **8%** | **3%** | |

Thú săn là đòn bẩy lớn nhất, gấp đôi gọi mưa. Hai thứ cộng lại: người làm cả hai kết sớm hơn người không làm gì ~21%. Với bảng giá hiện tại, kết game rơi vào ~17 ngày, vẫn nằm trong 2–4 tuần.

Diễn biến một seed (seed 1, 8h/ngày). Dải vùng: ░ đất hoang, số = Sức khoẻ/10, ★ = Cân bằng.

| Ngày | Mùa | Vùng | Thỏ | Cáo | Ong | Cá | Diệc | Sinh khí/phút | Tích luỹ |
|------|-----|------|-----|-----|-----|----|------|---------------|----------|
| 1 | Hạ | `░░░░░2★★3░░░░░` | 13 | 2 | 2 | 0 | 0 | 23 | 5k |
| 3 | Đông | `░░░░6★★★★★6░░░` | 12 | 0 | 6 | 9 | 2 | 64 | 44k |
| 5 | Hạ | `░░░░6★★★★★8★░░` | 15 | 2 | 21 | 29 | 9 | 116 | 108k |
| 8 | Xuân | `░░░58★★★★6★★★░` | 7 | 4 | 27 | 7 | 10 | 92 | 252k |
| 9 | Hạ | `░░★★★8★67★★★8░` | 58 | 5 | 28 | 17 | 11 | 120 | 303k |
| 12 | Xuân | `3★★★★★★6★★★★6░` | 10 | 8 | 29 | 10 | 13 | 106 | 480k |
| 13 | Hạ | `★★★★★★★★★★★★★░` | 71 | 15 | 33 | 26 | 14 | 183 | 551k |
| 16 | Xuân | `78★6★5★★6★★★7░` | 8 | 11 | 26 | 9 | 14 | 109 | 757k (kết ở giờ 128) |

Thỏ và cá xuống đáy mỗi mùa Xuân (sau mùa Đông cỏ mọc chậm, nhiều con chết đói), rồi bùng lên lại vào mùa Hạ.

## 11. Bài học rút ra từ mô hình
1. **Mặt nước chặn đường lan của sinh vật.** Giun chỉ lan sang cột đất kề bên, nên không vượt được ao; ong cũng không vượt được nếu không có luật chia đàn. Bản nháp đầu có 3 vùng phía sau ao mãi không đủ vai trò. Cần luật "tự tìm đến đoạn biome mới" (§7.1). Luật này còn là nguồn khoảnh khắc đều đặn nhất của game.
2. **Điều kiện mời phải đạt được chỉ với một vùng.** Bản nháp đặt "Cá cần ≥ 6 bèo", nhưng một ao chỉ có 4 cột nước, nên cá chỉ mời được khi đã có ao thứ hai, chậm hơn ~38 giờ.
3. **Mọi phép đếm liên quan đến thú săn phải tính cả đoạn kề.** Thú săn đi lang thang, nên đếm theo từng đoạn làm tỉ lệ mồi:săn nhảy liên tục (Cân bằng kẹt ở 0.8) và làm luật "tự đến" thả quá nhiều diệc.
4. ⚠️ **Tiến trình bị giới hạn bởi Sinh khí, không phải bởi sức khoẻ.** Vùng mới đạt Khoẻ chỉ sau vài giờ, nhưng người chơi phải chờ thêm **8–16 giờ** mới đủ tiền (đo ở các bản trước khi có cân bằng tự nhiên). Hệ quả:
   - Giá hồi sinh là **núm chỉnh nhịp chính**, và nó hoạt động tốt: kết game ổn định trong khoảng ±2 ngày giữa các seed.
   - **Chăm sóc chỉ nhanh hơn khoảng 9%** (21.4 so với 23.4 ngày khi không giảm giá), yếu hơn nhiều so với +65% Sinh khí của 07. Ở quy mô thế giới, mưa tự nhiên cộng với hạt ngủ trong đất đã đủ giữ các vùng sống.
   - ⚠️ **Giảm giá theo Sức khoẻ không sửa được điều này.** Nó làm *cả hai* kiểu người chơi nhanh hơn ~16–19%, còn khoảng cách chăm/không chăm lại hẹp đi, từ 9% xuống 6%. Lý do: các vùng của người không gọi mưa cũng gần như luôn Cân bằng (được giảm trung bình 21–28%, so với 23–28% khi chăm). Sức khoẻ vùng **đã bão hoà**: thứ người chơi làm hầu như không đổi được nó.
   - ✅ **Chuỗi thức ăn sửa được.** Khi thú ăn cỏ có thể vượt sức chứa và chết đói (§7.3), việc người chơi làm có tác động thật: mời thú săn giúp kết sớm hơn **18%**, gọi mưa thêm **8%**. Quy tắc rút ra: **phần thưởng cho người chơi phải đến từ một cơ chế mà tự nhiên không tự lo được.** Hệ số an toàn ×0.7 của 07 đã "lo hộ" người chơi, nên mọi thứ người chơi làm đều thừa.
5. **Luật "đói thì bỏ đi" của 07 che mất chu kỳ tự nhiên.** Con vật biến mất không để lại gì, nên người chơi không thấy nhân quả "đông quá → hết cỏ → chết đói". Đổi sang chết đói (để lại Mùn) cho người chơi thấy điều đó, mà vẫn không có vòng xoáy chết nhờ cỏ ngủ khô, hạt ngủ trong đất và luật tự tìm đến lại (§7.1). Một vùng có thể mất hết thỏ, nhưng tối đa ~17 giờ sau đã có thỏ lại, kể cả khi người chơi không làm gì.
6. ⚠️ **Thời lượng theo ngày lịch tỉ lệ nghịch với số giờ mở app.** Tổng số giờ mở app để kết gần như cố định (~140 giờ), nên app mở 4h/ngày thì mất **~33 ngày**, 12h/ngày thì **~11 ngày**. Mục tiêu "2–4 tuần" chỉ đúng với người mở app 6–12 giờ/ngày. Xem câu hỏi Q18.
7. **Mùa Xuân là đáy dân số.** Sau mùa Đông (cỏ mọc ×0.3, sinh sản ×0.2, nhiều con chết đói), số thỏ và cá xuống thấp nhất, Sinh khí thấp hơn mùa Hạ liền sau 30–50%. Vì vậy Vườn thường mở vào Hạ hoặc Thu. Đây là nhịp mùa tự nhiên, nên giữ.
8. **Mâm xôi phủ gần kín tầng bụi** (~110 bụi trên ~125 cột đất đã hồi sinh). Vấn đề này đã có từ 07 (36/48 cột) và cần xem lại khi thêm tầng tán.

## 12. Thay đổi kéo theo ở các tài liệu khác
- **Cấp thần (07 §7.4):** Sinh khí tích luỹ giờ lớn hơn nhiều (~760k khi kết ở seed 1), nên mốc cũ đến quá sớm (cấp 4 ở ngày 6). Giãn ra theo Sinh khí tích luỹ của seed 1 ở 8h/ngày (💡 số liệu; đã ghi vào 07 §7.4):

  | Cấp | Mốc cũ | Mốc đề xuất | Thời điểm (8h/ngày) | Mở khoá |
  |-----|--------|-------------|---------------------|---------|
  | 2 | 2,000 | 5,000 | cuối ngày 1 | Gió, Nắng ấm |
  | 3 | 25,000 | 50,000 | ngày 3–4 | Nắn đất |
  | 4 | 150,000 | 250,000 | ngày 8 | Sét |

Các đề xuất dưới đây ✅ đã được áp dụng vào tài liệu gốc ngày 2026-10-23:
- **05 §5:** ghi rõ thời lượng 2–4 tuần là cho người mở app 6–12 giờ/ngày; người mở ít hơn được Sinh khí nghỉ ngơi bù (§2).
- **03 §4b:** ghi Ao "mượn" loài thụ phấn từ đồng cỏ kế bên (§6.4).
- **07 §6.2–6.3, §7.3–7.4, §9:** sức chứa thú ăn cỏ ×1.0, đói thì chết, bỏ Chúc phúc, giãn mốc cấp thần như bảng trên.
- **04 §1–2, 02, 01, 03:** bỏ Chúc phúc và mọi nhắc tới bệnh/ốm.

`ecosim.py` và C# `EcoWorld` **vẫn chạy luật cũ của 07**. Việc cập nhật chúng thuộc giai đoạn Technical Doc → triển khai.

## 13. Câu hỏi mở phát sinh
✅ Đã chốt hết ngày 2026-10-23 (chi tiết trong [06](06-cau-hoi-mo.md)):
- **Q17.** Làm sao để chăm sóc được thưởng rõ ràng? Đã thử ba cách: giảm giá hồi sinh (không đủ, khoảng cách chăm/không chăm 9% → 6%), dịch bệnh + Chúc phúc (19%, nhưng **đã loại** vì quá phức tạp với game chill), và cân bằng tự nhiên (§7.3: thú săn giúp kết sớm hơn 18%, mưa thêm 8%). ✅ **Giữ giảm giá + cân bằng tự nhiên, giữ bảng giá hiện tại.** Còn phải thử cảm giác trong prototype xem ~1 cái chết đói mỗi 3 giờ trên màn hình có quá buồn không. Nếu quá buồn, cho thú ăn cỏ đói thì ngừng sinh sản sớm hơn, thay vì quay lại luật "bỏ đi".
- **Q18.** ✅ Có **Sinh khí nghỉ ngơi**, bù tới 8 giờ/ngày, tối đa 2 giờ Sinh khí (§2).
- **Q19.** ✅ Sinh vật tự tìm đến vùng mới **không cần** click đón; click bong bóng chỉ để nhận thưởng thêm (§7.1).
- **Q20.** ✅ **Bỏ Chúc phúc.** Vai trò "vuốt ve" chuyển sang click khoảnh khắc.

## 14. Giới hạn của mô hình & việc tiếp theo
- Rừng, Thảo nguyên khô, Đồi đá đang được thay tạm bằng đồng cỏ. Khi thêm các biome này, phải chạy lại để kiểm tra giá hồi sinh, vì biome khó sống sẽ làm chậm phần Sức khoẻ.
- Tầng tán và nhịp ×100: [11](11-nhip-va-tang-tan.md). Chưa có: Gió, Nắng ấm, Nắn đất, Sét, cháy, khoảnh khắc (phần thưởng khi click), Sinh khí nghỉ ngơi.
- Lệnh kiểm tra `meadow` chạy theo luật 07 (sức chứa ×0.7, đói thì bỏ đi) để vẫn so được với `ecosim.py`.
- Khu Vườn Thiêng mới chỉ là một giá; chưa mô hình hoá việc mời loài đại diện.
- Người chơi mô hình là "người chơi tối ưu đơn giản": ghé đều mỗi 30 phút, hồi sinh ngay khi đủ tiền (không chờ được giảm tối đa). Người thật sẽ bỏ lỡ một số lần ghé. Mời thú săn chỉ cần làm một lần cho mỗi loài, nên người chơi bận vẫn nhận gần đủ phần thưởng lớn nhất. Mô hình chưa đo kịch bản ghé thưa.
- **Bước tiếp theo:** hoàn thiện GDD cho vertical slice (khoảnh khắc, UI), rồi viết Technical Doc, sau đó mới port Ao, luật nhiều vùng và cân bằng tự nhiên sang C# (`EcoWorld`) kèm test khớp `worldsim.py`. Có thể thêm vào mô hình kịch bản "ghé mỗi 2 giờ" và Sinh khí nghỉ ngơi để kiểm chứng.

Chạy lại mô hình sau mỗi lần đổi số:

```bash
python3 Docs/GDD/sim/worldsim.py survey
```

```bash
python3 Docs/GDD/sim/worldsim.py survey idle
```

```bash
python3 Docs/GDD/sim/worldsim.py survey hpd=4
```

```bash
python3 Docs/GDD/sim/worldsim.py survey nodiscount
```

```bash
python3 Docs/GDD/sim/worldsim.py survey nopred
```

```bash
python3 Docs/GDD/sim/worldsim.py survey legacy
```

```bash
python3 Docs/GDD/sim/worldsim.py meadow
```

```bash
python3 Docs/GDD/sim/worldsim.py 40 1
```
