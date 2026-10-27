# 09 · Khoảnh khắc: đặc tả chi tiết (vòng ngắn)

> Phạm vi: **vertical slice**: Đồng cỏ (07), Ao và hồi sinh vùng (08).
> Khái niệm ở [02 §Vòng ngắn](02-core-loop.md#vòng-ngắn-liếc-và-chạm-1060-giây). Thời gian trong file này tính bằng **phút app mở**.
> Trạng thái: 💡 đề xuất, **chưa kiểm chứng bằng mô hình**. Tần suất ở §6 là ước tính từ số liệu đã đo trong 07/08 (xem §9).

## 1. Mục tiêu
| Mục tiêu | Cách đạt |
|----------|----------|
> ↻ **2026-10-24:** mọi thời gian trong file này (thời gian sống, mờ dần, chờ lại, giãn cách, tỉ lệ mỗi phút) là **phút thật**; điều kiện sinh thái đọc từ mô phỏng chạy nhịp ×100 ([11 §1.3](11-nhip-va-tang-tan.md#13-khoảnh-khắc-và-ui)). Khám phá 🌱 có thêm Sồi, Táo dại, Liễu ([11 §2.4](11-nhip-va-tang-tan.md#24-mở-khoá--q24-khám-phá-)).

> ↻ **2026-10-27 ([15 §3](15-sinh-dong-va-phan-hoi.md#3-khoảnh-khắc-m5-rút-gọn)):** 💡 đề xuất làm trước một **bản rút gọn** (6 loại) với số mới cho nhịp ×100: số tần suất, thời gian sống, giãn cách của file này được viết cho nhịp 8 giờ/ngày nên ở slice ~1.3 giờ thật chỉ còn 2–3 khoảnh khắc.

> ↻ **2026-10-24 ([12](12-moi-truong-song.md)):** bỏ 💌 Lời mời và 🌿 Sẵn sàng hồi sinh (không còn mời, không còn hồi sinh); thêm ✨ **Loài mới** (lần đầu một loài tự đến) và ✨ **Biome mới thành hình**. Các khoảnh khắc còn lại giữ nguyên.

| Mỗi lần liếc (10–30 phút) thấy **ít nhất một điều mới** | ~2 khoảnh khắc mỗi giờ trên toàn thế giới (§6) |
| Đọc được bằng một cái liếc, không cần chữ | Mỗi loại một biểu tượng riêng; chữ chỉ hiện khi rê chuột |
| **Không làm phiền** (✅ trụ cột 3) | Không modal, không âm thanh tự phát, không nhấp nháy; giới hạn số bong bóng (§5) |
| **Bỏ qua không bị phạt** (✅ 02) | Mọi khoảnh khắc tự biến mất. Thứ quan trọng (khám phá loài, lời mời) luôn quay lại sau |
| Click là thao tác **"vuốt ve"** chính (✅ Q20) | Click có phản hồi ngay: tinh linh bay tới, lấp lánh, Sinh khí bay về khay |
| Thưởng thêm nhưng không thành bắt buộc | Phần thưởng tối đa ~5–8% Sinh khí, ngang với gọi mưa (§4) |

## 2. Ba nhóm khoảnh khắc
| Nhóm | Ý nghĩa | Click thì | Tốn Sinh khí? |
|------|---------|-----------|---------------|
| **A · Quà** | Chuyện đẹp vừa xảy ra | Nhận quà (Sinh khí, khám phá) | Không |
| **B · Lời đề nghị** | Có một việc người chơi *có thể* làm ngay | Làm việc đó bằng một click | Có, đúng giá thường |
| **C · Gợi ý** | Hệ sinh thái đang lệch, kèm hướng xử lý | Hiện một dòng gợi ý | Không |

## 3. Danh sách khoảnh khắc

### 3.1 Bảng tổng
| # | Khoảnh khắc | Nhóm | Biểu tượng | Vị trí | Tồn tại | Hồi lại |
|---|-------------|------|------------|--------|---------|---------|
| 1 | Sinh vật đến nơi mới | A | ✨ | Trên cặp vừa đến | 30 phút | Theo sự kiện |
| 2 | Con non / đàn ong mới | A | 🐣 | Trên con non | 30 phút | Theo sự kiện, có lọc |
| 3 | Hạt lạ theo gió | A | 🌱 | Hạt nằm trên một cột trống | 30 phút | 2 giờ nếu bị bỏ qua |
| 4 | Khách lạ | A | 🦋 | Trên khách, đang đi ngang | Tới khi khách rời đi (~10 phút) | Hiếm, ~1 lần/ngày lịch |
| 5 | Lời mời | B | 💌 | Trên con vật đứng ở mép đoạn biome | 30 phút | 2 giờ (✅ 04 §3) |
| 6 | Vùng đang khô | B | 💧 | Giữa vùng | Tới khi hết khô, tối đa 30 phút | 2 giờ mỗi vùng |
| 7 | Sẵn sàng hồi sinh | B | 🌿 | Mép đất hoang giáp vùng khoẻ | Chừng nào còn đủ điều kiện | — |
| 8 | Ăn trụi | C | 🍂 | Giữa đoạn biome | Tới khi hết trụi, tối đa 30 phút | 6 giờ mỗi đoạn |
| 9 | Đặt tên vùng | B (miễn phí) | 🏷️ | Phía trên vùng vừa hồi sinh | 30 phút | Không |

### 3.2 Chi tiết từng loại

**1 · ✨ Sinh vật đến nơi mới** (✅ Q19)
- **Xuất hiện:** khi một cặp sinh vật tự tìm đến một đoạn biome theo luật [08 §7.1](08-nhieu-vung-va-ao.md#71-loài-tự-tìm-đến-đoạn-biome-mới), kể cả khi quay lại sau khi chết đói hết.
- **Click:** nhận quà thường (§4). Cặp vật **vẫn ở lại dù không click**.
- Bong bóng bám theo một trong hai con.

**2 · 🐣 Con non / đàn ong mới**
- **Xuất hiện** khi có một lần sinh nở thoả **một** trong các điều kiện sau. Lọc để bầy thỏ đông không sinh bong bóng liên tục.
  - Loài là **thú săn** (Cáo, Diệc).
  - Là **lần sinh đầu tiên** của loài đó trong đoạn biome kể từ khi đoạn được hồi sinh.
  - Loài đang **hồi phục**: đoạn có ≤ 4 con cùng loài trước lần sinh này.
  - **Ong chia đàn** ([08 §7.2](08-nhieu-vung-va-ao.md#72-ong-chia-đàn)): đàn mới bay tới chỗ mới.
- **Click:** nhận quà thường.
- Lứa nhiều con (thỏ 2, cá 3) chỉ có một bong bóng.

**3 · 🌱 Hạt lạ theo gió**
Đây là cách **khám phá thực vật** trong slice (✅ 04 §3: "gió mang hạt lạ tới"). Khi bắt đầu game chỉ biết Cỏ; Bèo và Lau sậy được biết khi hồi sinh ao đầu tiên (08 §4.2).

| Hạt | Xuất hiện khi | Rơi ở đâu |
|-----|---------------|-----------|
| Hoa dại | ≥ 10 cỏ sống trên toàn thế giới | Cột trống tầng Thảm, độ phù hợp q > 0.5 |
| Mâm xôi | ≥ 20 cỏ sống | Cột trống tầng Bụi, q > 0.5 |
| Sen | Có một ao với ≥ 3 bèo sống | Cột nước trống tầng Bụi |

- Các ngưỡng này **trùng với lúc người chơi mô hình gieo** ở 07/08, nên nếu người chơi click kịp thì nhịp đã kiểm chứng không đổi.
- **Click:** loài được **khám phá** (thêm vào Sổ tay, hiện nút gieo trong khay thần), và hạt **nảy mầm ngay tại chỗ, miễn phí**.
- **Bỏ qua:** hạt bị gió thổi đi; 2 giờ sau một hạt khác cùng loài lại tới. Không bao giờ mất hẳn cơ hội khám phá.
- **Hạt quà** (sau khi đã khám phá): thỉnh thoảng gió mang tới một hạt của loài đã biết, rơi vào cột phù hợp. Click thì nảy mầm miễn phí. Tối đa 1 hạt quà mỗi 3 giờ.

**4 · 🦋 Khách lạ** (03 §6 "Sinh vật lạ ghé qua")
- **Xuất hiện:** mỗi đoạn biome đang **Cân bằng** (Sức khoẻ ≥ 85 ở mọi vùng trong đoạn) có xác suất **1/480 mỗi phút** (≈ 8 giờ một lần) có một khách lạ đi ngang. Toàn thế giới tối đa 1 khách mỗi 4 giờ.
- Khách **không thuộc hệ sinh thái**: không ăn, không bị săn, không ảnh hưởng mô phỏng. Khách đi ngang đoạn trong ~10 phút rồi rời khỏi mép.
- **Click:** nhận **quà lớn** (§4), và lần đầu gặp loài khách đó thì thêm vào trang "Khách ghé thăm" của Sổ tay.
- Slice có 2 khách (💡 tên tạm, đổi được): **Hươu sao** (đồng cỏ, ban ngày) và **Rùa đầm** (ao). Bản đầy đủ thêm khách theo biome.

**5 · 💌 Lời mời** (✅ 04 §3)
- **Xuất hiện:** khi một loài động vật chưa khám phá đạt điều kiện mời (07 §6.5, 08 §6.3), một con của loài đó **đi lạc vào mép đoạn biome** nơi điều kiện đạt rõ nhất.
- **Click:** nếu đủ Sinh khí thì trả giá mời và loài được thêm vào Sổ tay. Nếu thiếu, bong bóng mờ đi và hiện số Sinh khí còn thiếu khi rê chuột; con vật vẫn đứng chờ cho tới hết 30 phút.
- **Bỏ qua:** con vật đi mất; 2 giờ sau quay lại nếu điều kiện vẫn đạt.

**6 · 💧 Vùng đang khô**
- **Xuất hiện:** độ ẩm trung bình các cột đất của vùng < **25**, **và** ≥ 3 cây trong vùng đã ngả vàng (máu < 60, 07 §5.2). Như vậy chỉ hiện khi người chơi *nhìn thấy* cây vàng, không hiện chỉ vì con số.
- **Click:** gọi mưa ngay giữa vùng (phủ 7 cột, giá thường 30). Thao tác kéo mưa bình thường vẫn dùng được.
- **Tự hết:** khi độ ẩm trung bình ≥ 40 (mưa tự nhiên hoặc người chơi), hoặc sau 30 phút. Sau đó vùng này không hiện lại trong 2 giờ.

**7 · 🌿 Sẵn sàng hồi sinh** (08 §4)
- **Xuất hiện:** một vùng đất hoang ở rìa giáp vùng Khoẻ (≥ 60). Mép đất hoang phát sáng xanh mờ, kèm một chiếc lá nhỏ.
- **Rê chuột:** giá hiện tại, phần đã được giảm (🍃 −x%), và Sức khoẻ vùng kề.
- **Click:** đủ Sinh khí thì hồi sinh (08 §4.2) rồi chuyển sang khoảnh khắc 🏷️. Thiếu thì hiện số còn thiếu.
- Đây là **trạng thái**, không phải sự kiện, nên không có thời gian tự biến mất. Nó chỉ hiện ở chỉ báo ngoài màn hình **hai lần**: lúc mới đủ điều kiện, và lúc vừa đủ Sinh khí.

**8 · 🍂 Ăn trụi** (08 §7.3)
- **Xuất hiện:** đoạn biome đang bị ăn trụi (> 50% cột cỏ/bèo dưới 20 sinh khối hoặc đang ngủ khô), **và** ≥ 3 thú ăn cỏ đang đói (độ no < 60). **Không hiện vào mùa Đông**, vì cỏ thưa mùa Đông là bình thường.
- **Click / rê chuột:** hiện **một dòng gợi ý** trong 5 giây, chọn theo thứ tự:
  1. Thú săn của loài đó chưa khám phá → *"Ở đây cần một loài săn mồi."*
  2. Đã khám phá nhưng vắng mặt ở đoạn này → *"Cáo sẽ sớm tìm đến khi có đủ thỏ."* (luật 08 §7.1)
  3. Đất đang khô → *"Cỏ cần mưa để mọc lại."*
  4. Còn lại → *"Gieo thêm cỏ, hoặc để thiên nhiên tự cân bằng."*
- Không có quà, không tốn gì. Không hiện ở chỉ báo ngoài màn hình (không thúc ép).

**9 · 🏷️ Đặt tên vùng** (✅ 05 §3, Q16)
- **Xuất hiện:** ngay sau khi một vùng hồi sinh. Một nhãn gỗ nhỏ với tên gợi ý ngẫu nhiên, theo loại vùng (ví dụ "Đồi Gió", "Ao Sen").
- **Click:** sửa tên ngay trên nhãn, tối đa 16 ký tự, Enter để lưu. **Bỏ qua:** giữ tên gợi ý. Sửa lại được sau trong Sổ tay.

## 4. Phần thưởng
```
Quà thường = max(5, Sinh khí/phút hiện tại × 3)      ← ✨ 🐣 🌱(hạt quà)
Quà lớn    = max(20, Sinh khí/phút hiện tại × 20)    ← 🦋
```
- Tính theo tốc độ hiện tại nên quà luôn có ý nghĩa, dù ở giờ đầu hay ngày thứ 15.
- 🌱 lần khám phá không cho Sinh khí: phần thưởng là loài mới cộng một cây miễn phí.
- **Ước tính tổng** (chưa kiểm chứng): ~8 quà thường + ~1 quà lớn mỗi ngày lịch (§6), tức ~44 phút Sinh khí trên 480 phút mở app, khoảng **+9% Sinh khí** nếu click hết, ~4–5% nếu click một nửa. Mức này ngang với lợi ích của việc gọi mưa (+8%, 08 §10).
- Mọi phần thưởng bay về khay thần thành một vệt sáng nhỏ. Không hiện số nổi lên giữa màn hình.

## 5. Hiển thị & giới hạn

### 5.1 Hình thức
- Bong bóng là sprite pixel **12×12** (vẽ ở tỉ lệ 2×, vùng click tối thiểu **20×20 pt**), nổi lên xuống nhẹ (biên độ 1px, chu kỳ 2 giây). **Không nhấp nháy.**
- Hiện dần trong 1 giây; **trong 3 phút cuối đời** thì mờ dần (độ trong suốt 100% → 40%), để người chơi liếc biết "sắp đi".
- Nhóm C dùng màu nhạt hơn nhóm A/B, đọc như một ghi chú chứ không phải lời gọi.
- **Rê chuột:** hiện một dòng chữ ngắn (tên loài / việc cần làm / giá). Thời gian sống **tạm dừng** khi chuột đang ở trên bong bóng.
- **Click:** tinh linh bay tới (✅ 04 §0, ~0.3 giây) → lấp lánh → hiệu ứng riêng (mầm nhú lên, mưa rơi…). Âm thanh chỉ phát ở bước này (✅ 01: âm thanh chỉ khi người chơi chủ động click).

### 5.2 Giới hạn để không rối
| Luật | Giá trị |
|------|---------|
| Tối đa bong bóng **trong khung nhìn** cùng lúc | 3 (thừa thì ẩn bớt theo thứ tự ưu tiên; khi một cái mất thì cái bị ẩn hiện lại) |
| Tối đa mỗi **vùng** | 1 |
| Khoảng cách giữa 2 khoảnh khắc **nhóm A mới** trên toàn thế giới | ≥ 10 phút. Sự kiện tới sớm hơn thì **bỏ**, không xếp hàng (ngoại trừ 🌱 lần khám phá: chờ tới lượt) |
| Khi tắt app | Không tích luỹ. Mở lại không có khoảnh khắc nào đang chờ (✅ 02: không có bản tóm tắt) |

**Thứ tự ưu tiên** (cao → thấp): 🌿 Sẵn sàng hồi sinh → 💌 Lời mời → 🌱 Hạt lạ (khám phá) → 🦋 Khách lạ → 💧 Vùng khô → 🏷️ Đặt tên → 🐣 Con non → ✨ Đến nơi mới → 🌱 Hạt quà → 🍂 Ăn trụi.

## 6. Tần suất ước tính
Ước tính cho app mở 8h/ngày, khi thế giới đã hồi sinh được nửa (sau ~ngày 6):

| Khoảnh khắc | Mỗi ngày lịch | Nguồn ước tính |
|-------------|---------------|----------------|
| ✨ Đến nơi mới | ~2 | Đo được ở 08 §7.1 (34 lần / 16 ngày) |
| 🐣 Con non (đã lọc) | ~3–5 | Ước tính: lứa của cáo/diệc + lần sinh đầu ở vùng mới + đàn ong mới |
| 🌱 Hạt quà | ~2 | Giới hạn 1 mỗi 3 giờ |
| 🦋 Khách lạ | ~1 | 1/480 mỗi phút mỗi đoạn Cân bằng, tối đa 1 mỗi 4 giờ |
| 💧 Vùng khô | ~2–3 | Mô hình gọi mưa ~3–5 lần/ngày, nhiều lần trùng nhau |
| 🍂 Ăn trụi | ~1–2 | Hồi 6 giờ mỗi đoạn, không hiện mùa Đông |
| 💌 Lời mời · 🌱 khám phá · 🌿 hồi sinh · 🏷️ tên | rải rác | 6 lời mời + 6 hạt khám phá (3 cây cũ + 3 cây tán) + 9 lần hồi sinh trong cả game |
| **Tổng** | **~12–16**, tức **~1.5–2 mỗi giờ** | Đúng mục tiêu "mỗi lần liếc thấy một điều mới" |

> Ngày đầu chơi ít khoảnh khắc hơn (thế giới nhỏ), nhưng bù bằng chuỗi lời mời và hạt khám phá dày đặc: Giun, Thỏ, Hoa dại, Ong, Cáo, Mâm xôi trong ~6 giờ đầu.

## 7. Chỉ báo ngoài màn hình (05 §2)
- **Nút ◀ / ▶:** khi có khoảnh khắc nhóm A hoặc B ở phía đó ngoài khung nhìn, nút hiện **biểu tượng của khoảnh khắc ưu tiên cao nhất** phía đó (thu nhỏ 8×8), kèm một chấm nhỏ nếu có từ 2 khoảnh khắc trở lên.
  - Nhóm C (🍂) **không** hiện ở đây.
  - 🌿 chỉ hiện hai lần như §3.2 mục 7.
  - Biểu tượng tự tắt khi khoảnh khắc hết hạn hoặc khi người chơi cuộn tới.
- **Bản đồ mini** (trong khay thần): mỗi khoảnh khắc A/B là một chấm sáng 1 pixel ở cột tương ứng. Click bản đồ thì nhảy tới đó (05 §2).
- **Chế độ theo dõi** (✅ tắt mặc định): khi bật, khung nhìn chỉ trượt tới khoảnh khắc **nhóm A**, tối đa 1 lần mỗi 10 phút, và chỉ khi chuột không ở trên dải đất.
- **Khi app bị ẩn tạm** (✅ 02, menu bar / system tray): biểu tượng tray **không** đổi theo khoảnh khắc. Đây là ứng dụng chạy nền; không có badge, không có thông báo hệ điều hành.

## 8. Cài đặt liên quan
Toàn bộ cài đặt của slice ở [10 §9](10-giao-dien.md#9-cài-đặt-tối-giản).

| Cài đặt | Mặc định | Ghi chú |
|---------|----------|---------|
| Hiện gợi ý (nhóm C) | Bật | Tắt thì chỉ còn nhóm A và B |
| Chỉ báo ngoài màn hình | Bật | |
| Chế độ theo dõi | Tắt | ✅ Q12 |

## 9. Kiểm chứng cần làm
- **Thêm khoảnh khắc vào `worldsim.py`** (khi bắt đầu giai đoạn kiểm chứng slice): đếm tần suất thật từng loại, đo khoảng trống dài nhất không có khoảnh khắc nào, và đo ảnh hưởng của phần thưởng lên ngày kết game (giả định: người chơi click 50% và 100%).
- Tiêu chí đạt: (1) trung bình ≥ 1.5 khoảnh khắc mỗi giờ sau ngày 2; (2) không có khoảng 45 phút nào trống hoàn toàn khi thế giới ≥ 3 vùng; (3) click hết thì ngày kết sớm hơn không quá 10%.
- **Chơi thử trong prototype:** 3 bong bóng trong khung nhìn có rối không; 30 phút có đủ dài với người liếc mỗi 30 phút không.
