# 17 · Rừng có Hươu và Sói

> Trạng thái: ✅ **Đã chốt** 2026-10-28 (Q50–Q57, [06](06-cau-hoi-mo.md)), đã kiểm chứng bằng `sim/forestsim.py` (§6). Số trong bảng §2–§3 là bản **đã chỉnh** sau khi đo (số tạm ban đầu không đạt).
> Thêm vào [12 §3](12-moi-truong-song.md#3-động-vật-tự-đến--q29--2-con-chờ-2-giờ-mô-phỏng). Hành vi bầy, hang, né, rượt theo [13](13-bay-dan-va-sinh-san.md) và [14](14-hang-tho-va-san-moi.md).

## 1. Vì sao
✅ Người chơi muốn **mỗi biome đều có một loài ăn cỏ và một loài ăn thịt của riêng nó** để môi trường tự cân bằng. Hiện nay:

| Biome | Ăn cỏ | Ăn thịt |
|-------|-------|---------|
| Đồng cỏ | 🐇 Thỏ | 🦊 Cáo |
| Ao | 🐟 Cá | 🪶 Diệc |
| Rừng | 🐿️ Sóc | — (Cáo của Đồng cỏ ghé sang bắt sóc) |

✅ Chọn (2026-10-28): thêm **🦌 Hươu** (ăn Dương xỉ) và **🐺 Sói** (săn Hươu). Sóc vẫn là mồi phụ của Cáo như nay.

## 2. 🦌 Hươu
| | 💡 Đề xuất (số tạm) | Giống |
|-|---------------------|-------|
| Biome | Rừng | Sóc |
| Thức ăn | Gặm **Dương xỉ** sống, như thỏ gặm cỏ | Thỏ |
| Tự đến khi | Đoạn Rừng có **≥ 8 Dương xỉ** sống (tạm: 12) và **≥ 2 cây tán** (chỗ trú); không mùa Đông | Thỏ (≥ 12 cỏ, ≥ 1 chỗ trú) |
| Sống theo | **Đàn tối đa 4 con**, đi cùng nhau; không có hang | Bầy thỏ, cá (13) |
| Sinh sản | Trưởng thành 3 giờ mp, **1 con mỗi lứa**, nghỉ giữa lứa 8 giờ mp, sống 4 ngày mp | Chậm hơn thỏ: thú lớn |
| Ăn | **0.5** sinh khối Dương xỉ mỗi phút mp (tạm: 1) | Thỏ 1.5 |
| Né Sói | Thấy Sói đói trong 5 cột thì **chạy ra xa** (không có hang để trốn) | Cá chạy sang đầu ao bên kia (14) |
| Ngủ | Ban đêm nằm nghỉ tại chỗ (chỉ là hình) | — |

**💡 Hệ quả cần đổi:** Dương xỉ hiện **không mọc lại** khi bị gặm (`regrow` = 0). Có Hươu thì Dương xỉ phải mọc lại như Cỏ (đề xuất `regrow` 0.4, Cỏ 0.6), nếu không Hươu ăn trụi Rừng và Rừng biến thành đất trống. Xem Q51.

## 3. 🐺 Sói
| | 💡 Đề xuất (số tạm) | Giống |
|-|---------------------|-------|
| Biome | Rừng | — |
| Mồi | **Hươu**; ✅ Q52: không có Hươu trong tầm tìm mồi thì bắt **Sóc** | Cáo bắt Thỏ, Sóc |
| Tự đến khi | Đoạn Rừng + đoạn kề có **≥ 6 Hươu** và **≥ 3 cây tán** (hang); không mùa Đông | Cáo (≥ 8 mồi, ≥ 3 chỗ làm hang) |
| Sống theo | **Theo cặp**, chung một hang, giữ lãnh thổ | Cáo (13) |
| Ăn | No **24 giờ mp** sau mỗi con Hươu; sức chứa **5 Hươu mỗi Sói** | Cáo 15 giờ, 8 mồi |
| Sinh sản | Trưởng thành 6 giờ mp, lứa 2, nghỉ giữa lứa 3 000 phút mp, sống 4 ngày mp | Cáo |
| Săn | Rình, rượt rồi vồ như Cáo; vồ trúng **40%** (tạm: 60%, Cáo 90%): Hươu chạy nhanh | Cáo (14) |
| Thức | 15h–9h | Cáo |

## 4. Không đổi
- Cáo vẫn sống ở Đồng cỏ và Rừng, bắt Thỏ và Sóc. Sói **không** bắt Thỏ; chỉ bắt Sóc khi không có Hươu (Q52). Cáo **không** bắt Hươu.
- Luật biome (12 §2), luật tự đến chung (12 §3: vắng < 2 con, đủ điều kiện liên tục 2 giờ mp thì một cặp vào từ mép đoạn), luật chết đói.
- Lần đầu Hươu, Sói xuất hiện là khoảnh khắc ✨ Loài mới (15 §3.2).
- 💡 **Kết game** (12 §5: "mọi loài đã từng xuất hiện") sẽ đòi thêm Hươu và Sói. Xem Q53.

## 5. Quyết định (2026-10-28)
- ✅ **Q50.** Dùng số **đã chỉnh** ở §2–§3.
- ✅ **Q51.** Dương xỉ **mọc lại** khi bị gặm (`regrow` 0.4).
- ✅ **Q52.** Sói bắt **Sóc** khi không có Hươu trong tầm tìm mồi. Hươu vẫn là mồi chính.
- ✅ **Q53.** Kết game chờ cả Hươu và Sói xuất hiện.
- ✅ **Q54.** Giữ **khoảng 1 cặp** thú săn mỗi khu: thú săn chỉ coi là **vắng** khi cả vùng lang thang của nó (đoạn + đoạn kề, nới thêm lãnh thổ: Cáo 10, Sói 12 cột) không có con nào cùng loài. Áp cho Sói, Cáo (đổi luật 12 §3; Diệc: Q56).
- ✅ **Q56.** Diệc **giữ luật tự đến cũ** (vắng khi đoạn + đoạn kề < 2 con). Luật Q54 chỉ áp cho Sói, Cáo.
- ✅ **Q57.** Sói, Cáo còn **một mình** (không có con trưởng thành cùng loài trong vùng lang thang) **1 ngày mp** thì coi như **vắng**: một cặp mới được tới, có thể nhận chung hang với con lẻ (§6.2).
- ✅ **Q55.** Con vật **lạc đàn** đi tới nhập đàn cùng loài gần nhất còn chỗ (Hươu, Thỏ, Cá; cá chỉ trong ao của nó). Thỏ nhập đàn thì về chung hang của gia đình đó (đổi luật 13, 14).

## 6. Kiểm chứng (`sim/forestsim.py`, 8 seed, 2026-10-28)
Chạy lại: `python3 Docs/GDD/sim/forestsim.py survey 8 tuned` (thêm `long` để chạy 4 giờ thật; bỏ `tuned` để xem số tạm). Gốc so sánh là `huntsim.py survey 8`. "Nửa sau" là nửa sau mỗi lần chạy.

| | Số tạm ban đầu | **Đã chỉnh** (bảng §2–§3) | Gốc (không Hươu, Sói) |
|-|----------------|---------------------------|------------------------|
| Hươu có mặt (nửa sau) | 78%; 3 seed dưới 50% | **100%**, trung bình 8 con | — |
| Sói có mặt (nửa sau) | 45%; 3 seed 0%, 1 seed không bao giờ tới | **88%**, trung bình 5 con | — |
| Kết game | 7/8, trung vị 1.3 giờ thật | **8/8, trung vị 1.1 giờ** (0.6–1.3) | 8/8, 1.2 giờ (0.6–2.1) |
| Cột Rừng / Dương xỉ sống | 26 / 17 | 26 / 17 | 25 / 17 |
| Thỏ · Cáo · Sóc · Cá · Diệc (cả lần chạy) | | 26.5 · 5.4 · 0.7 · 21.1 · 4.7 | 26.9 · 5.6 · 1.2 · 20.1 · 4.9 |

- **Đến lần đầu:** Hươu 0.2–0.5 giờ thật, Sói 0.3–0.8 giờ thật.
- **Rừng không bị ăn trụi:** số cột Rừng và Dương xỉ như gốc. Dương xỉ vẫn tụt mạnh mỗi mùa Hạ (còn 6–8 cây), nhưng gốc cũng vậy: do khô hạn, không phải do Hươu.
- **Dương xỉ không mọc lại** (`regrow` 0): Hươu không sinh sản được (sức chứa đàn tính theo độ mọc lại), Sói không bao giờ tới, **0/8 kết game**. Q51 là bắt buộc.
- **Kết game có đòi Hươu và Sói hay không:** như nhau (8/8, 1.1 giờ).

**Vấn đề còn lại (cần quyết, xem Q54–Q55):**
- **Nhiều Sói hơn đề xuất:** khoảng 5 con mỗi khu Rừng (vài cặp), không phải 1 cặp. Sói đi lang thang ra ngoài đoạn Rừng + đoạn kề thì luật tự đến coi là "vắng", nên cặp mới lại vào.
- **Rừng nhỏ và bị chia mảnh:** người chơi mô hình chỉ có 16–38 cột Rừng, đôi khi tách thành hai mảnh 13 và 9 cột. Mảnh nhỏ không đủ Dương xỉ để Hươu quay lại. Người chơi thật trồng nhiều Dương xỉ hơn thì đỡ hơn.
- **Hươu lạc đàn:** một con còn lại một mình không nhập đàn khác nên không sinh được (giới hạn có sẵn của luật bầy 13).
- Mô hình chưa có giấc ngủ của Sói (như Cáo trong `huntsim.py`) và chưa tính Sói vào luật cân bằng thú săn / mồi của Sinh khí.

### 6.1 Đo lại với Q52, Q54, Q55 (8 seed)
Chạy lại: `python3 Docs/GDD/sim/forestsim.py survey 8 tuned` (cả ba luật), thêm `skipheron` để Diệc giữ luật tự đến cũ; thêm `long` để chạy 4 giờ thật.

| | Trước Q52–Q55 | Cả ba luật | Cả ba luật, **Diệc giữ luật cũ** | Gốc |
|-|---------------|-----------|----------------------------------|-----|
| Hươu: trung bình / có mặt | 8.0 / 100% | 8.1 / 100% | 8.6 / 100% | — |
| Sói: trung bình / có mặt | 5.0 / 88% | 3.4 / 98% | 3.2 / 98% | — |
| Sói mỗi đoạn Rừng | 2.8 | 1.8 | 1.9 | — |
| Thỏ · Cáo · Sóc · Cá · Diệc | 26.5 · 5.4 · 0.7 · 21.1 · 4.7 | 31.0 · 4.7 · 0.7 · 21.2 · **1.8** | 30.9 · 5.0 · 0.6 · 21.2 · 4.8 | 26.9 · 5.6 · 1.2 · 20.1 · 4.9 |
| Kết game | 8/8, 1.1 giờ | 8/8, 1.3 giờ | 8/8, 1.2 giờ (0.7–1.3) | 8/8, 1.2 giờ |

- **Q54 đạt cho Sói:** khoảng 2 Sói mỗi khu Rừng (một cặp), có mặt 98%.
- **Q54 làm Diệc gần tuyệt (4.7 → 1.8):** diệc sống một mình, một con còn sót ở ao chặn diệc mới tới mãi mãi nhưng không có bạn để sinh sản. Xem Q56.
- **Cùng vấn đề với Sói khi chạy dài (4 giờ thật):** một con Sói sống sót chặn Sói mới, Sói có mặt còn 68% (Diệc giữ luật cũ: 87%). Xem Q57.
- **Q52 gần như không xảy ra** (0–0.13 Sóc bị Sói bắt mỗi ngày mp): trong 15 cột quanh Sói hầu như luôn có Hươu. Không hại gì.
- **Q55:** con lẻ nhập đàn ~11 lần mỗi ngày mp; Thỏ tăng ~15% (26.5 → 31), không phải vấn đề.

### 6.2 Đo lần cuối với Q56, Q57 (8 seed)
Chạy lại: `python3 Docs/GDD/sim/forestsim.py survey 8 tuned` (thêm `long` để chạy 4 giờ thật). Đây là bộ luật đã chốt.

| | Dừng ở kết game | Chạy dài 4 giờ thật |
|-|-----------------|---------------------|
| Hươu: trung bình / có mặt | 8.6 / 100% | 10.3 / 99% |
| Sói: trung bình / có mặt | 3.3 / 98% | 4.1 / 91% |
| Sói mỗi đoạn Rừng | 2.0 (một cặp) | 2.3 |
| Thỏ · Cáo · Sóc · Cá · Diệc | 30.7 · 5.0 · 0.6 · 21.2 · 4.8 | 32.8 · 7.7 · 8.4 · 18.4 · 4.7 |
| Gốc `huntsim.py` | 26.9 · 5.6 · 1.2 · 20.1 · 4.9 | 27.8 · 9.4 · 7.5 · 18.2 · 4.6 |
| Kết game | 8/8, trung vị 1.2 giờ thật (0.7–1.3), như gốc | |

- **Q57 hiếm khi xảy ra** (0.05–0.07 lần mỗi ngày mp): con lẻ thường chết già hoặc chết đói trước. Thử chờ 720 và 2 880 phút mp cũng như nhau trong độ lệch giữa các seed; giữ 1 440.
- **Cáo ít hơn gốc khoảng 2 con** khi chạy dài: đó là tác dụng mong muốn của Q54 (một cặp mỗi khu), không phải lỗi.
