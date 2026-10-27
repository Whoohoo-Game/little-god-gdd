# 10 · Giao diện: đặc tả chi tiết (vertical slice)

> Phạm vi: **vertical slice**: khay thần, nút cuộn, bản đồ mini, sổ tay tối giản, hiệu ứng thức dậy, cùng các phần nhỏ đi kèm (thẻ thông tin, cài đặt, menu hệ thống).
> Bong bóng khoảnh khắc đã đặc tả ở [09](09-khoanh-khac.md); file này chỉ nói chỗ chúng chạm vào UI.
> Trạng thái: 💡 đề xuất, chờ chơi thử trong prototype. Kích thước tính bằng **pt** (macOS) / **px** (Windows), như dải đất (✅ 01).

## 1. Nguyên tắc
| Nguyên tắc | Hệ quả |
|------------|--------|
| **Thế giới là nhân vật chính** (✅ 01) | UI chiếm ít nhất có thể: lúc nghỉ chỉ còn một cục nhỏ ở góc phải và hai nút cuộn gần như trong suốt |
| **Đọc bằng một cái liếc** | Số chỉ có trong khay thần và sổ tay. Ngoài đó dùng màu, biểu tượng, chuyển động |
| **Click xuyên qua vùng trống** (✅ 01) | Mọi phần tử UI nhận click đều là vùng "không trong suốt". Giữ chúng **nhỏ** để không chặn cửa sổ bên dưới |
| **Không chiếm con lăn** (✅ 04 §1) | Không phần tử nào dùng con lăn chuột. Cuộn bằng nút giữ |
| **Không modal** | Không có hộp thoại chặn thao tác. Sổ tay và cài đặt là cửa sổ riêng, đóng bất cứ lúc nào |
| **Không làm phiền** (✅ trụ cột 3) | Không âm thanh từ UI khi người chơi không click. Không nhấp nháy. Mở/đóng đều có chuyển động mềm 150–250 ms |

## 2. Bố cục dải đất
```
 ←──────────────────────────── chiều rộng màn hình ────────────────────────────→
┌──────────────────────────────────────────────────────────────────────────────┐ ▲
│                                                                              │ │
│◀           (bầu trời trong suốt: click xuyên qua)                           ▶│ │ 180pt
│  ✨                    🐇 🐇       🦊                     💌        ┌───────┐ │ │
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│✿ 1.2k │▓│ │ mặt đất 12pt
└──────────────────────────────────────────────────────────────────────────────┘ ▼
  ▲ nút cuộn (16×48, giữa chiều cao)                              ▲ khay thần (thu gọn)
```
- **Khay thần** neo ở **góc phải dưới**, ngồi trên mặt đất, cách mép phải 24pt để chừa chỗ cho nút ▶.
- **Nút cuộn** ◀ ▶ ở hai mép, giữa chiều cao dải.
- Bong bóng khoảnh khắc **không bao giờ nằm dưới khay**: khi một bong bóng rơi vào vùng khay, nó được đẩy sang trái cho tới khi không còn chồng lên.

## 3. Khay thần

### 3.1 Trạng thái thu gọn (lúc nghỉ)
```
┌─────────┐
│ ✿ 1.2k ●│    64 × 22 pt
└─────────┘
```
| Thành phần | Nội dung |
|------------|----------|
| ✿ Biểu tượng | Tinh linh thu nhỏ, đổi màu theo mùa (✅ 04 §0) |
| Số Sinh khí | Đang có, rút gọn: `840` · `1.2k` · `56k` · `1.3M` |
| ● Chấm báo | Hiện khi có 💌 lời mời đang chờ hoặc 🌿 vùng sẵn sàng hồi sinh **mà đủ Sinh khí**. Không đếm số |

Nền tối trong mờ (độ đục 70%), bo góc 4pt, viền nhạt theo màu mùa.

### 3.2 Trạng thái mở rộng (khi rê chuột vào)
Mở sau khi chuột ở trên khay **150 ms** (tránh mở nhầm khi chuột lướt qua). Đóng sau khi chuột rời khay **600 ms**. Panel mọc lên phía trên và sang trái, giữ góc phải dưới cố định.

