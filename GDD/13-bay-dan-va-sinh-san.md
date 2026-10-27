# 13 · Bầy đàn, lãnh thổ & nhịp sinh sản

> Trạng thái: ✅ **Đã chốt** 2026-10-24 (Q32–Q33, [06](06-cau-hoi-mo.md)). 💡 Đã kiểm chứng bằng `sim/socialsim.py` (§6). Kỹ thuật: [Tech Doc 07](../Tech%20Doc/07-bay-dan.md).
> ↻ 2026-10-25: thỏ sống theo **gia đình có hang**, con mồi né thú săn, thú săn rượt và vồ: đề xuất ở [14](14-hang-tho-va-san-moi.md).
> Phần này **thay** cách đi của động vật ở 07 §6.1 ("no thì đi lang thang") và bổ sung luật sinh sản ở 07 §6.2. Luật ăn, đói, săn, sức chứa giữ nguyên trừ chỗ ghi ở §4.

## 1. Vấn đề
Đo bằng mô hình hiện tại (`socialsim.py survey 16 old`, giống `biomesim.py`):

- **Đi lung tung.** Mỗi phút mô phỏng, mỗi con bước ngẫu nhiên sang trái, phải hoặc đứng yên. Ở nhịp ×100 (11 §1) đó là ~1.7 lần mỗi giây thật, nên một con **quay đầu ~33 lần mỗi phút thật**. Không loài nào đi theo bầy hay giữ chỗ của mình.
- **Sinh và chết quá nhanh.** Cả dải có ~30 thỏ nhưng **~230 con chết mỗi ngày mô phỏng** (14 phút thật), tức cứ ~4 giây thật lại có một con chết và một con ra đời. Phần lớn là bị săn: mỗi cáo bắt ~13 thỏ mỗi ngày mô phỏng, mỗi diệc bắt ~10 cá. Thỏ đẻ 2 con mỗi 1.5 giờ mô phỏng (54 giây thật).

## 2. Ý tưởng
Mỗi loài sống theo **một trong hai kiểu**, giống ngoài tự nhiên:

| Kiểu | Loài | Ngoài tự nhiên | Trong game |
|------|------|----------------|------------|
| **Bầy** | Thỏ, Cá | Thỏ sống thành đàn quanh hang chung; cá bơi theo đàn | Cả bầy gặm cỏ quanh một **chỗ của bầy**, ăn hết thì cả bầy dời đi. Bầy đông thì tách ra |
| **Đơn độc, có lãnh thổ** | Cáo, Diệc, Sóc | Cáo sống theo cặp trong lãnh thổ riêng; diệc đứng câu một mình; sóc giữ cây của nó | Mỗi con (cáo: mỗi cặp) giữ một **hang** và tuần tra quanh đó, tránh con cùng loài khác |
| (giữ nguyên) | Ong, Giun | Đàn ong ở tổ; giun ở đất | Như 07, 08 §7.2 |

Con vật **đi tới một chỗ rồi dừng lại** một lúc (gặm cỏ, nằm, đứng câu), rồi mới đi tiếp. Không còn bước ngẫu nhiên mỗi phút.

## 3. Cách đi

### 3.1 Đi tới đích, rồi nghỉ
- Mỗi con có một **trung tâm** (chỗ của bầy, hoặc hang) và **bán kính** đi lại quanh đó.
- Con vật chọn một **đích** ngẫu nhiên trong bán kính, đi thẳng tới đó, rồi **nghỉ** một lúc ngẫu nhiên, rồi chọn đích mới.
- Bị tụt ra ngoài bán kính (bầy vừa dời đi, lạc khỏi lãnh thổ) thì **đi về ngay, không nghỉ**.

| Loài | Kiểu | Bán kính | Tốc độ (cột / phút mp) | Nghỉ (phút mp) | ≈ thời gian thật |
|------|------|----------|------------------------|----------------|------------------|
| Thỏ | Bầy | ± 2 cột quanh chỗ của bầy | 1 | 10–40 | nghỉ 6–24 giây |
| Cá | Bầy | ± 1 cột | 1 | 5–20 | nghỉ 3–12 giây |
| Cáo | Đơn độc (cặp) | ± 10 cột quanh hang | 2 | 20–60 | nghỉ 12–36 giây |
| Diệc | Đơn độc | ± 15 cột quanh chỗ đứng | 2 | 30–90 | đứng câu 18–54 giây |
| Sóc | Đơn độc | ± 4 cột quanh cây Sồi của nó | 1 | 10–30 | nghỉ 6–18 giây |

- **Diệc đói** vẫn bay thẳng tới cá gần nhất như 08 §6 (không nghỉ).
- **Cáo, diệc, sóc tránh nhau:** khi chọn đích, tránh chỗ cách con cùng loài khác (không phải bạn đời) dưới 4 cột (sóc: 2).

