# 11 · Nhịp ×100 & tầng tán (cây gỗ)

> Trạng thái: ✅ **Đã chốt** 2026-10-24 (Q21–Q24, [06](06-cau-hoi-mo.md)). 💡 Số liệu đã kiểm chứng bằng `worldsim.py`.
> Phần này **thay** các chỗ cũ nói "1 mùa = 1 ngày thật", "Sinh khí nghỉ ngơi tối đa 2 giờ" và "tầng tán sẽ đặc tả sau" (03 §7, 07 §3.3, 08 §2). Các file đó đã ghi chú trỏ về đây.

## 1. Nhịp ×100

### 1.1 Đồng hồ
- ✅ **1 phút thật = 100 phút mô phỏng** (`time.simMinutesPerRealMinute`). Mọi luật sinh thái trong `balance.json` tính theo **phút mô phỏng**, nên giữ nguyên số; chỉ đồng hồ chạy nhanh hơn. Vì vậy cân bằng của 07 và 08 vẫn đúng.
- ✅ **Q21: một mùa = 30 phút thật** (3 000 phút mp, `time.seasonMinutes`) = **3 ngày đêm** của game (§1.5); một năm = 2 giờ thật. ↻ **2026-10-24:** trước là 2 880 phút mp ≈ 29 phút thật. Mùa tính theo **thời gian mô phỏng đã chạy**, không theo ngày lịch. Tắt app thì thế giới ngủ, mùa đứng yên.
- ✅ Tuyết tan: mỗi lần sang Xuân (07 §3.1), không còn gắn với ngày lịch.
- ~~Ngày / đêm: vẫn theo giờ máy.~~ ✅ **Thay bằng:** ngày đêm theo thời gian chơi, 5 phút ngày + 5 phút đêm, thú có nếp sinh hoạt (§1.5). ↻ **Đổi 2026-10-24.**

| Việc | Phút mô phỏng | Thời gian thật (×100) |
|------|---------------|-----------------------|
| Cỏ mọc tới trưởng thành | 20 | 12 giây |
| Mâm xôi trưởng thành | 120 | 1 phút 12 giây |
| Thỏ sống | 2 880 | 29 phút |
| Cáo sống | 5 760 | 58 phút |
| Sồi trưởng thành / sống | 2 880 / 43 200 | 29 phút / 7.2 giờ |
| Một mùa | 3 000 | 30 phút |
| Một ngày đêm (§1.5) | 1 000 | 10 phút |

### 1.2 Sinh khí nghỉ ngơi (✅ Q22: giữ, trần 10 phút thật)
Thay công thức 08 §2. Mỗi ngày lịch, lần đầu thế giới thức dậy:

```
Sinh khí nghỉ ngơi = Sinh khí/phút mp hiện tại × 100 × min(10, max(0, 480 − số phút thật app mở hôm trước) / 48)
```

Tức là bù tối đa **10 phút thật** thu nhập (= 1 000 phút mp, cỡ một lần hồi sinh nhỏ), tăng dần khi hôm trước mở app ít hơn 8 giờ. Lý do giữ: người bận cả ngày quay lại vẫn có quà; lý do trần thấp: cả slice chỉ ~1.5–2 giờ, quà lớn hơn sẽ bỏ qua cả chặng.

`balance.json`: `restEssence.targetMinutes = 480` (phút thật), `restEssence.maxMinutes = 10` (phút thật).

### 1.3 Khoảnh khắc và UI
- ✅ Mọi thời gian của khoảnh khắc (09: thời gian sống, mờ dần, chờ lại, giãn cách, tỉ lệ Khách lạ mỗi phút) tính bằng **phút thật**: bong bóng là thứ người chơi phải thấy và bấm. Điều kiện sinh thái để bong bóng xuất hiện vẫn đọc từ mô phỏng.
- ✅ Bản Dev: nút tốc độ đổi thành **×1 / ×10 / ×60** trên nền nhịp ×100 (×1 = nhịp thật của game).
- Quyền năng giữ giá (Mưa 30). Sinh khí kiếm được nhanh ×100 theo thời gian thật, nhưng giá và thu nhập đều tính theo mô phỏng nên tương quan không đổi.

