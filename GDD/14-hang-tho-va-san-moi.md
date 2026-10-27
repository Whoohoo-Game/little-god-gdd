# 14 · Hang thỏ, né thú săn & rượt bắt

> Trạng thái: ✅ **Đã chốt** 2026-10-25 (Q34, [06](06-cau-hoi-mo.md)). 💡 Đã kiểm chứng bằng `sim/huntsim.py` (§6). Kỹ thuật: [Tech Doc 08](../Tech%20Doc/08-hang-va-san-moi.md).
> Phần này **bổ sung** [13](13-bay-dan-va-sinh-san.md): bầy thỏ thành **gia đình có hang**; con mồi biết tránh và chạy trốn; thú săn **rượt và vồ** thay cho bắt theo xác suất mỗi phút (07 §6.4). Luật ăn, sinh sản, sức chứa của 13 giữ nguyên.

## 1. Ý tưởng
- **Mỗi hang là một gia đình thỏ.** Thỏ đào hang, cả nhà gặm cỏ quanh hang. Con lớn tách ra thì đi đào hang mới.
- **Con mồi sợ thú săn.** Lúc bình thường chúng tránh chỗ có cáo. Thấy cáo đang đói lại gần thì chạy về hang trốn.
- **Thú săn đi săn thì chạy nhanh.** Cáo đói chọn một con, chạy nhanh tới và vồ. Vồ trượt thì mệt, phải nghỉ một lúc rồi mới săn tiếp.

Người chơi sẽ thấy cảnh nhân quả rõ ràng: cáo xuất hiện thì cả nhà thỏ chạy về hang, con nào ở xa hang thì dễ bị bắt.

## 2. Hang thỏ

### 2.1 Gia đình và hang
- Bầy thỏ của 13 §3.2 giờ là **một gia đình**, và **chỗ của bầy là cái hang**. Hang là một cột cố định, **đào sâu xuống đất**: miệng hang ở mặt đất, đường hầm dốc xuống một buồng ngủ (vẽ dạng mặt cắt, §5).
- Thỏ đi lại trong **± 4 cột quanh hang** (13: ± 2 quanh chỗ của bầy). **Đói thì đi xa tới ± 8 cột** để kiếm cỏ.
- ↻ **Mỗi hang tối đa 4 con** (2026-10-26; trước: 8 như bầy ở 13). Con non sinh ra thuộc gia đình của mẹ. Hang còn bao nhiêu chỗ thì lứa chỉ có chừng ấy con (đang 3 con mà đẻ lứa 2 thì chỉ được 1).
- **Tách nhà:** gia đình đủ 4 con thì một nửa số con trưởng thành trẻ nhất (2 con) đi **đào hang mới** ở bãi cỏ tốt nhất, cách mọi hang khác **≥ 6 cột** (trước: 8). Không còn chỗ thì cả nhà ở lại và không đẻ thêm.

### 2.2 Dời hang
- Cả nhà không còn dời chỗ từng cột như bầy ở 13. Thay vào đó, khi **một nửa gia đình đói liên tục 60 phút mô phỏng** (~36 giây thật), cả nhà **bỏ hang, đi đào hang mới** ở bãi cỏ tốt nhất trong 12 cột (phải cách hang cũ ≥ 3 cột).
- **Hang bỏ trống** vẫn còn **3 ngày mô phỏng** (~43 phút thật) rồi sập. Gia đình nào đào hang trong vòng 3 cột của một hang bỏ trống thì **dùng lại** hang đó.
- Cả nhà chết hết thì hang cũng thành hang bỏ trống.

## 3. Con mồi tránh thú săn

| Loài | Lúc bình thường | Thấy thú săn đang đói trong … | Chạy về | Trốn |
|------|-----------------|------------------------------|---------|------|
| Thỏ | Không chọn chỗ đi cách cáo < 4 cột | 4 cột | **Hang** của gia đình, 2 cột / phút | Trong hang, tới khi hết cáo đói trong 4 cột thêm 10 phút |
| Sóc | Không chọn chỗ đi cách cáo < 3 cột | 5 cột | **Cây** của nó, 2 cột / phút | Trên cây, như thỏ |
| Cá | (ao hẹp, không tránh được) | 4 cột | **Đầu ao xa diệc nhất**, 1 cột / phút | Không trốn được |

- "Thú săn đang đói" = độ no < 60. Cáo no đi ngang thì thỏ chỉ tránh xa, không chạy trốn.
- **Trốn trong hang thì không ăn.** Đây là cái giá của sợ hãi: vùng nhiều cáo thì thỏ gầy hơn.
- Thỏ chưa có hang (vừa tới, chưa có gia đình) hoặc sóc chưa có cây thì chạy ra xa thú săn.

