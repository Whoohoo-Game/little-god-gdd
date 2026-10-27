# 05 · Mở rộng thế giới & tiến trình

✅ Trục tiến trình chính là **mở rộng thế giới**.
✅ Thế giới có **độ dài cố định, dài hơn màn hình**. Người chơi di chuyển giữa các vùng bằng **nút cuộn trên UI**.

## 1. Ý tưởng chính: Hồi sinh đất hoang
💡 Khi bắt đầu, thế giới gần như là **đất hoang**: xám, nứt nẻ, không sự sống. Chỉ có một mảnh xanh nhỏ khoảng 5 cột ở **giữa thế giới**, nơi vị thần thức tỉnh. Sự sống lan dần ra hai phía.

```
Toàn thế giới (~3 màn hình):
Bắt đầu:   ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
                                  [  khung nhìn  ]
Vài ngày:  ░░░░░░░░░▓▓▓▓≈≈≈▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓^^^^▓▓▓▓░░░░░░░░░░░░░░░░
Kết:       ▓▓▓▓▓▓▓▓▓▓▓▓≈≈≈▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓^^^^▓▓▓▓▓▓▓▓▓≈≈≈≈▓▓▓▓▓▓▓
░ = đất hoang   ▓ = đã hồi sinh   ≈ = nước   ^ = đá
```

