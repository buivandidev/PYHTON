from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
import json
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ivie.db")

dong_co = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

PhienLamViec = sessionmaker(autocommit=False, autoflush=False, bind=dong_co)
CoSo = declarative_base()

# Database Models (Mô hình CSDL)
class SanPham(CoSo):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    category = Column(String, nullable=False)  # wedding_modern, traditional
    sub_category = Column(String) # flared, short, etc.
    gender = Column(String, nullable=False)  # male, female

    description = Column(Text)
    rental_price_day = Column(Float, nullable=False)
    rental_price_week = Column(Float, nullable=False)
    purchase_price = Column(Float, nullable=False)
    image_url = Column(String)
    is_new = Column(Boolean, default=False)
    is_hot = Column(Boolean, default=False)
    # New detail fields
    fabric_type = Column(String)
    color = Column(String)
    recommended_size = Column(Text)
    makeup_tone = Column(Text)
    # Số lượng và hết hàng
    so_luong = Column(Integer, default=10)
    het_hang = Column(Boolean, default=False)

class ChuyenGia(CoSo):
    __tablename__ = "experts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    title = Column(String, nullable=False)
    bio = Column(Text)
    years_experience = Column(Integer)
    brides_count = Column(Integer)
    specialties = Column(Text)  # JSON string
    image_url = Column(String)
    social_facebook = Column(String)
    social_instagram = Column(String)
    category = Column(String, default="makeup") # makeup, photo
    level = Column(String, default="senior") # senior, master, top_artist
    location = Column(String, default="Hà Nội")
    price = Column(Float, default=1000000)
    is_top = Column(Boolean, default=False)

class DichVu(CoSo):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    features = Column(Text)  # JSON string
    price_from = Column(Float, nullable=False)
    is_featured = Column(Boolean, default=False)
    icon = Column(String)

class Banner(CoSo):
    __tablename__ = "banners"
    
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=False)
    title = Column(String)
    subtitle = Column(String)
    link = Column(String)
    is_active = Column(Boolean, default=True)
    order = Column(Integer, default=0)

class GioiThieu(CoSo):
    __tablename__ = "about_us"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, default="Câu Chuyện Của IVIE")
    subtitle = Column(String, default="Hơn 10 năm kinh nghiệm trong lĩnh vực cưới hỏi")
    description = Column(Text)
    image_url = Column(String)
    stat1_number = Column(String, default="500+")
    stat1_label = Column(String, default="Cặp Đôi")
    stat2_number = Column(String, default="10+")
    stat2_label = Column(String, default="Năm Kinh Nghiệm")
    stat3_number = Column(String, default="100%")
    stat3_label = Column(String, default="Hài Lòng")

class DiemNhanHome(CoSo):
    __tablename__ = "home_highlights"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    image_url = Column(String)
    order = Column(Integer, default=0)

class ThuVien(CoSo):
    __tablename__ = "gallery"
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=False)
    title = Column(String)
    order = Column(Integer, default=0)

class LienHeGui(CoSo):
    __tablename__ = "contact_submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String)
    address = Column(String, nullable=True) # New field
    message = Column(Text, nullable=False)
    created_at = Column(String)
    status = Column(String, default="pending")

class NguoiDung(CoSo):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False) # New field
    email = Column(String, unique=True, index=True, nullable=True) # Now optional
    full_name = Column(String)
    phone = Column(String) # New field
    address = Column(String) # New field
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    orders = relationship("DonHang", back_populates="user")
    chat_messages = relationship("TinNhanChat", back_populates="user")
    coupons = relationship("MaGiamGia", back_populates="user")

class GioHang(CoSo):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    items = relationship("ChiTietGioHang", back_populates="cart")

class ChiTietGioHang(CoSo):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    
    cart = relationship("GioHang", back_populates="items")
    product = relationship("SanPham")

class DonHang(CoSo):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    customer_name = Column(String, nullable=False)
    customer_email = Column(String, nullable=False)
    customer_phone = Column(String, nullable=False)
    shipping_address = Column(Text, nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float, nullable=False)
    status = Column(String, default="pending") # pending, processing, shipped, delivered, cancelled
    
    user = relationship("NguoiDung", back_populates="orders")
    items = relationship("ChiTietDonHang", back_populates="order")

class ChiTietDonHang(CoSo):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False) # Price at the time of order
    
    order = relationship("DonHang", back_populates="items")
    product = relationship("SanPham")

class TinNhanChat(CoSo):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tin_nhan = Column(Text, nullable=False)
    thoi_gian = Column(DateTime, default=datetime.utcnow)
    is_from_admin = Column(Boolean, default=False)
    
    user = relationship("NguoiDung", back_populates="chat_messages")

class MaGiamGia(CoSo):
    __tablename__ = "coupons"
    id = Column(Integer, primary_key=True, index=True)
    ma_code = Column(String, unique=True, index=True, nullable=False)
    phan_tram = Column(Float, default=5.0)
    ngay_het_han = Column(DateTime, nullable=True)
    is_used = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Optional: tied to a specific user
    
    user = relationship("NguoiDung", back_populates="coupons")

class KhieuNai(CoSo):
    __tablename__ = "complaints"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    customer_name = Column(String)
    customer_phone = Column(String)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    status = Column(String, default="pending") # pending, resolved, closed
    admin_reply = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class HoSoDoiTac(CoSo):
    __tablename__ = "partner_applications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    partner_type = Column(String) # makeup, media (photo/video)
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    experience = Column(Text)
    portfolio_url = Column(String)
    cv_url = Column(String)
    status = Column(String, default="pending") # pending, rejected, interviewing, accepted
    admin_reply = Column(Text)
    contract_content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class DanhGia(CoSo):

    __tablename__ = "product_reviews"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    user_name = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    image_url = Column(String, nullable=True) # New field
    is_approved = Column(Boolean, default=False) # Moderation field
    created_at = Column(DateTime, default=datetime.utcnow)
    
    product = relationship("SanPham")

# Blog / Tin tức
class BaiViet(CoSo):
    __tablename__ = "blog_posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True)
    excerpt = Column(String) # Tóm tắt ngắn
    content = Column(Text, nullable=False)
    image_url = Column(String)
    category = Column(String, default="tips") # tips, news, wedding-story
    is_published = Column(Boolean, default=False)
    views = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Danh sách yêu thích
class YeuThich(CoSo):
    __tablename__ = "wishlists"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("NguoiDung")
    product = relationship("SanPham")


# Dependency
def lay_csdl():
    db = PhienLamViec()
    try:
        yield db
    finally:
        db.close()

# Create tables
def khoi_tao_csdl():
    CoSo.metadata.create_all(bind=dong_co)
