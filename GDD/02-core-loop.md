# 02 · Vòng lặp cốt lõi

Game chạy theo **3 thang thời gian** lồng vào nhau. Vòng ngắn nhất phải thú vị ngay cả khi chỉ chơi 10 giây.

```
 ┌───────────── Vòng dài (nhiều ngày) ───────────────┐
 │  Hồi sinh vùng đất mới → biome mới → loài mới      │
 │   ┌──────── Vòng giữa (vài giờ) ────────┐          │
 │   │ Tích Sinh khí → mở quyền năng /      │          │
 │   │ mời loài mới → hệ sinh thái phức tạp │          │
 │   │   ┌── Vòng ngắn (10–60 giây) ──┐     │          │
 │   │   │ Liếc → thấy điều mới →      │     │          │
 │   │   │ can thiệp 1–3 lần → quay    │     │          │
 │   │   │ lại làm việc                │     │          │
 │   │   └─────────────────────────────┘     │          │
 │   └───────────────────────────────────────┘          │
 └──────────────────────────────────────────────────────┘
```

## Vòng ngắn: "Liếc và chạm" (10–60 giây)
💡 Người chơi liếc xuống dải đất và thấy một **khoảnh khắc** đang chờ:
- một bong bóng nhỏ trên đầu con vật: sinh vật mới đến, con non vừa chào đời;
- một đàn thú ăn cỏ đang gầy đi vì cỏ quanh đó đã trụi (gợi ý: mời thú săn, gọi mưa, gieo cỏ);
- một vùng đất đang khô vàng, cần mưa;
- một hạt giống lạ do gió thổi tới, chờ được gieo.

Người chơi click hoặc kéo 1–3 lần, thế giới phản hồi ngay bằng hiệu ứng nhỏ (lấp lánh, mầm nhú lên), rồi người chơi quay lại làm việc. Click khoảnh khắc là thao tác **"vuốt ve"** chính của game (✅ Q20: không có Chúc phúc).

**Quy tắc:** khoảnh khắc **không bao giờ là modal** và **tự biến mất** nếu bị bỏ qua. Bỏ qua chỉ mất cơ hội thưởng thêm, không bị phạt.

Đặc tả chi tiết (9 loại bong bóng, điều kiện, phần thưởng, giới hạn hiển thị): [09 · Khoảnh khắc](09-khoanh-khac.md).

## Vòng giữa: "Nuôi hệ sinh thái" (vài giờ)
💡 Sinh vật sống tạo ra **Sinh khí** (Life Essence), là tài nguyên chính. Người chơi dùng Sinh khí để:
- dùng quyền năng: gieo hạt, gọi mưa… (xem [04](04-quyen-nang-than.md));
- **mời loài mới** khi môi trường đã đủ điều kiện, ví dụ đủ cỏ thì mời thỏ;
- nâng cấp quyền năng.

Loài mới làm hệ sinh thái phức tạp hơn. Hệ phức tạp và cân bằng thì sinh nhiều Sinh khí hơn. Đây là vòng tăng trưởng chính.

## Vòng dài: "Hồi sinh vùng đất" (nhiều ngày)
💡 Phần lớn dải đất ban đầu là **đất hoang**. Khi một khu vực đủ khoẻ, nó lan sự sống sang vùng đất hoang bên cạnh. Mỗi vùng mới hồi sinh mang thuộc tính riêng (độ ẩm, loại đất) nên sẽ thành **biome khác nhau**. Chi tiết ở [05](05-mo-rong-the-gioi.md).

## Khi người chơi vắng mặt
- **App đang mở, người chơi không nhìn:** mô phỏng chạy bình thường trên **toàn bộ thế giới**, kể cả phần ngoài khung nhìn. Đây là trạng thái phổ biến nhất.
- **App đã tắt:** ✅ **không mô phỏng bù**. Tắt app thì thế giới **ngủ** và mở lại thì tiếp tục đúng chỗ cũ.
  - 💡 Thể hiện bằng lời: khi tắt app, vị thần "đi ngủ" cùng thế giới. Khi mở lại có hiệu ứng thức dậy ngắn (sương tan, chim hót) chứ không có bản tóm tắt. Kịch bản từng giây: [10 §8](10-giao-dien.md#8-hiệu-ứng-thức-dậy--đi-ngủ--02).
  - ✅ **Sinh khí nghỉ ngơi** (Q18): mỗi ngày lịch một lần, khi thế giới thức dậy, thần nhận thêm Sinh khí để bù cho người mở app ít giờ: bù phần còn thiếu so với 8 giờ của hôm trước, tối đa **10 phút thật** Sinh khí (↻ [11 §1.2](11-nhip-va-tang-tan.md#12-sinh-khí-nghỉ-ngơi--q22-giữ-trần-10-phút-thật)). Thế giới không chạy thêm, nên không mâu thuẫn với việc không mô phỏng bù. Công thức ở [08 §2](08-nhieu-vung-va-ao.md#2-thời-gian-giờ-app-mở--mùa-theo-ngày-lịch).
  - Hệ quả: người chơi không bao giờ mở máy ra thấy thế giới hỏng. Tiến trình gắn với **thời gian app được mở**, nên khuyến khích để game chạy nền.
  - ✅ Để dễ giữ app chạy:
    - **Khởi động cùng máy:** tắt mặc định, hỏi nhẹ nhàng một lần sau phiên chơi đầu tiên.
    - **Ẩn tạm:** thu dải đất vào biểu tượng trên menu bar (macOS) hoặc system tray (Windows). Thế giới vẫn chạy khi bị ẩn. Click biểu tượng để hiện lại.
  - Mùa chạy theo **thời gian mô phỏng** (1 mùa = 30 phút thật = 3 ngày đêm, [11 §1](11-nhip-va-tang-tan.md#1-nhịp-100)); tắt app thì mùa đứng yên. Thế giới chuyển dần sang mùa mới trong giờ mô phỏng đầu (khoảng 36 giây thật).
- **Không có vòng xoáy chết:** hệ sinh thái có thể suy giảm nhưng không bao giờ bị xoá sạch. Luôn còn "hạt giống ngủ" trong đất để hồi phục.

## Ví dụ một ngày chơi
| Thời điểm | Chuyện xảy ra |
|-----------|---------------|
| 9:00 | Mở máy, thế giới thức dậy. Hôm nay sang mùa thu nên lá dần chuyển đỏ. Click mời đàn ong đang chờ từ hôm qua. |
| 10:30 | Liếc xuống: một vùng đất đang ngả vàng. Kéo gọi mưa qua đó. |
| 12:00 | Một con cáo con chào đời. Click bong bóng để nhận chút Sinh khí. |
| 15:00 | Đủ Sinh khí. Mở quyền năng "Gió" để hạt giống bay xa hơn. |
| 16:00 | Nút ▶ bên phải hiện bong bóng 💌. Giữ nút cuộn sang: một con nai đang đứng ở mép rừng. |
| 17:30 | Vùng rừng đủ khoẻ, bắt đầu lan sang đất hoang bên phải và lộ ra một dòng suối ngầm. |