- ✅ **Độ dài thế giới:** **144 cột** (≈ 3 màn hình MacBook 14"). Mỗi cột rộng cố định 32pt, nên màn rộng thấy được nhiều cột hơn nhưng thế giới thì như nhau với mọi người chơi.
- Toàn bộ thế giới được **mô phỏng liên tục**, kể cả phần nằm ngoài khung nhìn. Phần ngoài khung nhìn chỉ không được render.

## 2. Di chuyển giữa các vùng
Nguyên tắc: **không chiếm con lăn chuột, không tự di chuyển khung nhìn**. Người chơi hoàn toàn chủ động.

| Thành phần | Hành vi |
|------------|---------|
| ✅ **Nút cuộn ◀ ▶** | Nằm ở hai mép dải. Mặc định gần như trong suốt, hiện rõ khi chuột lại gần. **Giữ** để cuộn; càng giữ lâu cuộn càng nhanh. Số liệu: [10 §4](10-giao-dien.md#4-nút-cuộn--). |
| 💡 **Double-click nút cuộn** | Nhảy thẳng sang vùng kế tiếp theo hướng đó. |
| 💡 **Bản đồ mini** | Một thanh mỏng trong khay thần, mỗi pixel là một cột, tô màu theo biome; có ô vuông đánh dấu khung nhìn hiện tại. Click vào bản đồ để nhảy đến vị trí đó. Chi tiết: [10 §5](10-giao-dien.md#5-bản-đồ-mini). |
| 💡 **Chỉ báo ngoài màn hình** | Khi có khoảnh khắc (sinh vật mới, hạn hán…) ở ngoài khung nhìn, nút cuộn phía đó hiện một bong bóng nhỏ ✨ hoặc 💌. Liếc là biết có chuyện ở bên trái hay bên phải. Chi tiết: [09 §7](09-khoanh-khac.md#7-chỉ-báo-ngoài-màn-hình-05-2). |
| 💡 **Giữ vị trí** | Khung nhìn được lưu lại và mở app lần sau sẽ ở đúng chỗ cũ. |
| ✅ **Chế độ theo dõi** | Tuỳ chọn trong cài đặt, **tắt mặc định**. Khi bật, khung nhìn trượt chậm đến khoảnh khắc mới, nhưng chỉ khi chuột không ở trên dải đất (không giật khung nhìn lúc người chơi đang thao tác). |

## 3. Cách hồi sinh một vùng
> ↻ **2026-10-24:** Hồi sinh vùng bằng Sinh khí được thay bằng [12 · Môi trường sống](12-moi-truong-song.md): đất hoang bị cỏ phủ của biome kề bên lấn dần, người chơi đẩy nhanh bằng gieo cỏ phủ và gọi mưa.

💡 Đất hoang được chia thành **vùng** khoảng 8–12 cột. Một vùng hồi sinh khi vùng bên cạnh **đủ khoẻ** (Sức khoẻ ≥ ngưỡng) **và** người chơi chủ động dùng Gió hoặc Gieo hạt để đưa sự sống sang. Tiến trình vì vậy vừa tự nhiên vừa có lựa chọn: mở rộng về bên trái hay bên phải trước?

Mỗi vùng đất hoang có **thuộc tính ẩn**, chỉ lộ ra khi hồi sinh:
- loại nền: đất, cát, đá, có mạch nước ngầm…;
- độ ẩm và nhiệt độ nền;
- đôi khi có **di tích tự nhiên**: suối ngầm, hang động, gốc cây cổ thụ. Đây là bất ngờ khi khám phá.

✅ **Đặt tên vùng:** khi một vùng hồi sinh, game gợi ý một tên ngẫu nhiên (ví dụ "Đồi Gió") và người chơi có thể sửa. Tên hiện trên bản đồ mini và trong sổ tay. Đây là cách chính để người chơi gắn bó, thay cho việc đặt tên sinh vật.

💡 Thuộc tính của các vùng được **thiết kế tay** (không sinh ngẫu nhiên) để đảm bảo nhịp khám phá và cái kết hay. Có thể thêm biến thể nhỏ ngẫu nhiên.

## 4. Biome hình thành tự nhiên
> ↻ **2026-10-24:** Bảng biome theo vùng được thay bằng [12 · Môi trường sống](12-moi-truong-song.md): biome theo từng cột, do cỏ phủ đang mọc quyết định (Cỏ → Đồng cỏ, Dương xỉ → Rừng).

💡 Người chơi **không chọn** biome. Biome **hình thành** từ chỉ số môi trường và các loài sống ở đó.

| Biome | Điều kiện hình thành | Loài đặc trưng |
|-------|---------------------|----------------|
| Đồng cỏ | Đất thường, ẩm vừa, ít cây gỗ | Cỏ, hoa dại, thỏ, ong, cáo |
| Rừng | Tán cây phủ ≥ 50% cột | Sồi, nấm, sóc, cú, nai |
| Đầm lầy / Ao | Có cột Nước, độ ẩm cao | Lau sậy, sen, ếch, cá, diệc |
| Thảo nguyên khô | Đất cát, ít ẩm | Cỏ khô, xương rồng, thằn lằn, đại bàng |
| Đồi đá | Nền đá | Rêu, dê núi, chim ưng |
| ✅ **Khu Vườn Thiêng** | Không hình thành tự nhiên, xem §5 | Cây Thế Giới và một loài đại diện của mỗi biome |

Biome còn **đổi diện mạo theo mùa** (xem [03 §7](03-he-sinh-thai.md#7-thời-gian)), ví dụ rừng mùa thu lá đỏ, đồng cỏ mùa đông phủ tuyết.

## 5. Mục tiêu cuối (vì là game premium)
Game premium cần một **cái kết** rõ ràng, sau đó mới là chế độ sandbox.

✅ **Khu Vườn Thiêng** là vùng đất hoang cuối cùng. 💡 Nó nằm ở **đầu phải** của thế giới, nên người chơi có một hướng đi rõ ràng.
- Có thể nhìn thấy từ đầu game: một gốc cây khô khổng lồ trên nền đá xám, có ánh sáng mờ. Đây là lời hứa về đích đến.
- **Điều kiện mở:** mọi vùng khác đã hồi sinh **và** đều đạt trạng thái "Cân bằng" cùng lúc.
- **Hồi sinh:** người chơi **mời một loài đại diện từ mỗi biome** về Vườn. Mỗi loài đến làm gốc cây khô hồi lại một phần. Đây là màn kết, kéo dài khoảng 1–2 phiên chơi, chứ không xong trong một cú click.
- **Kết chính:** khi đủ loài, **Cây Thế Giới nở hoa**, kèm cảnh kết thúc ngắn ngay trên dải đất. Cảnh này chỉ có hiệu ứng, không có chữ dài, không chiếm toàn màn hình.
- **Sau kết:** chơi tiếp tự do, sưu tầm hết loài hiếm, có achievement trên Steam.
- 💡 Thời lượng mục tiêu để xong kết chính: **khoảng 2–4 tuần** chạy nền, mỗi ngày tương tác khoảng 10–20 phút. Vì không có mô phỏng bù, thời lượng này tính theo **giờ app đang mở**, không theo ngày lịch.
  - ↻ Ở nhịp ×100 ([11 §1.4](11-nhip-va-tang-tan.md#14-kiểm-chứng-worldsimpy-survey-8--mùa-2-880-phút-mp)), kết chính của slice cần **~1.5–2 giờ app mở** với người ghé mỗi 3–6 phút, ~3.3 giờ nếu ghé mỗi 18 phút. Số dưới đây là của nhịp cũ.
  - Mô hình nhiều vùng ([08](08-nhieu-vung-va-ao.md)) cho thấy kết chính cần **~130–140 giờ app mở**. Với người mở app 6–12 giờ/ngày, đó là ~11–22 ngày lịch. Người mở ít hơn được **Sinh khí nghỉ ngơi** bù (✅ Q18), nên người mở 4h/ngày ước tính mất ~22 ngày thay vì ~33.

## 6. Mở rộng tiềm năng sau v1 (chưa cam kết)
- **Tầng trời:** mây, chim di cư, một dải mỏng phía trên.
- **Thế giới thứ 2:** một dải đất khác (bờ biển, núi tuyết), chuyển qua lại như các "trang".
- **Steam Workshop:** cho người chơi tự tạo loài mới.