```
┌──────────────────────────────────────────────────┐
│ ✿ Sinh khí 1,243   +38/ph        🌸 Xuân · Cấp 2 ▮▮▮▯▯│  ← hàng 1: trạng thái
│ [🌱 Gieo ▾] [🌧 Mưa 30] [🔒] [🔒]   [💌 1]           │  ← hàng 2: quyền năng
│ ░░░░░▓▓▓▓█████████▓▓≈≈▓▓▓░░░░░░░░░░░░░░░░░░░░░░⌂   │  ← hàng 3: bản đồ mini
│                                   [📖] [⚙] [–]      │  ← hàng 4: nút phụ
└──────────────────────────────────────────────────┘
                                           ~320 × 104 pt
```

**Hàng 1 · Trạng thái**
| Thành phần | Nội dung |
|------------|----------|
| Sinh khí | Số đầy đủ có dấu phân cách (`1,243`). Rê chuột: tổng tích luỹ từ đầu |
| Tốc độ | `+38/ph`. Rê chuột: *"Đa dạng ×2.4 · Cân bằng ×1.0"* của khung nhìn hiện tại |
| Mùa | Biểu tượng mùa + tên mùa. Rê chuột: *"Mai sang Hạ"* |
| Cấp thần | `Cấp 2` + thanh 5 ô tiến tới cấp kế tiếp (07 §7.4). Rê chuột: *"Cấp 3 ở 50,000 · mở Nắn đất"* |

**Hàng 2 · Quyền năng**
| Nút | Hành vi |
|-----|---------|
| 🌱 **Gieo ▾** | Click: mở một hàng nhỏ **xổ ngang** ngay trên khay, mọc sang trái (✅ 2026-10-24: dải chỉ cao 180 pt nên xổ dọc bị cắt ở mép trên; 💌 / 🌿 cũng vậy), gồm các loài **đã khám phá** (biểu tượng + giá, ví dụ `Cỏ 5`, `Hoa dại 10`, `Mâm xôi 25`, `Sen 25`, `Táo dại 100`, `Sồi 150`, `Liễu 120`). Chọn một loài thì bật công cụ Gieo (§3.3). Loài chưa khám phá không hiện |
| 🌧 **Mưa 30** | Bật công cụ Mưa (§3.3) |
| 🔒 ô khoá | Quyền năng cấp cao hơn, hiện bóng mờ. Rê chuột: *"Gió · mở ở Cấp 2"*. Trong slice, Gió / Nắng ấm / Nắn đất / Sét **vẫn khoá kể cả khi đủ cấp**, kèm dòng *"Sắp có"* |
| 💌 **n** | Chỉ hiện khi có lời mời đang chờ (09 §3.2). Click: khung nhìn trượt tới con vật đang chờ. Không mời trực tiếp từ khay, vì lời mời là khoảnh khắc ở ngoài thế giới |

- Nút đang chọn có viền sáng. Không đủ Sinh khí thì nút mờ 50% và giá chuyển màu đỏ nhạt; vẫn bấm được để xem.
- **Mặc định không chọn công cụ nào.** Khi đó click mặt đất không làm gì, click sinh vật hiện thẻ thông tin (§7). Nhờ vậy người chơi không bao giờ tiêu Sinh khí nhầm.

**Hàng 3 · Bản đồ mini:** §5.

**Hàng 4 · Nút phụ**
| Nút | Hành vi |
|-----|---------|
| 📖 Sổ tay | Mở / đóng cửa sổ Sổ tay (§6) |
| ⚙ Cài đặt | Mở / đóng cửa sổ Cài đặt (§9) |
| – Ẩn | Thu dải đất vào menu bar / system tray (✅ Q14). Thế giới vẫn chạy |

> ↻ **2026-10-24 ([12](12-moi-truong-song.md)):** khay bỏ nút 💌 và 🌿. Công cụ Gieo gieo được trên đất hoang cách đất sống ≤ 5 ô; bản đồ mini tô theo biome của từng cột (đồng cỏ, rừng, ao, đất hoang).

