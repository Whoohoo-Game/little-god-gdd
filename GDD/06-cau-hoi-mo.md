# 06 · Câu hỏi mở

Các quyết định cần chốt trước khi làm prototype gameplay. Mỗi câu có đề xuất đi kèm; khi chốt thì chuyển vào *Nhật ký quyết định* trong [README](README.md).

## Đã chốt
- ✅ **Q1.** Thế giới có độ dài cố định, dài hơn màn hình, cuộn bằng giữ nút UI (không dùng con lăn chuột). Chi tiết: [05 §2](05-mo-rong-the-gioi.md#2-di-chuyển-giữa-các-vùng).
- ✅ **Q2.** Không mô phỏng bù khi tắt app; thế giới ngủ. Chi tiết: [02](02-core-loop.md#khi-người-chơi-vắng-mặt).
- ✅ **Q3.** Mùa theo ngày thật, 1 mùa = 1 ngày thật. Chi tiết: [03 §7](03-he-sinh-thai.md#7-thời-gian).

- ✅ **Q11.** Thế giới dài 144 cột.
- ✅ **Q12.** Có chế độ theo dõi, tắt mặc định.
- ✅ **Q13.** Ngày đầu luôn là Xuân.
- ✅ **Q14.** Có khởi động cùng máy (tắt mặc định) và ẩn tạm vào menu bar/system tray.
- ✅ **Q4.** Khoảng 40 loài (20 thực vật và 20 động vật). Danh sách dự kiến ở [03 §4b](03-he-sinh-thai.md#4b-danh-sách-loài-v1).
- ✅ **Q5.** Thần là một tinh linh nhỏ. Chi tiết ở [04 §0](04-quyen-nang-than.md#0-hình-dạng-của-thần).
- ✅ **Q6.** Cái chết nhẹ nhàng, nhìn thấy được.
- ✅ **Q7.** Không đặt tên sinh vật.

- ✅ **Q15.** Tinh linh không tiến hoá ở v1, chỉ đổi màu theo mùa.
- ✅ **Q16.** Người chơi đặt tên cho vùng đất đã hồi sinh.
- ✅ **Q8.** Biome cuối là Khu Vườn Thiêng, gắn với kết chính. Chi tiết ở [05 §5](05-mo-rong-the-gioi.md#5-mục-tiêu-cuối-vì-là-game-premium).
- ✅ **Q9.** Chọn 1 màn hình trong cài đặt, mặc định là màn hình chính.
- ✅ **Q10.** Ambient bật mặc định, nhạc tuỳ chọn tắt mặc định.

- ✅ **Q17.** Giữ cả **cân bằng tự nhiên** (thú ăn cỏ vượt sức chứa thì chết đói, thú săn điều hoà) lẫn **giảm giá hồi sinh tới 30%** khi vùng kề Cân bằng. Giữ bảng giá hiện tại (kết ~17 ngày ở 8h/ngày), chỉnh lại sau khi chơi thử vertical slice. Chi tiết: [08 §4.1](08-nhieu-vung-va-ao.md#41-điều-kiện--giá), [08 §7.3](08-nhieu-vung-va-ao.md#73-cân-bằng-tự-nhiên-ăn-trụi-chết-đói-thú-săn).
- ✅ **Q18.** Có **Sinh khí nghỉ ngơi**: mỗi ngày lịch một lần, bù phần giờ mở app còn thiếu so với 8 giờ của ngày hôm trước, tối đa 2 giờ Sinh khí. Chi tiết: [08 §2](08-nhieu-vung-va-ao.md#2-thời-gian-giờ-app-mở--mùa-theo-ngày-lịch).
- ✅ **Q19.** Sinh vật tự tìm đến vùng mới **không cần** người chơi click đón; click bong bóng chỉ để nhận thêm phần thưởng nhỏ.
- ✅ **Q20.** **Bỏ Chúc phúc.** Vai trò "vuốt ve" chuyển sang việc click khoảnh khắc ([02](02-core-loop.md#vòng-ngắn-liếc-và-chạm-1060-giây)).

- ✅ **Q21.** Nhịp ×100; **1 mùa = 30 phút thật** (3 000 phút mp, ↻ 2026-10-24, trước 2 ngày mô phỏng ≈ 29 phút), mùa theo thời gian mô phỏng ([11 §1.1](11-nhip-va-tang-tan.md#11-đồng-hồ)).
- ✅ **Q22.** Giữ **Sinh khí nghỉ ngơi**, trần **10 phút thật** thu nhập ([11 §1.2](11-nhip-va-tang-tan.md#12-sinh-khí-nghỉ-ngơi--q22-giữ-trần-10-phút-thật)).
- ✅ **Q23.** Tầng tán có cả **Sồi, Táo dại, Liễu** ([11 §2.3](11-nhip-va-tang-tan.md#23-loài--q23-cả-ba)).
- ✅ **Q24.** Cây tán mở bằng **khám phá 🌱** ([11 §2.4](11-nhip-va-tang-tan.md#24-mở-khoá--q24-khám-phá-)).

- ✅ **Q25.** Không có lệnh hồi sinh: đất hoang bị cỏ phủ của biome kề bên lấn dần ([12 §2.1](12-moi-truong-song.md#21-cỏ-lấn-đất-hoang--q25)).
- ✅ **Q26.** Biome theo cột, do cỏ phủ quyết định (Cỏ → Đồng cỏ, Dương xỉ → Rừng); gieo cỏ phủ cách biome của nó ≤ 5 ô thì nối thành hành lang để lấn ([12 §2.2](12-moi-truong-song.md#22-gieo-và-đẩy-ranh-giới--q26)).
- ✅ **Q27.** Thực vật ngoài biome: × 0.5 trong 5 ô giáp ranh, không mọc khi sâu hơn ([12 §2.3](12-moi-truong-song.md#23-thực-vật-ngoài-biome--q27)).
- ✅ **Q28.** Thêm **Sóc** (rừng sồi, chôn hạt, mồi phụ của cáo).
- ✅ **Q29.** Giữ "< 2 con là vắng" và chờ 2 giờ mô phỏng.

- ✅ **Q30.** Vườn mở khi đất hoang phủ kín, mọi loài đã từng xuất hiện, mọi biome đang có đều Khoẻ; kết game khi Vườn phủ ≥ 80% ([12 §5](12-moi-truong-song.md#5-kết-game--q30)).
- ✅ **Q31.** Sinh khí dư để mở quyền năng mới theo cấp, thiết kế sau slice.

- ✅ **Q32.** Tạm giữ nhịp sinh / chết của [13](13-bay-dan-va-sinh-san.md) (~1 con chết mỗi ~25 giây thật trên màn hình), xem lại sau khi chơi thử.
- ✅ **Q33.** Cáo sống theo **cặp chung hang** ([13 §3.3](13-bay-dan-va-sinh-san.md#33-đơn-độc-cáo-diệc-sóc)).

- ✅ **Q34.** Cảnh vồ mồi: cáo vồ, bụi cỏ tung lên, con mồi biến mất, cáo thong thả về hang ([14 §5](14-hang-tho-va-san-moi.md#5-hiển-thị)). Thay phần săn mồi của Q6.

## Đang mở
*Hiện chưa có câu hỏi nào đang mở.*
