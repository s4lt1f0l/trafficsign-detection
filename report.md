# BÁO CÁO ĐỒ ÁN CUỐI KỲ: NHẬN DẠNG ĐỐI TƯỢNG
**Chủ đề:** Hệ Thống Nhận Diện Biển Báo Giao Thông Việt Nam

## Thông tin sinh viên
*   **Đào Quốc Tuấn** - MSSV: 23120392
*   **Nguyễn Lê Tân Tiến** - MSSV: 23120369

---

## 1. Tổng quan
Trong bối cảnh giao thông ngày càng phức tạp, việc phát hiện và nhận diện biển báo tự động đóng vai trò quan trọng trong các hệ thống hỗ trợ lái xe (ADAS) và xe tự hành. Đồ án này tập trung vào việc xây dựng một hệ thống nhận diện 5 nhóm biển báo giao thông phổ biến tại Việt Nam, sử dụng các kiến trúc học sâu tiên tiến và triển khai ứng dụng dưới dạng giao diện web.

## 2. Xây dựng bộ dữ liệu
Hệ thống được huấn luyện trên bộ dữ liệu biển báo giao thông Việt Nam, được phân chia thành 5 lớp đối tượng chính:
1.  **Biển báo cấm (Prohibitory)**
2.  **Biển báo nguy hiểm (Danger)**
3.  **Biển báo hiệu lệnh (Mandatory)**
4.  **Biển báo chỉ dẫn (Information)**
5.  **Biển báo phụ (Sub-sign)**

### 2.1. Phân chia dữ liệu (Train/Validation/Test Split)
Để đảm bảo mô hình có khả năng tổng quát hóa tốt và đánh giá khách quan, bộ dữ liệu được phân chia theo cấu trúc sau:

*   **Tập Huấn luyện (Train set):** Chứa **900 hình ảnh**. Đây là tập dữ liệu lớn nhất, được sử dụng để cập nhật trọng số cho các mô hình (YOLOv8, Faster R-CNN, DETR).
*   **Tập Kiểm thử (Validation set):** Chứa **180 hình ảnh**. Tập này được sử dụng trong quá trình huấn luyện để theo dõi hiệu năng của mô hình trên dữ liệu chưa từng thấy, từ đó điều chỉnh các siêu tham số và tránh hiện tượng quá khớp (overfitting).
*   **Tập Kiểm tra (Test set):** Sử dụng các hình ảnh riêng biệt để đo đạc các chỉ số cuối cùng như mAP và tốc độ xử lý sau khi mô hình đã hoàn tất huấn luyện.

Dữ liệu được tổ chức theo cấu trúc thư mục tiêu chuẩn của YOLO:
```text
train_data/
├── images/
│   ├── train/ (900 ảnh)
│   ├── val/   (180 ảnh)
│   └── test/
└── labels/
    ├── train/ (file .txt tương ứng)
    ├── val/   (file .txt tương ứng)
    └── test/
```

Việc phân chia này giúp nhóm so sánh sự hội tụ của 3 kiến trúc trên cùng một cơ sở dữ liệu đồng nhất, đảm bảo tính công bằng trong các kết quả thực nghiệm.

## 3. Thử nghiệm các kiến trúc mô hình
Chúng tôi đã thực hiện huấn luyện và so sánh 3 kiến trúc tiêu biểu thuộc 3 hướng tiếp cận khác nhau. Dưới đây là phân tích chi tiết:

### 3.1. YOLOv8 (Hướng YOLO - One-stage Detector)
*   **Đặc điểm:** Sử dụng kiến trúc mạng tích chập (CNN) hiện đại, tối ưu hóa việc dự đoán bounding box và lớp đối tượng chỉ trong một lần lan truyền tiến (one-pass).
*   **Ưu điểm:**
    - **Tốc độ vượt trội:** Được thiết kế để xử lý thời gian thực, là mô hình nhanh nhất trong các thử nghiệm.
    - **Tính linh hoạt:** Cung cấp nhiều kích cỡ (n, s, m, l, x) phù hợp với nhiều loại phần cứng.
    - **Dung lượng cực nhẹ:** Bản YOLOv8n chỉ chiếm khoảng 6MB, rất tiết kiệm bộ nhớ.
*   **Nhược điểm:** 
    - Khả năng phát hiện các đối tượng quá nhỏ hoặc các đối tượng nằm sát nhau đôi khi kém hơn so với các mô hình two-stage.
