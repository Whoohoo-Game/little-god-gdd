# 04 · Quyền năng của thần

Thần **không điều khiển** sinh vật. Thần chỉ thay đổi **điều kiện** và đưa ra **lời mời**. Mỗi quyền năng tốn Sinh khí và có thời gian hồi.

## 0. Hình dạng của thần
✅ Vị thần hiện trên dải đất là một **tinh linh nhỏ** (khoảng 8–10px, phát sáng nhẹ). Đây là nhân vật đại diện của game, dùng cho icon app và ảnh Steam.

💡 Hành vi:
- **Khi người chơi dùng quyền năng:** tinh linh bay đến chỗ click rồi mới thi triển (bay nhanh, khoảng 0.3 giây). Hành động có "người làm" thay vì hiện ra từ hư không.
- **Khi không ai tương tác:** tinh linh lang thang chậm, đậu trên ngọn cây, đùa với bướm. Sau khoảng 5 phút yên lặng thì ngủ trên một cành cây (có "z z z" nhỏ).
- **Ban đêm:** tinh linh sáng hơn, giống một con đom đóm lớn.
- ✅ **Theo mùa:** tinh linh đổi màu: xuân xanh lá, hạ vàng, thu cam, đông trắng. Ở v1 tinh linh không tiến hoá hình dạng (có thể làm sau v1).
- **Khi người chơi cuộn sang vùng khác:** tinh linh bay theo khung nhìn.
- Tinh linh **không nhận click** (để không chắn sinh vật) và không ảnh hưởng mô phỏng. Nó chỉ để tạo cảm xúc.

## 1. Cách điều khiển
💡 Trong dải đất cao 180pt, chỉ chuột là đủ:

| Thao tác | Kết quả |
|----------|---------|
| Click mặt đất | Dùng quyền năng đang chọn tại cột đó |
| Kéo ngang trên mặt đất | Quyền năng dạng vùng (mưa, gió) phủ các cột đã kéo qua |
| Click sinh vật | Xem thông tin ngắn (tên loài, trạng thái) |
| Click bong bóng | Nhận khoảnh khắc: quà, lời đề nghị hoặc gợi ý (xem [09](09-khoanh-khac.md)) |
| Di chuột vào **khay thần** ở góc | Khay mở rộng: chọn quyền năng, xem Sinh khí, bản đồ mini, sổ tay |
| Giữ nút **◀ / ▶** ở mép dải | Cuộn khung nhìn dọc thế giới (xem [05 §2](05-mo-rong-the-gioi.md#2-di-chuyển-giữa-các-vùng)) |

✅ Game **không dùng con lăn chuột** để điều khiển. Ở vùng trong suốt, con lăn vẫn đi xuống cửa sổ bên dưới như bình thường.
> ⚠️ Giới hạn kỹ thuật: khi chuột nằm **trên mặt đất hoặc sinh vật** (vùng không trong suốt), hệ điều hành gửi sự kiện cuộn cho cửa sổ game, nên cửa sổ bên dưới không nhận được. Phần mặt đất mỏng (12pt) nên ảnh hưởng nhỏ. Cần thử thực tế xem có khó chịu không.

💡 **Khay thần** (God Tray) là một cục nhỏ ở góc phải dải đất. Bình thường chỉ hiện biểu tượng và số Sinh khí. Khi di chuột vào, khay mở ra một hàng quyền năng. Không có menu toàn màn hình nào ngoài **Sổ tay thiên nhiên**, và sổ tay mở thành cửa sổ riêng phía trên dải đất. Đặc tả chi tiết khay, công cụ Gieo/Mưa và sổ tay: [10](10-giao-dien.md).

## 2. Danh sách quyền năng

| Quyền năng | Mở khoá | Tác dụng | Ghi chú |
|------------|---------|----------|---------|
| 🌱 **Gieo hạt** | Ban đầu | Gieo một loài đã khám phá vào cột | Chỉ nảy mầm nếu cột phù hợp. Game hiện trước tỉ lệ thành công. |
| 🌧️ **Mưa** | Ban đầu | Kéo để tăng Độ ẩm trên một đoạn cột | Mưa quá nhiều làm úng, có hại cho cây ưa khô |
| 💌 **Lời mời** | Khi đủ điều kiện | Mời một loài động vật mới đến vùng đất | Loài chỉ nhận lời khi môi trường đủ điều kiện, ví dụ Thỏ cần ≥ 10 cỏ sống (07 §6.5). Xem mục 3. |
| 🌬️ **Gió** | Cấp 2 | Thổi hạt giống bay xa theo một hướng | Giúp lan sang vùng đất hoang |
| ☀️ **Nắng ấm** | Cấp 2 | Tăng Ánh sáng, cây trong vùng lớn nhanh hơn | Làm giảm Độ ẩm |
| ⛰️ **Nắn đất** | Cấp 3 | Đào ao hoặc đắp gò ở một cột | Cách duy nhất để tạo nước mới. Đắt. |
| ⚡ **Sét** | Cấp 4 | Gây cháy có kiểm soát | Công cụ "phá để tái sinh": tro làm Đất màu tăng mạnh |

✅ **Không có Chúc phúc** (Q20, 2026-10-23): game không có bệnh để chữa. Thao tác "vuốt ve" chính là **click khoảnh khắc** ([02 §Vòng ngắn](02-core-loop.md#vòng-ngắn-liếc-và-chạm-1060-giây)).

## 3. Lời mời: cơ chế khám phá loài
💡 Đây là cách chính để có loài động vật mới, và là **vòng thưởng mạnh nhất** của game.

1. Sổ tay hiện bóng đen của loài chưa biết kèm gợi ý mờ, ví dụ *"Một sinh vật thích nơi có nhiều cỏ và bụi rậm…"*.
2. Khi điều kiện đạt, một con của loài đó **đi lạc vào mép dải đất** và có bong bóng 💌.
3. Người chơi click để mời ở lại (tốn Sinh khí). Loài được thêm vào sổ tay, có ảnh minh hoạ và mô tả.
4. Nếu người chơi bỏ qua, con vật đi mất và quay lại sau.

Thực vật mới được khám phá theo cách khác: **gió mang hạt lạ tới**, hoặc khi một vùng mới được hồi sinh. Chi tiết: khoảnh khắc 🌱 ở [09 §3.2](09-khoanh-khac.md#32-chi-tiết-từng-loại).

## 4. Tiến cấp của thần
💡 Tổng Sinh khí **tích luỹ từ đầu** (không phải số đang có) quyết định **cấp thần**. Mỗi cấp mở một quyền năng mới hoặc nâng cấp quyền năng cũ, ví dụ mưa phủ rộng hơn hay thời gian hồi ngắn hơn. Tiêu Sinh khí không làm tụt cấp, nên người chơi không phải đắn đo giữa tiêu và giữ.