### 1.4 Kiểm chứng (`worldsim.py survey 8 …`, mùa 2 880 phút mp)
Người chơi mô hình nay ghé mỗi **300 phút mp = 3 phút thật** (`modelPlayer.visitMinutes`). Mỗi lần ghé làm bù nhiều việc: hồi sinh liền mấy vùng nếu đủ Sinh khí, gieo nhiều lượt. Lệnh cũ chạy lại đúng số cũ với `survey hpd=8 pe=30 notrees`.

| Người chơi | Vùng 5 | Vùng 9 | Kết game (giờ mp) | **Kết game (giờ thật)** | Thỏ vắng | ★ |
|------------|--------|--------|-------------------|-------------------------|----------|---|
| Ghé mỗi 3 phút thật, có cây tán (mặc định) | 40–45h | 80–115h | 120–210h | **1.2–2.1h, trung vị 1.4h** | 0h | 13/13 |
| Ghé mỗi 3 phút, không cây tán (`notrees`) | 35–45h | 85–130h | 125–215h | 1.2–2.1h, trung vị 1.5h | 0h | 13/13 |
| Ghé mỗi 6 phút (`pe=600`) | 40–50h | 110–150h | 140–220h | 1.4–2.2h, trung vị 2.0h | 4–8h | 13/13 |
| Ghé mỗi 18 phút (`pe=1800`) | 120–210h | 210–270h | 240–360h (6/8 seed trong 400h) | 2.4–3.6h, trung vị 3.3h | 24–52h | 12–13 |
| Không gọi mưa (`idle`) | 40–45h | 95–135h | 140–215h | 1.4–2.1h, trung vị 1.5h | 0–13h | 13/13 |

- Cả slice (14 vùng + Khu Vườn) còn **~1.5–2 giờ mở app** với người chơi chăm; trước đây ~16 ngày lịch.
- Người ghé thưa (18 phút) tiến chậm hơn rõ, thỏ có lúc vắng ở vùng chờ chăm, nhưng thế giới vẫn tự cân bằng và vẫn tới kết. Trụ cột "ghé lại mỗi 10–30 phút" (01) vẫn chơi được, chỉ là ghé dày thì tiến nhanh.
- Hiệu năng: ≈ 1.7 bước mỗi giây × 0.137 ms, không đáng kể (Tech Doc 05 §4).
- **Mùa 3 000 phút mp (2026-10-24, `survey 8`, cùng seed):** bảng trên đo ở mùa 2 880. Đổi lên 3 000, `worldsim.py` vẫn kết 8/8 seed, trung vị **1.4 giờ thật** (1.1–3.4, trước 1.3–2.0); `biomesim.py` (mô hình hiện tại, 12) kết 7/8, trung vị **1.2 giờ** (0.7–3.3, trước 1.1, 0.6–3.0). Thỏ không vắng, ★ 13/13. Khác biệt nằm trong độ dao động giữa các seed.

### 1.5 Ngày đêm và nếp sinh hoạt (✅ 2026-10-24, chỉ là hình)
↻ Thay "ngày đêm theo giờ máy" (03 §7, §1.1 cũ). Trời sáng tối theo **thời gian chơi**, không theo đồng hồ của máy.