## 3b. Ngủ trong hang (✅ 2026-10-25)
Ngoài giờ thức của loài (GDD 11 §1.5; mỗi con lệch tới 0.7 giờ trong ngày):
- **Thỏ đi bộ về hang và ngủ trong hang**; **sóc về cây** của nó. Đang ngủ thì như đang trốn: **không ăn, thú săn không vồ được**.
- Ngủ thì nằm yên nên **đói chậm hơn: × 0.3** (cỏ không ăn được nhưng cũng ít tốn sức).
- Bị đe doạ lúc đang đi về thì chạy như §3. Sáng ra, thức dậy thì ra khỏi hang như hết trốn (sau 10 phút).
- Thỏ chưa có hang (vừa tới) hoặc sóc chưa có cây thì ngủ tại chỗ, vẫn bị vồ được.
- Thỏ con sinh lúc mẹ đang trong hang thì cũng ở trong hang.
- Hệ quả: cáo chỉ bắt được thỏ lúc thỏ ra ngoài (ban ngày, chạng vạng). Để cáo không chết đói, **cáo no lâu hơn: 1 con mồi / 15 giờ mô phỏng** (13 §4.4: 10 giờ). Trong hình, cáo đổi sang **thức lúc chạng vạng và ban ngày** (15h–9h): thú săn đi săn lúc con mồi ra ngoài.
- Các loài khác (cáo, diệc, ong, cá) vẫn ngủ **chỉ là hình** như GDD 11 §1.5.

| Chỉ số (`huntsim.py survey 16`) | Thỏ ngủ ngoài hang (hình) | **Thỏ ngủ trong hang** |
|---------------------------------|---------------------------|------------------------|
| Kết game | 16/16, trung vị 1.1 giờ thật | **15/16, trung vị 0.7 giờ thật** (0.5–1.3) |
| Thỏ · Cáo | 29 · 6.8 | 28 · 5.9 |
| Bị săn · chết đói / ngày mp (cáo chết đói) | 45.8 · 47.9 (1.2) | 27.3 · 34.2 (1.2) |
| Tổng số con chết / ngày mp | ~94 | **~62** |
| Thời gian thỏ ở trong hang (ngủ + trốn) | 5–10% | ~53% |

- Seed không kết (1/16) là do diệc vắng ở ao lúc cần đủ loài, cùng kiểu dao động với các mô hình trước (`biomesim.py` 7/8).
- **Bài học khi chỉnh số:** chỉ cho thỏ ngủ trong hang thì thỏ giảm một nửa (không ăn gần nửa ngày) và cáo chết đói 4 con / ngày mp. Cần cả hai: ngủ đói chậm (× 0.3) và cáo no lâu hơn.
- Thông số ở `balance.json` → `hunting.sleep` (`inRefuge`: giờ thức theo loài, `lagHours`, `drain`) và `social.species.fox.minutesPerCatch`.

## 4. Thú săn rượt và vồ
Thay luật "mỗi phút có xác suất bắt" của 07 §6.4.

1. **Chọn mồi:** thú săn đói (độ no < 60), không mệt, chọn **con mồi gần nhất đang không trốn** trong tầm nhìn (cáo 12 cột, diệc 30 cột).
2. **Rượt:** chạy tới với **tốc độ săn** (cáo 4 cột / phút, gấp đôi lúc đi bộ; diệc 3). Con mồi trốn được vào hang thì thú săn chọn con khác.
3. **Vồ:** khi tới được trong phút này (cách ≤ tốc độ săn + 1 cột), thú săn **lao tới sát và vồ luôn** một lần. Trúng với xác suất `vồ × độ hiếm × nơi trú ẩn`:
   - **vồ:** cáo 0.9, diệc 0.4;
   - **độ hiếm** và **nơi trú ẩn** (bụi, tán cây: × 0.5) giữ như 07 §6.4.
4. **Trượt** thì thú săn **mệt**, nghỉ (cáo 20, diệc 30 phút mô phỏng). Rượt quá **15 phút** (diệc 20) mà không tới được thì cũng bỏ cuộc và mệt.
5. **Luật cặp cuối** giữ nguyên: trong tầm chỉ còn ≤ 2 con mồi thì không săn.
6. Trúng thì như cũ: thú săn no 100, con mồi để lại 2 mùn.

