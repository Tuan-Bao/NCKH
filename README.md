# Hệ Thống Điều Khiển Chuột, Cuộn Màn Hình Bằng Hướng Đầu

Hệ thống này cho phép người dùng điều khiển chuột trên máy tính và cuộng màn hình bằng cách sử dụng hướng đầu của họ thông qua webcam và nhận diện giọng nói. Backend được xây dựng bằng Flask, trong khi frontend sử dụng React.

## Cấu Trúc Dự Án

```
/backend
    ├── app.py                  # File chạy backend
    ├── requirements.txt        # Danh sách các thư viện cần thiết cho backend
    ├── estimator.py            # File thử xử lý các phép toán liên quan đến xác định hướng đầu
    └── headPoseEstimation.py   # File thử xử lý các phép toán liên quan đến xác định hướng đầu

/frontend
    ├── src/
    │   ├── App.jsx             # File chính của frontend
    │   └── ...                 # Các file khác của frontend
    ├── package.json            # Danh sách các thư viện cần thiết cho frontend
    └── vite.config.js          # Cấu hình cho Vite
```

## Cài Đặt

### Backend

1. **Cài đặt môi trường ảo python**
2. **Cài đặt các thư viện cần thiết**:

   ```
   pip install -r requirements.txt
   ```

3. **Chạy server**:
   ```
   flask run
   ```

### Frontend

1. **Cài đặt Node.js**: Đảm bảo bạn đã cài đặt Node.js.
2. **Cài đặt các thư viện cần thiết**:

   ```bash
   npm install
   ```

3. **Chạy ứng dụng**:
   ```bash
   npm run dev
   ```

## Sử Dụng

1. Mở trình duyệt và truy cập vào địa chỉ `http://localhost:5173` (hoặc cổng mà frontend đang chạy).
2. Cho phép truy cập webcam khi được yêu cầu.
3. Sử dụng giọng nói để điều khiển camera và chế độ hoạt động (cursor hoặc scroll).

## Công Nghệ Sử Dụng

- **Backend**: Flask, Flask-SocketIO, Mediapipe, OpenCV, PyAutoGUI
- **Frontend**: React, Vite

## Tính Năng

- Nhận diện hướng đầu và điều khiển chuột tương ứng.
- Hỗ trợ điều khiển bằng giọng nói.
- Giao tiếp thời gian thực giữa client và server.

## Ghi Chú

- Đảm bảo rằng webcam của bạn hoạt động tốt và có đủ ánh sáng để nhận diện chính xác.
- Hệ thống có thể cần điều chỉnh thêm để phù hợp với các điều kiện môi trường khác nhau.
