# Hướng dẫn triển khai ứng dụng Plant Disease Detection lên Heroku

## Chuẩn bị

1. **Tạo tài khoản Heroku**
   - Đăng ký tài khoản tại [Heroku](https://signup.heroku.com/)
   - Xác nhận email và đặt mật khẩu

2. **Cài đặt công cụ cần thiết**
   - [Git](https://git-scm.com/downloads)
   - [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
   - [Python](https://www.python.org/downloads/) (đảm bảo đã cài đặt)

3. **Xác minh cài đặt**
   ```
   git --version
   heroku --version
   python --version
   ```

## Các bước triển khai

### Bước 1: Cài đặt các gói cần thiết
```
pip install gunicorn
cd "Flask Deployed App"
pip install -r requirements.txt
```

### Bước 2: Khởi tạo Git và commit code
```
git init
git add .
git commit -m "Initial commit for Heroku deployment"
```

### Bước 3: Đăng nhập vào Heroku
```
heroku login
```
(Một cửa sổ trình duyệt sẽ mở ra để bạn đăng nhập)

### Bước 4: Tạo ứng dụng Heroku
```
heroku create plant-disease-detector
```

### Bước 5: Cấu hình biến môi trường
```
heroku config:set GROQ_API_KEY=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
```

### Bước 6: Triển khai lên Heroku
```
git push heroku master
```

### Bước 7: Khởi động ứng dụng
```
heroku ps:scale web=1
```

### Bước 8: Mở ứng dụng trong trình duyệt
```
heroku open
```

## Xử lý sự cố

### 1. Lỗi khi push lên Heroku
Nếu gặp lỗi khi đẩy code lên Heroku, hãy thử các lệnh sau:
```
git push heroku main
```
hoặc
```
heroku git:remote -a your-app-name
git push heroku master
```

### 2. Xem log để tìm lỗi
```
heroku logs --tail
```

### 3. Lỗi liên quan đến kích thước model
Heroku có giới hạn slug size là 500MB. Nếu tổng kích thước quá lớn, bạn có thể:
- Sử dụng Git LFS để quản lý file lớn
- Lưu trữ model trên Google Drive hoặc AWS S3 và tải xuống khi cần

## Quản lý ứng dụng

### Khởi động lại ứng dụng
```
heroku restart
```

### Mở bảng điều khiển Heroku
```
heroku dashboard
```

### Xem thông tin ứng dụng
```
heroku info
```

## Lưu ý quan trọng

1. **Tệp model lớn**: File model AI (`plant_disease_model_1_latest.pt`) có kích thước lớn (~210MB), có thể gặp vấn đề khi triển khai.

2. **Các file tải lên**: Heroku không lưu trữ file vĩnh viễn, nên các ảnh người dùng tải lên sẽ bị mất khi ứng dụng khởi động lại.

3. **Thời gian ngủ**: Dyno miễn phí của Heroku sẽ "ngủ" sau 30 phút không hoạt động, khiến lần truy cập đầu tiên có thể chậm.

4. **Giới hạn tài nguyên**: Gói miễn phí có giới hạn bộ nhớ (512MB RAM), có thể không đủ cho model AI phức tạp.

5. **Phiên bản Python**: Heroku hỗ trợ Python 3.9.12 theo cấu hình trong `runtime.txt`.

## Nâng cấp và cải thiện

1. **Triển khai CD/CI**: Sử dụng GitHub Actions để tự động triển khai khi code được cập nhật.

2. **Nâng cấp dyno**: Chuyển lên gói trả phí để có nhiều tài nguyên hơn và không bị "ngủ".

3. **Lưu trữ file**: Tích hợp Amazon S3 hoặc Google Cloud Storage để lưu trữ ảnh người dùng tải lên.

4. **Giảm kích thước model**: Sử dụng các kỹ thuật nén hoặc lượng tử hóa để giảm kích thước model. 