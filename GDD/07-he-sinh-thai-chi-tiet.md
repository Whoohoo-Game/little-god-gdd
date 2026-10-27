# 07 · Hệ sinh thái: đặc tả chi tiết (cho prototype)

> Phạm vi: **một vùng đồng cỏ 48 cột** với 7 loài: Cỏ, Hoa dại, Mâm xôi, Giun, Thỏ, Ong, Cáo.
> Mọi con số dưới đây đã chạy qua mô hình [`sim/ecosim.py`](sim/ecosim.py) (20 seed × 96 giờ). Khi đổi số ở đây, phải sửa trong mô hình và chạy lại (xem §9).
> Trạng thái: 💡 đề xuất đã kiểm chứng bằng mô hình, chờ thử cảm giác trong prototype Unity.
> ⚠️ **Đổi luật 2026-10-23** (cân bằng tự nhiên, bỏ Chúc phúc): §6.2, §6.3, §7.3, §7.4 và §9 đã cập nhật. Các kết quả ở §1 và §8 được **đo bằng luật cũ** (sức chứa ×0.7, đói thì bỏ đi); kết quả với luật mới nằm ở [08 §7.3](08-nhieu-vung-va-ao.md#73-cân-bằng-tự-nhiên-ăn-trụi-chết-đói-thú-săn). `ecosim.py` và C# `EcoWorld` vẫn chạy luật cũ cho tới giai đoạn Technical Doc.

## 1. Mục tiêu nhịp chơi (pacing)
Các con số được chỉnh để đạt các mục tiêu sau. Đây là thứ cần giữ, còn con số cụ thể có thể đổi.

| Mục tiêu | Kết quả mô hình (người chơi ghé mỗi 30 phút) |
|----------|----------------------------------------------|
| Mời được loài động vật đầu tiên trong ≤ 3 giờ | Giun ~1.0h, **Thỏ ~2.2h** |
| Đủ chuỗi thức ăn đồng cỏ (4 vai trò) trong một buổi làm việc | Ong ~4.0h, **Cáo ~5.4h** |
| Hệ sinh thái sống qua cả năm mà không cần can thiệp | ✅ Không loài nào biến mất vĩnh viễn kể cả khi người chơi không làm gì |
| Chăm sóc thì được thưởng rõ ràng | Chăm (gọi mưa khi khô): **+65% Sinh khí** so với bỏ mặc |
| Không có con số tăng vọt | Tối đa 26 thỏ, 3 cáo trên 48 cột; tỉ lệ thỏ:cáo trung bình 5:1 |
| Hạn hán là *khoảnh khắc*, không phải thảm hoạ | Cỏ ngủ khô vàng úa nhiều giờ trước khi ảnh hưởng động vật |

## 2. Đơn vị & tick
- Mọi tốc độ trong tài liệu này tính **theo phút thật**. Game chạy tick 1 giây thì chia cho 60.
- **Tick môi trường:** 1 phút. **Tick sinh vật:** 1 giây (di chuyển, hoạt ảnh); logic đói/sinh sản có thể chạy mỗi phút.
- Mọi chỉ số môi trường nằm trong khoảng 0–100.

## 3. Môi trường

### 3.1 Độ ẩm 💧
| Tham số | Xuân | Hạ | Thu | Đông |
|---------|------|----|-----|------|
| Bốc hơi (/phút) | 0.05 | 0.10 | 0.06 | 0.02 |
| Xác suất mưa tự nhiên (/giờ) | 30% | 6% | 15% | 5% |
| Hệ số lớn của cây (cả hút nước) | ×1.25 | ×1.0 | ×0.8 | ×0.3 |
| Hệ số sinh sản động vật | ×1.5 | ×1.0 | ×0.7 | ×0.2 |

- **Mưa** (tự nhiên hoặc quyền năng): +30 cho các cột bị phủ.
- **Tuyết tan:** đầu mỗi mùa Xuân (theo mùa mô phỏng, [11 §1.1](11-nhip-va-tang-tan.md#11-đồng-hồ)), mọi cột +40. Mỗi năm thế giới được "reset nước" một lần.
- **Khuếch tán:** mỗi phút, mỗi cột nhích 5% về phía trung bình của 2 cột bên cạnh.
- Cây hút nước theo bảng loài, nhân với hệ số lớn của mùa.

> Hệ quả thiết kế: không gọi mưa thì **mùa hạ khô hạn sau khoảng 10–15 giờ**. Đây là khoảnh khắc "gọi mưa" chính của game.

### 3.2 Đất màu 🌱 & Mùn 🍂
- Mỗi phút, Mùn chuyển thành Đất màu theo tỉ lệ **2%** của lượng Mùn (cột có giun: **6%**), hiệu suất **80%**.
- Cây hút Đất màu theo bảng loài. Sinh vật chết để lại Mùn (bảng loài).
- Vùng mới hồi sinh bắt đầu với Đất màu 35, Mùn 10, Độ ẩm 50.

### 3.3 Ánh sáng ☀️
- Mặc định 100. Cột có cây bụi trưởng thành thì tầng thảm chỉ nhận **70**. Dưới tán cây gỗ (tầng 2), tầng thảm và tầng bụi nhận **55**: xem [11 §2](11-nhip-va-tang-tan.md#2-tầng-tán-cây-gỗ-có-vai-trò).

## 4. Độ phù hợp (q)
Mỗi cây có **độ phù hợp q ∈ [0, 1]** với cột của nó. q quyết định tốc độ lớn, sức khoẻ, ra hạt và khả năng nảy mầm.

```
q = q_ẩm × q_màu × q_sáng

q_ẩm:  0 nếu ẩm < min
       tăng tuyến tính từ min → lo
       1 trong [lo, hi]
       giảm tuyến tính từ hi → max, nhưng không dưới 0.5   ← quá ẩm chỉ làm chậm, không giết
q_màu: tăng tuyến tính từ (màu_min × 0.5) → màu_min, sau đó = 1
q_sáng: tăng tuyến tính từ (sáng_min × 0.5) → sáng_min, sau đó = 1
```

## 5. Thực vật

### 5.1 Vòng đời
1. **Hạt → Mầm:** khi hạt rơi vào ô trống của đúng tầng, nảy mầm với xác suất = q tại cột đó.
2. **Mầm → Trưởng thành:** tiến độ += `q × hệ số mùa / thời gian lớn` mỗi phút.
3. **Trưởng thành:** sinh Sinh khí, ra hạt (trừ mùa Đông), là thức ăn.
4. **Già:** hết tuổi thọ thì chết và để lại Mùn; nếu q > 0.3, một cây non cùng loài mọc lại ngay tại chỗ. Nhờ vậy thảm cỏ không chết hàng loạt.

### 5.2 Sức khoẻ, héo và ngủ khô
- Máu cây (0–100) thay đổi **(q − 0.35) × 1.0** mỗi phút. Ở q = 0, cây héo từ đầy máu đến cạn mất khoảng **4h45**, đủ lâu để người chơi kịp thấy và cứu.
- 🎨 Hiển thị: máu < 60 thì cây ngả vàng, máu < 30 thì vàng úa và rũ xuống.
- **Cây lâu năm** (Cỏ, Mâm xôi) cạn máu thì **ngủ khô** chứ không chết: chuyển màu nâu, không hút nước, không sinh Sinh khí, không ra hạt. Khi q ≥ 0.5, máu hồi 0.5/phút; đạt 30 thì thức dậy (khoảng 1 giờ sau mưa).
- **Cây một năm** (Hoa dại) cạn máu thì chết, nhưng hạt còn trong đất (xem 5.4).

### 5.3 Ra hạt & thụ phấn
- Mỗi cây trưởng thành ra hạt với xác suất `số hạt/giờ ÷ 60 × q` mỗi phút.
- Hạt rơi cách 1..tầm hạt cột, sang trái hoặc phải ngẫu nhiên.
- **Thụ phấn:** cây có hoa nằm trong vùng hoạt động của ong thì ra hạt **×2**.

### 5.4 Hạt ngủ trong đất (seed bank)
- Mỗi cột ghi nhớ những loài **đã từng trưởng thành** ở đó.
- Ô trống của cột đó nảy mầm lại loài cũ với xác suất **(1/180) × q** mỗi phút, tức khoảng 3 giờ khi điều kiện tốt.
- Đây là cơ chế đảm bảo lời hứa **"không có vòng xoáy chết"**: một vùng từng xanh sẽ luôn xanh lại.

### 5.5 Bảng loài thực vật
| | Cỏ | Hoa dại | Mâm xôi |
|---|---|---|---|
| Tầng | Thảm | Thảm | Bụi |
| Thời gian lớn | 20 phút | 40 phút | 2 giờ |
| Tuổi thọ | 1 ngày | 1 ngày | 4 ngày |
| Lâu năm (ngủ khô)? | Có | Không | Có |
| Độ ẩm min / lo / hi / max | 15 / 30 / 85 / 100 | 25 / 40 / 80 / 100 | 30 / 45 / 85 / 100 |
| Đất màu tối thiểu | 10 | 25 | 35 |
| Ánh sáng tối thiểu | 40 | 60 | 40 |
| Hạt/giờ · tầm hạt | 3.0 · 2 cột | 1.5 · 3 cột | 0.4 · 2 cột |
| Hút nước · đất màu (/phút) | 0.02 · 0.004 | 0.025 · 0.006 | 0.04 · 0.008 |
| Mùn khi chết | 8 | 6 | 20 |
| Có hoa (cần thụ phấn) | Không | Có | Có |
| Sinh khí/phút | 0.05 | 0.10 | 0.15 |
| Đặc biệt | Là thức ăn: sinh khối 0–100, mọc lại 0.6 × q × mùa /phút | Thức ăn cho ong | Thỏ đứng cạnh thì khó bị bắt; quả nuôi cáo vào mùa hạ và thu |

## 6. Động vật

### 6.1 Độ no & kiếm ăn
- **Độ no** 0–100. Ăn đủ nhu cầu trong phút đó thì **+0.9**; luôn trừ **0.4** mỗi phút. Không có gì ăn thì từ 80 về 10 mất khoảng **3 giờ**.
- **Kiếm ăn:** khi độ no < 60, con vật đi về phía cột có nhiều thức ăn nhất trong tầm **12 cột**. Khi no thì đi lang thang. ↻ **Thay bằng** (2026-10-24) đi theo bầy / lãnh thổ, đi tới đích rồi nghỉ, và nhịp sinh sản chậm hơn: [13](13-bay-dan-va-sinh-san.md).
- **Cỏ ngủ khô vẫn ăn được**, nhưng chỉ có giá trị **50%** và không mọc lại.

### 6.2 Sinh sản & sức chứa
Một con sinh sản khi thoả **tất cả** các điều kiện:
- độ no > 70, đủ tuổi trưởng thành, hết thời gian chờ;
- có ít nhất một con cùng loài trong vùng sống;
- tung xác suất thành công `0.5 × hệ số mùa × chỗ trống` (mỗi phút).

**Chỗ trống** = `1 − số con cùng loài trong vùng / sức chứa`:
- **Thú ăn cỏ:** sức chứa = Σ(tốc độ cỏ mọc lại *thực tế* trong vùng) × **1.0** ÷ nhu cầu. Dùng tốc độ thực tế (có q và mùa). Không chừa biên an toàn, nên khi sang Đông hoặc gặp hạn, cỏ mọc chậm lại và đàn đang có trở thành quá đông: chúng ăn trụi cỏ rồi chết đói. Đây là chu kỳ tự nhiên mong muốn (✅ 2026-10-23, xem 08 §7.3). Luật cũ dùng hệ số 0.7 để không bao giờ vượt.
- **Thú săn:** sức chứa = số con mồi trong vùng ÷ **8**.
- **Thụ phấn:** sức chứa = số cây có hoa trong vùng ÷ **6**.

### 6.3 Chết đói & quay lại
- ✅ Khi độ no ≤ 10, con vật **chết đói**: nằm xuống, mờ dần, để lại Mùn bằng lượng Mùn khi chết (✅ 03 §3). Áp dụng cho mọi loài, kể cả thú săn khi hết mồi. (Luật cũ: bỏ đi, không để lại gì.)
- Sinh vật **chết** vì già, bị săn hoặc chết đói.
- **Loài đã khám phá tự quay lại miễn phí**: khi điều kiện mời của loài đó đạt **liên tục 2 giờ**, và loài đang vắng hẳn **hoặc chỉ còn 1 con**, thì **một cặp** đi vào từ cùng một mép.
- Điều kiện mời chỉ đếm cây **trưởng thành, không ngủ khô**. Nếu không, con vật sẽ quay lại giữa mùa hạn rồi lại bỏ đi ngay.

### 6.4 Săn mồi
- Thú săn bắt đầu săn khi độ no < 60. Mỗi phút có xác suất bắt = **0.25 × độ hiếm × nơi trú ẩn**:
  - **Luật cặp cuối:** không săn khi trong vùng chỉ còn **≤ 2** con mồi.
  - **Độ hiếm** = min(1, số con mồi trong vùng ÷ 6).
  - **Nơi trú ẩn:** con mồi đứng cạnh bụi mâm xôi trưởng thành thì ×0.5.
- Bắt được thì độ no = 100, con mồi để lại 2 Mùn.
- **Ăn tạp:** vào mùa hạ và thu, cáo đói đứng cạnh mâm xôi được +0.3 độ no/phút.
- **Mùa đông:** thú săn nằm ổ nhiều nên nhu cầu ăn **×0.5**.

### 6.5 Bảng loài động vật
| | Thỏ | Cáo | Ong (1 đàn) | Giun |
|---|---|---|---|---|
| Vai trò | Ăn cỏ | Săn mồi | Thụ phấn | Phân huỷ |
| Ăn | Sinh khối cỏ 1.5/phút | 1 thỏ / 4 giờ | Cần ≥ 3 cây có hoa trong vùng | Mùn |
| Vùng sống · tầm kiếm ăn | 5 · 12 cột | 12 · 12 cột | 6 cột | Từng cột |
| Trưởng thành | 1 giờ | 3 giờ | 4 giờ | — |
| Tuổi thọ | 2 ngày | 4 ngày | 2 ngày | — |
| Mỗi lứa · nghỉ giữa 2 lứa | 2 · 1.5 giờ | 1 · 12 giờ | 1 · 8 giờ | — |
| Sinh khí/phút (khi trưởng thành) | 0.25 | 0.60 | 0.30 | 0.04 mỗi cột |
| Mùn khi chết | 5 | 10 | 0 | — |
| Mời: điều kiện · giá | ≥ 10 cỏ sống · 60 | ≥ 6 thỏ · 200 | ≥ 4 hoa dại sống · 80 | ≥ 6 cỏ sống · 20 |

- **Giun** không mô phỏng từng con. Đây là thuộc tính của cột (có/không), tự lan sang cột bên cạnh nếu cột đó có cỏ. Thỉnh thoảng có một con giun ngoi lên để người chơi thấy.
- **Ong** là một đàn, vẽ thành 3–5 chấm bay quanh hoa. Không có hoa thì độ no giảm 0.5/phút.

## 7. Sinh khí

### 7.1 Công thức
```
Sinh khí/phút = Σ(sinh khí cơ bản) × Đa dạng × Cân bằng

Σ cơ bản = cây trưởng thành và không ngủ khô + động vật đã trưởng thành + 0.04 × số cột có giun

Đa dạng  = 1 + 0.15 × (số loài − 1) + 0.25 × (số vai trò − 1)
           vai trò: sản xuất (cây), ăn cỏ, săn mồi, thụ phấn, phân huỷ
           → đồng cỏ đủ 7 loài, 5 vai trò: 1 + 0.9 + 1.0 = 2.9

Cân bằng = 1.0
           − 1.5 × (tỉ trọng loài lớn nhất − 0.4)   nếu loài lớn nhất > 40% sinh khối
                                                    (động vật tính ×3 sinh khối)
           − 0.2   nếu có thú săn và tỉ lệ mồi:săn nằm ngoài [4, 10]
           − 0.2   nếu > 30% cột trống trơn
           + 0.2   nếu đủ 5 vai trò và không bị trừ điểm nào
           kẹp trong [0.3, 1.2]
```

### 7.2 Tốc độ tham khảo (từ mô hình)
| Thời điểm | Sinh khí/phút | Sinh khí tích luỹ |
|-----------|---------------|-------------------|
| Giờ đầu | ~0.4 | ~15 |
| 4 giờ | ~8 | ~550 |
| 8 giờ | ~26 | ~4,900 |
| 1 ngày | ~48 | ~45,000 |
| 4 ngày | 16–53 (dao động theo mùa) | ~200,000 |

### 7.3 Giá hành động (đề xuất ban đầu)
| Hành động | Giá |
|-----------|-----|
| Sinh khí khởi đầu | 40 |
| Gieo cỏ · hoa dại · mâm xôi | 5 · 10 · 25 |
| Gọi mưa | 30 |
| Mời Giun · Thỏ · Ong · Cáo | 20 · 60 · 80 · 200 |

### 7.4 Cấp thần (theo Sinh khí tích luỹ từ đầu)
| Cấp | Mốc | Thời điểm dự kiến | Mở khoá |
|-----|-----|-------------------|---------|
| 1 | 0 | Bắt đầu | Gieo hạt, Mưa, Lời mời |
| 2 | 5,000 | cuối ngày 1 | Gió, Nắng ấm |
| 3 | 50,000 | ngày 3–4 | Nắn đất |
| 4 | 250,000 | ngày 8 | Sét |

> 💡 Mốc giãn ra ngày 2026-10-23 theo mô hình nhiều vùng ([08 §12](08-nhieu-vung-va-ao.md#12-thay-đổi-kéo-theo-ở-các-tài-liệu-khác)). Thời điểm tính theo ngày lịch, app mở 8h/ngày. Mốc cũ (2k · 25k · 150k) đến quá sớm khi cả thế giới cùng sinh Sinh khí.

> Giá **hồi sinh vùng mới** và đường cong cho cả 14 vùng: xem [08 §4](08-nhieu-vung-va-ao.md#4-hồi-sinh-một-vùng).

## 8. Kết quả kiểm chứng
20 seed × 96 giờ (trọn 1 năm trong game), 48 cột, bắt đầu với 5 cỏ ở giữa.

| Chỉ số (trung bình mỗi seed) | Bỏ mặc (không gọi mưa) | Chăm (ghé 30 phút, gọi mưa khi khô) |
|------------------------------|------------------------|-------------------------------------|
| Số giờ không có thỏ (trên 90 giờ) | 22.4 | **0** |
| Số giờ không có cáo | 45.9 | **7.8** (chỉ mùa đông) |
| Thỏ trung bình · tối đa | 5.7 · 26 | 10.0 · 26 |
| Cáo trung bình · tối đa | 1.0 · 3 | 2.0 · 3 |
| Sinh khí/phút: trung vị | 18.6 | 37.7 |
| Sinh khí tích luỹ 96 giờ | ~119,000 | ~196,000 |
| Số lần gọi mưa | 0 | ~6 (khoảng 1.5 lần/ngày) |

## 9. Bài học rút ra từ mô hình
Đây là các **quy tắc thiết kế** phát hiện được khi chạy mô hình. Nên giữ chúng khi đổi số.

1. **Mọi tốc độ môi trường phải tính theo giờ, không theo phút.** Bản nháp đầu làm đất khô sạch trong 1 giờ.
2. **Quá ẩm không được giết cây cạn.** Nếu không, một trận mưa trong lúc người chơi đi họp sẽ xoá sạch đồng cỏ.
3. **Héo phải chậm** (khoảng 5 giờ) và **nhìn thấy được**. Người chơi idle cần thời gian để kịp phản ứng.
4. **Cây lâu năm ngủ khô thay vì chết**, và luôn có **hạt ngủ trong đất**. Đây là hai cơ chế giữ lời hứa "không vòng xoáy chết".
5. **Loài đã khám phá tự quay lại miễn phí.** Nếu không, mỗi lần một loài chết đói hết người chơi lại phải trả tiền mời lại. (Bản đầu kết hợp với "đói thì bỏ đi"; từ 2026-10-23 con vật chết đói, xem 08 §11 mục 5: bỏ đi che mất nhân quả "đông quá → hết cỏ → chết đói".)
6. **Con vật phải biết đi tìm thức ăn**, và **cặp quay lại phải vào cùng một mép**. Đi lang thang ngẫu nhiên làm con vật chết đói ngay cạnh đồng cỏ.
7. **Sức chứa tính theo tốc độ mọc thực tế** (có q và mùa). Dùng tốc độ lý tưởng sẽ gây bùng nổ rồi sụp đổ quá mạnh. (Bản đầu thêm hệ số an toàn 0.7; từ 2026-10-23 bỏ hệ số này để có chu kỳ ăn trụi theo mùa và để thú săn có vai trò, xem 08 §11 mục 4.)
8. **Thú săn cần luật cặp cuối, độ hiếm, nguồn ăn phụ và nghỉ đông.** Nếu không, cáo ăn sạch thỏ rồi tự chết đói.
9. **Tuổi thọ phải tính bằng ngày, không phải giờ.** Con vật sống 8 giờ làm người chơi thấy cái chết liên tục, và quần thể sụp vào mùa đông.

Chạy lại mô hình sau mỗi lần đổi số:

```bash
python3 Docs/GDD/sim/ecosim.py 96 1
```

```bash
python3 Docs/GDD/sim/ecosim.py survey rain
```

## 10. Giới hạn của mô hình & việc tiếp theo
- Mô hình chạy theo bước 1 phút; game thật dùng 1 giây cho sinh vật. Hành vi trung bình tương đương, nhưng cần kiểm tra lại trong Unity.
- Tầng tán (Sồi, Táo dại, Liễu): [11 §2](11-nhip-va-tang-tan.md#2-tầng-tán-cây-gỗ-có-vai-trò). Biome, Dương xỉ, Sóc, động vật tự đến: [12](12-moi-truong-song.md). Chưa có: chim sẻ, cháy, quyền năng Gió/Nắng. Nhiều vùng và biome Ao: xem 08.
- ✅ **Đã port sang C#:** `Assets/LittleGod/Scripts/Simulation` (assembly `LittleGod.Simulation`, không phụ thuộc Unity). Unit test ở `Assets/LittleGod/Tests/EditMode` cho kết quả khớp mô hình Python, ví dụ người chơi chăm: Sinh khí tổng 195k so với 196k. Khi đổi số trong `EcoConfig.CreateDefault()`, cập nhật cả mô hình Python và file này. ⚠️ Code C# và `ecosim.py` vẫn theo luật cũ (×0.7, bỏ đi); cập nhật trong giai đoạn Technical Doc → triển khai.
- ✅ **Đã mở rộng sang nhiều vùng:** xem [08 · Nhiều vùng & biome Ao](08-nhieu-vung-va-ao.md) và [`sim/worldsim.py`](sim/worldsim.py). Mốc cấp thần ở §7.4 đã giãn theo 08.
