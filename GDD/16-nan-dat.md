# 16 · Nắn đất: đào ao, lấp ao

> Trạng thái: ✅ **Đã chốt** 2026-10-27 (Q43–Q49, [06](06-cau-hoi-mo.md)). Chưa kiểm chứng bằng mô hình (chưa có mô hình Python cho ao động); đo bằng test thống kê C#.
> Đặc tả quyền năng ⛰️ **Nắn đất** đã có ở mức ý tưởng trong [04 §2](04-quyen-nang-than.md#2-danh-sách-quyền-năng) ("đào ao hoặc đắp gò ở một cột, cách duy nhất để tạo nước mới, đắt").
> **Thay** ao cố định 4 cột nước ở giữa vùng ao (08 §3): ao giờ là bất kỳ dải cột nước liền nhau nào, do thế giới sinh ra hoặc do người chơi đào.

## 1. Vì sao
Sau chơi thử 2026-10-27: người chơi muốn tự **đổi ô đất thành ô nước và ngược lại**, để mở rộng, thu hẹp, hay tạo ao mới. Cá, diệc, bèo, sen, lau, liễu đều phụ thuộc vào nước, nhưng người chơi chưa có cách nào chỉnh "nước nhiều hay ít" và "nước ở đâu".

## 2. Đã chốt
| # | Quyết định |
|---|------------|
| ✅ Q43 | **Đào ao mới ở bất kỳ đâu.** Mỗi lần đào / lấp đúng **1 ô** (một cột). Muốn ao dài thì đào từng ô. **Môi trường của ao tự sinh ra theo độ rộng ao** (§4) |
| ✅ Q44 | **Mở ngay** trong slice. Giá: **đào 150**, **lấp 100** Sinh khí mỗi ô |
| ✅ Q45 | **Công cụ ⛰️ riêng** trong khay thần, cạnh Gieo / Mưa |
| ✅ Q46 | **Không giới hạn** độ rộng ao: rộng bao nhiêu tuỳ người chơi đào bao nhiêu ô (mỗi lần 1 ô) |

## 3. Ao là gì (✅ suy ra từ Q43, Q46)
- **Ao = một dải cột nước liền nhau.** Ba ao có sẵn của thế giới (08) vẫn còn, nhưng không còn đặc biệt: luật như mọi ao người chơi đào.
- **Đào** một cột đất:
  - giữa đất liền → **ao mới** rộng 1 ô;
  - kề một ao → ao đó **rộng thêm** 1 ô;
  - nằm giữa hai ao (cách nhau đúng 1 ô) → hai ao **nhập làm một**.
- **Lấp** một cột nước:
  - ở mép ao → ao **hẹp lại** 1 ô;
  - ở giữa ao → ao **tách làm hai**;
  - ô nước cuối cùng của ao → ao **biến mất** (Q47).
- Đào được trên: **cột đất có sự sống** (không đào đất hoang, không đào trong Khu Vườn Thiêng). Lấp được: mọi cột nước.
- Vùng có tên (14 vùng) vẫn giữ để gọi tên, đo Sức khoẻ, bản đồ mini; ao không còn gắn với "vùng ao".

## 4. Môi trường tự sinh theo độ rộng (✅ Q48)
Ý của Q43: ao càng rộng thì càng nhiều sự sống, không cần người chơi gieo từng thứ.

| Khi | Tự sinh ngay |
|-----|--------------|
| Mỗi **cột nước mới** (đào) | Một cụm **Bèo** mọc ở cột đó nếu ao đã có bèo hoặc ao vừa đào ≥ 2 ô; ao 1 ô chỉ là vũng nước, chưa có bèo |
| Mỗi **bờ mới** (cột đất kề nước, trống tầng bụi) | **Lau sậy** mọc ở bờ, tối đa 1 cây mỗi bờ mỗi lần đào |
| Ao rộng ≥ 4 ô | Đủ chỗ cho **Cá** tự tìm đến theo luật cũ (≥ 4 bèo, 12 §3); ao càng rộng càng nhiều bèo nên càng nhiều cá. Mỗi 8 ô nước có chỗ cho thêm một bầy cá (GDD 13: bầy cách nhau ≥ 8 cột) |
| Có cá | **Diệc**, **Sen** (khám phá), **Liễu** (bờ có lau) đến theo luật cũ |

Như vậy độ rộng quyết định ao "sống" tới đâu: vũng 1 ô → ao nhỏ có bèo, lau → ao ≥ 4 ô có cá → ao lớn nhiều bầy cá và diệc.

## 5. Hệ quả lên ô bị đổi (✅)
| Đổi | Cây trên ô | Động vật trên ô | Đất |
|-----|-----------|-----------------|-----|
| **Đào** (đất → nước) | Cây cạn (cả cây tán) chết, để lại Mùn như chết thường | Thú trên cạn bước sang cột đất kề. Hang thỏ đè lên thì nhà dời hang (✅ luật hang chỉ trên đất, 14 §2) | Thành nước: ẩm 100. Cột kề thành **bờ** (Lau sậy, Liễu mọc được) |
| **Lấp** (nước → đất) | Bèo, Sen chết, để lại Mùn | Cá ở ô đó bơi sang ô nước còn lại của ao | Thành đất ẩm 80, đất màu như bờ ao, mang biome của cột đất kề; cỏ phủ lấn tới như đất mới (12 §2.1) |

- ✅ **Q47.** Lấp ô nước cuối cùng của ao: cá trong ao **rời đi nhẹ nhàng** (biến mất, không tính chết, không để xác), diệc của ao đó bay đi.

## 6. Thao tác
- Khay thần: nút **⛰️ Nắn đất**. Cầm công cụ, rê lên một cột: cột đất sống sáng **xanh nước** = sẽ đào (giá 150); cột nước sáng **nâu** = sẽ lấp (giá 100); không đổi được (đất hoang, Vườn) tô đỏ, thẻ báo lý do. Click: đổi đúng 1 ô, bụi đất / tia nước bắn lên.
- Chuột phải / Esc / 20 giây không dùng thì thả công cụ (như Gieo, Mưa).
- ✅ **Q49.** **Chỉ click từng ô**; không kéo chuột đào liền nhiều ô.

## 7. Việc kéo theo
- **Kỹ thuật:** mô phỏng đang gắn ao vào vùng (cá bơi trong `WaterStart..WaterEnd` của vùng, diệc / bầy cá theo "ao" = vùng). Phải đổi sang ao động (dải nước liền nhau, tính lại sau mỗi lần đào / lấp), save lên phiên bản mới. Viết ở Tech Doc khi các câu trên đã chốt.
- **Cân bằng:** người chơi có thể đào rất nhiều nước. Đào đắt (150) và mất đất trồng cỏ nên tự hạn chế; sẽ đo lại kết game, số cá / diệc khi đã có code (chưa có mô hình Python cho ao động).