### 3.2 Bầy (Thỏ, Cá)
- **Chỗ của bầy:** một cột. Thành viên đi lại trong ± bán kính quanh đó.
- **Bầy dời đi khi đói:** khi **ít nhất một nửa** bầy đói (độ no < 60) và cả bầy đang ở gần nhau, chỗ của bầy nhích **1 cột mỗi 3 phút mp** (cá: 5) về phía bãi cỏ (cá: bèo) nhiều nhất trong 12 cột. Bãi đã có bầy khác thì coi như ít cỏ hơn (× 0.3), nên các bầy tự giãn ra.
- **Con non theo bầy mẹ.** Con vật mới đến (một cặp tự tìm đến, 12 §3) lập bầy mới, hoặc nhập bầy cùng loài gần đó nếu bầy chưa đầy.
- **Tách bầy:** bầy có **8 con**, hoặc có **≥ 5 con** mà bãi cỏ quanh bầy đã hết chỗ (§4.2), thì **một nửa số con trưởng thành trẻ nhất** tách ra làm bầy mới, đi tới bãi cỏ tốt nhất cách mọi bầy khác **≥ 8 cột**. Không còn chỗ như vậy thì bầy giữ nguyên.
- Cá: mỗi ao thường chỉ có một bầy (ao rộng 4 cột, không đủ chỗ cho bầy thứ hai cách 8 cột), nên **mỗi ao tối đa 8 cá**.

### 3.3 Đơn độc (Cáo, Diệc, Sóc)
- **Hang:** mỗi con trưởng thành tìm một hang. Hang mới phải cách mọi hang cùng loài **≥ 16 cột** (diệc: 20, sóc: 4), tìm trong 40 cột quanh nó (sóc: 20).
  - **Thú săn làm hang nơi có nhiều mồi nhất** trong lãnh thổ (gần hơn thì hơn khi bằng nhau). Không chỗ nào có mồi thì chưa làm hang.
  - **Sóc làm tổ trên một cây Sồi trưởng thành.**
- **Cáo sống theo cặp:** cáo trưởng thành chưa có hang thì ưu tiên **về ở chung** với một hang đang có một con. Hang đủ 2 con là một cặp. Diệc và sóc không sống theo cặp.
- **Con non ở hang mẹ** cho tới khi trưởng thành, rồi đi tìm hang riêng (hoặc bạn đời).
- **Không tìm được hang** (mọi chỗ đã có chủ) thì đi lang thang và **không sinh sản**. Đây là cách lãnh thổ tự giới hạn số thú săn: dải 144 cột chỉ có chỗ cho khoảng 6–8 hang cáo.

## 4. Sinh sản

### 4.1 Ai được sinh
| Kiểu | Điều kiện (thêm vào 07 §6.2) |
|------|-------------------------------|
| Bầy | Có ít nhất một con trưởng thành khác **trong bầy**, và bầy **chưa đủ 8 con** |
| Đơn độc, cặp (Cáo) | Đang **có hang** và hang **có đủ cặp**. Mỗi cặp chỉ con lớn tuổi hơn sinh, nên **một lứa mỗi cặp** |
| Đơn độc (Diệc, Sóc) | Đang **có hang**, và có con cùng loài trong vùng sống như cũ |

Các điều kiện cũ vẫn giữ: đủ tuổi, hết thời gian nghỉ, có chỗ trống (sức chứa), tung xác suất `0.5 × hệ số mùa × chỗ trống` mỗi phút.

### 4.2 Sức chứa của bầy
Với bầy, **chỗ trống** tính cho **cả bầy**: `1 − số con trong bầy / sức chứa của bãi`, trong đó bãi = chỗ của bầy ± (bán kính + tầm ăn), sức chứa tính như 07 §6.2 (tốc độ cỏ mọc lại thực tế × 1.0 ÷ nhu cầu). Lý do: thỏ đứng sát nhau nên nếu mỗi con chỉ đếm quanh mình, bầy không bao giờ lớn quá 3–4 con và không tách được.

### 4.3 Nhịp sinh sản chậm lại
| Thông số | Cũ | Mới | Ghi chú |
|----------|----|-----|---------|
| Hệ số mùa (Xuân · Hạ · Thu · Đông) | 1.5 · 1.0 · 0.7 · 0.2 | **1.2 · 0.8 · 0.4 · 0** | Mùa Đông không sinh, như ngoài tự nhiên |
| Độ no tối thiểu để sinh | > 70 | **> 75** | Đói một chút là ngừng sinh (gợi ý cũ ở 08 Q17) |
| Thỏ: nghỉ giữa 2 lứa | 1.5 giờ mp | **4 giờ mp** (2.4 phút thật) | Lứa 2 con như cũ |
| Cá: nghỉ giữa 2 lứa | 3 giờ mp | **6 giờ mp** | Lứa 3 như cũ |
| Cáo: lứa · nghỉ | 1 con · 12 giờ mp | **2 con · 50 giờ mp** (1 mùa) | Mỗi cặp một lứa mỗi mùa |
| Diệc: nghỉ | 15 giờ mp | **50 giờ mp** | |
| Sóc: nghỉ | 6 giờ mp | **12 giờ mp** | |

