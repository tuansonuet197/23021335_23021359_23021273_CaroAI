# Bài Tập Lớn Giữa Kì Caro AI (Nhóm 3 thành viên)

Dự án phát triển Game cờ Caro 9×9 tích hợp trí tuệ nhân tạo (AI) sử dụng thuật toán **Minimax** kết hợp **Alpha-Beta Pruning** cực mạnh, được viết bằng ngôn ngữ Python với giao diện Pygame.

##  Thành viên nhóm
- 23021335 - Nguyễn Tuấn Sơn
- 23021359 - Nguyễn Văn Thắng
- 23021273 - Vũ Hữu Hoạt

---

##  Luật chơi

- Bàn cờ tiêu chuẩn: **9×9**
- Điều kiện thắng: Đạt **4 quân liên tiếp** (ngang, dọc, chéo).
- **Đặc biệt:** Không áp dụng luật chặn 2 đầu.

---

## ⚙️ Cài đặt & Cách chạy

### Yêu cầu hệ thống
- Python **3.10** trở lên.
- Các thư viện phụ thuộc trong file `requirements.txt`.

### Bước 1: Cài đặt thư viện
Mở terminal tại thư mục gốc của dự án, chạy lệnh:
```bash
pip install -r requirements.txt
```

### Bước 2: Chạy game
Di chuyển vào thư mục `source_code` và khởi chạy file `main.py`:
```bash
cd source_code
python main.py
```
> **Mẹo:** Trong `main.py`, bạn có thể trực tiếp thay đổi tham số `depth` (độ sâu tìm kiếm) hoặc cờ `use_alpha_beta` để kiểm nghiệm sức mạnh của từng thuật toán.

---

## 🔬 Benchmark hiệu năng AI

Hệ thống được tích hợp sẵn một script kiểm thử hiệu năng. Kịch bản này mô phỏng 5 trạng thái bàn cờ khác nhau (từ dễ đến cực khó) để so sánh tốc độ và khả năng cắt tỉa nhánh của Minimax so với Alpha-Beta Pruning.

```bash
cd source_code
python benchmark.py
```

Nhờ việc tối ưu hóa **Transposition Table (Bộ nhớ đệm với cờ Toán học)** và kỹ thuật **Move Ordering (Ray Casting)** đếm chuỗi, số lượng nhánh phải duyệt của Alpha-Beta được giảm đến **hơn 75%** so với Minimax ở các thế cờ phức tạp, giúp tốc độ phản hồi chỉ còn ~1 giây cho độ sâu D=4.

---

##  Phân tích thuật toán AI

### Thuật toán Minimax
- Duyệt toàn bộ cây trò chơi không cắt nhánh để tìm nước đi tốt nhất.
- Độ phức tạp thời gian: $O(b^d)$ (với b là số nhánh trung bình, d là độ sâu).
- Vai trò: Dùng làm Baseline chuẩn xác để so sánh.

### Alpha-Beta Pruning & Cải tiến
1. **Cắt nhánh (Pruning):** Giảm tải các phép toán không cần thiết bằng cách đánh giá các ngưỡng Alpha (cận dưới) và Beta (cận trên).
2. **Transposition Table:** 
   - Mã hóa trạng thái bàn cờ siêu tốc ($O(N)$) và lưu các giá trị với cờ `EXACT`, `LOWER` và `UPPER`. Điều này ngăn việc AI duyệt lại các nhánh đã tính một cách toán học chuẩn xác.
3. **Move Ordering:**
   - Dùng kỹ thuật Ray Casting phát tia từ vị trí định đánh ra 4 hướng để đếm chuỗi.
   - Nhận diện cực sớm các thế cờ nguy hiểm của địch (ví dụ: Địch có 3 quân $\rightarrow$ gán trọng số khẩn cấp $+5000$).
   - AI sẽ luôn ưu tiên phòng thủ các nhánh chết người này đầu tiên, giúp lượng nhánh cắt tỉa tăng vọt.

### Hàm Heuristic đánh giá
Chương trình ứng dụng kỹ thuật *Sliding Window* 5 ô để phát hiện các thế cờ (Live 3, Dead 3, Open 2...). Điểm phạt phòng ngự luôn lớn hơn điểm thưởng tấn công, giúp AI thi đấu chắc chắn và luôn bẻ gãy đòn đánh của bạn trước.

---

##  Cấu trúc dự án

```text
├── README.md              # Giới thiệu dự án
├── requirements.txt       # Danh sách thư viện Python
├── report/                # Chứa báo cáo LaTeX và file PDF hoàn thiện
│   ├── main.tex
│   └── main.pdf
└── source_code/
    ├── main.py            # File chạy chính kết nối Game loop
    ├── ui.py              # Xử lý giao diện đồ hoạ, bắt sự kiện click với Pygame
    ├── board.py           # Quản lý logic bàn cờ, thắng thua, sinh nước đi
    ├── evaluate.py        # Hàm Heuristic đánh giá trạng thái và Ray Casting
    ├── ai.py              # Lõi AI chứa Minimax và Alpha-Beta Search
    └── benchmark.py       # Script so sánh hiệu suất AI
```
