# 03 · Hệ sinh thái (mechanic trung tâm)

Đây là "động cơ" của game. Mục tiêu: **đủ đơn giản để người chơi đoán được nguyên nhân và kết quả, đủ phong phú để sinh ra bất ngờ.**

> File này mô tả **khái niệm**. Số liệu, công thức và kết quả kiểm chứng nằm ở [07 · Đặc tả chi tiết](07-he-sinh-thai-chi-tiet.md).

## 1. Không gian: các cột đất
💡 Thế giới là một dãy **cột** (column) xếp từ trái sang phải. Mỗi cột rộng 1 đơn vị (32pt), nên một màn hình 1512pt có khoảng 47 cột.

Mỗi cột có các **chỉ số môi trường** (0–100):

| Chỉ số | Ý nghĩa | Tăng khi | Giảm khi |
|--------|---------|----------|----------|
| 🌱 **Đất màu** (Fertility) | Dinh dưỡng cho cây | Nấm/giun phân huỷ xác hữu cơ | Cây hút dinh dưỡng |
| 💧 **Độ ẩm** (Moisture) | Nước trong đất | Mưa, gần nước | Nắng, cây hút |
| ☀️ **Ánh sáng** (Light) | Ánh sáng chạm mặt đất | Ban ngày, không bị che | Bị tán cây che |
| 🍂 **Mùn** (Detritus) | Xác lá, xác sinh vật | Sinh vật chết, lá rụng | Bị phân huỷ thành Đất màu |

Mỗi cột còn có **loại nền** cố định: Đất thường, Cát, Đá, Nước (ao hoặc suối). Loại nền quyết định loài nào sống được ở đó.

## 2. Thực vật
Mỗi cột có **3 tầng**, mỗi tầng chứa tối đa 1 cây:

```
  Tầng Tán   ── cây gỗ (sồi, thông…)       → che sáng cho 2 tầng dưới
  Tầng Bụi   ── cây bụi (mâm xôi, dương xỉ)
  Tầng Thảm  ── cỏ, hoa, rêu, nấm
```

**Vòng đời:** Hạt → Mầm → Trưởng thành (ra hoa/quả/hạt) → Già → Chết, để lại Mùn.

**Lan rộng:** cây trưởng thành thả hạt sang các cột lân cận. Hạt chỉ nảy mầm nếu chỉ số của cột nằm trong **ngưỡng chịu đựng** của loài đó. Gió đưa hạt đi xa hơn, ong và bướm làm cây ra hạt nhiều hơn.

**Cạnh tranh:** cây lớn che sáng nên cỏ dưới tán chết dần, nhưng dương xỉ và nấm ưa bóng lại phát triển. Nhờ vậy rừng và đồng cỏ tự hình thành ranh giới mà không cần người chơi vẽ.

## 3. Động vật
💡 Động vật được mô phỏng **từng cá thể** (nhìn thấy được trên dải đất). Giới hạn mềm khoảng 60–100 con cho cả thế giới để giữ hiệu năng và để màn hình không rối.

Mỗi con có: **vùng sống** (vài cột quanh tổ), **độ no**, **tuổi**, và trạng thái no hoặc đói.

| Vai trò | Ví dụ | Ăn gì | Đóng góp |
|---------|-------|-------|----------|
| Thụ phấn | Ong, bướm | Mật hoa | Cây ra hạt nhiều hơn |
| Ăn cỏ | Thỏ, sóc, nai | Cỏ, quả, hạt | Phát tán hạt (sóc chôn hạt sồi) |
| Săn mồi | Cáo, cú | Thỏ, chuột | Giữ số lượng thú ăn cỏ ở mức hợp lý |
| Phân huỷ | Giun, nấm, bọ cánh cứng | Mùn | Biến Mùn thành Đất màu |

**Sinh sản:** khi đủ no và vùng sống còn chỗ, con vật sinh con. ✅ Thỏ, cá sống theo **bầy**; cáo, diệc, sóc giữ **lãnh thổ**; mùa Đông không sinh: xem [13](13-bay-dan-va-sinh-san.md). **Sức chứa** của mỗi loài = lượng thức ăn trong vùng sống của nó, nên số lượng tự điều chỉnh.

