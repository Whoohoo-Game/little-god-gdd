# 18 · Thời gian thật & nhịp theo lần liếc

> Trạng thái: ✅ **Đã chốt** 2026-10-28 (bỏ tăng tốc, mùa 1 giờ, vòng đời chỉnh theo nhóm, slice ~1 ngày làm việc; Q58–Q62, [06](06-cau-hoi-mo.md)). Đo bằng `sim/glancesim.py`. Kỹ thuật: [Tech Doc 12](../Tech%20Doc/12-thoi-gian-that.md).
> Phần này **thay** đồng hồ ×100 và bảng thời gian của [11 §1](11-nhip-va-tang-tan.md#1-nhịp-100), thời gian sống của khoảnh khắc ở [15 §3.3](15-sinh-dong-va-phan-hoi.md#33-thời-gian-phút-thật), và thêm một luật nhịp cho động vật tự đến ([12 §3](12-moi-truong-song.md#3-động-vật-tự-đến--q29--2-con-chờ-2-giờ-mô-phỏng)).

## 0. Vì sao
- ✅ (2026-10-22) Nhịp chơi là **idle**: người chơi ghé lại mỗi 10–30 phút. ✅ (2026-10-28) Thiết kế cho người **liếc mỗi 15–30 phút**.
- ✅ (2026-10-28) **Bỏ tăng tốc thời gian.** Người chơi chill cùng thời gian của game, không có "1 phút thật = 100 phút mô phỏng". Mọi thời gian trong game tính bằng **thời gian thật**. Bù lại, vòng đời của từng nhóm sinh vật được đặt lại để thế giới vẫn đổi đủ nhanh mà không chán.
- ✅ (2026-10-28) **Một mùa = 1 giờ** app mở. **Slice dài ~1 ngày làm việc** (6–8 giờ app mở). Vòng đời **chỉnh theo từng nhóm** chứ không chia đều một hệ số.

## 1. Vì sao ×100 không hợp với người liếc (đo 2026-10-28)
`glancesim.py` dùng luật GDD 17 đã chốt (có Hươu, Sói), mọi cây gieo được mở từ đầu (04 §3), 8 seed. Người chơi mô hình như `biomesim.py`. **Chuyện lớn** = chuyện liếc qua là nhận ra: loài mới, ao thức dậy, rừng thành hình (≥ 3 cột Rừng), đất hoang phủ kín, Vườn mở, kết game.

| Đồng hồ ×100 | Liếc 15 phút | Liếc 30 phút |
|---|---|---|
| Kết game (trung vị) | 1.4 giờ | 3.5 giờ |
| Số lần liếc tới kết | **6** | **7** |
| Chuyện lớn dồn vào một lần liếc (nhiều nhất) | 5 | 5 |
| Bong bóng ✨ / 🐣 được thấy (sống 8 phút) | 52% | 26% |

Thế giới chạy trong lúc người chơi không nhìn. Ở ×100, mỗi lần liếc thấy quá nhiều thay đổi (Thỏ, Ong, Cá, Diệc và một ao thức dậy cùng lúc), và cả slice hết sau ~6 lần nhìn.

## 2. Thời gian thật

### 2.1 Giữ nguyên
- ✅ **Ngày đêm** như [11 §1.5](11-nhip-va-tang-tan.md#15-ngày-đêm-và-nếp-sinh-hoạt--2026-10-24-chỉ-là-hình): 10 phút (5 phút ngày + 5 phút đêm) theo thời gian chơi, nếp ngủ / thức của từng loài, thỏ ngủ trong hang, sóc ngủ trên cây.
- ✅ **Hình và hành vi** ([13](13-bay-dan-va-sinh-san.md), [14](14-hang-tho-va-san-moi.md), [15 §1–2](15-sinh-dong-va-phan-hoi.md)) giữ nhịp như người chơi đang thấy: đi lại, nghỉ, rượt, vồ, trốn về hang, động tác nhỏ, sinh vật trang trí, mây, mưa, cầu vồng.
- ✅ Thời gian của khoảnh khắc, Sinh khí nghỉ ngơi ([11 §1.2](11-nhip-va-tang-tan.md#12-sinh-khí-nghỉ-ngơi--q22-giữ-trần-10-phút-thật)) vốn đã tính bằng phút thật.
- Bản Dev giữ nút ×1 / ×10 / ×60, giờ là tốc độ so với thời gian thật.

### 2.2 Đổi
- ✅ **Một mùa = 60 phút** (trước 30). Một mùa có đúng **6 ngày đêm**, nên mùa nào cũng bắt đầu lúc bình minh như cũ. Một năm = 4 giờ.
- Bỏ khái niệm "phút mô phỏng" trong GDD: mọi số ở bảng dưới là thời gian thật. Cách mô phỏng chia bước là việc của Tech Doc (§6).

## 3. Vòng đời theo nhóm (✅ Q58)
✅ Hai nhóm tốc độ:
- **Cây tầng Thảm và Bụi** (cỏ, hoa, dương xỉ, bèo, mâm xôi, sen, lau sậy) **lớn nhanh**: gieo xong là thấy kết quả trong vòng một lần liếc, giữ cảm giác "chạm nhẹ, có hồi đáp" (trụ cột 2).
- **Mọi thứ còn lại** (tuổi thọ cây, cây tán, động vật, đói no, sinh sản, săn, đất, nước, Sinh khí) chậm hơn ×100 khoảng **6 lần** và giữ nguyên tỉ lệ với nhau. Cân bằng của 07–17 vì vậy giữ nguyên, chỉ khác ở hai chỗ: cây Thảm / Bụi lớn nhanh hơn so với phần còn lại, và mùa ngắn hơn so với vòng đời (§5.2).

| Nhóm | Loài | Lớn tới trưởng thành | Sống | Ở ×100 (lớn / sống) |
|------|------|----------------------|------|---------------------|
| Thảm | Cỏ, Bèo | **24 giây** | 1.4 giờ | 12 giây / 14 phút |
| | Hoa dại | 47 giây | 1.4 giờ | 24 giây / 14 phút |
| | Dương xỉ | 35 giây | 2.8 giờ | 18 giây / 29 phút |
| Bụi | Lau sậy | 1.8 phút | 4.2 giờ | 54 giây / 43 phút |
| | Mâm xôi | 2.4 phút | 5.6 giờ | 1.2 phút / 58 phút |
| | Sen | 3.5 phút | 5.6 giờ | 1.8 phút / 58 phút |
| Tán | Sồi | **1.4 giờ** | 42 giờ (qua cả slice) | 14 phút / 7.2 giờ |
| | Táo dại, Liễu | 1.4 giờ | 20 giờ | 14 phút / 3.4 giờ |

| Loài | Trưởng thành | Nghỉ giữa hai lứa | Sống | Ở ×100 (sống) |
|------|--------------|-------------------|------|---------------|
| 🐇 Thỏ | 3.5 phút | 14 phút | **2.8 giờ** | 29 phút |
| 🐟 Cá | 7 phút | 21 phút | 2.8 giờ | 29 phút |
| 🐝 Ong | 14 phút | 28 phút | 2.8 giờ | 29 phút |
| 🐿️ Sóc | 7 phút | 42 phút | 2.8 giờ | 29 phút |
| 🦌 Hươu | 11 phút | 28 phút | 5.6 giờ | 58 phút |
| 🦊 Cáo | 11 phút | 2.9 giờ | **5.6 giờ** | 58 phút |
| 🪶 Diệc | 14 phút | 2.9 giờ | 5.6 giờ | 58 phút |
| 🐺 Sói | 21 phút | 2.9 giờ | 5.6 giờ | 58 phút |

- **Động vật tự đến** ([12 §3](12-moi-truong-song.md#3-động-vật-tự-đến--q29--2-con-chờ-2-giờ-mô-phỏng)): môi trường đủ điều kiện liên tục **7 phút** thì một cặp đến (trước: 2 giờ mô phỏng ≈ 1.2 phút).
- **Cây tán qua từng bậc** ([15 §1.2](15-sinh-dong-va-phan-hoi.md#12-gieo)): 5 bậc trong 1.4 giờ, mỗi bậc **~17 phút**, khoảng một bậc mỗi lần liếc. Mục tiêu "một bước lớn mỗi ~3 phút" của 15 §0.3 đổi theo.
- **Sinh khí**: thu nhập mỗi phút thật bằng ~1/6 hiện tại, giá gieo và mưa giữ nguyên. Hiện Sinh khí đang dư hàng chục nghìn ([12 §6](12-moi-truong-song.md#6-hệ-quả)); mô hình cho thấy người chơi vẫn đủ tiền tới kết (§5).
- Mọi số khác của `balance.json` theo cùng tỉ lệ ×1/6 (đói no, săn, bốc hơi, phân huỷ, mưa tự nhiên…), trừ phần hành vi ở §2.1.

## 4. Nhịp cho người liếc
Các mục này đo cùng với §3 ở §5.

### 4.1 Loài mới đến lần lượt (✅ Q59)
✅ Một loài **chưa từng xuất hiện** trong thế giới chỉ được đến khi loài mới trước đó đã đến **≥ 15 phút**. Tới sớm hơn thì cặp đó chưa đến: đồng hồ chờ của nó về 0 và đếm lại. Chỉ áp dụng cho **lần đầu** của mỗi loài (✨ Loài mới); cặp tự đến đoạn biome mới, con non, cân bằng quần thể không đổi. 15 phút = lần liếc ngắn nhất, nên mỗi lần liếc có nhiều nhất ~1 loài mới.

### 4.2 Bong bóng sống 30 phút (✅ Q60)
✅ ✨ và 🐣 sống **30 phút** (trước 8), mờ dần trong **5 phút cuối**. Giới hạn hiển thị giữ như cũ (tối đa 3 trong khung nhìn, 1 mỗi vùng), nên sống lâu không làm dải đất rối hơn.

### 4.3 Mây 💧 (✅ Q61)
Mây chờ sống 10 giây là cho người **đang nhìn**. Người liếc vẫn thấy vùng khô qua cây ngả vàng, và vẫn kéo mưa được.
- ✅ **A:** giữ nguyên.
- ~~**B:** mây chờ quay lại mỗi ~3 phút khi vùng còn khô (tối đa 30 phút). Dễ thành cảm giác bị nhắc việc (lý do Q39 đã giãn 💧).~~

### 4.4 Mùa Đông là quãng nghỉ (✅ Q62)
Không loài nào đến vào mùa Đông (12 §3). Mùa Đông dài 1 giờ, tức 2–4 lần liếc không có loài mới. ✅ Coi đây là **quãng nghỉ có chủ ý**, không thêm luật: tuyết phủ, ao đóng băng, cây trơ cành ([11 §2.6](11-nhip-va-tang-tan.md#26-hình)), rồi Xuân về thì tuyết tan và loạt con non đầu mùa.

## 5. Kết quả đo
`glancesim.py` với `balance.json` đã chốt (16.7 bước / phút, mùa 1 000 bước, cây Thảm / Bụi lớn nhanh, loài mới cách 15 phút, bong bóng 30 phút), **16 seed**. Chuỗi lặng không tính mùa Đông (§4.4).

```bash
python3 Docs/GDD/sim/glancesim.py survey 16 every=3,15,30 hours=16
```

> ↻ **2026-10-28, sửa đo:** bản trước của mục này (đo ở 17 bước / phút, kết ~6.1 giờ cho mọi nhịp ghé) **sai**: người chơi mô hình của `biomesim.py` chỉ ghé ở bước kiểm tra định kỳ (mỗi 30 bước), nên nhịp ghé không chia hết cho 30 thì thực ra ghé thưa hơn (ở 17 bước / phút cả ba nhóm đều là ~30 phút). `glancesim.py` nay cho người chơi ghé đúng nhịp.

### 5.1 Nhịp
| | Ghé 3 phút | **Liếc 15 phút** | **Liếc 30 phút** |
|---|---|---|---|
| Kết game: trung vị (ngắn nhất – dài nhất) | 4.7 giờ (3.1–12.2) | **5.1 giờ** (4.5–7.0) | **6.5 giờ** (5.1–10.1) |
| Kết được (trong 16 giờ) | 16/16 | 16/16 | 16/16 |
| Số lần liếc tới kết | 95 | **21** | 13 |
| Lần liếc có chuyện lớn | 14% | 50% | 71% |
| … có chuyện lớn hoặc đất lan ≥ 3 cột | 23% | 62% | 73% |
| Chuyện lớn dồn nhiều nhất trong một lần liếc | 2 | 3 | 4 |
| Chuỗi lặng dài nhất (trừ Đông) | 45 phút | 45 phút | 30 phút |
| Bong bóng được thấy | 100% | 100% | 100% |

- ⚠️ **Ngắn hơn mục tiêu một chút:** slice chốt ~6–8 giờ (§0), đo được 5.1 giờ với người liếc 15 phút và 6.5 giờ với người liếc 30 phút. Chưa chỉnh số; chờ chơi thử.
- Ghé chăm chỉ nhanh hơn một chút (4.7 so với 5.1–6.5 giờ): game đi theo năm tháng của nó, người chơi chăm sóc chứ không tua.
- Kết game rơi vào **năm thứ hai**: năm đầu dựng đồng cỏ, ao, rừng; qua Đông thì Sóc, Giun đến, Vườn mở, Cây Thế Giới nở hoa.

Ví dụ seed 2, liếc 15 phút (bỏ các lần liếc không có gì):

```
  30'       Ong
  45'       Ao Sen thức dậy · Cá · rừng thành hình
  60' Hạ    Thỏ
  75'       Ao Đông thức dậy
  90'       Cáo
 105'       Hươu · Ao Sậy thức dậy
 120' Thu   Diệc
 150'       Sói · đất hoang đã phủ kín
 180' Đông  (nghỉ: tuyết, ao đóng băng)
 240' Xuân
 270'       Sóc
 285'       Giun · Khu Vườn Thiêng mở
 315'       Cây Thế Giới nở hoa
```

- ⚠️ **Mở đầu chậm:** loài đầu tiên đến ở phút **~20–30**; lần liếc đầu chỉ thấy cỏ mọc. Phiên đầu của người mới cài thường là ngồi xem, nên quãng này cần phần hình của 15 §1–2 gánh, hoặc một luật mở đầu riêng (chưa đề xuất, chờ chơi thử).

### 5.2 Cân bằng
Quần thể lúc kết (trung vị, liếc 15 phút): Thỏ 52 · Cá 26 · Hươu 20 · Cáo 6 · Diệc 4 · Sói 6 · Sóc 6 · Ong 16 đàn. Mọi loài có mặt, không loài nào bị xoá sổ. Mỗi ngày mô phỏng (1 440 bước) ~14 con chết đói, ~19 con bị săn.

Khác với trước: một mùa nay ngắn hơn so với vòng đời (thỏ sống ~3 mùa, trước ~1 mùa), nên mùa Đông (không sinh sản, cây lớn chậm) đến dày hơn trong đời mỗi con. Mô hình cho thấy các quần thể vẫn qua Đông được.

## 6. Việc của Tech Doc
- **Hai nhịp** ([Tech Doc 12 §1](../Tech%20Doc/12-thoi-gian-that.md#1-hai-nhịp-hành-vi-và-sinh-thái--t6)): sinh thái đi mỗi bước **3.6 giây** (16.7 bước mỗi phút, §5), hành vi (đi, rượt, trốn, động tác) giữ tick 0.6 giây như hiện tại (§2.1). Python chưa có tick hành vi, nên luật săn của 14 phải đo lại bằng code.
- `balance.json`: bỏ `time.simMinutesPerRealMinute`; đổi các thời gian sang đơn vị thật (hoặc giữ đơn vị bước, ghi rõ 1 bước = 60/17 giây); thêm hệ số lớn nhanh ×3 cho tầng Thảm / Bụi; `time.seasonMinutes` 60 phút; `moments.lifetimeMinutes` 30, `moments.fadeLastMinutes` 5; thêm `biomeModel.arrival.newSpeciesGapMinutes` 15.
- Sửa GDD [11 §1](11-nhip-va-tang-tan.md#1-nhịp-100) (bảng thời gian, mùa 1 giờ), [15 §0.3 và §1.2](15-sinh-dong-va-phan-hoi.md) (bậc cây tán ~17 phút), [15 §3.3](15-sinh-dong-va-phan-hoi.md#33-thời-gian-phút-thật), [12 §3](12-moi-truong-song.md#3-động-vật-tự-đến--q29--2-con-chờ-2-giờ-mô-phỏng), [05 §5](05-mo-rong-the-gioi.md#5-mục-tiêu-cuối-vì-là-game-premium) (slice ~6 giờ); ghi chú trỏ về đây.
- Giới hạn của mô hình: người chơi mô hình làm cố định một lượt lấn đất mỗi mép mỗi lần ghé; không có giới hạn "3 trong khung nhìn"; không mô hình mây 💧 10 giây.
