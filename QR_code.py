import qrcode
import requests
import os

UPLOAD_URL = "http://127.0.0.1:8000/cloudinary/upload/"


def generate_qr_code(vehicle_id, save_dir="qr_codes"):
    """Tạo mã QR code từ vehicle_id và lưu ảnh vào thư mục"""
    qr_content = f"vehicle_id:{vehicle_id}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(qr_content)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")

    # Tạo thư mục lưu QR code
    os.makedirs(save_dir, exist_ok=True)

    file_path = os.path.join(save_dir, f"vehicle_{vehicle_id}.png")
    img.save(file_path)

    return file_path


def upload_qr_code(file_path):
    """Tải lên Cloudinary và trả về URL"""
    with open(file_path, "rb") as file:
        response = requests.post(UPLOAD_URL, files={"file": file})

    if response.status_code == 200:
        return response.json()  # Giả sử API trả về URL dưới dạng JSON
    return None


def generate_and_upload_qr_codes():
    """Tạo 100 mã QR, tải lên và lưu URL"""
    qr_code_urls = {}

    for vehicle_id in range(1, 101):
        file_path = generate_qr_code(vehicle_id)
        qr_url = upload_qr_code(file_path)

        if qr_url:
            qr_code_urls[vehicle_id] = qr_url
            print(f"Uploaded QR for Vehicle {vehicle_id}: {qr_url}")
        else:
            print(f"Failed to upload QR for Vehicle {vehicle_id}")

    return qr_code_urls


# Chạy chương trình
qr_code_links = generate_and_upload_qr_codes()

# In ra danh sách URL
print(qr_code_links)