### 3.3 Công cụ đang dùng
Khi bật một công cụ, con trỏ trên mặt đất có thêm một biểu tượng nhỏ (12×12) đi kèm. ✅ (2026-10-24) **Khay ẩn hẳn** trong lúc cầm công cụ để có chỗ đặt; huỷ công cụ thì khay hiện lại (thu gọn). Nút cuộn ◀ ▶ vẫn hiện để đi tới chỗ khác mà không bỏ công cụ. **Huỷ công cụ:** chuột phải, Esc. Công cụ **tự huỷ sau 20 giây** không dùng. Gieo xong một cây thì vẫn cầm công cụ, để gieo tiếp.

✅ **Xem trước khi gieo:** cột dưới con trỏ hiện **hình mờ (55%) của cây khi đã lớn**, đứng đúng chỗ sẽ mọc (cây tán theo dáng mùa hiện tại, chiều cao trung bình của loài). Không gieo được ở đó thì hình ngả đỏ và mờ hơn; tỉ lệ nảy mầm thấp (< 30%) thì ngả vàng.

**🌱 Gieo**
- Rê trên mặt đất: cột dưới chuột được tô nền theo **khả năng nảy mầm** (= độ phù hợp q, 07 §5.1). Xanh: ≥ 70%; vàng: 30–70%; đỏ: < 30%; xám gạch chéo: tầng đó đã có cây, hoặc sai loại nền (cây cạn trên nước và ngược lại). Kèm dòng chữ nhỏ *"Hoa dại · 82%"* (✅ 04 §2: hiện trước tỉ lệ thành công).
- Click: trả giá, hạt rơi xuống. Nảy mầm thì mầm nhú lên kèm lấp lánh; không nảy mầm thì hạt tan thành bụi nhỏ.
- Công cụ giữ nguyên sau khi gieo, để gieo liền nhiều cột.

**🌧 Mưa**
- **Click:** mưa phủ **7 cột** quanh chỗ click (bán kính 3, 08 §9), giá 30.
- **Kéo ngang:** vệt xanh nhạt theo chuột cho thấy các cột sẽ được mưa. Giá = `30 × ⌈số cột / 7⌉`, tối đa **21 cột** (90 Sinh khí) mỗi lần kéo. Thả chuột thì mây kéo tới và mưa rơi trong ~3 giây.
- Rê chuột: mỗi cột hiện một vạch nhỏ độ ẩm (xanh đậm = ẩm), chỉ khi đang cầm công cụ Mưa.
- Click lên bong bóng 💧 (09) là một cách nhanh, tương đương click giữa vùng.

## 4. Nút cuộn ◀ ▶
| Thuộc tính | Giá trị |
|------------|---------|
| Kích thước · vị trí | 16 × 48 pt, sát mép trái/phải, giữa chiều cao dải |
| Độ đục | 15% lúc nghỉ → 80% khi chuột cách nút < 64 pt (chuyển trong 200 ms) |
| **Giữ** | Cuộn 4 cột/giây, tăng dần lên **24 cột/giây** sau 1.5 giây giữ. Thả ra thì trượt chậm lại trong 0.25 giây |
| **Click một lần** | Cuộn 4 cột |
| **Double-click** | Nhảy tới mép của vùng kế tiếp theo hướng đó (05 §2): khung nhìn trượt sao cho vùng đó vào giữa, trong 0.6 giây |
| Ở mép thế giới | Nút phía đó **ẩn** |
| Chỉ báo khoảnh khắc | Biểu tượng 8×8 nằm ngay trên nút, kèm chấm nếu ≥ 2 (✅ 09 §7) |

- Khung nhìn không bao giờ tự di chuyển, trừ khi bật chế độ theo dõi (✅ Q12).
- **Giữ vị trí:** vị trí khung nhìn được lưu; mở app lần sau ở đúng chỗ cũ (05 §2).
- Khi đang cầm công cụ Mưa và kéo tới sát nút cuộn, khung nhìn **không** tự cuộn theo (tránh mưa nhầm).

## 5. Bản đồ mini
Nằm trong khay mở rộng (hàng 3). Mỗi cột thế giới = **2 pt**, nên rộng 288 pt cho 144 cột, cao 10 pt.