### 4.4 Thú săn no lâu hơn
- **Cáo: 1 con mồi / 10 giờ mp** (cũ: 4 giờ), **Diệc: 1 cá / 10 giờ mp** (cũ: 5 giờ). Luật săn khác (độ hiếm, cặp cuối, nơi trú ẩn) giữ nguyên.
- Lý do: với luật cũ một cáo bắt ~13 thỏ mỗi ngày mô phỏng, nên thỏ phải đẻ liên tục để bù. Đây là nguồn chính của cảnh "sinh rồi chết" liên tục.

### 4.5 Kéo theo: rừng tự nuôi đất
- **Dương xỉ để lại 15 mùn khi chết** (cũ: 6).
- Lý do: trước đây đất rừng được bón chủ yếu nhờ **xác thỏ đi lạc vào rừng** rồi chết ở đó. Khi thỏ ở yên trong bầy trên đồng cỏ, đất rừng nghèo đi (đất màu 10–16 thay vì 12–28), Sồi ít, Sóc đến muộn và ~1/3 số seed không kết được game. Cho rừng tự bón bằng lá dương xỉ thì hết.

## 5. Vai trò theo vùng sống
- 💡 Khi tính **vai trò** của một đoạn biome (08 §5, Sức khoẻ, Đa dạng), con vật góp vai trò cho **mọi đoạn mà vùng sống của nó chạm tới** (lãnh thổ quanh hang, bãi của bầy), không chỉ đoạn nó đang đứng.
- Số con (để tính tỉ trọng, tỉ lệ mồi : săn) vẫn đếm theo chỗ đứng.
- Lý do: cáo có hang ở mép đồng cỏ vẫn đi săn sang rừng bên cạnh. Trước đây rừng "có" thú săn chỉ vì cáo đi lang thang ngang qua.

## 6. Kiểm chứng (`socialsim.py survey 16`, 16 seed, mỗi seed tối đa 4 giờ thật)
Cả hai cột đều dùng Dương xỉ 15 mùn (§4.5).

| Chỉ số (trung bình mỗi seed) | Luật cũ (`old`) | **Luật mới** |
|------------------------------|-----------------|--------------|
| Quay đầu / con / phút thật | 32.8 | **2.2** |
| Bước đi / con / phút thật | 62 | **6** |
| Chết đói / ngày mp | 29.5 | 38.9 |
| Bị săn / ngày mp | 203.6 | **66.9** |
| Tổng số con chết / ngày mp (≈ sinh) | ~233 (1 con / 4 giây thật) | **~106 (1 con / 8 giây thật)** |
| Thỏ · Cáo · Cá · Diệc · Sóc | 33 · 6.9 · 22 · 11.5 · 1.1 | 26 · 6.4 · 21 · 6.6 · 1.0 |
| Bầy thỏ · cỡ bầy | — | ~6 bầy · 3–6 con |
| Hang cáo | — | 1.6–4.6 |
| Kết game | 16/16 seed, trung vị 1.2 giờ thật (0.5–1.5) | **16/16 seed, trung vị 1.3 giờ thật (0.6–3.2)** |

- Cả dải 144 cột, nên trên màn hình (~47 cột, khoảng 1/3 dải) chỉ thấy một con chết **mỗi ~25 giây thật** thay vì ~12 giây.
- Thỏ chết đói nhiều hơn một chút (bầy đứng sát nhau ăn trụi bãi nhanh hơn rồi mới dời đi). Đây vẫn là chu kỳ "đông quá thì ăn trụi" của 08 §7.3.
- Nhịp kết game gần như không đổi; một seed chậm hơn (3.2 giờ) vì Sóc đến muộn.

Chạy lại:

```bash
python3 Docs/GDD/sim/socialsim.py survey 16
```

```bash
python3 Docs/GDD/sim/socialsim.py survey 16 old
```

## 7. Hiển thị (gợi ý cho Tech Doc)
- Thành viên một bầy đứng **lệch nhau trong cột** (vài pt) để không chồng lên nhau, và nghỉ thì có hoạt ảnh gặm cỏ / nằm.
- Con vật đi bằng tốc độ đi bộ đều tới đích, không trượt theo từng bước mô phỏng.
- Cáo đứng gần hang nhiều hơn; hang có thể là một ụ đất nhỏ (để sau).

## 8. Câu hỏi cho người thiết kế
- ✅ **Q32.** Nhịp ~106 con chết mỗi ngày mô phỏng (mỗi ~25 giây thật trên màn hình): **tạm giữ như vậy**, xem lại sau khi chơi thử. Nếu cần chậm hơn: kéo dài tuổi thọ và giãn thời gian nghỉ giữa 2 lứa.
- ✅ **Q33.** Cáo sống theo **cặp chung hang**.