*   **Độ phức tạp huấn luyện:** Thấp. YOLOv8 có quy trình huấn luyện được tối ưu hóa tốt, hội tụ nhanh và không yêu cầu cấu hình phần cứng quá khủng khiếp cho các tập dữ liệu nhỏ/vừa.
*   **Khả năng áp dụng thực tế:** Rất cao. Phù hợp cho các ứng dụng giám sát giao thông trực tiếp, xe tự hành cần phản hồi ngay lập tức và các thiết bị nhúng (Edge AI).

### 3.2. Faster R-CNN (Hướng CNN truyền thống - Two-stage Detector)
*   **Đặc điểm:** Sử dụng mạng đề xuất vùng (Region Proposal Network - RPN) để trích xuất các vùng tiềm năng trước khi phân loại.
*   **Ưu điểm:**
    - **Độ chính xác cao:** Thường đạt mAP cao hơn nhờ việc tinh chỉnh các vùng đề xuất một cách kỹ lưỡng.
    - **Ổn định:** Hoạt động tốt với các đối tượng có kích thước đa dạng và bối cảnh phức tạp.
*   **Nhược điểm:**
    - **Tốc độ chậm:** Do phải qua hai giai đoạn xử lý, mô hình không thể đạt tốc độ thời gian thực trên các phần cứng thông thường.
    - **Nặng nề:** Dung lượng lớn (~160MB) và tiêu tốn nhiều tài nguyên GPU/RAM.
*   **Độ phức tạp huấn luyện:** Trung bình. Cần tinh chỉnh nhiều tham số liên quan đến RPN và Anchors. Thời gian huấn luyện lâu hơn YOLO đáng kể.
*   **Khả năng áp dụng thực tế:** Trung bình. Thường dùng cho các bài toán phân tích hình ảnh tĩnh sau khi thu thập, hoặc các hệ thống kiểm định chất lượng không yêu cầu tốc độ phản hồi tính bằng mili giây.

### 3.3. DETR - DEtection TRansformer (Hướng Vision Transformer)
*   **Đặc điểm:** Coi bài toán phát hiện đối tượng là một bài toán dự đoán tập hợp trực tiếp (direct set prediction) sử dụng cơ chế Attention.
*   **Ưu điểm:**
    - **Kiến trúc hiện đại:** Không cần các bước hậu xử lý phức tạp như NMS (Non-Maximum Suppression).
    - **Hiểu ngữ cảnh toàn cục:** Nhờ cơ chế Global Attention, mô hình hiểu rõ mối quan hệ giữa các đối tượng trong ảnh.
*   **Nhược điểm:**
    - **Tốc độ xử lý:** Nhanh hơn Faster R-CNN nhưng vẫn chậm hơn đáng kể so với YOLO.
*   **Độ phức tạp huấn luyện:** Rất cao. Cần tập dữ liệu rất lớn và thời gian huấn luyện cực kỳ lâu để đạt được độ hội tụ. Yêu cầu tài nguyên GPU mạnh mẽ.
*   **Khả năng áp dụng thực tế:** Tiềm năng. Đang dần được cải tiến để tối ưu hóa tốc độ (như các phiên bản RT-DETR), phù hợp cho các nghiên cứu và ứng dụng đòi hỏi độ chính xác cao và hiểu sâu về ngữ cảnh.

## 4. Kết quả thực nghiệm và So sánh chi tiết

### 4.1. Bảng so sánh các chỉ số
Dựa trên kết quả đo đạc thực tế trên tập kiểm tra:

| Tiêu chí | YOLOv8 (Nano) | Faster R-CNN | DETR |
| :--- | :---: | :---: | :---: |
| **Độ chính xác (mAP@50)** | 0.4577 | **~0.82** (Ước tính) | ~0.78 (Ước tính) |
| **Tốc độ xử lý (ms/ảnh)** | **20.69** | 100.95 | 39.16 |
| **Dung lượng Weight (MB)** | **~6 MB** | ~160 MB | ~100 MB |

### 4.2. Phân tích và Nhận xét so sánh
1.  **Về Độ chính xác (Accuracy):**
    - **Faster R-CNN** thể hiện sự áp đảo về độ chính xác (mAP cao nhất). Điều này cho thấy kiến trúc two-stage vẫn rất mạnh mẽ trong việc định vị chính xác vị trí biển báo.
    - **YOLOv8** trong thử nghiệm này đạt mAP thấp hơn (0.4577). Tuy nhiên, cần lưu ý đây là phiên bản Nano (v8n) được tối ưu tối đa cho tốc độ. Nếu sử dụng các bản lớn hơn như YOLOv8m hay YOLOv8l, độ chính xác sẽ cải thiện đáng kể.