- ✅ **Một ngày đêm = 10 phút thật** = 1 000 phút mp (`time.dayNightMinutes`): **5 phút ngày, 5 phút đêm**. Tính theo `World.Minute`, nên tắt app thì trời cũng đứng yên, mở lại vẫn đúng giờ đó.
- Thế giới mới bắt đầu lúc **bình minh**. Đổi ra "giờ trong ngày" để vẽ: `giờ = 6 + 24 × (phút mp mod 1 000) / 1 000`; ngày là 6h–18h, đêm 18h–6h.
- Chuyển sáng tối dần quanh 6h và 18h (5h–7h, 17h–19h, mỗi lần ≈ 50 giây thật), có ráng hồng ở chân trời. Sao hiện khi tối.
- Một mùa (30 phút thật) có **đúng 3 ngày đêm**, nên mùa nào cũng bắt đầu lúc bình minh.
- Không đổi luật sinh thái: cây, thú vẫn ăn, lớn, sinh sản như cũ cả ngày lẫn đêm. Cân bằng ở 07, 08, 12 giữ nguyên.
- ↻ **Ngoại lệ (2026-10-25):** thỏ ngủ trong hang, sóc ngủ trên cây là **luật thật** (không ăn, không bị vồ, đói chậm), xem [14 §3b](14-hang-tho-va-san-moi.md#3b-ngủ-trong-hang--2026-10-25). Cáo đổi giờ thức sang 15h–9h.

**Nếp sinh hoạt (chỉ là hình):** mỗi loài có giờ thức riêng. Lúc ngủ, con vật đứng yên ở chỗ nó vừa nằm, hiện "z" bay lên; mỗi con đi ngủ / thức dậy lệch nhau tới ~40 phút trong ngày (≈ 17 giây thật) để không đồng loạt.

| Loài | Nếp | Thức (giờ trong ngày) | Lúc ngủ |
|------|-----|-----------------------|---------|
| Thỏ | Ngày | 5h30 – 18h30 | Nằm thu mình, "z" |
| Sóc | Ngày | 6h – 18h | Nằm thu mình, "z" |
| Ong | Ngày | 6h30 – 17h30 | Đậu xuống sát cỏ, thôi bay lượn |
| Diệc | Ngày | 5h30 – 18h30 | Đứng im, "z" |
| Cáo | Đêm, cả lúc chạng vạng | 17h – 7h | Ngủ ban ngày, nằm thu mình, "z" |
| Cá | Luôn thức | — | Đêm bơi chậm, lặn sâu hơn |

- Thỏ và Cáo cùng thức lúc chạng vạng (17h–18h30, 5h30–7h), như ngoài tự nhiên.
- Vì mô phỏng không đổi, đôi khi một con vẫn bị săn hay được sinh ra lúc đang ngủ. Khi đó nó **thức dậy** để diễn (thỏ chạy, thú săn đuổi theo), xong thì ngủ tiếp nếu còn giờ ngủ. Hoạt ảnh đuổi mồi ưu tiên thú săn đang thức.
- Con vật ngủ không đi theo cột mô phỏng (mô phỏng vẫn cho nó lang thang); thức dậy thì đi bộ tới chỗ của nó. Chỉ là hình nên không lưu.
- Ambient (01) đổi theo ngày đêm của game: đêm có dế.

## 2. Tầng tán: cây gỗ có vai trò

### 2.1 Vì sao
GDD 03 §2 đã có ý tưởng tầng tán ("cây gỗ che sáng cho 2 tầng dưới"). Cây gỗ cho slice thêm **một quyết định dài hạn**: trồng cây tán thì được giữ ẩm, đất màu, nơi trú ẩn, quả; nhưng mất chỗ cho hoa dại (cần nắng), nên ít ong hơn ở đó. Ranh giới "lùm cây / đồng cỏ" tự hình thành, đúng tinh thần 03 §2.

### 2.2 Luật chung (✅)
- **Tầng 2 (tán).** Gốc chiếm 1 cột. Tán của cây trưởng thành phủ **3 cột** (gốc ± 1, `canopyRadius`). Gốc mới (gieo, hạt rơi, hạt trong đất) phải có **ít nhất 1 ô trống** giữa nó và gốc khác (`canopySpacing` = 1; ✅ 2026-10-24, trước là 2), nên trồng được cây chính xen vào khoảng giữa để thành rừng.
- **Che bóng:** dưới tán, ánh sáng cho tầng thảm và tầng bụi giảm từ 100 xuống **55** (`canopyShade` 45; lấy mức thấp hơn nếu đã có bụi che). Cỏ (cần 40) và mâm xôi (40) vẫn sống; **hoa dại (60) yếu dần và không nảy mầm** dưới tán. Cây non tầng tán dưới tán của cây khác cũng chỉ nhận 55.
- **Giữ ẩm:** bốc hơi dưới tán **×0.5** (`canopyEvaporation`).
- **Lá rụng mùa Thu:** mỗi cây trưởng thành thêm Mùn cho 5 cột (gốc ± 2), tổng **20 Mùn mỗi cột mỗi mùa Thu** (`leafLitterPerAutumn`), rải đều theo phút.
- **Nơi trú ẩn:** con mồi đứng dưới tán bị bắt với xác suất **×0.5**, như cạnh mâm xôi (07 §6.4); không cộng dồn.
- **Mùa Đông:** rụng lá, không che bóng, không giữ ẩm, không trú ẩn. Hình: Thu lá vàng cam, Đông trơ cành.
- ✅ **Cây non ngủ khô (2026-10-24):** cây non tầng tán cạn sức khoẻ (hạn, đất xấu) thì **ngủ khô** như cây trưởng thành: trơ cành, ngừng lớn, tỉnh lại khi điều kiện tốt. Trước đó cây non chết luôn, và vì lớn lâu nên gần như không cây nào qua nổi một đợt hạn (mô hình: chỉ 7% Sồi gieo lớn được).
- **Chết** (hết tuổi hoặc cạn sức khoẻ khi đã trưởng thành mà quá tuổi): để lại Mùn ở cột gốc. Không tự mọc lại tại chỗ khi chết già (khác cỏ); thế hệ sau đến từ hạt.
- Sinh khí, Đa dạng và Sức khoẻ: cây tán tính như một loài cây (thêm Đa dạng, vai trò "sản xuất"), **không** thêm vai trò mới, nên công thức Sức khoẻ của 08 §4 giữ nguyên.

### 2.3 Loài (✅ Q23: cả ba)
| | **Sồi** 🌳 | **Táo dại** 🍎 | **Liễu** 🌿 |
|---|---|---|---|
| Biome | Đồng cỏ | Đồng cỏ | Ao: chỉ cột đất **kề mặt nước** (`bank`) |
| Lớn tới trưởng thành (phút mp) | 1 440 (✅ trước: 2 880) | 1 440 | 1 440 |
| Sống (phút mp) | 43 200 (30 ngày mp, sống qua cả slice) | 20 160 (14 ngày mp) | 20 160 |
| Độ ẩm (chết / tốt / tốt / úng) | 15 / 30 / 85 / 100 (✅ trước: 20 / 35) | 25 / 40 / 80 / 100 | 40 / 60 / 100 / 100 |
| Đất màu tối thiểu · Ánh sáng tối thiểu | 20 (✅ trước: 30) · 50 | 30 · 60 | 20 · 50 |
| Hạt | 0.05/giờ mp, rơi ± 2 cột | 0.1/giờ, ± 3 cột | 0.05/giờ, ± 2 cột (chỉ nảy ở bờ) |
| Vai trò riêng | Tán, giữ ẩm, lá rụng, trú ẩn | Như Sồi, cộng: **ra hoa** (ong tính là một cây hoa, được thụ phấn thì ra hạt ×2); **quả** Hạ–Thu: thỏ và cáo đói đứng trong ± 2 cột được +0.3 no/phút | Như Sồi; tán phủ cột nước kề bên, nên **cá dưới tán khó bị diệc bắt** (×0.5) |
| Mùn khi chết | 60 | 40 | 40 |
| Sinh khí/phút | 0.4 | 0.3 | 0.3 |
| Giá gieo | 150 | 100 | 120 |

Quả dùng chung một luật (`fruitEaters` theo loài cây, `animalRules.fruitGain`): Mâm xôi cho cáo (như 07), Táo dại cho thỏ và cáo. Trường `eatsBerries` cũ của cáo bỏ đi.

**Kiểm chứng sống sót (2026-10-24, `worldsim.py`, 6 seed, gieo mọi cột q > 0.5 lúc 60 giờ mp, theo dõi 4 mùa):**

| | Sồi | Táo dại | Liễu |
|---|---|---|---|
| Trước (cây non chết, Sồi 2 880 phút, 20/35, màu 30) | 7% lớn được | 30% | 57% |
| ✅ Sau (cây non ngủ khô + Sồi 1 440 phút, 15/30, màu 20) | **98%**, trung bình sau ~40 phút thật | 84%, ~53 phút | 97%, ~37 phút |

Sau khi sửa, nhịp slice không đổi (kết game trung vị 1.4 giờ thật, 1.1–2.4), đất dưới tán 14–37% (trước 7–19%), ong và hoa như cũ.

**Kiểm chứng khoảng cách gốc 1 ô (2026-10-24, 6 seed):** người chơi mô hình như trước → kết game 1.3–2.0 giờ thật (trung vị 1.4), 29–37 cây tán, đất bị che 16–24%. Người chơi **trồng kín** mọi chỗ được ở các đồng cỏ → 51–56 cây tán, che 28–59%, kết game vẫn tới (1.1–1.4 giờ thật), ong 12–32 đàn, thỏ không tuyệt (thấp nhất 3–23 con). Rừng dày làm mất hoa ở chỗ đó nhưng không làm sụp hệ.

### 2.4 Mở khoá (✅ Q24: khám phá 🌱)
Như Hoa dại / Mâm xôi / Sen (09 §3.2 🌱): đạt điều kiện thì hạt lạ theo gió xuất hiện, người chơi nhặt rồi gieo được.

| Loài | Điều kiện (`moments.discover`) | Thường mở lúc (mô hình, giờ mp → phút thật) |
|------|-------------------------------|-------------------------------------------|
| Táo dại | Cả thế giới ≥ 10 Hoa dại sống **và** ≥ 1 Ong | 6–10h → 4–6 phút |
| Sồi | Một vùng có ≥ 4 Mâm xôi sống | 14–16h → 8–10 phút |
| Liễu | Một ao có ≥ 2 Lau sậy sống | 14–23h → 8–14 phút |

### 2.5 Kiểm chứng (`worldsim.py`, 4 seed, 240 giờ mp, người chơi mô hình gieo 1 Sồi + 1 Táo mỗi đồng cỏ, 1 Liễu mỗi ao)
- **Độ ẩm mùa Hạ:** dưới tán **50–69**, ngoài tán **20–31**. Cây tán là cách thứ hai (sau Mưa) để giữ một góc xanh qua mùa hạ.
- **Phủ:** 7–19% cột đất nằm dưới tán. Cây tán là điểm nhấn, không lấn đồng cỏ.
- **Hoa dại:** hầu hết nằm ngoài tán (ví dụ 92 ngoài / 2 dưới tán). Trade-off hiện rõ nhưng không làm sụp ong: số ong trung bình 12–20 đàn, như khi không có cây.
- **Nhịp và quần thể:** như bảng §1.4; có hay không cây tán thì kết game, thỏ, cá, chết đói, bị săn đều cùng khoảng. Cây tán đổi **cảnh quan và lựa chọn**, không đổi độ khó.

### 2.6 Hình
✅ (2026-10-24) Cây tán phải **cao vượt trội** so với cỏ, bụi và thú, để dải đất có cảm giác thiên nhiên thật. Dải cao 180 pt, đất 36 pt, còn 144 pt cho trời:

| Loài | Cao khi đủ lớn (✅ ngẫu nhiên mỗi cây) | Tán (hình) | Dáng |
|------|---------------------------|------------|------|
| Sồi | **100–140 pt**, cây cao nhất gần chạm mép trên dải | ~4 cột | Thân to, tán nhiều khối tròn chồng nhau |
| Liễu | 90–116 pt | ~3.5 cột | Thân cao, cành rủ dài gần chạm mặt nước |
| Táo dại | 65–90 pt | ~3 cột | Cây ăn quả thấp, tán tròn |

✅ Mỗi cây có chiều cao riêng, chọn ngẫu nhiên đều trong khoảng của loài khi cây nảy mầm, cố định suốt đời cây (lưu lại được vì suy ra từ cột và phút nảy mầm).

Tán hình có thể rộng hơn 3 cột của luật che bóng (§2.2); luật không đổi. #### Lá mọc và rụng (✅ 2026-10-24)
Lá không bật / tắt đột ngột khi giao mùa:
- **Mọc lá** (sang Xuân, hoặc cây tỉnh khỏi ngủ khô): tán lá phóng to dần từ giữa tán, khoảng 6 giây.
- **Rụng lá** (sang Đông, hoặc cây ngủ khô vì hạn): tán thưa và mờ dần trong khoảng 4 giây, từng chiếc lá cùng màu tán (Thu: cam vàng; ngủ khô giữa mùa: xanh úa) rơi lượn xuống đất rồi tan.
- **Đổi màu** (Xuân → Hạ → Thu): tán cũ mờ dần sang tán mới trong khoảng 3 giây.
- Các thời gian trên là ở tốc độ ×1; tua nhanh (bản Dev) thì lá mọc / rụng nhanh theo, luôn khớp với mùa.
- Lúc bình thường cây là **một khối** (thân + tán liền nhau), nên cây mờ phía xa không lộ thân xuyên qua lá; chỉ trong lúc mọc / rụng / đổi màu mới tách hai lớp.
- Cây vừa trôi vào khung nhìn thì hiện đúng trạng thái hiện tại, không diễn lại hiệu ứng. Cây phía xa cũng mọc / rụng lá như vậy, lá rơi mờ như cây.

#### Mùa Đông (✅ 2026-10-24, chỉ là hình)
Mùa Đông phải nhìn ra là mùa Đông ngay khi liếc xuống:
- **Tuyết phủ đất:** lớp tuyết trắng dày dần trên mặt đất (lấp mép cỏ) trong giờ đầu của mùa Đông, tan dần đầu Xuân. Cỏ, bụi, hoa ngả trắng xám; ngọn cỏ vẫn nhô lên khỏi tuyết.
- **Ao đóng băng:** mặt ao phủ lớp băng xanh trắng có vết nứt; cá vẫn bơi mờ mờ bên dưới.
- **Tuyết đọng trên cây:** cành trơ có tuyết trắng đọng phía trên; cây phía xa cũng vậy.
- **Mưa thành tuyết:** mưa tự nhiên và quyền năng Mưa trong mùa Đông hiện là tuyết rơi chậm, lượn nhẹ (luật không đổi: vẫn cộng độ ẩm). Ngoài ra luôn có vài bông tuyết bay lất phất khắp dải.
- Trời mùa Đông đã có màu xám lạnh (SkyView).

#### Rừng phía xa (✅ 2026-10-24, chỉ là hình)
Để có cảm giác khu rừng có chiều sâu:
- ✅ (sửa 2026-10-24) Ngay khi có **hai cây tán** (kể cả cây non) đứng liền nhau (không có cây tán khác ở giữa) với gốc cách nhau **< 8 cột**, giữa hai cây mọc thêm **3–5 cây phía xa** (số lượng ngẫu nhiên theo cặp). Trồng thêm cây chính vào giữa thì cặp cũ chia thành hai cặp nhỏ, mỗi cặp có nhóm cây xa riêng.
- Cây phía xa: cùng loài với một trong hai cây chính, **mờ hơn** (độ đục 35–60%), ngả xanh lam nhẹ như bị sương xa, nhỏ hơn (60–90% chiều cao loài), đứng sau cây chính, **rải đều** lấp khoảng giữa hai gốc (lệch nhẹ ngẫu nhiên, không chụm lại).
- **Lớn cùng cây chính:** cây phía xa nảy mầm cùng lúc với cây chính trẻ hơn trong cặp và lớn theo đúng nhịp của cây đó; chết già theo tuổi thọ loài. ✅ (2026-10-27) Chết già thì **một cây non mọc lại đúng chỗ đó** (thế hệ sau, lớn theo nhịp của loài), nên khi cặp cây chính còn sống thì khoảng giữa không bao giờ trống. Trước đây cây xa chết hẳn, cây chính già sống tiếp nên khoảng giữa trống mãi.
- **Theo cây chính của nó:** đổi lá theo mùa như cây chính; cây chính ngủ khô (trơ cành) thì cây phía xa cùng loài cũng trơ cành.
- **Không tương tác:** không che bóng, không giữ ẩm, không có quả, không trú ẩn, không tính Sinh khí hay Đa dạng; thú không ăn, chuột không chọn được.
- Nếu **một trong hai cây chính mất** (chết, bị thay), cả nhóm cây phía xa của cặp đó **tàn lụi dần** rồi biến mất.

Cây non lớn từ một mầm nhỏ tới **80%** cỡ khi trưởng thành, rồi lớn tiếp tới đủ cỡ sau thêm 2 lần thời gian lớn (Sồi: khoảng 1 giờ thật nữa), nên cây già trông to hơn cây vừa trưởng thành. Chim và ong bay qua trước tán. Cây non lớn dần từ một mầm nhỏ; mùa Thu lá vàng cam, mùa Đông trơ cành; Táo dại có hoa trắng hồng mùa Xuân và quả đỏ mùa Hạ–Thu; Liễu rủ cành xuống mặt nước.