| Lớp | Hiển thị |
|-----|----------|
| Nền | Đất hoang: xám nâu · Đồng cỏ: xanh lá, đậm hay nhạt theo Sức khoẻ vùng (08 §5.3) · Ao: xanh dương ở cột nước · Khu Vườn Thiêng (chưa mở): bóng cây vàng mờ ở đầu phải, luôn hiện như một lời hứa (✅ 05 §5) |
| Ranh giới vùng | Vạch dọc 1 pt mờ giữa các vùng |
| Vùng Cân bằng | Vài điểm sáng nhỏ lấp lánh chậm trên vùng đó |
| Khung nhìn | Khung chữ nhật viền trắng, độ rộng đúng bằng phần đang thấy |
| Khoảnh khắc | Chấm sáng 1 pt phía trên thanh, ở cột có khoảnh khắc nhóm A/B (✅ 09 §7) |
| Vùng sẵn sàng hồi sinh | Mép đất hoang đó có viền xanh mờ |

- **Rê chuột:** tên vùng + trạng thái bằng chữ: *"Ao Sen · Cân bằng"*, *"Đồi Tây · Đất hoang"*, *"Bãi Gió · Đang hồi phục"*. Trạng thái: Đất hoang · Đang hồi phục (< 60) · Khoẻ (60–84) · Cân bằng (≥ 85).
- **Click / kéo:** khung nhìn nhảy tới đó (trượt 0.4 giây; kéo thì đi theo chuột).
- Không hiện số nào trên bản đồ.

## 6. Sổ tay thiên nhiên (tối giản)
Cửa sổ **riêng, nổi phía trên dải đất**, neo ở mép phải (✅ 04 §1). Kích thước 480 × 320 pt, không thay đổi được. Đóng bằng nút ✕, Esc, hoặc nút 📖 trên khay. Mở / đóng không dừng thế giới.

```
┌──────────────────────────────────────────────── ✕ ┐
│  [ Loài ]  [ Vùng đất ]  [ Khách ghé thăm ]        │
├────────────────────────────────────────────────────┤
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐          │
│  │ 🌿 │ │ 🌼 │ │ ▒▒ │ │ 🐇 │ │ ▒▒ │ │ ▒▒ │   …       │
│  │ Cỏ │ │Hoa │ │ ?  │ │Thỏ │ │ ?  │ │ ?  │          │
│  └────┘ └────┘ └────┘ └────┘ └────┘ └────┘          │
│  ─────────────────────────────────────────────     │
│  🐇 Thỏ · Ăn cỏ                       Đang có: 23   │
│  "Đông con khi cỏ dày; đói khi cỏ trụi. Cáo giữ    │
│   cho đàn thỏ không ăn hết đồng cỏ."               │
└────────────────────────────────────────────────────┘
```

### 6.1 Tab Loài
- Lưới thẻ **12 loài của slice**: Cỏ, Hoa dại, Mâm xôi, Giun, Thỏ, Ong, Cáo, Bèo, Sen, Lau sậy, Cá, Diệc. Xếp theo biome, rồi theo vai trò.
- **Đã khám phá:** tranh pixel, tên, biểu tượng vai trò (sản xuất · ăn cỏ · săn mồi · thụ phấn · phân huỷ). Chọn thẻ thì hiện bên dưới: mô tả 1–2 câu và *"Đang có: n"* (số cá thể trên cả thế giới; với cây là số cây; với giun là số cột).
- **Chưa khám phá:** bóng đen + gợi ý mờ (✅ 04 §3). Gợi ý cho slice:

  | Loài | Gợi ý |
  |------|-------|
  | Hoa dại | *"Gió sẽ mang tới một hạt có màu, khi đồng cỏ đủ dày…"* |
  | Mâm xôi | *"Một bụi gai có quả, cần đồng cỏ thật rộng…"* |
  | Giun | *"Thứ gì đó dưới đất, thích nơi có cỏ…"* |
  | Thỏ | *"Một sinh vật thích nơi có nhiều cỏ…"* |
  | Ong | *"Nó đi theo mùi hoa…"* |
  | Cáo | *"Nó theo dấu những đàn thỏ đông…"* |
  | Bèo · Lau sậy | *"Cần có nước…"* (lộ ra khi hồi sinh ao đầu tiên) |
  | Sen | *"Một bông hoa nổi trên mặt ao…"* |
  | Cá | *"Nó sống nơi mặt ao phủ kín bèo…"* |
  | Diệc | *"Đôi chân dài, đứng chờ bên ao nhiều cá…"* |

