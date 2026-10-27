# 12 · Môi trường sống: biome tự lan, động vật tự đến

> Trạng thái: ✅ **Đã chốt** 2026-10-24 (Q25–Q31, [06](06-cau-hoi-mo.md)). 💡 Đã kiểm chứng bằng `sim/biomesim.py` (§7) và đã có trong game (C# khớp thống kê, [Tech Doc 06](../Tech%20Doc/06-moi-truong-song.md)).
> Phần này **thay** hồi sinh vùng (05 §3, 08 §4), lời mời 💌 (07 §6.5, 09) và biome theo vùng thiết kế sẵn (08 §3).

## 1. Ý tưởng
Người chơi **không mua** động vật, **không mở khoá** vùng hay biome. Người chơi tạo môi trường: gieo cây cỏ, gọi mưa. Thiên nhiên làm phần còn lại:
- **Cỏ của mỗi biome** lan dần, chiếm đất hoang thành biome của nó.
- Hai biome gặp nhau thì đứng ở ranh giới. Người chơi **đẩy ranh giới** bằng cách gieo cỏ của biome mình gần ranh giới.
- Mỗi biome có **thực vật đặc trưng**. Thực vật lạ mọc kém ở vùng giáp ranh, không mọc nổi khi ở sâu trong biome khác.
- Động vật **tự đến** nơi có đủ môi trường sống của chúng.

## 2. Biome theo cột
- Mỗi cột đất mang **một biome** (hoặc chưa có: đất hoang). Biome của cột là biome của **cỏ phủ** đang mọc ở đó; cỏ chết thì cột giữ biome cũ cho tới khi cỏ khác chiếm.
- Cột nước luôn là **Ao**. Ao (nước) "thức dậy" khi một cột đất kề nó có sự sống; lúc đó tự có 2 cụm bèo, 1 lau sậy ở bờ, và **nước mang hạt sang bờ bên kia**: bờ đối diện mọc cỏ phủ của biome đã chạm tới ao (không có luật này thì cỏ không vượt được 4 ô nước, đất hoang sau ao không bao giờ được lấn).

| Biome | Cỏ phủ (lan biome) | Thực vật đặc trưng |
|-------|--------------------|--------------------|
| **Đồng cỏ** | **Cỏ** | Cỏ, Hoa dại, Mâm xôi |
| **Rừng** | 🆕 **Dương xỉ** (ưa bóng, ẩm) | Dương xỉ, Sồi, Táo dại, Mâm xôi |
| **Ao** | (nước) Bèo | Bèo, Sen |
| Bờ ao (mọi biome) | — | Lau sậy, Liễu: chỉ cần cột đất kề nước, không theo biome |

- **Đoạn biome** (08 §5.1) giờ là các cột sống liền nhau cùng biome; Sinh khí, Đa dạng tính theo đoạn như cũ. Các vùng có tên (14 vùng) vẫn còn để gọi tên, đo Sức khoẻ và cho bản đồ mini.

### 2.1 Cỏ lấn đất hoang (✅ Q25)
- Hạt của **cỏ phủ** rơi xuống cột đất hoang thì nảy mầm như ở đất thường (theo độ ẩm, đất màu). Mầm nảy thì cột **có sự sống** và mang biome của cỏ đó.
- Lấn nhanh hay chậm phụ thuộc độ ẩm ở mép đất sống: mùa hạ khô thì gần như dừng lấn, gọi mưa ở mép thì lấn nhanh lại. Cỏ (cần ẩm 15) lấn nhanh hơn Dương xỉ (cần ẩm 25).
- 💡 Hạt rơi xuống đất hoang nảy với xác suất **× 0.4** so với đất thường (đất cằn). Cột vừa được lấn có **đất màu 35** (như vùng hồi sinh cũ): đất màu thấp hơn thì Sồi, Mâm xôi không mọc nổi trên đất mới và rừng không thành hình (§7).
- Không có lệnh hồi sinh, không có giá hồi sinh, không có giảm giá hồi sinh.

### 2.2 Gieo và đẩy ranh giới (✅ Q26)
- Người chơi gieo được trên đất sống và trên **đất hoang cách đất sống ≤ 5 ô**.
- Gieo **cỏ phủ của biome A** vào trong biome B, **cách cột A gần nhất ≤ 5 ô**: khoảng cột ở giữa thành **hành lang của A**. Trong hành lang, cỏ A mọc như ở nhà; thực vật của B mọc kém (× 0.5, như giáp ranh). Cỏ A dần chiếm từng cột, cột đổi sang biome A khi cỏ A trưởng thành ở đó. Hết hành lang khi mọi cột trong đó đã là A.
- Xa hơn 5 ô thì không nối: cỏ A gieo sâu trong B mọc kém hoặc không mọc (§2.3).

### 2.3 Thực vật ngoài biome (✅ Q27)
| Cột | Hệ số độ phù hợp q |
|-----|--------------------|
| Biome thuộc danh sách của loài | × 1 |
| Cách cột biome của loài **≤ 5 ô** (giáp ranh), hoặc trong hành lang của biome đó | × 0.5 |
| Sâu hơn 5 ô trong biome khác | × 0 (không mọc) |
| Đất hoang | Cỏ phủ: × 1 (lấn đất). Loài khác: như giáp ranh nếu cách biome của nó ≤ 5 ô, không thì × 0 |
| ✅ **Cỏ phủ** (Cỏ, Dương xỉ) ở bất kỳ đâu | **Ít nhất × 0.5**: cỏ phủ là cây tiên phong. Nhờ vậy người chơi luôn mở được biome mới giữa biome khác: một mảng Dương xỉ gieo giữa đồng cỏ lớn chậm, trưởng thành thì cột thành Rừng, rồi Sồi mọc được quanh đó. Không có luật này thì khi đồng cỏ đã phủ kín, rừng không bao giờ thành hình |

Cây đang sống mà biome quanh nó đổi (bị lấn) thì yếu dần và chết theo luật sức khoẻ thường (07 §5): rừng lấn đồng cỏ làm hoa dại ở đó tàn dần, đồng cỏ lấn rừng thì sồi già ở đó ngủ khô rồi chết.

## 3. Động vật tự đến (✅ Q29: ≥ 2 con, chờ 2 giờ mô phỏng)
- Mỗi 30 phút mô phỏng, xét từng **đoạn biome** (cá, diệc: từng ao). Loài **vắng** ở đó (< 2 con; giun: chưa có cột nào; ong: chưa có đàn nào; thú săn: tính cả đoạn kề) mà đoạn đạt **đủ mọi điều kiện sống** (bảng dưới) **liên tục 2 giờ mô phỏng** (~1.2 phút thật) thì **một cặp** đi vào từ mép đoạn (cá: 3 con xuất hiện trong ao; ong: 2 đàn, vì ong cần ≥ 2 đàn gần nhau mới chia đàn được).
- Lần đầu một loài xuất hiện trong thế giới là khoảnh khắc ✨ **"Loài mới"** (thay 💌): click để chào đón, có thưởng nhỏ. Không tốn gì.
- Không đến vào mùa Đông (trừ giun). Không có luật "rời đi": điều kiện sống mất thì quần thể tự suy theo luật hiện có.

| Loài | Biome | Thức ăn | Chỗ trú / khác |
|------|-------|---------|----------------|
| 🪱 Giun | Đồng cỏ, Rừng | — | Cột có cỏ phủ sống, **mùn ≥ 5**, **ẩm ≥ 30**. Cả mùa Đông. Lan sang cột kề như nay |
| 🐝 Ong | Đồng cỏ, Rừng, Ao | **≥ 6 cây ra hoa** sống trong đoạn | ≥ 1 bụi hoặc cây tán trong đoạn (tổ). Xuân–Hạ |
| 🐇 Thỏ | Đồng cỏ | **≥ 12 cỏ** sống trong đoạn | ≥ 1 bụi hoặc cây tán trong đoạn (chỗ trốn) |
| 🦊 Cáo | Đồng cỏ, Rừng | **≥ 8 thỏ + sóc** trong đoạn và đoạn kề | ≥ 3 cây tán hoặc mâm xôi trong đoạn (hang); đoạn + kề dài ≥ 20 cột. (Bản đầu đòi "đồng cỏ giáp rừng": ao chen giữa nên gần như không có chỗ nào như vậy, cáo không đến) |
| 🐟 Cá | Ao | **≥ 4 bèo** sống | Không mùa Đông (mặt ao đóng băng) |
| 🪶 Diệc | Ao | **≥ 6 cá** | Bờ có ≥ 2 lau sậy hoặc 1 liễu |
| 🐿️ **Sóc** 🆕 (Q28) | Rừng | **≥ 2 Sồi trưởng thành** trong đoạn | Không mùa Đông |

### 3.1 Sóc (🆕)
- Ăn hạt sồi: no khi có ≥ 2 Sồi trưởng thành trong 6 cột (như ong với hoa); mỗi Sồi nuôi 2 sóc; sống 2 ngày mô phỏng, trưởng thành 2 giờ, lứa 2, nghỉ giữa lứa 6 giờ mô phỏng.
- **Chôn hạt:** Sồi có sóc trong 6 cột thì hạt rơi xa **± 5 cột** (thay ± 2) → rừng tự lan.
- Là **mồi thứ hai của cáo** (cáo bắt thỏ hoặc sóc, con nào gần).

## 4. Khám phá thực vật 🌱
| Loài | Điều kiện |
|------|-----------|
| Hoa dại, Mâm xôi, Sen | Như cũ (09 §3.2) |
| **Dương xỉ** 🆕 | Một vùng có ≥ 4 Mâm xôi sống (thay cho Sồi) |
| Sồi | Thế giới có ≥ 4 Dương xỉ sống |
| Táo dại | Đã có Rừng và ≥ 1 đàn ong |
| Liễu | Một ao có ≥ 2 Lau sậy sống |

## 5. Kết game (✅ Q30)
**Khu Vườn Thiêng mở** khi cùng lúc:
1. **Đất hoang đã phủ kín**: mọi cột đất ngoài Vườn đều có sự sống.
2. **Mọi loài đã từng xuất hiện**: Giun, Ong, Thỏ, Cáo, Cá, Diệc, Sóc.
3. **Mọi biome đang có đều Khoẻ**: Sức khoẻ của biome (mỗi đoạn tính như Sức khoẻ vùng 08 §5.3 trên cột của đoạn, rồi lấy trung bình theo số cột mọi đoạn cùng biome) **≥ 60**.

Vườn mở thì thiên nhiên các biome kề tràn vào Vườn như đất hoang; **kết game** khi Vườn có sự sống phủ ≥ 80% cột. Không tốn Sinh khí. Điều kiện cũ "13 vùng cùng lúc Cân bằng" bỏ: vùng giờ lẫn nhiều biome nên gần như không đạt được cùng lúc.

## 6. Hệ quả
- **Sinh khí** chỉ còn dùng để gieo và gọi mưa (bỏ mời ~780 và hồi sinh ~520 000), nên dư rất nhiều. ✅ **Q31:** Sinh khí dư dùng để **mở quyền năng mới theo cấp** (Gió mang hạt, Nắng ấm…), thiết kế sau slice. Trong slice, Sinh khí dư chỉ đẩy cấp thần lên.
- **Khoảnh khắc (09):** bỏ 💌 Lời mời và 🌿 Sẵn sàng hồi sinh; thêm ✨ Loài mới và ✨ "Biome lan tới …". Ghi chú lại ở 09 khi chốt số.
- **UI (10):** khay bỏ nút 💌 và 🌿; công cụ Gieo cho gieo trên đất hoang trong tầm 5 ô, xem trước cho thấy hành lang khi gieo cỏ phủ gần ranh giới.

## 7. Kiểm chứng (`sim/biomesim.py`, 8 seed, 2026-10-24)
`biomesim.py` dùng chung luật cây / thú / Sinh khí của `worldsim.py`, thay phần vùng, hồi sinh, mời; thông số ở `balance.json` → `biomeModel`. Người chơi mô hình: mưa vùng khô, trồng hoa / bụi theo đồng cỏ, Sồi / Táo / Mâm xôi ở chỗ có ≥ 3 cột rừng, Sen / Liễu ở ao; khi dư ≥ 150 Sinh khí thì lấn đất hoang ở hai mép (trái bằng Dương xỉ, phải bằng Cỏ); đất kín mà rừng < 6 cột thì gieo một mảng 6 cột Dương xỉ giữa đồng cỏ.

| Kịch bản | Đất hoang phủ kín | Vườn mở → kết game (giờ thật) | Ghi chú |
|----------|-------------------|-------------------------------|---------|
| Ghé mỗi 3 phút | 0.4–1.1 giờ | **7/8 seed, trung vị 1.1** (0.6–3.0) | Sóc là loài đến cuối (0.6–2.9 giờ) |
| Ghé mỗi 3 phút, không gọi mưa | 0.4–0.7 giờ | **8/8, trung vị 1.3** (0.7–2.0) | |
| Ghé mỗi 6 phút | 0.7–1.3 giờ | **8/8, trung vị 1.4** (1.2–1.9) | |
| Ghé mỗi 18 phút | 0.6–1.8 giờ | **4/8 trong 8 giờ thật, trung vị 5.1** (4.1–7.0) | Ít rừng → Sóc đến muộn (3.3–7.2 giờ) |
| Không gieo, không mưa | 0.9–2.3 giờ | không kết | Chỉ có đồng cỏ + ao: thỏ, cá, diệc, giun. Không hoa → không ong; không bụi / cây → không cáo, sóc |

- **Lần đầu xuất hiện** (ghé 3 phút): Thỏ, Ong, Cá, Cáo 0.1–0.2 giờ · Diệc 0.2 · Giun 0.3–1.2 · Sóc 0.6–2.9.
- Nhịp slice (~1.1–1.4 giờ thật với người chơi chăm) gần với nhịp ×100 cũ (~1.4 giờ, GDD 11 §1.4).
- **Những chỗ phải sửa khi chạy thử** (đã đưa vào luật ở trên):
  - bờ ao bên kia mọc cỏ khi ao thức dậy, vì cỏ không vượt được 4 ô nước;
  - đất mới lấn có màu 35, vì với màu thấp Sồi và Mâm xôi không mọc nổi;
  - ong đến 2 đàn, vì 1 đàn không chia đàn được;
  - cáo đến đồng cỏ hoặc rừng, vì ao chen giữa nên gần như không có "đồng cỏ giáp rừng";
  - Sức khoẻ vùng lấy trung bình mọi đoạn trong vùng (vùng ao gồm nước + bờ);
  - Sóc cần 2 Sồi trưởng thành, mỗi Sồi nuôi 2 sóc; Sồi mở khi có ≥ 4 Dương xỉ;
  - cỏ phủ là cây tiên phong, gieo đâu cũng mọc nửa sức (nếu không, đồng cỏ kín thì không bao giờ có rừng);
  - điều kiện kết đổi theo Q30 (vùng lẫn nhiều biome nên "13 vùng cùng lúc Cân bằng" gần như không đạt).
- **Còn biết:** ong ít hơn mô hình cũ (2–12 đàn so với 12–23) vì hoa dại chết khô hàng loạt khi đất sống rộng nhanh; Sinh khí dư (Q31, quyền năng theo cấp sau slice).