## 5. Hiển thị
- **Ngủ:** chập tối, thỏ đi bộ thong thả về hang rồi chui vào; sáng ra chui ra. Sóc leo lên cây ngủ.
- ↻ **Hang thỏ (mặt cắt, 2026-10-26):** dải đất vẽ như **mặt cắt**: thấy miệng hang ở mặt đất (cạnh một ụ đất đào lên), đường hầm dốc xuống và **buồng ngủ** dưới đất, rộng chừng 1.5 cột, đủ chỗ 4 con nằm cạnh nhau. Hang bỏ trống mờ dần trong 3 ngày rồi biến mất.
- **Thỏ trong hang:** thỏ đi tới miệng hang, chui theo đường hầm xuống buồng và **vẫn nhìn thấy** ở trong đó: mỗi con một chỗ nằm riêng trong buồng. Ngủ thì nằm cuộn lại, có "z". Trốn cáo thì ngồi im trong buồng. Ra khỏi hang thì đi ngược lên miệng hang.
- **Chạy trốn:** thỏ, sóc nhảy cao và nhanh hơn lúc đi. Sóc trèo lên thân cây.
- **Rượt:** cáo chạy sát đất, nhanh, không nghỉ.
- **Vồ (✅ Q34):** cáo nhảy vồ, **bụi cỏ tung lên** che chỗ đó, bụi tan thì con mồi không còn, cáo thong thả đi về hang. Không máu, không xác. Diệc mổ xuống nước, **tia nước bắn lên**, cá biến mất.

## 6. Kiểm chứng (`huntsim.py survey 16`, 16 seed, mỗi seed tối đa 4 giờ thật)

| Chỉ số (trung bình mỗi seed) | GDD 13 (bắt theo xác suất) | **GDD 14** |
|------------------------------|----------------------------|------------|
| Kết game | 16/16 seed, trung vị 1.3 giờ thật | **16/16 seed, trung vị 1.1 giờ thật** (0.7–2.0) |
| Thỏ · Cáo · Cá | 26 · 6.4 · 21 | 29 · 6.8 · 20.5 |
| Hang thỏ đang có người | (~6 bầy) | ~5.7 |
| Bị săn / ngày mp | 66.9 | **45.8** (33–62) |
| Chết đói / ngày mp (cáo chết đói) | 38.9 | 47.9 (1.2) |
| Tổng số con chết / ngày mp | ~106 | **~94** |
| Cáo vồ trúng | — | ~1/3 số lần vồ |
| Thời gian thỏ trốn trong hang | — | 5–10% |
| Quay đầu / con / phút thật | 2.2 | 3.5 (chạy trốn rồi quay lại là chuyển động có lý do) |

- **Bài học khi chỉnh số:**
  - Bản đầu cho thỏ thấy cáo từ 6 cột và trốn 20 phút: thỏ trốn 30% thời gian, cáo chỉ vồ trúng 1/5 và chết đói, thỏ lại chỉ bị khống chế bằng chết đói. Thú săn phải **thắng đủ thường** thì mới giữ được vai trò ở 08 §7.3.
  - Gia đình bám quá chặt quanh hang (± 4 cột) thì thỏ chết đói nhiều hơn 13. Cho thỏ đói đi xa tới ± 8 cột thì về lại mức cũ.
  - Bản đầu cho thú săn dừng sát mồi rồi **phút sau** mới vồ: con mồi chạy trước nên luôn giữ khoảng cách, chỉ bị bắt khi chạy ngược về phía thú săn. Thú săn phải **lao tới và vồ trong cùng một phút** thì "chạy nhanh hơn" mới có nghĩa.

Chạy lại:

```bash
python3 Docs/GDD/sim/huntsim.py survey 16
```

```bash
python3 Docs/GDD/sim/huntsim.py survey 16 13
```

Thông số ở `balance.json` → `hunting` (`burrow`, `prey`, `predators`).

### 6.1 Gia đình tối đa 4 con (2026-10-26, `huntsim.py survey 16`, có ngủ trong hang)

| Chỉ số | Gia đình 8 con, hang cách ≥ 8 | **Gia đình 4 con, hang cách ≥ 6** |
|--------|-------------------------------|-----------------------------------|
| Kết game | 15/16, trung vị 0.7 giờ thật | 14/16, trung vị 1.1 giờ thật (0.6–1.4) |
| Thỏ · Cáo · Cá | 28 · 5.9 · 19 | 26 · 6.2 · 20 |
| Hang có người | ~5 | **~8.5** |
| Bị săn · chết đói / ngày mp | 27 · 34 | 28 · 28 |

- Giữ hang cách 8 cột thì không đủ chỗ đào thêm hang: thỏ chỉ còn ~18. Hang cách 5 cột thì đủ thỏ (~29) nhưng cáo chết đói nhiều hơn. Chọn **6 cột**.
- Cả 2 seed không kết đều vì **diệc không bao giờ đến ao** (giống seed hỏng của các bản trước), không liên quan tới thỏ.

## 7. Câu hỏi cho người thiết kế
- ✅ **Q34.** Cảnh vồ: cáo vồ, **bụi cỏ tung lên**, con mồi biến mất, cáo thong thả về hang (thay phần "săn mồi chỉ là đuổi ra khỏi màn hình" của Q6). Không máu, không xác.
