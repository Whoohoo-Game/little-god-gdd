# 15 · Sinh động & phản hồi

> Trạng thái: ✅ **Đã chốt** 2026-10-27 (Q35–Q38, [06](06-cau-hoi-mo.md)). Tần suất khoảnh khắc ở §3.7 đã đo bằng `sim/momentsim.py`.
> §1 và §2 **chỉ là hình**: không đổi luật, không đổi `balance.json`, không cần chạy lại mô hình. §3 thay số của [09](09-khoanh-khac.md) cho nhịp ×100 và cần đo tần suất (§3.7).
> Bổ sung cho [09](09-khoanh-khac.md) (làm trước một bản rút gọn), [11 §2.6](11-nhip-va-tang-tan.md#26-hình), [13 §7](13-bay-dan-va-sinh-san.md#7-hiển-thị-gợi-ý-cho-tech-doc) và [14 §5](14-hang-tho-va-san-moi.md#5-hiển-thị).

## 0. Vấn đề và mục tiêu

### 0.1 Từ lần chơi thử 2026-10-27
- **Phải chờ quá lâu mới thấy biến chuyển.** Mô phỏng không chậm (cỏ lớn trong 12 giây, thỏ đến sau 6–12 phút). Vấn đề là **mắt không nhận ra thay đổi**:
  - cỏ lấn thêm một cột, hay thỏ tăng từ 5 lên 6 con, thì liếc qua không thấy khác;
  - hệ khoảnh khắc (M5), thứ được thiết kế để mỗi lần liếc có một điều mới, chưa có trong game;
  - thao tác của thần thiếu phản hồi: gọi mưa xong chỉ thấy mưa rơi; gieo Sồi thì gần 15 phút thật sau mới thấy cây ra dáng.
- **Cuộc sống chưa sinh động.** Mọi thứ trên màn hình đều là sinh vật của mô phỏng, mà số lượng được giữ thưa để cân bằng (~26 thỏ trên 144 cột, mỗi màn hình chỉ thấy khoảng 1/3). [13](13-bay-dan-va-sinh-san.md) còn chủ ý giảm đi lại. Trong lúc nghỉ (6–36 giây thật), con vật đứng yên.

### 0.2 Nguyên tắc
1. **Không đụng cân bằng.** Mọi thứ trong §1, §2 đọc từ mô phỏng, không ghi vào mô phỏng, không lưu, và dùng **dòng số ngẫu nhiên riêng của phần hình** (không dùng PRNG của `World`), để lưu–đọc vẫn tất định.
2. **Đẹp là thông tin.** Sinh vật trang trí chỉ xuất hiện khi môi trường thật sự đủ điều kiện (bướm khi có hoa, đom đóm khi đất ẩm). Thế giới khoẻ thì nhìn rộn ràng, suy thì vắng lặng. Liếc qua vẫn đọc được tình trạng (01 · Phong cách hình ảnh).
3. **Hình không nói dối.** Hiệu ứng có thể đi trước luật vài giây, nhưng không bao giờ cho thấy điều trái với mô phỏng. Ví dụ: cây vàng không xanh lại tức thì sau mưa; chỉ cây **đang hồi sức thật** mới có dấu hiệu hồi sức.
4. **Không làm phiền** (trụ cột 3): không nhấp nháy mạnh, không âm thanh tự phát, có cài đặt giảm hiệu ứng (§2.5).

### 0.3 Mục tiêu đo được
| Chỉ số | Mục tiêu | Đo bằng |
|--------|----------|---------|
| Thao tác của thần → thấy thay đổi | **≤ 1 giây** | Thử tay |
| Thao tác của thần → thấy kết quả có ý nghĩa | **≤ 5 giây** (cỏ, mưa); cây tán: một bước lớn **mỗi ~3 phút** | Thử tay |
| Khoảng lặng trong khung nhìn (không con nào làm gì ngoài đi / đứng yên) khi khung nhìn có ≥ 3 con thức | **≤ 3 giây** | Bộ đếm dev (§2.4) |
| Khoảnh khắc trên toàn thế giới | trung bình **≥ 1 mỗi 4 phút thật** | Mô hình (§3.7) |
| Khoảng trống dài nhất không có khoảnh khắc (sau 10 phút đầu) | **≤ 10 phút thật** | Mô hình (§3.7) |

---

## 1. Phản hồi tức thì

### 1.1 Mưa
Luật không đổi: Mưa cộng độ ẩm cho 7 cột ([04](04-quyen-nang-than.md)). Thêm phần hình:

| Hiệu ứng | Khi nào | Thời gian | Ghi chú |
|----------|---------|-----------|---------|
| **Đất ướt**: mặt đất các cột bị mưa sẫm lại | Từ giọt mưa đầu tiên | Hiện trong 1 giây; nhạt dần theo **độ ẩm thật** của cột | Độ ẩm ≥ 60: sẫm hẳn; 40–60: sẫm vừa; < 40: như thường. Đây là thông tin thật, không chỉ trang trí |
| **Vũng nước** nhỏ (1–2 vũng / 7 cột) | Cột chưa có cây tầng Thảm che kín | 20 giây, co lại rồi mất | Không có mùa Đông (tuyết) |
| **Cây ngẩng lên**: cỏ, hoa, bụi nhún nhẹ (co 0.92 rồi dãn 1.04 rồi về 1) | Khi mưa chạm cột | 0.4 giây, lệch nhau 0–0.3 giây mỗi cây | Cho cảm giác "được tưới" ngay |
| **Hồi sức**: một chấm lá xanh nhỏ bay lên khỏi cây | Cây có máu < 100 **và** máu đang tăng | Mỗi cây tối đa 1 chấm mỗi 3 giây, trong 30 giây sau mưa; tối đa 8 chấm cùng lúc trên khung nhìn | Theo nguyên tắc 3: chỉ cây hồi thật mới có |
| **Cầu vồng** | Mưa (của thần hoặc tự nhiên) tắt lúc ban ngày (7h–16h), không phải mùa Đông | Hiện 2 giây, giữ 15 giây, mờ 3 giây (theo tốc độ chơi). ✅ (2026-10-27) Không bao giờ còn sau 17h: mờ hẳn trong khoảng 16h–17h | Xác suất **25%** mỗi lần mưa tắt; toàn thế giới tối đa 1 lần mỗi 5 phút thật. Vòng cung mờ (độ đục ≤ 35%) phía sau cây |

### 1.2 Gieo
| Bước | Thời gian | Hình |
|------|-----------|------|
| Tinh linh bay tới chỗ gieo | 0.3 giây | Như 04 §0 |
| Hạt rơi xuống, đất bung nhẹ | 0.2 giây | Bụi đất (`DustPuff`), 3–4 hạt đất |
| **Mầm nhú lên** | 0.5 giây | Ngay cả khi mô phỏng chưa coi là nảy mầm, chỗ gieo hiện một mầm 2 lá (hạt đã nằm trong đất là thật) |
| Lấp lánh | 0.6 giây | `Sparkle` như hiện tại |

**Cây lớn qua từng giai đoạn nhìn thấy được.** Hiện cây lớn đều theo tỉ lệ, nên trong 15 phút không có lúc nào đáng chú ý. Đề xuất chia thành các bậc, mỗi lần lên bậc có hiệu ứng **"lớn lên"** (nhún 1 → 1.08 → 1 trong 0.4 giây, 3 chấm lá bay lên):

| Loại | Thời gian lớn (phút thật) | Các bậc (theo % thời gian lớn) | Một bậc mỗi |
|------|---------------------------|--------------------------------|-------------|
| Cây tán (Sồi, Táo dại, Liễu) | 14.4 | Mầm 2 lá (0%) → Cây con (20%) → Cây nhỡ (40%) → Cây non tán thưa (60%) → Cây non tán dày (80%) → Trưởng thành (100%) | ~2.9 phút |
| Mâm xôi | 1.2 | Mầm (0%) → Bụi nhỏ (50%) → Đủ bụi (100%) | ~36 giây |
| Cỏ, Dương xỉ, Hoa dại, Bèo, Sen, Lau sậy | ≤ 1.2 | Giữ lớn liền như hiện tại; **Hoa dại nở** có nhún + 2 cánh hoa bay lên | — |

- Giữa hai bậc cây vẫn lớn dần như hiện tại; bậc chỉ đổi **dáng** (số cành, độ dày tán) và tạo lúc để mắt bắt được.
- Cây tán ở bậc 1–2 có **cọc nhỏ và dây buộc** (dấu tay của thần), mất khi lên Cây nhỡ. Liếc qua là biết "cây mình trồng".
- Sau Trưởng thành, cây lớn tiếp tới đủ cỡ như [11 §2.6](11-nhip-va-tang-tan.md#26-hình); không thêm bậc.
- Cây vừa trôi vào khung nhìn hiện đúng bậc hiện tại, không diễn lại hiệu ứng (như luật lá ở 11 §2.6).

### 1.3 Đất hoang được lấn
Luật: cột đất hoang có sự sống khi cỏ phủ nảy mầm ([12 §2.1](12-moi-truong-song.md#21-cỏ-lấn-đất-hoang--q25)).

- **Đổi màu đất:** cột chuyển từ màu đất hoang sang màu đất của biome trong **2 giây**, lan từ phía cột sống kề bên sang, nên một chuỗi cột liền nhau trông như **sự sống đang bò tới**.
- **Dấu "mới":** viền cỏ của cột sáng nhẹ (độ sáng +15%) trong **60 giây thật** rồi về bình thường.
- **Biome mới thành hình** (lần đầu một đoạn Rừng đạt ≥ 3 cột liền nhau; hay lần đầu một Ao thức dậy): dải lá / gợn sóng lấp lánh chạy dọc cả đoạn trong 1.5 giây. Đây đồng thời là khoảnh khắc ✨ ở §3 nếu đủ giãn cách.

### 1.4 Ong và quả
- Ong đậu hoa: **phấn hoa** (2–3 chấm vàng) rơi khỏi hoa. Hoa được thụ phấn ([08 §7.2](08-nhieu-vung-va-ao.md#72-ong-chia-đàn)) có một chấm vàng nhỏ ở nhuỵ tới khi tàn.
- Quả (Mâm xôi, Táo dại) **chín dần** từ xanh sang đỏ trong 20 giây thật đầu mùa có quả, thay vì hiện đỏ ngay. Thú ăn quả ([11 §2.3](11-nhip-va-tang-tan.md#23-loài--q23-cả-ba)) đứng dưới cây thì có hoạt ảnh **với lên ăn** (§2.2).

### 1.5 Click vào con vật
Hiện click con vật mở thẻ thông tin ([10](10-giao-dien.md)). Thêm: con vật **phản ứng** trong 1 giây (thỏ giật tai và nhìn lên con trỏ, cáo vẫy đuôi, sóc đứng thẳng, diệc nghiêng đầu, cá quẫy). Con đang ngủ thì chỉ trở mình, không thức dậy.

---

## 2. Sinh vật trang trí & hành vi nhỏ

### 2.1 Sinh vật trang trí (chỉ là hình)
Không ăn, không bị săn, không tính Sinh khí hay Đa dạng, không lưu, không click được (click đi xuyên qua tới thứ phía dưới). Chỉ sinh trong khung nhìn cộng **4 cột** mỗi bên, để cuộn tới đã thấy sẵn.

Giờ dưới đây là **giờ trong ngày** của game ([11 §1.5](11-nhip-va-tang-tan.md#15-ngày-đêm-và-nếp-sinh-hoạt--2026-10-24-chỉ-là-hình)); 1 giờ trong ngày ≈ 25 giây thật.

| Sinh vật | Điều kiện (đọc từ mô phỏng) | Số lượng | Hành vi | Sống |
|----------|-----------------------------|----------|---------|------|
| 🦋 **Bướm** | Đồng cỏ, Xuân–Thu, 7h–17h, có Hoa dại đang nở | 1 bướm cho mỗi **4 Hoa dại** nở trong vùng sinh; tối đa **5** | Bay lượn lên xuống (biên độ 6–12 pt), **đậu lên hoa** 3–8 giây rồi bay tiếp | 40–90 giây, rồi bay lên khỏi dải |
| 🪰 **Chuồn chuồn** | Ao có ≥ 2 Lau sậy hoặc ≥ 1 Sen; Xuân–Hạ; 7h–17h | 1–2 mỗi ao | Lướt ngang mặt nước, **dừng giữa không trung** 1–2 giây, đậu ngọn lau 4–10 giây | Ở lại khi còn điều kiện |
| ✨ **Đom đóm** | 20h–4h, Hạ (và nửa sau Xuân), cột có độ ẩm ≥ 50 và có cỏ hoặc bụi | 1 cho mỗi **3 cột** đủ điều kiện; tối đa **8** | Bay chậm sát đất (≤ 30 pt), **sáng–tắt** chu kỳ 2–4 giây, lệch nhau | Tới 4h thì tắt dần trong 10 giây |
| 🐦 **Đàn chim bay ngang** | Bình minh (5h–7h) hoặc chạng vạng (17h–19h); thế giới có ≥ 3 cây tán trưởng thành; không mùa Đông | Đàn 3–7 con; **1–2 đàn** mỗi lần bình minh / chạng vạng trên khung nhìn | Bay ngang trời phía sau cây, hình chữ V lỏng, vỗ cánh lệch nhịp | Bay hết khung nhìn trong 8–12 giây |
| 🐤 **Chim sẻ trên cây** | Cây tán trưởng thành đang có lá, 6h–18h | **30%** số cây trong vùng sinh có 1–2 con (Đông: 10%, 1 con) | Nhảy giữa cành mỗi 3–6 giây; thỉnh thoảng (mỗi 30–60 giây) bay sang cây khác trong 10 cột | Tối về thì bay đi |
| 🐟 **Cá nhảy** | Ao có cá (con cá thật), không đóng băng | Mỗi ao **1 lần mỗi 20–40 giây** | Một con cá thật vọt lên khỏi mặt nước rồi rơi lại; **vòng sóng** lan 1.5 giây | — |
| 🍄 **Nấm** | Cột vừa có thú chết (đói, bị săn, chết già); hoặc cột Rừng có mùn ≥ 40 vào mùa Thu sau mưa | Chỗ thú chết: **1–3 cây nấm**, mọc sau 20 giây; Rừng: tối đa 3 cụm trên khung nhìn | Mọc lên trong 3 giây | **3 phút thật**, rồi teo dần trong 10 giây |
| 🟤 **Ụ đất giun** | Cột có Giun | Trên khung nhìn: 1 ụ mới mỗi **30–60 giây**, chọn ngẫu nhiên một cột có giun | Đất đùn lên thành ụ nhỏ trong 1 giây | 20 giây rồi phẳng lại |
| 🌸 **Cánh hoa bay** | Táo dại đang ra hoa (Xuân) | Mỗi cây 1 cánh mỗi 4–8 giây | Lượn theo gió (§2.3) rồi tan dưới đất | Như lá rơi hiện tại (`FallingLeaf`) |

Ghi chú:
- ✅ **Cỡ côn trùng (sau thử tay 2026-10-27):** theo tỉ lệ thật (Cáo 14 px ≈ 105 cm, ~7.5 cm/px) côn trùng dưới 1 px, nên vẽ **nhỏ nhất còn thấy**: chuồn chuồn thân 3 × 1 px + cánh 1 px, bướm 2 × 2 px, ong 1 px vàng + 1 px cánh. Bản đầu (chuồn chuồn 5 px) to gần bằng thỏ.
- 🍄 Nấm là hình của chuỗi "cáo để lại xác, xác nuôi nấm, nấm làm đất màu mỡ" ở trụ cột 2. Luật mùn đã có sẵn; nấm làm nó nhìn thấy được.
- 🐟 Cá nhảy dùng một con cá thật trong ao, nên ao không có cá thì không có cá nhảy.
- Bướm, chuồn chuồn, chim sẻ **tránh con trỏ**: chuột tới gần trong 40 pt thì bay ra xa 1–2 giây. Đây là phản ứng duy nhất với con trỏ trong vòng này (✅ Q35).

### 2.2 Hành vi nhỏ của động vật (chỉ là hình)
Trong lúc **nghỉ** ([13 §3.1](13-bay-dan-va-sinh-san.md#31-đi-tới-đích-rồi-nghỉ)), con vật không đứng yên mà diễn một chuỗi **động tác**:

- Mỗi động tác dài 1–3 giây. Giữa hai động tác đứng yên **1.5–4 giây** (vẫn có hoạt ảnh thở: phập phồng 1 pt, chu kỳ 2 giây).
- Chọn động tác theo **trọng số** trong bảng, chỉ trong các động tác đang **hợp điều kiện**. Không chọn cùng một động tác hai lần liền.
- Động tác **không đổi vị trí** quá ±0.3 cột, để không lệch khỏi cột mô phỏng.
- Bắt đầu đi tới đích mới thì cắt ngang động tác đang diễn.

| Loài | Động tác (trọng số) | Điều kiện riêng |
|------|---------------------|-----------------|
| 🐇 **Thỏ** | Gặm cỏ: cúi đầu, nhai (40) · Vẫy tai (20) · **Đứng hai chân ngó quanh** (15) · Rửa mặt bằng hai chân trước (10) · Nhảy tại chỗ (10) · Nằm duỗi dài (5) | Gặm cỏ: cột có cỏ. Nằm duỗi: độ no ≥ 80. Có cáo đang thức trong **12 cột**: đứng hai chân thành trọng số **60** và quay mặt về phía cáo |
| 🐇 **Thỏ con** | Theo sát mẹ (luôn) · Nhảy vòng quanh mẹ (40) · **Vờn nhau** (30) · Gặm cỏ (30) | Vờn nhau: có thỏ con khác trong 1 cột; hai con đuổi nhau 2–3 giây |
| 🦊 **Cáo** | Ngồi liếm chân (25) · Ngáp (15) · Ngửi đất (25) · Vểnh tai về phía con mồi gần nhất (20) · Gãi tai (15) · **Vươn vai** (luôn diễn ngay sau khi thức dậy) | Vểnh tai: có thỏ / sóc trong 12 cột. Ngáp: gần giờ ngủ (±1 giờ trong ngày) thì trọng số ×3 |
| 🦊 **Cáo con** | Vờn nhau trước hang (40) · Nằm phơi bụng (20) · **Nhảy vồ bướm** (40) | Nhảy vồ bướm: có 🦋 trong 2 cột (không bao giờ trúng). Không ra xa hang quá 2 cột |
| 🐿️ **Sóc** | Ngồi gặm hạt (30) · Chạy lên thân cây rồi xuống (25) · Vẫy đuôi (25) · **Đào đất chôn hạt** (20) | Gặm hạt, chôn hạt: mùa Thu (trọng số ×2), đúng với luật chôn hạt ([12 §3.1](12-moi-truong-song.md#31-sóc-)) |
| 🪶 **Diệc** | Đứng một chân (30) · Rỉa lông (25) · Duỗi cổ (20) · Vỗ cánh (10) · Nhìn xuống nước, nghiêng đầu (15) | Đứng một chân giữ lâu 4–8 giây. Không có "mổ hụt": mổ chỉ dùng cho cảnh bắt cá thật ([14 §5](14-hang-tho-va-san-moi.md#5-hiển-thị)) |
| 🐟 **Cá** | Đớp mặt nước: vòng sóng nhỏ (25) · Quẫy đổi hướng (40) · **Cả bầy quay đầu cùng lúc** (35) | Quay đầu cùng lúc: cả bầy làm chung, mỗi bầy tối đa 1 lần mỗi 10 giây. Đêm: trọng số đớp mặt nước ×0.3 |
| 🐝 **Ong** | Bay từ hoa này sang hoa khác, đậu 1–2 giây, rơi phấn (§1.4) | Ngủ: đậu sát cỏ như 11 §1.5 |

- **Con đang ngủ:** mỗi **10–20 giây** trở mình hoặc giật tai một lần (0.5 giây). "z" như hiện tại.
- **Ăn quả** (§1.4): thỏ hoặc cáo đang đói đứng dưới cây có quả thì thay động tác bằng "với lên ăn" (2 giây), lặp tới khi no hoặc đi.

### 2.3 Gió lướt qua
- Mỗi **40–90 giây thật** có một **cơn gió** chạy dọc cả dải, theo một hướng ngẫu nhiên, tốc độ **8 cột/giây**.
- Cỏ, hoa, dương xỉ, lau sậy ngả theo gió (nghiêng tối đa 15°, lệch nhịp theo cột) rồi bật lại trong 1 giây, nên thấy một **làn sóng** chạy qua đồng cỏ. Tán cây lay nhẹ hơn (5°).
- Gió cuốn theo lá rơi, cánh hoa, và đẩy bướm, chuồn chuồn lệch đi một chút.
- Mùa Đông: gió mạnh hơn (×1.5), cuốn bông tuyết bay ngang.
- Khi đang mưa: không có cơn gió riêng (mưa đã có chuyển động).

### 2.4 Ngân sách hiệu năng
| Mục | Giới hạn |
|-----|----------|
| Sinh vật trang trí trên khung nhìn cùng lúc | **≤ 24** (đếm cả ụ đất, nấm). Thừa thì không sinh thêm, ưu tiên loại đang có ít nhất |
| Chấm hiệu ứng nhỏ (lá, phấn, sóng, hồi sức) cùng lúc | **≤ 40** |
| Đối tượng | Dùng pool như `AnimalView` / `ColumnView`; số GameObject không tăng theo kích thước thế giới (Tech Doc 05 M2) |
| CPU | Cả game vẫn trong ngân sách ≤ 2% (01). Đo lại bằng test hiệu năng sau khi thêm |
| Bộ đếm dev (`LITTLEGOD_DEV`) | Hiện số trang trí, số chấm, và **khoảng lặng hiện tại** (giây kể từ động tác / chuyển động gần nhất trên khung nhìn) để kiểm mục tiêu §0.3 |

### 2.5 Cài đặt
Thêm vào [10 §9](10-giao-dien.md#9-cài-đặt-tối-giản):

| Cài đặt | Mặc định | Ghi chú |
|---------|----------|---------|
| Hiệu ứng thiên nhiên: **Đầy đủ / Ít / Tắt** | Đầy đủ | *Ít*: trang trí và chấm hiệu ứng còn một nửa số giới hạn, không có cầu vồng, không có gió. *Tắt*: chỉ còn sinh vật mô phỏng và hành vi nhỏ. Dành cho máy yếu hoặc người thấy rối |

---

## 3. Khoảnh khắc M5 rút gọn

### 3.1 Vì sao phải đổi số của 09
GDD [09](09-khoanh-khac.md) viết cho nhịp cũ (app mở 8 giờ/ngày, kết game sau ~17 ngày lịch). Từ khi có nhịp ×100 ([11](11-nhip-va-tang-tan.md)) và môi trường sống ([12](12-moi-truong-song.md)), cả slice chỉ còn **~1.1–1.4 giờ thật**:

| | Số của 09 | Hệ quả ở nhịp ×100 |
|---|-----------|--------------------|
| Tần suất mục tiêu | ~1.5–2 khoảnh khắc **mỗi giờ** | Cả slice chỉ có **2–3** khoảnh khắc |
| Giãn cách nhóm A | ≥ 10 phút | Tối đa ~8 khoảnh khắc A cả slice |
| Thời gian sống | 30 phút | Dài bằng 1/3 cả slice; bong bóng cũ còn nằm khi thế giới đã đổi khác |
| Khách lạ | 1/480 mỗi phút mỗi đoạn, tối đa 1 mỗi 4 giờ | Gần như không bao giờ gặp |
| Hạt quà | 1 mỗi 3 giờ | Tối đa 0–1 lần |

Mô hình người chơi chăm của 11, 12 ghé mỗi **3 phút thật**. Bản rút gọn đặt nhịp theo đó.

### 3.2 Danh sách rút gọn
| # | Khoảnh khắc | Nhóm | Biểu tượng | Xuất hiện khi | Click thì |
|---|-------------|------|------------|---------------|-----------|
| 1 | **Loài mới** | A | ✨ (vàng) | Lần đầu một loài động vật xuất hiện trong thế giới ([12 §3](12-moi-truong-song.md#3-động-vật-tự-đến--q29--2-con-chờ-2-giờ-mô-phỏng)). 7 lần cả game | Quà vừa; loài vào Sổ tay |
| 2 | **Đến nơi mới** | A | ✨ (trắng) | Một cặp tự đến một đoạn biome (12 §3), trừ lần là Loài mới | Quà thường |
| 3 | **Con non** | A | 🐣 | Như [09 §3.2 mục 2](09-khoanh-khac.md#32-chi-tiết-từng-loại): thú săn, lần sinh đầu của loài trong đoạn, hoặc loài đang hồi phục (≤ 4 con); ong chia đàn | Quà thường |
| 4 | **Hạt lạ** (khám phá) | A | 🌱 | Ngưỡng như 09 / 12 §4 (code tạm thời đang tự khám phá khi đạt ngưỡng; nay đi qua bong bóng). Theo chung luật giới hạn §3.3 | Loài mới + một cây miễn phí (không đổi) |
| ~~5~~ | ~~**Khách lạ**~~ | | 🦋 | ✅ **Bỏ** 2026-10-28 (người chơi không cần) | |
| 6 | **Vùng đang khô** | B | ☁️ (✅ 2026-10-27: đám mây, không còn bong bóng 💧, §3.4b) | Như 09: độ ẩm trung bình vùng < 25 **và** ≥ 3 cây đã vàng (máu < 60) | Mây lan dài 10 ô, xám lại, mưa dưới cả bề ngang mây, vừa mưa vừa trôi tới hết bản đồ; giá một lần gọi mưa (30) |

**Hoãn sang bản đầy đủ:** 🌱 Hạt quà, 🍂 Ăn trụi (gợi ý nhóm C), 🏷️ Đặt tên vùng (vùng không còn hồi sinh, cần đặc tả lại), chế độ theo dõi. Đã bỏ từ 12: 💌 Lời mời, 🌿 Sẵn sàng hồi sinh.

### 3.3 Thời gian (phút thật)
| Thông số | 09 | **Rút gọn** |
|----------|----|-------------|
| Hiện dần | 1 giây | 1 giây |
| Thời gian sống | 30 phút | **8 phút** (💧: tới khi hết khô, tối đa 8 phút) |
| Mờ dần (100% → 40%) | 3 phút cuối | **2 phút cuối** |
| Rê chuột | Tạm dừng thời gian sống | Như 09 |
| Giãn cách 2 khoảnh khắc nhóm A **mới** trên toàn thế giới | ≥ 10 phút | **≥ 60 giây**. Tới sớm hơn thì **bỏ**; riêng ✨ Loài mới và 🌱 khám phá thì **xếp hàng** chờ lượt |
| 🌱 bị bỏ qua: hạt khác cùng loài tới sau | 2 giờ | **2 phút** (Tech Doc 09 §2) |
| 🐣 hồi lại mỗi đoạn biome | — | **5 phút** |
| ✨ Đến nơi mới hồi lại mỗi đoạn biome | — | **5 phút** |
| 💧 hồi lại mỗi vùng | 2 giờ | **30 phút** (✅ Q39; trước đề xuất 10 phút) |
| Tối đa trong khung nhìn · mỗi vùng | 3 · 1 | 3 · 1 (như 09) |
| Khi tắt app | Không tích luỹ | Như 09 |

**Thứ tự ưu tiên** (khi thừa chỗ trong khung nhìn): ✨ Loài mới → 🌱 khám phá → 💧 → 🐣 → ✨ Đến nơi mới.

### 3.4 Hiển thị và chỉ báo
- Bong bóng, hover, click giữ như [09 §5.1](09-khoanh-khac.md#51-hình-thức): sprite 12×12 ở tỉ lệ 2×, vùng click ≥ 20×20 pt, nổi nhẹ, không nhấp nháy. Âm thanh chỉ phát khi click.
- Click: tinh linh bay tới (0.3 giây) → lấp lánh → hiệu ứng riêng → vệt sáng bay về khay.
- **Giữ chỉ báo ngoài màn hình** (09 §7): nút ◀ / ▶ hiện biểu tượng khoảnh khắc ưu tiên cao nhất phía đó; bản đồ mini có chấm sáng. Khung nhìn chỉ thấy ~1/3 thế giới, nên thiếu phần này thì phần lớn khoảnh khắc sẽ trôi qua mà người chơi không biết.

### 3.4b Mây mưa thay bong bóng 💧 (✅ 2026-10-27)
Sau chơi thử: bong bóng 💧 lơ lửng giữa trời trông lạc lõng. Thay bằng **một đám mây**:

- **Lúc chờ:** một đám mây trắng nhỏ, **cao hơn ngọn cây** (dải trên cùng của trời), trôi **theo gió như mây nền** (sang phải) với tốc độ **gấp 25 lần mây nền** (✅ sau thử tay 2026-10-27, hai lần ×5: 1 cột/giây, tức 60 cột/phút thật). Mây chờ chỉ **sống 10 giây** (mờ dần 3 giây cuối), xuất phát phía trước vùng đang khô sao cho bay ngang qua giữa vùng đúng giây thứ 5; trôi ra khỏi bản đồ trước khi được click thì tan. Thỉnh thoảng (mỗi 1.5–3 giây) một giọt nước nhỏ xuống từ đáy mây để khác mây trời thường. Rê chuột: thẻ thông tin "Vùng đang khô · Gọi mưa · 30 Sinh khí"; ✅ **con trỏ chuột không bao giờ chặn hay làm dừng chuyển động** (mây vẫn trôi qua con trỏ). Bản trước Claude tự thêm luật "rê chuột thì mây dừng", không có trong yêu cầu, đã bỏ 2026-10-27.
- **Click:** trả giá một lần gọi mưa (30; thiếu thì mây ở lại, thẻ báo thiếu bao nhiêu). Mây **lan dài ra đủ 10 ô** trong 1 giây (các cụm mây tản ra hai bên), **hoá mây đen**, mưa rơi **trong suốt bề ngang mây**, vừa mưa vừa trôi tiếp. ✅ (2026-10-27, sau thử tay) Mây **mưa 15 giây** tính từ lúc click (gồm cả 1 giây lan ra), rồi **co rút lại** (các cụm dồn về giữa, ~1 giây), tắt mưa, mờ dần và biến mất; trong lúc co rút mây vẫn trôi nhưng không mưa thêm. Chạm mép bản đồ trước khi hết 15 giây thì co rút luôn tại đó. Mùa Đông là tuyết.
- **Mưa:** lúc mây vừa lan ra, cả 10 cột bên dưới được mưa ngay; khi trôi, mép trước của mây mưa xuống từng cột mới. Mỗi cột đất sống nhận lượng ẩm bằng **một lần mưa thường** (một lần mỗi cột). Ở tốc độ 1 cột/giây, một lần gọi mây mưa khoảng **25 cột** (10 + ~15). Cây dưới mây nhún, có vũng nước, chấm hồi sức như §1.1.
- ✅ **Tốc độ khi mưa (sau thử tay 2026-10-27):** mây **giữ đúng tốc độ lúc chờ** (gấp 25 lần mây nền), chỉ hoá thành **mây đen** rộng hơn và mưa. Lượng nước không đổi (mỗi cột một lần mưa). Tốc độ ở `balance.json → moments.rainCloud.columnsPerRealMinute`, thời gian sống ở `lifetimeSeconds`, thời gian mưa ở `rainSeconds`, bề ngang ở `width`.
- ⚠️ Mây chờ chỉ sống 10 giây mà vẫn hồi 30 phút mỗi vùng (Q39) khi tan, nên ở bản thường người chơi rất khó bắt gặp mây. Cần xem lại thời gian hồi khi thử bản thường.
- Không lưu: tắt app giữa chừng thì đám mây tan (phần đã mưa vẫn giữ).

### 3.5 Khách lạ
✅ **Bỏ hẳn** (2026-10-28, sau thử tay: người chơi không cần cơ chế này). Không còn Hươu sao, Rùa đầm, Cú mèo, bong bóng 🦋, quà lớn. Q37 (Cú mèo) và Q41 (khách ở vùng Khoẻ) không còn hiệu lực.

### 3.6 Quà
Sinh khí đang **dư** từ khi bỏ mời và hồi sinh ([12 §6](12-moi-truong-song.md#6-hệ-quả)), nên quà khoảnh khắc là để **có cảm giác được đáp lại**, không phải để đẩy tiến trình.

```
Quà thường = max(5,  Sinh khí/phút mp hiện tại × 33)    ← ✨ Đến nơi mới, 🐣   (≈ 20 giây thật thu nhập)
Quà vừa    = max(10, Sinh khí/phút mp hiện tại × 100)   ← ✨ Loài mới            (≈ 1 phút thật)
```

Số ở `balance.json → moments` (`giftMinutes` 33, `newSpeciesGiftMinutes` 100). Quà lớn của 🦋 đã bỏ cùng Khách lạ (2026-10-28).

### 3.7 Tần suất đo được (`sim/momentsim.py`)
✅ Đo 2026-10-27 bằng `momentsim.py survey 16` (16 seed, tối đa 4 giờ thật mỗi seed). Mô hình là `huntsim.py` (luật GDD 14, người chơi ghé mỗi 3 phút) cộng bộ đếm theo đúng điều kiện, hồi lại và giãn cách ở §3.2–3.5. Bộ đếm **không đổi luật**: khách lạ dùng chuỗi số ngẫu nhiên riêng, nên kết game giống hệt `huntsim.py` (14/16 seed, trung vị 1.1 giờ thật, 0.6–1.4; như [14 §6.1](14-hang-tho-va-san-moi.md#61-gia-đình-tối-đa-4-con-2026-10-26-huntsimpy-survey-16-có-ngủ-trong-hang)). Không mô hình giới hạn "3 trong khung nhìn, 1 mỗi vùng", vì đó là giới hạn hiển thị.

Các bảng dưới đây đo **trước Q39–Q41** (💧 hồi lại 10 phút, khách lạ ở vùng Cân bằng). Số **sau khi chốt** ở cuối mục.

**Số mỗi loại trong cả slice** (trung vị 16 seed, số trước khi kết game hoặc hết 4 giờ):

| Khoảnh khắc | Ước tính trước | **Đo được** | Ghi chú |
|-------------|----------------|-------------|---------|
| ✨ Loài mới | 7 | **7** | Thỏ 4–10 phút, Ong 5–11, Cá 8–12, Diệc 9–19, Cáo 7–30, Giun 16–75, Sóc 29–153 |
| ✨ Đến nơi mới | ~10–20 | **10** | Thêm ~20 lần bị bỏ vì giãn cách hoặc hồi lại |
| 🐣 Con non | ~10–20 | **18** | Thêm ~70 lần bị bỏ: lọc §3.3 đang làm đúng việc |
| 🌱 Khám phá | 6 | **7** | |
| 🦋 Khách lạ | ~3–5 | **1** (0–2; hai seed không kết có 5–6) | Ít hơn dự tính: vùng **Cân bằng** (Sức khoẻ ≥ 85) hiếm và thường chỉ có ở cuối slice |
| 💧 Vùng khô | ~4–8 | **21** (7–35) | Nhiều hơn dự tính nhiều. **68% rơi vào mùa Hạ** (Xuân 51 · Hạ 258 · Thu 65 · Đông 6, cộng mọi seed) |
| **Tổng** | ~40–60 | **62** (31–80 ở seed có kết) | **1 khoảnh khắc mỗi 1.1 phút thật** |

**So với tiêu chí:**

| Tiêu chí | Kết quả | |
|----------|---------|---|
| (1) Trung bình ≥ 1 khoảnh khắc mỗi 4 phút thật | Mỗi **1.1 phút** (1.0–1.5) | ✅ Dư gần 4 lần |
| (2) Sau 10 phút đầu, không khoảng trống > 10 phút | Trung vị **4.0 phút**; seed có kết: tối đa **7.0 phút** | ✅ Với seed có kết. Hai seed không kết có khoảng trống ~20 phút ở cuối, khi thế giới đã đứng yên vì thiếu Sóc / Diệc |
| (3) Click hết quà thì kết sớm hơn không quá 5% | **0%**: `survey 16 rewards` kết y hệt | ✅ Sinh khí dư hàng chục nghìn từ giữa slice (12 §6), quà không đẩy được gì |
| 10 phút đầu (Q38) | Khoảnh khắc đầu tiên ở **phút 1.2** (0.9–2.4); **6** khoảnh khắc trong 10 phút đầu; khoảng trống dài nhất **3.9 phút** (1.5–5.4) | ⚠️ Vượt ngưỡng 3 phút ở 9/16 seed. Khoảng trống nằm giữa các hạt 🌱 đầu tiên và lúc Thỏ đến (phút 4–10) |

**Thử các phương án giãn** (16 seed, trung vị):

| Phương án | Tổng | Mỗi | 🐣 | ✨ Đến | 💧 | Trống dài nhất sau 10 phút đầu |
|-----------|------|-----|----|-------|----|-----------------------------|
| Đề xuất ban đầu (giãn 60 giây, 💧 hồi 10 phút) | 62 | 1.1 phút | 18 | 10 | 21 | 4.0 phút |
| Giãn 90 giây | 54 | 1.3 phút | 12 | 7 | 21 | 3.7 phút |
| 💧 hồi 30 phút | 54 | 1.3 phút | 18 | 10 | 13 | 4.2 phút |
| Giãn 90 giây + 💧 hồi 30 phút | 47 | 1.5 phút | 12 | 7 | 13 | 4.2 phút |

**Nhận xét:**
- Khoảnh khắc **không thiếu**, mà còn dày. Nới giãn cách nhóm A chỉ bớt 🐣 và ✨ Đến; phần dày nhất là 💧, vốn thuộc nhóm B nên không chịu giãn cách.
- 💧 hiện ~20 lần trong ~70 phút, dồn vào mùa Hạ: dễ thành cảm giác **bị nhắc việc**, trái với "không làm phiền". Hồi lại 30 phút bớt được ~40%.
- 🦋 gần như không gặp. Muốn có 3–5 lần mỗi slice thì phải hạ điều kiện, ví dụ vùng **Khoẻ** (≥ 60) thay vì Cân bằng.
- 10 phút đầu đã có 6 khoảnh khắc, khoảng trống chỉ hơi vượt 3 phút. Phần §1–§2 (mầm nhú, cây lên bậc, bướm, hành vi nhỏ) lấp đúng khoảng này mà không đổi luật.

**Sau khi chốt Q39–Q42** (💧 hồi lại 30 phút, giãn cách 60 giây, khách lạ ở vùng Khoẻ; `momentsim.py survey 16`, kết game không đổi: 14/16 seed, trung vị 1.1 giờ thật):

| Khoảnh khắc | Trước | **Sau** |
|-------------|-------|---------|
| ✨ Loài mới · ✨ Đến nơi mới · 🐣 · 🌱 | 7 · 10 · 18 · 7 | 7 · 10 · 17 · 7 |
| 🦋 Khách lạ | 1 | **2** (1–4 ở seed có kết; 7–12 ở hai seed không kết) |
| 💧 Vùng khô | 21 | **13** (7–18 ở seed có kết) |
| **Tổng** | 62, mỗi 1.1 phút | **54, mỗi 1.2 phút** (31–68 ở seed có kết) |
| Trống dài nhất sau 10 phút đầu | 4.0 phút | **3.9 phút**; seed có kết tối đa 5.8 |
| 10 phút đầu | 6 khoảnh khắc, trống tới 3.9 phút | Không đổi (✅ Q42: lấp bằng §1–§2) |

- Cả ba tiêu chí vẫn đạt.
- 🦋 vẫn dưới mức mong muốn 3–5 lần, vì ngoài điều kiện Khoẻ còn bị giới hạn giờ (Hươu sao chỉ ban ngày, Cú mèo chỉ ban đêm) và giới hạn 1 lần mỗi 12 phút. 💡 Nếu chơi thử vẫn thấy hiếm: tăng xác suất từ 1/30 lên 1/15 mỗi phút, hoặc giảm giới hạn xuống 1 lần mỗi 8 phút.

**Sau khi bỏ Khách lạ (2026-10-28)**, `momentsim.py survey 16`: trung vị **54** khoảnh khắc mỗi slice (**1 mỗi 1.3 phút thật**): ✨ Loài mới 7 · ✨ Đến 9 · 🐣 17 · 🌱 7 · 💧 12; trống dài nhất sau 10 phút đầu trung vị 5.2 phút. Vẫn đạt tiêu chí ≥ 1 mỗi 4 phút. (Mô hình vẫn dùng mây 💧 kiểu cũ, sống 8 phút; mây 10 giây của §3.4b chưa mô hình hoá.)

Chạy lại:

```bash
python3 Docs/GDD/sim/momentsim.py survey 16
```

```bash
python3 Docs/GDD/sim/momentsim.py survey 16 gap=90 dry=10
```

---

## 4. Danh sách kiểm khi chơi thử
- [ ] Gọi mưa: thấy đất sẫm và cây nhún trong ≤ 1 giây; cây vàng có chấm hồi sức; thỉnh thoảng có cầu vồng.
- [ ] Gieo Sồi: thấy mầm ngay; ngồi làm việc rồi liếc lại sau ~3 phút thì cây đã lên một bậc rõ ràng.
- [ ] Liếc xuống bất kỳ lúc nào có con vật thức trên khung nhìn: trong 3 giây thấy ít nhất một con làm gì đó.
- [ ] Đồng cỏ có hoa nhìn rộn ràng hơn đồng cỏ trơ trụi; ao có lau, sen có chuồn chuồn; đêm Hạ có đom đóm.
- [ ] Không cảm thấy rối ở chế độ Đầy đủ; chế độ Ít vẫn thấy sống.
- [ ] Trong 30 phút chơi đầu, mỗi lần quay lại (3–10 phút) có ít nhất một bong bóng hoặc chỉ báo ◀ ▶.
- [ ] CPU vẫn trong ngân sách.

## 5. Câu hỏi cho người thiết kế
- ✅ **Q35.** Giữ cả 9 loại sinh vật trang trí của §2.1; bướm, chuồn chuồn, chim sẻ **né con trỏ**.
- ✅ **Q36.** Khoảnh khắc rút gọn: sống **8 phút**, giãn cách nhóm A **60 giây** (§3.3). Đo xong nếu thấy dày quá thì nới giãn cách lên 90 giây.
- ~~✅ **Q37.** Thêm khách lạ **Cú mèo** cho Rừng (§3.5).~~ Bỏ cùng Khách lạ (2026-10-28).
- ✅ **Q38.** Chưa đổi điều kiện loài đến; **đo trước rồi quyết** (§3.7).

Từ kết quả đo §3.7 (2026-10-27):
- ✅ **Q39.** 💧 hồi lại mỗi vùng **30 phút** (thay 10 phút): ~21 → ~13 lần mỗi slice.
- ✅ **Q40.** Giữ giãn cách nhóm A **60 giây**; xem lại sau chơi thử.
- ~~✅ **Q41.** Khách lạ xuất hiện ở vùng **Khoẻ** (Sức khoẻ ≥ 60).~~ Bỏ cùng Khách lạ (2026-10-28).
- ✅ **Q42.** Chưa đổi luật loài đến; khoảng trống 10 phút đầu lấp bằng phần hình §1–§2, xem lại sau chơi thử.
