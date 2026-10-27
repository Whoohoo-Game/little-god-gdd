# Little God — Game Design Document

> Phiên bản: **v0.3 (nháp)** · Cập nhật: 2026-10-23

Một vị thần nhỏ chăm sóc hệ sinh thái sống trong một dải đất nằm ở đáy màn hình máy tính, ngay trên Dock/taskbar.
Thiên nhiên tự vận hành trong lúc người chơi làm việc. Người chơi thỉnh thoảng liếc xuống và can thiệp nhẹ để thế giới tiếp tục sinh sôi.

## Quy trình & phạm vi
✅ Quy trình: **GDD → [Technical Doc](../Tech%20Doc/README.md) → triển khai**. Thiết kế được chốt trong GDD trước, sau đó chuyển thành Technical Doc, rồi mới sửa code. Mô hình Python trong `sim/` chỉ dùng để kiểm chứng số liệu của GDD.

✅ **Phạm vi GDD v1:**
- **Khái niệm cho toàn game** (01–05): mọi biome, loài, quyền năng, UI và kết game đều được mô tả ở mức ý tưởng.
- **Đặc tả chi tiết (số liệu, UI) chỉ cho vertical slice:**

  | Phần | Tài liệu đặc tả | Trạng thái |
  |------|-----------------|------------|
  | Đồng cỏ (7 loài) | [07](07-he-sinh-thai-chi-tiet.md) | 💡 Đã kiểm chứng |
  | Ao (5 loài) | [08 §6](08-nhieu-vung-va-ao.md#6-biome-ao) | 💡 Đã kiểm chứng |
  | Hồi sinh vùng, Sức khoẻ, Sinh khí nhiều vùng | [08 §3–5, §7](08-nhieu-vung-va-ao.md) | 💡 Đã kiểm chứng |
  | Khoảnh khắc (vòng ngắn) | [09](09-khoanh-khac.md) | 💡 Đã đặc tả, chưa kiểm chứng |
  | UI vertical slice (khay thần, nút cuộn, bản đồ mini, sổ tay tối giản, hiệu ứng thức dậy) | [10](10-giao-dien.md) | 💡 Đã đặc tả, chờ chơi thử |
  | Nhịp ×100, tầng tán (Sồi, Táo dại, Liễu) | [11](11-nhip-va-tang-tan.md) | 💡 Đã kiểm chứng |

- Ngoài slice (đặc tả sau khi chơi thử slice): Rừng, Thảo nguyên khô, Đồi đá, Khu Vườn Thiêng chi tiết, quyền năng Gió/Nắng ấm/Nắn đất/Sét, cháy rừng, sổ tay đầy đủ.

## Mục lục

| # | Tài liệu | Nội dung | Trạng thái |
|---|----------|----------|------------|
| 01 | [Tổng quan](01-tong-quan.md) | Tầm nhìn, trụ cột thiết kế, ràng buộc | 💡 Nháp |
| 02 | [Vòng lặp cốt lõi](02-core-loop.md) | Vòng lặp theo 3 thang thời gian | 💡 Nháp |
| 03 | [Hệ sinh thái](03-he-sinh-thai.md) | Mô phỏng thực vật, động vật, chuỗi thức ăn | 💡 Nháp |
| 04 | [Quyền năng của thần](04-quyen-nang-than.md) | Cách người chơi tương tác | 💡 Nháp |
| 05 | [Mở rộng thế giới](05-mo-rong-the-gioi.md) | Tiến trình, biome, mục tiêu cuối | 💡 Nháp |
| 06 | [Câu hỏi mở](06-cau-hoi-mo.md) | Các quyết định cần chốt | ✅ Đã chốt hết vòng 2 |
| 07 | [Hệ sinh thái: đặc tả chi tiết](07-he-sinh-thai-chi-tiet.md) | Số liệu, công thức cho đồng cỏ (luật đổi 2026-10-23, một số kết quả đo bằng luật cũ) | 💡 Đã kiểm chứng bằng mô hình |
| 08 | [Nhiều vùng & biome Ao](08-nhieu-vung-va-ao.md) | Hồi sinh 14 vùng, giá hồi sinh, Sức khoẻ vùng, biome Ao, nhịp kết game | 💡 Đã kiểm chứng bằng mô hình |
| 09 | [Khoảnh khắc](09-khoanh-khac.md) | Loại bong bóng, điều kiện, phần thưởng, giới hạn hiển thị, chỉ báo ngoài màn hình | 💡 Đã đặc tả, chưa kiểm chứng |
| 10 | [Giao diện](10-giao-dien.md) | Khay thần, nút cuộn, bản đồ mini, sổ tay, thẻ thông tin, thức dậy, cài đặt | 💡 Đã đặc tả, chờ chơi thử |
| 11 | [Nhịp ×100 & tầng tán](11-nhip-va-tang-tan.md) | Đồng hồ ×100, mùa theo thời gian mô phỏng, Sinh khí nghỉ ngơi mới, cây gỗ (Sồi, Táo dại, Liễu) | 💡 Đã kiểm chứng bằng mô hình |
| 12 | [Môi trường sống](12-moi-truong-song.md) | Biome theo cột do cỏ phủ lan, đất hoang tự bị lấn, động vật tự đến theo điều kiện sống, Sóc (bỏ mời, bỏ hồi sinh) | 💡 Đã kiểm chứng bằng mô hình |
| 13 | [Bầy đàn, lãnh thổ & nhịp sinh sản](13-bay-dan-va-sinh-san.md) | Thỏ, cá đi theo bầy; cáo, diệc, sóc giữ lãnh thổ; đi tới đích rồi nghỉ; sinh sản chậm lại, thú săn no lâu hơn | ✅ Đã chốt, đã kiểm chứng bằng mô hình |
| 14 | [Hang thỏ, né thú săn & rượt bắt](14-hang-tho-va-san-moi.md) | Mỗi hang một gia đình thỏ; con mồi tránh và chạy trốn về hang / cây; thú săn rượt nhanh và vồ | ✅ Đã chốt, đã kiểm chứng bằng mô hình |
| — | [`sim/ecosim.py`](sim/ecosim.py) | Mô hình Python dùng để kiểm chứng số liệu của file 07 | Công cụ |
| — | [`sim/worldsim.py`](sim/worldsim.py) | Mô hình nhiều vùng cho file 08–09 | Công cụ |
| — | [`sim/biomesim.py`](sim/biomesim.py) | Mô hình môi trường sống cho file 12 (biome theo cột, lấn đất hoang, động vật tự đến) | Công cụ |
| — | [`sim/socialsim.py`](sim/socialsim.py) | Mô hình bầy đàn / lãnh thổ / nhịp sinh sản cho file 13 (dựa trên `biomesim.py`) | Công cụ |
| — | [`sim/huntsim.py`](sim/huntsim.py) | Mô hình hang thỏ, né thú săn, rượt bắt cho file 14 (dựa trên `socialsim.py`) | Công cụ |
| — | [`sim/balance.json`](sim/balance.json) | **Nguồn số cân bằng duy nhất** cho `worldsim.py` và Unity (Tech Doc 03 §1). Đổi số ở đây | Dữ liệu |

**Ký hiệu dùng trong tài liệu**
- ✅ **Đã chốt**: đã thống nhất, chỉ sửa khi có lý do rõ ràng.
- 💡 **Đề xuất**: hướng đề xuất, chờ duyệt.
- ❓ **Cần quyết định**: còn bỏ ngỏ, xem file 06.

## Nhật ký quyết định

| Ngày | Quyết định |
|------|------------|
| 2026-10-26 | ✅ Hang thỏ **đào sâu, vẽ mặt cắt** (thấy đường hầm, buồng ngủ, thỏ nằm bên trong); **mỗi hang tối đa 4 con**, hang cách nhau ≥ 6 cột, lứa không vượt chỗ trong hang ([14 §2.1, §5, §6.1](14-hang-tho-va-san-moi.md)) |
| 2026-10-25 | ✅ Thỏ ngủ **trong hang**, sóc ngủ trên cây là luật mô phỏng (không ăn, không bị vồ, đói × 0.3); cáo no 15 giờ mp sau mỗi mồi, thức 15h–9h. Kết 15/16, ~62 con chết / ngày mp ([14 §3b](14-hang-tho-va-san-moi.md)) |
| 2026-10-25 | ✅ **Q34:** cảnh vồ mồi: bụi cỏ tung lên, con mồi biến mất, cáo thong thả về hang (thay phần săn của Q6). GDD 14 chốt |
| 2026-10-25 | 💡 **Đề xuất [14](14-hang-tho-va-san-moi.md):** thỏ sống theo gia đình quanh hang (đói thì dời hang), con mồi tránh và chạy trốn, thú săn rượt nhanh rồi vồ. Mô hình: kết 16/16, bị săn 67 → 46, tổng số con chết ~90 / ngày mp. Chờ Q34 (cách vẽ cảnh vồ) |
| 2026-10-24 | ✅ **Q32–Q33:** tạm giữ nhịp sinh / chết của 13; cáo sống theo cặp chung hang. GDD 13 chốt |
| 2026-10-24 | 💡 **Đề xuất [13](13-bay-dan-va-sinh-san.md):** thỏ, cá sống theo bầy; cáo (theo cặp), diệc, sóc giữ lãnh thổ; con vật đi tới đích rồi nghỉ thay vì bước ngẫu nhiên mỗi phút; mùa Đông không sinh, nghỉ giữa lứa dài hơn, thú săn no lâu hơn. Mô hình: quay đầu 33 → 2 lần/phút thật, số con chết giảm ~55%, kết game không đổi. Dương xỉ để lại 15 mùn (đã đổi trong `balance.json`) |
| 2026-10-24 | ✅ **1 mùa = 30 phút thật** (3 000 phút mp, trước 2 880) = đúng 3 ngày đêm; nhịp slice gần như không đổi ([11 §1.1, §1.4](11-nhip-va-tang-tan.md)) |
| 2026-10-24 | ✅ Ngày đêm theo **thời gian chơi**, không theo giờ máy: 1 000 phút mp = 10 phút thật (5 phút ngày + 5 phút đêm); thú có nếp ngủ / thức theo loài, chỉ là hình ([11 §1.5](11-nhip-va-tang-tan.md)) |
| 2026-10-24 | ✅ **Q30–Q31:** Vườn mở khi đất phủ kín + đủ mọi loài + mọi biome Khoẻ; Sinh khí dư để mở quyền năng theo cấp (sau slice) |
| 2026-10-24 | ✅ **Q25–Q29 ([12](12-moi-truong-song.md)):** bỏ mời động vật và hồi sinh vùng; biome theo cột do cỏ phủ lan (Cỏ, Dương xỉ); đất hoang tự bị lấn; gieo cỏ phủ ≤ 5 ô để đẩy ranh giới; thực vật ngoài biome mọc kém / không mọc; động vật tự đến theo điều kiện sống; thêm Sóc |
| 2026-10-24 | ✅ Rừng: gốc cây tán chỉ cần cách nhau 1 ô trống; cây phía xa mọc giữa hai cây tán liền nhau cách < 8 cột ([11 §2.2, §2.6](11-nhip-va-tang-tan.md)) |
| 2026-10-24 | ✅ Cây tán dễ trồng hơn: cây non ngủ khô thay vì chết; Sồi lớn nhanh gấp đôi, chịu khô và đất nghèo hơn ([11 §2.2–2.3](11-nhip-va-tang-tan.md#23-loài--q23-cả-ba)) |
| 2026-10-24 | ✅ **Nhịp ×100:** 1 phút thật = 100 phút mô phỏng; luật sinh thái giữ nguyên số. Slice còn ~1.5–2 giờ mở app ([11](11-nhip-va-tang-tan.md)) |
| 2026-10-24 | ✅ **Q21–Q24:** 1 mùa = 2 ngày mô phỏng (≈ 29 phút thật); Sinh khí nghỉ ngơi trần 10 phút thật; tầng tán có Sồi, Táo dại, Liễu; mở bằng khám phá 🌱 |
| 2026-10-24 | ✅ Hình: nền trời phủ cả dải (theo mùa và giờ máy), click ở đâu trong dải cũng vào game; đất dày 36 pt cho thấy cá trong ao |
| 2026-10-22 | ✅ Nền tảng: macOS + Windows, Unity 6, cửa sổ trong suốt dạng dải ở đáy màn hình (UniWindowController) |
| 2026-10-22 | ✅ Fantasy: thần chăm sóc **thiên nhiên và hệ sinh thái** (động vật, thực vật), không xoay quanh con người |
| 2026-10-22 | ✅ Nhịp chơi: **idle là chính**; người chơi ghé lại mỗi 10–30 phút để đưa ra vài quyết định |
| 2026-10-22 | ✅ Trục tiến trình: **mở rộng thế giới** (vùng đất, biome mới) |
| 2026-10-22 | ✅ Phát hành: **Steam premium**, bán một lần, không IAP |
| 2026-10-22 | ✅ Thế giới có **độ dài cố định, dài hơn màn hình**, di chuyển giữa các vùng bằng **giữ nút cuộn trên UI** (không chiếm con lăn chuột) |
| 2026-10-22 | ✅ **Không mô phỏng bù** khi tắt app: tắt app thì thế giới ngủ |
| 2026-10-22 | ~~Mùa đổi theo ngày thật: 1 mùa = 1 ngày thật~~ (thay bằng Q21, 2026-10-24) |
| 2026-10-22 | ✅ Thế giới dài **144 cột** (khoảng 3 màn hình) |
| 2026-10-22 | ✅ Chế độ "theo dõi" tự đưa khung nhìn đến sự kiện: có, **tắt mặc định** |
| 2026-10-22 | ✅ Ngày đầu chơi luôn là **Xuân**, sau đó mỗi ngày lịch đổi một mùa |
| 2026-10-22 | ✅ Có tuỳ chọn **khởi động cùng máy** (tắt mặc định) và **ẩn tạm** vào menu bar/system tray |
| 2026-10-22 | ✅ v1 có khoảng **40 loài**: 20 thực vật và 20 động vật |
| 2026-10-22 | ✅ Vị thần hiện hình là một **tinh linh nhỏ** trên dải đất |
| 2026-10-22 | ✅ Cái chết **nhẹ nhàng, nhìn thấy được**: nằm xuống, mờ dần, để lại hoa hoặc mùn; săn mồi chỉ là đuổi ra khỏi màn hình |
| 2026-10-22 | ✅ **Không đặt tên** cho sinh vật; trọng tâm là quần thể và hệ sinh thái, không phải cá thể |
| 2026-10-22 | ✅ Tinh linh **không tiến hoá** ở v1, chỉ đổi màu theo mùa |
| 2026-10-22 | ✅ Người chơi được **đặt tên cho vùng đất** đã hồi sinh; tên hiện trên bản đồ mini |
| 2026-10-22 | ✅ Biome cuối là **Khu Vườn Thiêng**: chỉ hồi sinh khi mọi biome khác cân bằng; Cây Thế Giới nở hoa là kết chính |
| 2026-10-22 | ✅ Nhiều màn hình: mặc định màn hình chính, **chọn được màn khác** trong cài đặt |
| 2026-10-23 | ✅ Quy trình GDD → Technical Doc → triển khai. Phạm vi GDD v1: khái niệm cho toàn game, đặc tả chi tiết chỉ cho vertical slice (Đồng cỏ, Ao, hồi sinh vùng, khoảnh khắc) |
| 2026-10-23 | ✅ **Q17:** giữ cân bằng tự nhiên + giảm giá hồi sinh tới 30% khi vùng kề Cân bằng; giữ bảng giá hiện tại (kết ~17 ngày ở 8h/ngày) cho tới khi chơi thử |
| 2026-10-23 | ✅ **Q18:** có Sinh khí nghỉ ngơi, bù giờ mở app còn thiếu so với 8 giờ của hôm trước, tối đa 2 giờ Sinh khí mỗi ngày |
| 2026-10-23 | ✅ **Q19:** sinh vật tự tìm đến vùng mới không cần click đón; click chỉ để nhận thưởng thêm |
| 2026-10-23 | ✅ **Q20:** bỏ Chúc phúc; vai trò "vuốt ve" chuyển sang click khoảnh khắc |
| 2026-10-23 | ✅ **Không có dịch bệnh.** Cân bằng sinh thái đến từ chuỗi thức ăn như tự nhiên: thú ăn cỏ đông quá thì ăn trụi cỏ và **chết đói**; thú săn điều hoà bằng cách ăn thú ăn cỏ (xem [08 §7.3](08-nhieu-vung-va-ao.md#73-cân-bằng-tự-nhiên-ăn-trụi-chết-đói-thú-săn)) |
| 2026-10-22 | ✅ Âm thanh: **ambient** theo biome/mùa/ngày đêm (bật, âm lượng thấp) + **nhạc tuỳ chọn** (tắt mặc định) |