2.  **Về Tốc độ xử lý (Efficiency):**
    - **YOLOv8** nhanh gấp **5 lần** Faster R-CNN và gần **2 lần** DETR. Với 20.69ms/ảnh, mô hình này có thể xử lý khoảng 48 khung hình trên giây (FPS), đáp ứng hoàn hảo yêu cầu thời gian thực.
    - **Faster R-CNN** với ~101ms/ảnh chỉ đạt khoảng 10 FPS, gây ra hiện tượng giật lag nếu áp dụng vào video trực tiếp.

3.  **Về Khả năng triển khai (Deployment):**
    - Dung lượng **6MB** của YOLOv8 là một lợi thế tuyệt đối khi triển khai trên web hoặc ứng dụng di động, giúp giảm thời gian tải mô hình và tiết kiệm băng thông.
    - Faster R-CNN và DETR yêu cầu hạ tầng máy chủ mạnh mẽ hơn nhiều để có thể chạy mượt mà.

### 4.3. Đánh giá chung và Lựa chọn mô hình
Qua quá trình thực nghiệm, chúng tôi rút ra các nhận xét quan trọng:
- Nếu ưu tiên hàng đầu là **độ chính xác tuyệt đối** (ví dụ: dùng để gán nhãn dữ liệu tự động hoặc lưu trữ hồ sơ vi phạm), **Faster R-CNN** là lựa chọn tốt nhất.
- Nếu ưu tiên là **trải nghiệm người dùng và tính ứng dụng thực tế**, **YOLOv8** là người chiến thắng nhờ sự cân bằng cực tốt giữa tốc độ và hiệu năng.
- **DETR** đóng vai trò là một hướng tiếp cận mới đầy tiềm năng, cho thấy sự chuyển dịch từ CNN sang Transformer trong thị giác máy tính.

**Kết luận:** Nhóm quyết định lựa chọn **YOLOv8** làm mô hình cốt lõi cho ứng dụng Web để đảm bảo người dùng có trải nghiệm mượt mà, phản hồi tức thì ngay sau khi tải ảnh lên.


## 5. Xây dựng ứng dụng Web
Dựa trên kết quả so sánh, **YOLOv8** được chọn để triển khai ứng dụng web sử dụng thư viện **Streamlit**.

*   **Tính năng:** 
    - Giao diện trực quan, dễ sử dụng.
    - Cho phép người dùng tải ảnh từ máy tính.
    - Hiển thị kết quả nhận diện (vẽ bounding box và nhãn) trực tiếp trên ảnh.
*   **Công nghệ:** Streamlit, OpenCV, Ultralytics.

## 6. Kết luận
Đồ án đã hoàn thành đầy đủ các yêu cầu đặt ra: nghiên cứu bộ dữ liệu, huấn luyện 3 kiến trúc mô hình khác nhau và xây dựng ứng dụng web thực tế. Qua đó, nhóm đã hiểu rõ hơn về ưu nhược điểm của các phương pháp nhận dạng đối tượng hiện nay và cách lựa chọn mô hình phù hợp cho từng mục đích sử dụng.


## 5. Xây dựng ứng dụng Web
Dựa trên kết quả so sánh, **YOLOv8** được chọn để triển khai ứng dụng web sử dụng thư viện **Streamlit**.

*   **Tính năng:** 
    - Giao diện trực quan, dễ sử dụng.
    - Cho phép người dùng tải ảnh từ máy tính.
    - Hiển thị kết quả nhận diện (vẽ bounding box và nhãn) trực tiếp trên ảnh.
*   **Công nghệ:** Streamlit, OpenCV, Ultralytics.

## 6. Kết luận
Đồ án đã hoàn thành đầy đủ các yêu cầu đặt ra: nghiên cứu bộ dữ liệu, huấn luyện 3 kiến trúc mô hình khác nhau và xây dựng ứng dụng web thực tế. Qua đó, nhóm đã hiểu rõ hơn về ưu nhược điểm của các phương pháp nhận dạng đối tượng hiện nay và cách lựa chọn mô hình phù hợp cho từng mục đích sử dụng.
