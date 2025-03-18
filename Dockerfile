# Sử dụng Python 3.11 làm base image
FROM python:3.11

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép các tệp yêu cầu vào container
COPY requirements.txt .

# Cài đặt thư viện từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Mở cổng 10000
EXPOSE 10000

# Chạy ứng dụng FastAPI bằng Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
