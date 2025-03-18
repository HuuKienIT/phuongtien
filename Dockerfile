# Dockerfile cho user-service
FROM python:3.11-slim

# Thiết lập thư mục làm việc
WORKDIR /phuongtien

# Cài đặt libpq-dev để hỗ trợ psycopg2
# RUN apt-get update && apt-get install -y libpq-dev gcc
# RUN apt-get update && apt-get install -y curl
# Sao chép requirements.txt vào thư mục làm việc
COPY requirements.txt ./

# Cài đặt các thư viện từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào thư mục làm việc
COPY . .

# Chạy ứng dụng
CMD ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "5000"]

