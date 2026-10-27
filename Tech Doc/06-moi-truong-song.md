# 06 · Môi trường sống (GDD 12) → code

> Nguồn: GDD [12 Môi trường sống](../GDD/12-moi-truong-song.md). Tham chiếu số: `Docs/GDD/sim/biomesim.py` (C# phải khớp thống kê với nó, như `World` khớp `worldsim.py` ở 05 §3.2). Mốc **M4c** (05 §1).

## 1. Dữ liệu (`balance.json`)
- Giữ nguyên mục `biomeModel` mà `biomesim.py` đọc; `Balance` (C#) đọc thêm mục này (`BiomeModelBalance`). Không chép số sang chỗ khác.
- `biomeModel.plants` (Dương xỉ) và `biomeModel.animals` (Sóc) được **nối vào** bảng loài của `World` sau các loài trong `plants` / `animals`, nên chỉ số loài cũ không đổi.
- `invites` không còn dùng trong C# (worldsim v1 vẫn đọc để so sánh luật cũ). `revive.*` chỉ còn `healthy` (ngưỡng Khoẻ cho kết game).

## 2. Mô phỏng (`LittleGod.Simulation`)

| Thành phần | Thay đổi |
|------------|----------|
| `Biome` (enum mới) | `None` (đất hoang), `Meadow`, `Forest`, `Pond` |
| `Column` | `Biome`, `Corridor` (biome đang lấn qua hành lang, `None` nếu không), `Dist[biome]` (khoảng cách tới cột sống gần nhất của biome đó, tính lại mỗi bước cùng `Canopy`) |
| `PlantSpecies` | `Biomes` (bit theo `Biome`; 0 = cây bờ, không theo biome), `Cover` (biome mà cỏ phủ này lan; `None` nếu không phải cỏ phủ) |
| `AnimalSpecies` | `Diet.Nuts` (Sóc: `NutTree`, `MinTrees`, `TreesPerAnimal`, `BuryRange`); `PreyAlso` (Cáo: Sóc) |
| `Zone.Alive` | Không lưu nữa: `true` khi có ít nhất một cột sống trong vùng |
| Bỏ | `Frontier`, `CanRevive`, `ReviveCost`, `ReviveDiscount`, `TryRevive`, `IsInvitable`, `InviteCost`, `TryInvite`, `GlobalRequirementMet`, `RevivalCount` (giữ trường để đọc save cũ) |
| `ReviveZone` | Chỉ còn dùng lúc tạo thế giới cho Khởi Nguyên |
| Mới | `Colonize(x, cover, moisture)`, `WakePonds()`, `BiomeFactor(sp, col)`, `MarkCorridor(x, cover)`, `BiomeHealth()`, `Filled`, `Arrived` (loài đã từng xuất hiện), `Ended` |

### 2.1 Thứ tự một bước (thêm vào 02 §2)
1. `Season`, `Weather`, `Canopy` **+ tính `Dist` cho 3 biome** (hai lượt quét, 144 × 3).
2. `Environment`, `Plants` (`Suitability` nhân `BiomeFactor`; hạt của cỏ phủ rơi xuống đất hoang → `Colonize` với xác suất `wastelandSprout × q(cột nguồn)`; Sồi có Sóc trong 6 cột thì rơi xa `buryRange`).
3. `Animals` (thú săn chọn mồi trong `Prey ∪ PreyAlso`; Sóc ăn hạt).
4. `Periodic` mỗi 30 phút: cập nhật biome cột (cỏ phủ trưởng thành), giun lan, **động vật tự đến theo `biomeModel.habitat`**, kiểm tra Vườn / kết game.
5. `Essence`, `Minute++`.

### 2.2 Đoạn biome
Đoạn = các cột **sống** liền nhau cùng `Biome` (nước là `Pond`). Đoạn dựng lại khi có cột đổi biome hoặc được lấn (`regionsDirty`). Sức khoẻ vùng (08 §5.3) lấy trung bình vai trò và cân bằng của **mọi đoạn có cột trong vùng**, theo số cột. Sức khoẻ biome (GDD 12 §5) = trung bình theo cột của Sức khoẻ từng đoạn cùng biome.

### 2.3 Lệnh
- `TryPlant`: gieo được trên đất hoang cách cột sống ≤ `sowRangeOnWasteland` (cột được lấn ngay với ẩm `sownWastelandMoisture`); gieo **cỏ phủ** của biome A trong biome B cách cột A ≤ `corridorRange` thì đánh dấu hành lang A trên các cột giữa.
- `TryRain`: mưa được trong dải `[L, R]` như cũ (gồm cả cột đất hoang xen giữa).
- Bỏ `InviteCommand`, `ReviveCommand`.

## 3. Phiên chơi & lưu (`LittleGod.Game`)
- `SaveVersion` 3: `ColumnState` thêm `biome`, `corridor`; `WorldState` thêm `arrived`, `filled`, `ended`. Đọc save v1, v2: cột sống trên đất → `Meadow`, cột nước sống → `Pond`, `arrived` = các loài động vật đang có.
- `GameBalance.Moments.Discover`: luật thêm `needsBiome`; thêm Dương xỉ, đổi ngưỡng Sồi, Táo dại (GDD 12 §4).

## 4. Hiển thị & UI
- Khay: bỏ nút 💌 / 🌿 và chấm báo đi kèm.
- Bản đồ mini: mỗi cột tô theo biome (đồng cỏ xanh lá, rừng xanh đậm, ao xanh lam, đất hoang nâu xám, Vườn vàng khi chưa mở); bỏ vạch "hồi sinh được".
- Công cụ Gieo: xem trước dùng `CanGrowAt` mới (đất hoang ≤ 5 ô, hệ số biome); tỉ lệ nảy mầm hiển thị đã nhân hệ số biome.
- Sprite mới vẽ bằng code: Dương xỉ (tầng thảm, lá xẻ), Sóc (nâu đỏ, đuôi xù).
- Thẻ thông tin đất: dòng thứ hai là tên biome (hoặc "Đất hoang").
- Bảng chữ: `species.fern`, `species.squirrel`, `biome.*`, `moment.newSpecies`.

## 5. Kiểm thử
- Luật nhỏ, tất định: hệ số biome (× 1 / × 0.5 giáp ranh / × 0 sâu / cỏ phủ tối thiểu × 0.5); lấn đất hoang; ao thức dậy kèm bờ bên kia; hành lang; Sóc ăn hạt và chôn hạt; cáo bắt sóc; động vật tự đến đúng điều kiện (thỏ cần chỗ trốn, không đến mùa Đông); Vườn mở theo GDD 12 §5.
- Thống kê (`WorldStatsTests`, 10 seed, `SliceRunner` bắt chước người chơi mô hình của `biomesim.py`): kết game, phủ kín, lần đầu xuất hiện các loài, trong biên rộng quanh số của GDD 12 §7.
- Lưu–đọc tất định với cột biome, hành lang; save mẫu v1 vẫn đọc được.

## 6. Kết quả M4c (2026-10-24)
- 68 EditMode (+1 Explicit) và 3 PlayMode (+1 Explicit chụp hình) xanh; build macOS thường và Dev thành công. Một bước mô phỏng 0.135 ms trên thế giới phủ kín.
- `WorldStatsTests` (10 seed, C#) so với `biomesim.py` (8 seed):

| Chỉ số | `biomesim.py` | Biên | C# `World` |
|--------|---------------|------|------------|
| Kết game (người chơi ghé 3 phút) | 7/8 seed, trung vị 1.1 giờ thật (0.6–3.0) | ≥ 7/10, trung vị 0.5–2.5 | 10/10, 0.6–3.0, trung vị ~1.1 |
| Đất hoang phủ kín | 0.4–1.1 giờ thật | trung vị 0.2–1.5 | 0.5–1.1 |
| Không người chơi phủ kín | 0.9–2.3 giờ thật | ≥ 7/10 seed | 10/10, 0.7–2.2 |
| Sóc đến | 0.6–2.9 giờ thật | ≥ 7/10 seed | 10/10, 0.5–2.4 |
| Không người chơi | không ong, cáo, sóc, không kết | đúng như vậy | đúng như vậy |
| Thỏ / cá trung bình | 20–42 / 19–23 | 12–60 / 10–30 | 20–52 / 21–23 |

- Khác Tech Doc dự kiến: thời gian chờ "tự đến" dùng chung `arrivalTimers` (khoá = biome × 100 + vùng giữa đoạn, ao: 300 + vùng); khoá cũ trong save v1, v2 vô hại. `Zone.Alive` vẫn lưu cho tương thích nhưng được tính lại từ cột khi đọc save.
- UI: nút 💌 / 🌿 còn trong prefab nhưng luôn ẩn (chờ khoảnh khắc ✨ ở M5 dùng chấm báo).