- Không có biểu đồ, không có bảng số liệu (để dành cho bản đầy đủ).

### 6.2 Tab Vùng đất
- Danh sách **14 vùng theo thứ tự từ trái sang phải**, mỗi dòng: biểu tượng loại vùng · tên · trạng thái (như bản đồ mini) · ngày hồi sinh (ngày chơi thứ mấy, không ghi ngày giờ thật).
- Vùng đã hồi sinh: click vào tên để **đổi tên** (tối đa 16 ký tự; ✅ Q16).
- Vùng chưa hồi sinh hiện *"Đất hoang"*. Khu Vườn Thiêng chưa mở hiện *"???"* với bóng cây khô.
- Click một dòng: khung nhìn trượt tới vùng đó.

### 6.3 Tab Khách ghé thăm
- Thẻ của khách lạ đã gặp (09 §3.2: Hươu sao, Rùa đầm), ghi lần đầu gặp ở vùng nào. Khách chưa gặp hiện bóng đen, không có gợi ý (giữ sự bất ngờ).

## 7. Thẻ thông tin sinh vật
Khi không cầm công cụ: **rê chuột** lên sinh vật hoặc cây trong 300 ms thì hiện một thẻ nhỏ phía trên nó. **Click** thì thẻ ghim lại 4 giây.

| Đối tượng | Dòng 1 | Dòng 2 (trạng thái, chọn một) |
|-----------|--------|-------------------------------|
| Động vật | Tên loài · biểu tượng vai trò | `no` · `đói` (độ no < 60) · `con non` · `già` |
| Cây | Tên loài | `đang lớn` · `khoẻ` · `khát` (máu < 60) · `ngủ khô` |
| Đất (cột trống) | Tên vùng | `ẩm` / `khô` · `màu mỡ` / `cằn` (theo ngưỡng của 07) |

Không hiện số (✅ 03 §3: không đặt tên cá thể; trọng tâm là quần thể).

## 8. Hiệu ứng thức dậy & đi ngủ (✅ 02)

### 8.1 Thức dậy (mỗi lần mở app)
Tổng ~5 giây, **không chặn thao tác**: người chơi click được ngay từ giây đầu.

| Thời điểm | Hình | Tiếng (theo âm lượng ambient, ✅ Q10) |
|-----------|------|---------------------------------------|
| 0–1 s | Dải đất hiện dần từ trong suốt, phủ một lớp **sương** trắng | Im lặng |
| 1–3 s | Sương tan dần từ giữa ra hai mép | Ambient tăng dần từ 0 tới mức đã chỉnh |
| 1.5 s | Tinh linh trên cành cây vươn vai, rồi bay lên | Một tiếng chim (chỉ ban ngày; ban đêm là tiếng dế) |
| 3–4 s | Nếu có **Sinh khí nghỉ ngơi** (✅ Q18, 08 §2): một vệt sáng bay từ tinh linh về khay, số Sinh khí đếm lên trong 1 giây | — |
| 4–5 s | Nếu **mùa đã đổi** từ lần mở trước: vài chiếc lá (Thu), bông tuyết (Đông), cánh hoa (Xuân) hoặc nắng loé (Hạ) rơi qua. Thế giới chuyển dần sang mùa mới trong vài phút đầu (✅ 02) | — |

- Không có bảng tóm tắt, không có chữ (✅ 02).
- **Lần mở đầu tiên của save mới:** cảnh mở đầu riêng. Sương dày hơn, dải đất xám, chỉ có 5 cỏ ở giữa; tinh linh thức dậy lần đầu và bay một vòng quanh mảnh xanh. Không có hướng dẫn bằng chữ; lời mời đầu tiên (Giun, sau ~0.5–1 giờ, 07 §1) là "bài học" đầu tiên.
- **Lúc 0:00 khi app đang chạy:** không có sương. Chỉ có vệt sáng nếu có Sinh khí nghỉ ngơi, và hiệu ứng đổi mùa.
- **Hiện lại từ menu bar / system tray:** không chạy hiệu ứng thức dậy, vì thế giới không ngủ khi bị ẩn.