**Chết:** vì già, bị săn hoặc chết đói. Xác để lại Mùn, khép lại vòng tuần hoàn.
- ✅ **Đông quá thì ăn trụi rồi chết đói; thú săn giữ cân bằng.** Thú ăn cỏ sinh sản tới đúng lượng cỏ mọc lại; khi mùa Đông hoặc hạn hán làm cỏ mọc chậm, chúng ăn trụi cỏ và chết đói. Thú săn ăn bớt thú ăn cỏ nên giữ được cỏ. Loài đã khám phá vẫn tự quay lại miễn phí khi cỏ hồi phục, nên không có vòng xoáy chết. Chi tiết và số liệu ở [08 §7.3](08-nhieu-vung-va-ao.md#73-cân-bằng-tự-nhiên-ăn-trụi-chết-đói-thú-săn). Số liệu: [07 §6.2–6.3](07-he-sinh-thai-chi-tiet.md#63-chết-đói--quay-lại).
- ✅ **Thể hiện nhẹ nhàng nhưng nhìn thấy được:** con vật nằm xuống, mờ dần trong vài giây, để lại một bông hoa nhỏ hoặc một ụ mùn. Không có máu, không có xác nằm lại.
- ~~Săn mồi không được vẽ trực tiếp: thú săn đuổi con mồi chạy ra khỏi màn hình (hoặc vào bụi rậm), rồi quay lại một mình.~~ ✅ **Thay bằng (Q34, 2026-10-25):** thú săn rượt ngay trên màn hình, vồ thì bụi cỏ tung lên, con mồi biến mất, không máu: xem [14](14-hang-tho-va-san-moi.md).
- ✅ **Kích cỡ theo tự nhiên (2026-10-24), lấy Cáo làm chuẩn:** cáo đỏ dài ~105 cm (mũi tới chóp đuôi) = 14 px, tức 1 px ≈ 7.5 cm. Các loài khác vẽ theo kích thước thật: Thỏ 6 × 5 px (~40 cm, cao ~30 cm cả tai), Sóc 7 × 5 px (~40 cm cả đuôi), Diệc 9 × 13 px (đứng cao ~95 cm, cao hơn cáo), Cá 5 × 2 px (~35 cm). Ong (1.5 cm) và Giun (~12 cm) nhỏ hơn 1 px nên giữ cỡ nhỏ nhất còn nhìn thấy (2 × 2 và 3 × 1 px). Cây và thú không cùng tỉ lệ (cây tán ~140 pt là cây "thu nhỏ" để vừa dải). Thú nhỏ có vùng bắt chuột tối thiểu để vẫn rê chuột chọn được.
- ✅ **Không đặt tên cá thể.** Click vào con vật chỉ hiện tên loài và trạng thái (no, đói, đang mang thai…). Người chơi gắn bó với *quần thể* và *nơi chốn*, không phải từng con.

## 4. Chuỗi thức ăn khởi đầu (đồng cỏ)

```
        ☀️ + 💧 + 🌱
             │
   ┌─────────┼──────────┐
  Cỏ       Hoa dại    Bụi mâm xôi
   │          │ ▲         │
   │          ▼ │(thụ phấn)│
   │         Ong/Bướm      │
   ▼                       ▼
  Thỏ ◄──────────────── Chim sẻ
   │
   ▼
  Cáo
   │ (chết)
   ▼
  🍂 Mùn ──► Giun/Nấm ──► 🌱 Đất màu
```

## 4b. Danh sách loài v1
✅ Khoảng **40 loài: 20 thực vật và 20 động vật**. Có thể thêm loài qua các bản cập nhật miễn phí sau khi ra mắt.
💡 Phân bổ dự kiến (tên và vai trò còn đổi được):

| Biome | Thực vật (20) | Động vật (20) |
|-------|---------------|---------------|
| Đồng cỏ | Cỏ, Hoa dại, Bồ công anh, Mâm xôi | Ong, Bướm, Thỏ, Chim sẻ, Cáo |
| Rừng | Sồi, Thông, Dương xỉ, Nấm, Việt quất | Sóc, Nai, Cú, Gõ kiến, Nhím |
| Đầm lầy / Ao | Lau sậy, Sen, Bèo, Liễu | Ếch, Cá, Chuồn chuồn, Diệc |
| Thảo nguyên khô | Cỏ khô, Xương rồng, Keo, Ngải | Thằn lằn, Chuột nhảy, Đại bàng |
| Đồi đá | Rêu, Địa y, Hoa nhung tuyết | Dê núi, Chim ưng |
| Mọi biome | | Giun đất (phân huỷ) |

Mỗi biome cần đủ **4 vai trò** (thụ phấn, ăn cỏ, săn mồi, phân huỷ), hoặc mượn vai trò từ biome bên cạnh. Ví dụ: Ao và Đồi đá không có loài thụ phấn riêng nên phụ thuộc ong từ đồng cỏ kế bên (Ao đã đặc tả ở [08 §6.4](08-nhieu-vung-va-ao.md#64-chuỗi-thức-ăn)). Điều này khuyến khích người chơi đặt các biome cạnh nhau một cách có tính toán.

## 5. Sức khoẻ & Sinh khí
💡 Mỗi **vùng** (một đoạn cột liền nhau cùng biome) có chỉ số **Sức khoẻ** tính từ:
- **Độ phủ:** bao nhiêu % cột có thực vật;
- **Đa dạng:** số loài, cộng thêm điểm nếu có đủ các vai trò (thụ phấn, ăn cỏ, săn mồi, phân huỷ);
- **Cân bằng:** không loài nào chiếm quá ~40% sinh khối, tỉ lệ thú săn trên con mồi nằm trong khoảng hợp lý.

**Sinh khí/phút = Σ(sinh khí cơ bản của từng sinh vật) × hệ số Đa dạng × hệ số Cân bằng**

Vì có hai hệ số nhân này, 10 loài mỗi loài vài con sẽ cho nhiều Sinh khí hơn 100 con thỏ. Đây là cách cơ chế phục vụ trụ cột *"Cân bằng là vẻ đẹp"*.

## 6. Mất cân bằng & sự kiện tự nhiên
Những thứ này tạo ra **khoảnh khắc** để người chơi can thiệp. Tất cả đều có cách tự phục hồi chậm nếu người chơi bỏ qua.

| Sự kiện | Nguyên nhân | Dấu hiệu nhìn thấy | Can thiệp gợi ý |
|---------|-------------|--------------------|-----------------|
| Ăn trụi | Quá nhiều thú ăn cỏ, nhất là khi sang Đông hoặc gặp hạn | Cỏ thưa và vàng, đất lộ ra, thú ăn cỏ gầy rồi nằm xuống | Mời thú săn mồi, gọi mưa, gieo thêm cỏ, hoặc để tự nhiên tự cân bằng |
| Hạn hán | Lâu không mưa | Cây ngả vàng | Gọi mưa |
| Cháy rừng | Hạn hán + tán dày (hiếm) | Lửa lan theo cột | Gọi mưa, hoặc để cháy: tro làm đất rất màu mỡ |
| Sinh vật lạ ghé qua | Ngẫu nhiên, khi vùng Cân bằng | Bong bóng 🦋 | Click để đón, nhận quà lớn và ghi vào Sổ tay ([09](09-khoanh-khac.md)) |

## 7. Thời gian
- ~~Ngày/đêm theo giờ thật của máy.~~ ✅ **Thay bằng:** ngày đêm theo thời gian chơi (5 phút ngày + 5 phút đêm), mỗi loài có giờ thức / ngủ riêng. ↻ **Đổi 2026-10-24:** xem [11](11-nhip-va-tang-tan.md) §1.5. Ban đêm có cú, đom đóm; ban ngày có ong, bướm.
- ~~Mùa theo ngày thật: 1 mùa = 1 ngày thật.~~ ✅ **Thay bằng:** nhịp ×100 (1 phút thật = 100 phút mô phỏng), **1 mùa = 30 phút thật** (3 000 phút mp, 3 ngày đêm của game), tính theo thời gian mô phỏng đã chạy; tắt app thì mùa đứng yên. ↻ **Đổi 2026-10-24:** xem [11](11-nhip-va-tang-tan.md) §1.
  - 💡 Đổi mùa lúc **0:00 giờ máy**, chuyển dần trong khoảng 1 giờ để không giật.
  - 💡 Ảnh hưởng của mùa:

    | Mùa | Môi trường | Sinh vật |
    |-----|------------|----------|
    | Xuân | Mưa nhiều, cây nảy mầm nhanh | Mùa sinh sản, hoa nở, ong hoạt động mạnh |
    | Hạ | Nắng gắt, dễ hạn hán | Cây ra quả, cháy rừng có thể xảy ra |
    | Thu | Lá rụng, Mùn tăng mạnh | Sóc tích trữ hạt, chim di cư rời đi |
    | Đông | Lạnh, cây ngừng lớn, có tuyết | Một số loài ngủ đông (ẩn khỏi màn hình), cú và cáo nổi bật |

  - ✅ **Ngày đầu tiên chơi luôn là Xuân.** Mùa = `(số ngày lịch kể từ ngày bắt đầu save) % 4`, nên mỗi save có chu kỳ riêng.
- 💡 Tick mô phỏng: **1 giây/tick** cho động vật và thực vật, **1 phút/tick** cho chỉ số môi trường.

## 8. Ghi chú kỹ thuật (để sau)
- Tách **mô phỏng** (dữ liệu thuần, chạy được không cần render) khỏi **hiển thị**. Lý do: phần lớn thế giới nằm ngoài khung nhìn nhưng vẫn phải chạy, và tách ra thì dễ viết test.
- Chỉ tạo GameObject/sprite cho các cột **trong khung nhìn** cộng một đoạn đệm; sinh vật ngoài khung nhìn chỉ là dữ liệu.
- Lưu game định kỳ (vài phút/lần) và khi thoát, vì không có mô phỏng bù nên trạng thái lưu chính là trạng thái lúc mở lại.
- Dữ liệu loài đặt trong ScriptableObject (`SpeciesDefinition`) để cân bằng game mà không phải sửa code.
