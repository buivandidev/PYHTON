"""
Pydantic Schemas cho PostgreSQL API - IVIE Studio
"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ============ SẢN PHẨM ============
class SanPhamCoSo(BaseModel):
    ten: str
    ma: str
    danh_muc: str
    danh_muc_phu: Optional[str] = None
    gioi_tinh: str
    mo_ta: Optional[str] = None
    gia_thue_ngay: float
    gia_thue_tuan: float
    gia_mua: float
    anh_url: Optional[str] = None
    la_moi: bool = False
    la_hot: bool = False
    chat_lieu: Optional[str] = None
    mau_sac: Optional[str] = None
    kich_thuoc: Optional[str] = None
    tong_trang_diem: Optional[str] = None


class SanPhamTao(SanPhamCoSo):
    pass


class SanPhamCapNhat(BaseModel):
    ten: Optional[str] = None
    danh_muc: Optional[str] = None
    danh_muc_phu: Optional[str] = None
    gioi_tinh: Optional[str] = None
    mo_ta: Optional[str] = None
    gia_thue_ngay: Optional[float] = None
    gia_thue_tuan: Optional[float] = None
    gia_mua: Optional[float] = None
    anh_url: Optional[str] = None
    la_moi: Optional[bool] = None
    la_hot: Optional[bool] = None
    chat_lieu: Optional[str] = None
    mau_sac: Optional[str] = None
    kich_thuoc: Optional[str] = None
    tong_trang_diem: Optional[str] = None


class SanPhamPhanHoi(SanPhamCoSo):
    id: int
    ngay_tao: datetime

    class Config:
        from_attributes = True


# ============ NGƯỜI DÙNG ============
class NguoiDungCoSo(BaseModel):
    ten_dang_nhap: str
    email: Optional[str] = None
    ho_ten: Optional[str] = None
    dien_thoai: Optional[str] = None
    dia_chi: Optional[str] = None


class NguoiDungTao(NguoiDungCoSo):
    mat_khau: str


class NguoiDungCapNhat(BaseModel):
    email: Optional[str] = None
    ho_ten: Optional[str] = None
    dien_thoai: Optional[str] = None
    dia_chi: Optional[str] = None
    hoat_dong: Optional[bool] = None


class NguoiDungPhanHoi(NguoiDungCoSo):
    id: int
    hoat_dong: bool
    ngay_tao: datetime

    class Config:
        from_attributes = True


# ============ ĐƠN HÀNG ============
class DonHangCoSo(BaseModel):
    ten_khach: str
    email_khach: str
    dien_thoai_khach: str
    dia_chi_giao: str
    tong_tien: float


class DonHangTao(DonHangCoSo):
    nguoi_dung_id: Optional[int] = None


class DonHangCapNhat(BaseModel):
    trang_thai: Optional[str] = None
    dia_chi_giao: Optional[str] = None


class DonHangPhanHoi(DonHangCoSo):
    id: int
    nguoi_dung_id: Optional[int]
    trang_thai: str
    ngay_dat: datetime

    class Config:
        from_attributes = True


# ============ CHI TIẾT ĐƠN HÀNG ============
class ChiTietDonHangCoSo(BaseModel):
    don_hang_id: int
    san_pham_id: int
    so_luong: int
    gia: float


class ChiTietDonHangTao(ChiTietDonHangCoSo):
    pass


class ChiTietDonHangPhanHoi(ChiTietDonHangCoSo):
    id: int

    class Config:
        from_attributes = True


# ============ LIÊN HỆ ============
class LienHeCoSo(BaseModel):
    ho_ten: str
    email: str
    dien_thoai: Optional[str] = None
    dia_chi: Optional[str] = None
    noi_dung: str


class LienHeTao(LienHeCoSo):
    pass


class LienHeCapNhat(BaseModel):
    trang_thai: Optional[str] = None


class LienHePhanHoi(LienHeCoSo):
    id: int
    trang_thai: str
    ngay_gui: datetime

    class Config:
        from_attributes = True


# ============ THƯ VIỆN ẢNH ============
class ThuVienAnhCoSo(BaseModel):
    anh_url: str
    tieu_de: Optional[str] = None
    thu_tu: int = 0


class ThuVienAnhTao(ThuVienAnhCoSo):
    pass


class ThuVienAnhCapNhat(BaseModel):
    anh_url: Optional[str] = None
    tieu_de: Optional[str] = None
    thu_tu: Optional[int] = None


class ThuVienAnhPhanHoi(ThuVienAnhCoSo):
    id: int

    class Config:
        from_attributes = True
