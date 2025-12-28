from pydantic import BaseModel, EmailStr, field_serializer, ConfigDict
from datetime import datetime

# Mô hình Sản phẩm (Product Schemas)
class SanPhamCoBan(BaseModel):
    name: str
    code: str
    category: str
    sub_category: str | None = None
    gender: str

    description: str | None = None
    rental_price_day: float
    rental_price_week: float
    purchase_price: float
    image_url: str | None = None
    is_new: bool = False
    is_hot: bool = False
    # New detail fields
    fabric_type: str | None = None
    color: str | None = None
    recommended_size: str | None = None
    makeup_tone: str | None = None
    # Số lượng và hết hàng
    so_luong: int | None = 10
    het_hang: bool | None = False

class SanPhamTao(SanPhamCoBan):
    pass

class SanPhamCapNhat(BaseModel):
    name: str | None = None
    code: str | None = None
    category: str | None = None
    sub_category: str | None = None
    gender: str | None = None
    description: str | None = None
    rental_price_day: float | None = None
    rental_price_week: float | None = None
    purchase_price: float | None = None
    image_url: str | None = None
    is_new: bool | None = None
    is_hot: bool | None = None
    fabric_type: str | None = None
    color: str | None = None
    recommended_size: str | None = None
    makeup_tone: str | None = None
    so_luong: int | None = None
    het_hang: bool | None = None

class SanPham(SanPhamCoBan):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# Mô hình Chuyên gia (Expert Schemas)
class ChuyenGiaCoBan(BaseModel):
    name: str
    title: str
    bio: str | None = None
    years_experience: int
    brides_count: int
    specialties: list[str]
    image_url: str | None = None
    social_facebook: str | None = None
    social_instagram: str | None = None
    category: str = "makeup"
    level: str = "senior"
    location: str = "Hà Nội"
    price: float = 1000000
    is_top: bool = False

class ChuyenGiaTao(ChuyenGiaCoBan):
    pass

class ChuyenGia(ChuyenGiaCoBan):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# Mô hình Dịch vụ (Service Schemas)
class DichVuCoBan(BaseModel):
    name: str
    description: str | None = None
    features: list[str]
    price_from: float
    is_featured: bool = False
    icon: str | None = None

class DichVuTao(DichVuCoBan):
    pass

