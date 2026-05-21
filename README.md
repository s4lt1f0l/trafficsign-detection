# Hệ Thống Nhận Diện Biển Báo Giao Thông Việt Nam

Dự án này là một ứng dụng Học sâu (Deep Learning) dùng để phát hiện và phân loại các nhóm biển báo giao thông tại Việt Nam. Ứng dụng hỗ trợ giao diện web trực quan để người dùng tải ảnh và nhận kết quả dự đoán ngay lập tức.

## 1. Thành viên thực hiện
* **Đào Quốc Tuấn** - MSSV: 23120392
* **Nguyễn Lê Tân Tiến** - MSSV: 23120369

---

## 2. Các nhóm biển báo hỗ trợ
Hệ thống được huấn luyện để nhận diện **5 nhóm biển báo chính**:
1. **Biển báo cấm** (*Prohibitory*)
2. **Biển báo nguy hiểm** (*Danger*)
3. **Biển báo hiệu lệnh** (*Mandatory*)
4. **Biển báo chỉ dẫn** (*Information*)
5. **Biển báo phụ** (*Sub-sign*)

---

## 3. Kiến trúc và Hiệu năng
Dự án đã thực hiện thử nghiệm trên 3 kiến trúc: **YOLOv8**, **Faster R-CNN**, và **DETR**. Mô hình được chọn để triển khai thực tế là **YOLOv8** do ưu điểm vượt trội về tốc độ (12.36 ms/ảnh) và dung lượng cực nhẹ (~6 MB), phù hợp cho môi trường web.

---

## 4. Hướng dẫn Triển khai (Deployment)

### 4.1. Triển khai cục bộ (Local)
Yêu cầu: Python 3.9 trở lên.

1. **Cài đặt môi trường ảo và thư viện**:
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate

   pip install -r requirements.txt
   ```

2. **Chạy ứng dụng Web**:
   ```bash
   streamlit run web/app.py
   ```
   Sau đó truy cập địa chỉ: `http://localhost:8501`

### 4.2. Triển khai với Docker (Khuyên dùng)
Việc sử dụng Docker giúp đảm bảo ứng dụng chạy ổn định trên mọi môi trường.

1. **Xây dựng Image**:
   ```bash
   docker build -t trafficsign-app .
   ```

2. **Chạy Container**:
   ```bash
   docker run -p 8501:8501 trafficsign-app
   ```
   Ứng dụng sẽ khả dụng tại: `http://localhost:8501`

---

## 5. Cấu trúc thư mục
```text
TrafficSignProject/
├── web/app.py              # Ứng dụng giao diện Web (Streamlit)
├── weights/                # Chứa các tệp trọng số (YOLO, R-CNN, DETR)
├── models/dataset.py       # Xử lý dữ liệu
├── Dockerfile              # Cấu hình đóng gói Docker
├── .dockerignore           # Danh sách loại trừ khi build Docker
├── requirements.txt        # Danh sách thư viện đầy đủ
└── requirements-deploy.txt # Thư viện tối ưu cho môi trường deploy
```

---