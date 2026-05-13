# Đồ án Caro AI (Nhóm 3 thành viên)

## Thành viên
- 23021335 - Nguyễn Tuấn Sơn  
- 23021359 - Nguyễn Văn Thắng
- 23021273 - Vũ Hữu Hoạt

## Giới thiệu
Chương trình chơi cờ Caro AI áp dụng thuật toán Minimax và Alpha-Beta Pruning.
- **Kích thước bàn cờ**: 9x9
- **Luật chơi**: 4 quân liên tiếp (ngang, dọc, chéo) là thắng. Không cần chặn 2 đầu.
- **Giao diện**: Pygame đồ họa đơn giản.

## Cài đặt thư viện
1. Cài đặt Python (phiên bản 3.x)
2. Mở terminal tại thư mục gốc, chạy lệnh:
```bash
pip install -r requirements.txt
```

## Cách chạy chương trình
1. **Chơi game với AI:**
Mở terminal, di chuyển vào thư mục `source_code` và chạy:
```bash
cd source_code
python main.py
```
> Trong `main.py`, bạn có thể thay đổi biến `depth` (độ sâu) hoặc `use_alpha_beta` (chọn thuật toán) để thử nghiệm các chế độ AI khác nhau.

2. **Chạy script kiểm thử hiệu năng (Benchmark):**
Chạy script để thấy bảng so sánh tốc độ giữa Minimax và Alpha-Beta:
```bash
cd source_code
python benchmark.py
```

## Các module chính
- `board.py`: Cài đặt mảng lưới cờ, logic sinh nước đi và kiểm tra thắng thua.
- `ai.py`: Cài đặt hai thuật toán Minimax và Alpha-beta pruning.
- `evaluate.py`: Cài đặt hàm heuristic đánh giá điểm của trạng thái bàn cờ dựa trên chuỗi quân (2, 3, 4 quân).
- `ui.py`: Cài đặt giao diện vẽ bàn cờ, theo dõi click chuột bằng Pygame.
- `benchmark.py`: Cài đặt 5 trạng thái cờ khác nhau để đo đạc và phân tích thời gian chạy, số trạng thái duyệt.
