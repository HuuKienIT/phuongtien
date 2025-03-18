import os
import subprocess
import psycopg2
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from ..config import get_settings

# Lấy thông tin cấu hình từ settings
settings = get_settings()
print(f"🔗 Kết nối database: {settings.DATABASE_URL}")

# Sử dụng create_async_engine thay vì create_engine
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Cấu hình session bất đồng bộ
AsyncSessionLocal = async_sessionmaker(bind=engine, autoflush=True, expire_on_commit=False, class_=AsyncSession)

async def create_database_if_not_exists():
    """Tạo database nếu chưa tồn tại."""
    try:
        print(f"📡 Kiểm tra database {settings.DB_NAME}...")

        # Kết nối với PostgreSQL mà không cần chỉ định database cụ thể
        conn = psycopg2.connect(
            dbname="postgres",
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Kiểm tra database có tồn tại không
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (settings.DB_NAME,))
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(f"CREATE DATABASE {settings.DB_NAME}")
            print(f"✅ Cơ sở dữ liệu '{settings.DB_NAME}' đã được tạo.")
        else:
            print(f"✅ Cơ sở dữ liệu '{settings.DB_NAME}' đã tồn tại.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Lỗi khi kiểm tra/tạo database: {e}")

# Đường dẫn đến Alembic
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ALEMBIC_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))

async def init_db():
    """Chạy Alembic migrations khi khởi động ứng dụng."""
    try:
        await create_database_if_not_exists()

        # Lấy thư mục gốc dự án từ vị trí của script hiện tại
        BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        ALEMBIC_INI_PATH = os.path.join(BASE_DIR, "alembic.ini")

        print(f"📂 BASE_DIR: {BASE_DIR}")
        print(f"📂 ALEMBIC_DIR: {ALEMBIC_DIR}")
        print(f"📂 ALEMBIC_INI_PATH: {ALEMBIC_INI_PATH}")

        # Kiểm tra tệp alembic.ini có tồn tại không
        if not os.path.exists(ALEMBIC_INI_PATH):
            print(f"⚠️ Không tìm thấy alembic.ini tại {ALEMBIC_INI_PATH}, bỏ qua migrations.")
        else:
            print("🔄 Đang chạy Alembic migrations...")
            subprocess.run(
                ["alembic", "-c", "alembic.ini", "upgrade", "head"],
                check=True,
                cwd=ALEMBIC_DIR
            )
        print("✅ Alembic migrations đã hoàn tất.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi chạy migrations: {e}")
    except Exception as e:
        print(f"❌ Lỗi không mong muốn khi chạy migrations: {e}")

# Dependency để lấy session bất đồng bộ
async def get_db():
    async with AsyncSessionLocal() as db:
        yield db
