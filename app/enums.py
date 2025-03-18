import enum

class StationStatusEnum(str, enum.Enum):
    OPERATIONAL = "operational"  # Trạm hoạt động bình thường
    MAINTENANCE = "maintenance"  # Đang bảo trì
    CLOSED = "closed"            # Đóng cửa

class VehicleStatusEnum(str, enum.Enum):
    AVAILABLE = "available"       # Xe sẵn sàng
    IN_USE = "in_use"             # Xe đang được thuê
    MAINTENANCE = "maintenance"   # Xe đang bảo trì
    DAMAGED = "damaged"           # Xe bị hỏng
    INACTIVE = "inactive"         # Xe ngừng hoạt động

class ChargingStatusEnum(str, enum.Enum):
    CHARGING = "charging"          # Đang sạc
    FULLY_CHARGED = "fully_charged"  # Đã sạc đầy
    NOT_CHARGING = "not_charging"    # Không sạc

class InsuranceStatusEnum(str, enum.Enum):
    ACTIVE = "active"     # Bảo hiểm còn hiệu lực
    EXPIRED = "expired"   # Bảo hiểm hết hạn
    CANCELED = "canceled" # Bảo hiểm đã hủy

class MaintenanceStatusEnum(str, enum.Enum):
    SCHEDULED = "scheduled"    # Đã lên lịch bảo trì
    IN_PROGRESS = "in_progress"  # Đang bảo trì
    COMPLETED = "completed"    # Bảo trì hoàn thành
    CANCELED = "canceled"      # Bảo trì bị hủy

class RegistrationStatusEnum(str, enum.Enum):
    ACTIVE = "active"      # Đăng ký còn hiệu lực
    EXPIRED = "expired"    # Đăng ký đã hết hạn
    PENDING = "pending"    # Đang chờ phê duyệt
    CANCELED = "canceled"  # Đăng ký bị hủy bỏ