class DichVu(DichVuCoBan):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# Mô hình Liên hệ (Contact Schemas)
class LienHeTao(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    address: str | None = None # New field
    message: str

class LienHePhanHoi(BaseModel):
    message: str
    success: bool

class LienHe(BaseModel):
    id: int
    name: str
    email: str
    phone: str | None = None
    address: str | None = None # New field
    message: str
    created_at: str | None = None
    status: str = "pending"
    
    model_config = ConfigDict(from_attributes=True)

# Mô hình Banner (Banner Schemas)
class BannerCoBan(BaseModel):
    image_url: str
    title: str | None = None
    subtitle: str | None = None
    link: str | None = None
    is_active: bool = True
    order: int = 0

class BannerTao(BannerCoBan):
    pass

class Banner(BannerCoBan):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# Mô hình Giới thiệu
class GioiThieuCoBan(BaseModel):
    title: str
    subtitle: str
    description: str
    image_url: str | None = None
    stat1_number: str
    stat1_label: str
    stat2_number: str
    stat2_label: str
    stat3_number: str
    stat3_label: str

class GioiThieu(GioiThieuCoBan):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Mô hình Điểm nhấn trang chủ
class DiemNhanHomeCoBan(BaseModel):
    title: str
    description: str | None = None
    image_url: str | None = None
    order: int = 0

class DiemNhanHomeTao(DiemNhanHomeCoBan):
    pass

class DiemNhanHome(DiemNhanHomeCoBan):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Mô hình Thư viện (Gallery Schemas)
class ThuVienCoBan(BaseModel):
    image_url: str
    title: str | None = None
    order: int = 0

class ThuVienTao(ThuVienCoBan):
    pass

class ThuVien(ThuVienCoBan):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Mô hình Người dùng (User Schemas)
class NguoiDungCoBan(BaseModel):
    username: str # New field
    email: EmailStr | None = None # Now optional
    full_name: str | None = None
    phone: str | None = None # New field
    address: str | None = None # New field

class NguoiDungTao(NguoiDungCoBan):
    password: str

class NguoiDung(NguoiDungCoBan):
    id: int
    is_active: bool = True
    
    model_config = ConfigDict(from_attributes=True)

# Mô hình Chi tiết Giỏ hàng (Cart Item Schemas)
class ChiTietGioHangCoBan(BaseModel):
    product_id: int
    quantity: int

class ChiTietGioHang(ChiTietGioHangCoBan):
    id: int
    cart_id: int
    
    model_config = ConfigDict(from_attributes=True)

# Mô hình Giỏ hàng (Cart Schemas)
class GioHangCoBan(BaseModel):
    user_id: int | None = None

class GioHang(GioHangCoBan):
    id: int
    items: list[ChiTietGioHang] = []
    
    model_config = ConfigDict(from_attributes=True)

# Mô hình Chi tiết Đơn hàng (Order Item Schemas)
class ChiTietDonHangCoBan(BaseModel):
    product_id: int
    quantity: int
    price: float

class ChiTietDonHang(ChiTietDonHangCoBan):
    id: int
    order_id: int
    
    model_config = ConfigDict(from_attributes=True)

# Mô hình Đơn hàng (Order Schemas)
class DonHangCoBan(BaseModel):
    user_id: int | None = None
    customer_name: str
    customer_email: EmailStr
    customer_phone: str
    shipping_address: str
    total_amount: float
    status: str = "pending"

class DonHangTao(DonHangCoBan):
    cart_items: list[ChiTietGioHangCoBan]

class DonHang(DonHangCoBan):
    id: int
    order_date: str
    items: list[ChiTietDonHang] = []
    
    model_config = ConfigDict(from_attributes=True)

# Mô hình Đánh giá (Review Schemas)
class DanhGiaCoBan(BaseModel):
    product_id: int
    user_name: str
    rating: int
    comment: str | None = None
    image_url: str | None = None # Path to uploaded photo

class DanhGia(DanhGiaCoBan):
    id: int
    is_approved: bool = False # Current status
    created_at: datetime | None = None
    
    model_config = ConfigDict(from_attributes=True)

class NguoiDungCapNhat(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None
    password: str | None = None

class TinNhanChatCoBan(BaseModel):
    tin_nhan: str
    is_from_admin: bool = False

class TinNhanChatTao(TinNhanChatCoBan):
    pass

class TinNhanChat(TinNhanChatCoBan):
    id: int
    user_id: int
    thoi_gian: datetime
    model_config = ConfigDict(from_attributes=True)

class MaGiamGiaCoBan(BaseModel):
    ma_code: str
    phan_tram: float = 5.0
    ngay_het_han: datetime | None = None
    is_used: bool = False

class MaGiamGia(MaGiamGiaCoBan):
    id: int
    user_id: int | None = None
    model_config = ConfigDict(from_attributes=True)

# Khiếu nại (Complaints)
class KhieuNaiTao(BaseModel):
    title: str
    content: str
    customer_name: str | None = None
    customer_phone: str | None = None

class KhieuNai(BaseModel):
    id: int
    user_id: int | None = None
    customer_name: str | None = None
    customer_phone: str | None = None
    title: str
    content: str
    status: str
    admin_reply: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Hồ sơ Đối tác (Partner Application)
class HoSoDoiTacTao(BaseModel):
    partner_type: str
    full_name: str
    phone: str
    email: str
    experience: str | None = None
    portfolio_url: str | None = None
    cv_url: str | None = None

class HoSoDoiTac(BaseModel):
    id: int
    user_id: int
    partner_type: str
    full_name: str
    phone: str
    email: str
    experience: str | None = None
    portfolio_url: str | None = None
    cv_url: str | None = None
    status: str
    admin_reply: str | None = None
    contract_content: str | None = None
    created_at: str | None = None

    model_config = ConfigDict(from_attributes=True)

