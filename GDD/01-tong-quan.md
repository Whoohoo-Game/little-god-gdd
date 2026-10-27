# 01 · Tổng quan

## Câu chốt (elevator pitch)
💡 *"Hồi sinh một vùng đất hoang ngay dưới thanh Dock của bạn. Gieo một hạt mầm, gọi một cơn mưa, rồi quay lại làm việc. Vài tiếng sau, nơi đó đã thành một khu rừng có cáo, có ong, có cá bơi trong suối."*

## Fantasy cốt lõi
✅ Người chơi là một **vị thần nhỏ của thiên nhiên**. Thần không ra lệnh cho từng sinh vật, mà tạo **điều kiện** để sự sống tự tìm đến và tự cân bằng:
- gieo hạt, gọi mưa, sưởi nắng;
- mời một loài mới đến khi môi trường đã phù hợp;
- can thiệp khi hệ sinh thái mất cân bằng (hạn hán, quá nhiều thú ăn cỏ, thiếu thú săn).

Phần thưởng cảm xúc đến từ việc **thấy thế giới tự sống**: một con thỏ xuất hiện vì cỏ đã đủ dày, một con cáo theo sau vì thỏ đã đủ nhiều.

## Trụ cột thiết kế (Design Pillars)
Mọi mechanic mới đều phải phục vụ ít nhất một trụ cột và không được phá trụ cột nào.

1. **Sống động khi bạn không nhìn**
   Thế giới thay đổi theo thời gian thực. Mỗi lần liếc xuống, người chơi phải thấy *một điều gì đó mới*.
2. **Chạm nhẹ, lan rộng**
   Một hành động nhỏ của thần tạo ra chuỗi hệ quả. Gieo cỏ kéo theo thỏ đến, thỏ kéo theo cáo, cáo để lại xác, xác nuôi nấm, nấm làm đất màu mỡ hơn.
3. **Không làm phiền**
   Game sống chung với công việc của người chơi. Không popup, không âm thanh gây giật mình, không trừng phạt nặng khi người chơi bận cả ngày. Tốn rất ít CPU/GPU.
4. **Cân bằng là vẻ đẹp**
   Mục tiêu là sự **đa dạng và bền vững**, không phải con số lớn nhất. Một hệ sinh thái cân bằng được thưởng nhiều hơn một cánh đồng chỉ toàn một loài.

## Ràng buộc từ hình thức "dải đáy màn hình"
Những ràng buộc này định hình toàn bộ thiết kế.

| Ràng buộc | Hệ quả thiết kế |
|-----------|-----------------|
| Dải cao khoảng 180pt, rộng bằng màn hình | Thế giới về cơ bản là **1 chiều** (trái sang phải). Không gian chia theo **cột**, không theo lưới 2D. |
| Hầu hết thời gian người chơi không nhìn | Thông tin phải **đọc được bằng một cái liếc**: màu sắc, mật độ, chuyển động. Hạn chế chữ và số. |
| Vùng trong suốt cho click xuyên qua | Chỉ sinh vật và mặt đất nhận click. UI phải gọn, nằm ở một góc, chỉ mở rộng khi di chuột vào. |
| Chạy nền cả ngày | Mô phỏng chạy theo **tick chậm** (khoảng 1 tick/giây). Render ở 30fps hoặc thấp hơn. Ngân sách khoảng ≤2% CPU. |
| Người chơi có màn hình rộng hẹp khác nhau | ✅ Thế giới có **độ dài cố định** và dài hơn màn hình. Màn hình là một "khung nhìn" trượt dọc thế giới. Màn rộng chỉ thấy được nhiều hơn, thế giới không dài hơn. Xem [05 §2](05-mo-rong-the-gioi.md#2-di-chuyển-giữa-các-vùng). |
| Người chơi có thể dùng nhiều màn hình | ✅ Mặc định ở **màn hình chính**; chọn màn khác trong cài đặt. Nếu màn đã chọn bị rút ra, dải đất tự về màn chính. |
| Không được chiếm con lăn chuột | ✅ Cuộn bằng **giữ nút trên UI**. Game không bắt sự kiện scroll để người chơi vẫn cuộn bình thường ở cửa sổ bên dưới. |

## Đối tượng người chơi
💡 Người làm việc lâu trên máy tính (dev, designer, sinh viên, streamer) thích game nhẹ nhàng, ấm áp. Họ đã quen các game idle và các game "pet" nằm trên desktop.

## Phong cách hình ảnh & âm thanh
💡 Pixel art nhỏ (sprite 16px, tỉ lệ 2× trên màn hình). Bảng màu ấm, tươi khi hệ sinh thái khoẻ, xám và khô khi suy tàn, để chỉ cần liếc là biết tình trạng.
✅ Âm thanh gồm 2 lớp, chỉnh âm lượng riêng:
- **Ambient (bật mặc định, âm lượng thấp):** gió, chim, côn trùng, mưa. Thay đổi theo biome trong khung nhìn, theo mùa và ngày/đêm, ví dụ ban đêm có dế, mùa đông có gió lạnh.
- **Nhạc (tắt mặc định):** nhạc acoustic/lo-fi nhẹ, dành cho ai muốn. Vì người chơi thường đang nghe nhạc riêng khi làm việc, nên nhạc không bao giờ tự bật.
- 💡 Hiệu ứng âm thanh khi tương tác (gieo hạt, mưa) chỉ phát khi **người chơi chủ động click**, không bao giờ phát từ sự kiện tự động.

## Ngoài phạm vi (Non-goals)
- Không có con người hay xây dựng thành phố. Bản prototype hiện tại có dân làng, sẽ được thay bằng động vật.
- Không chiến đấu, không thua game hẳn.
- Không multiplayer, không IAP.