### 8.2 Đi ngủ (khi thoát app)
- Lưu game **trước**, rồi chạy ~1 giây: tinh linh bay về cành, cuộn tròn ("z z z" nhỏ), dải đất mờ dần. Ambient giảm về 0.
- Thoát do tắt máy hoặc mất điện thì không có hiệu ứng. Game vẫn lưu định kỳ vài phút một lần (03 §8).

## 9. Cài đặt (tối giản)
Cửa sổ riêng như Sổ tay, 320 × 240 pt.

| Mục | Lựa chọn | Mặc định | Nguồn |
|-----|----------|----------|-------|
| Màn hình | Danh sách màn hình | Màn hình chính | ✅ Q9 |
| Khởi động cùng máy | Bật / tắt | Tắt (hỏi nhẹ một lần sau phiên đầu) | ✅ Q14 |
| Âm lượng ambient | 0–100 | 30 | ✅ Q10 |
| Âm lượng nhạc | 0–100 | 0 (tắt) | ✅ Q10 |
| Hiện gợi ý (bong bóng nhóm C) | Bật / tắt | Bật | 09 §8 |
| Chỉ báo ngoài màn hình | Bật / tắt | Bật | 09 §8 |
| Chế độ theo dõi | Bật / tắt | Tắt | ✅ Q12 |
| Ngôn ngữ | Tiếng Việt / English | Theo hệ điều hành | 💡 |

Câu hỏi "Khởi động cùng máy?" sau phiên đầu là một **bong bóng nhỏ trên khay**, không phải hộp thoại. Bỏ qua thì không hỏi lại.

## 10. Menu hệ thống (menu bar / system tray)
Biểu tượng tinh linh đơn sắc. Click để mở menu: **Hiện / Ẩn dải đất** · **Sổ tay** · **Cài đặt** · **Thoát**. Không có badge, không có thông báo hệ điều hành (✅ 09 §7).

## 11. Chữ, màu, chuyển động
- **Phông pixel có đủ dấu tiếng Việt**, cỡ 8pt hoặc 10pt ở tỉ lệ 2×. Cần chọn phông hỗ trợ cả dấu chồng (ặ, ổ, ữ…) trước khi làm UI thật.
- **Màu nhấn theo mùa** dùng chung cho viền khay, tinh linh và nút đang chọn: Xuân xanh lá · Hạ vàng · Thu cam · Đông trắng xanh (✅ 04 §0).
- **Định dạng số:** dấu phẩy ngăn nghìn trong khay mở rộng và sổ tay (`12,345`); rút gọn trong khay thu gọn (`12k`). Bộ ngăn cách theo ngôn ngữ chọn.
- **Chuyển động:** mở/đóng 150–250 ms, trượt khung nhìn 0.25–0.6 s. Mọi số đếm lên/xuống trong ≤ 1 giây.
- **Tần suất cập nhật UI:** 4 lần/giây là đủ (số Sinh khí, thanh cấp), để giữ ngân sách CPU (✅ 01).

## 12. Chế độ dev (không có trong bản phát hành)
Prototype hiện có các nút tốc độ ×1 / ×10 / ×60 (↻ trên nền nhịp ×100, [11 §1.3](11-nhip-va-tang-tan.md#13-khoảnh-khắc-và-ui)) và nút Thoát trên khay. Trong bản thật:
- **Tốc độ thời gian** chỉ có ở bản dev, mở bằng tổ hợp phím, hiện thành một hàng riêng phía trên khay.
- **Thoát** chuyển vào menu hệ thống (§10).

## 13. Kiểm chứng cần làm trong prototype
- **Khay:** 150 ms mở / 600 ms đóng có bị mở nhầm khi người chơi kéo chuột qua góc màn hình để vào Dock / taskbar không. Nếu có, tăng lên 300 ms hoặc chỉ mở khi chuột dừng hẳn.
- **Nút cuộn:** 16 × 48 pt có đủ dễ trúng không; có chặn click vào cửa sổ bên dưới ở mép màn hình không.
- **Mưa kéo 21 cột:** có cần nhiều hơn khi thế giới rộng không.
- **Gieo không nảy mầm vẫn mất tiền** (giá nhỏ, tỉ lệ hiện trước): có làm người chơi khó chịu không. Nếu có, hoàn lại một nửa.
- **Sổ tay 480 × 320 pt:** có đủ chỗ cho 12 thẻ + mô tả trên màn 13" không.
