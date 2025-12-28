"""
API Endpoints cho PostgreSQL - IVIE Studio
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import sys
import os

# Thêm đường dẫn backend vào sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from ket_noi_postgresql import PhienLamViec, dong_co, CoSo
from ung_dung.co_so_du_lieu import SanPham, NguoiDung, DonHang, ChiTietDonHang, LienHeGui as LienHe, ThuVien as ThuVienAnh
from ung_dung.luoc_do_pg import (
    SanPhamTao, SanPhamCapNhat, SanPhamPhanHoi,
    NguoiDungTao, NguoiDungCapNhat, NguoiDungPhanHoi,
    DonHangTao, DonHangCapNhat, DonHangPhanHoi,
    ChiTietDonHangTao, ChiTietDonHangPhanHoi,
    LienHeTao, LienHeCapNhat, LienHePhanHoi,
    ThuVienAnhTao, ThuVienAnhCapNhat, ThuVienAnhPhanHoi
)
from passlib.context import CryptContext

bo_dinh_tuyen = APIRouter(prefix="/pg", tags=["PostgreSQL API"])

# Mã hóa mật khẩu
ma_hoa = CryptContext(schemes=["bcrypt"], deprecated="auto")


def lay_phien():
    """Dependency để lấy phiên làm việc database"""
    phien = PhienLamViec()
    try:
        yield phien
    finally:
        phien.close()


# ============ KHỞI TẠO BẢNG ============
@bo_dinh_tuyen.post("/khoi-tao-bang", summary="Khởi tạo tất cả bảng trong PostgreSQL")
def khoi_tao_bang():
    """Tạo tất cả bảng trong PostgreSQL"""
    try:
        CoSo.metadata.create_all(bind=dong_co)
        return {"thong_bao": "Đã tạo tất cả bảng thành công!"}
    except Exception as loi:
        raise HTTPException(status_code=500, detail=f"Lỗi tạo bảng: {str(loi)}")


# ============ SẢN PHẨM API ============
@bo_dinh_tuyen.get("/san-pham", response_model=List[SanPhamPhanHoi], summary="Lấy danh sách sản phẩm")
def lay_danh_sach_san_pham(
    bo_qua: int = Query(0, ge=0),
    gioi_han: int = Query(100, ge=1, le=1000),
    danh_muc: Optional[str] = None,
    gioi_tinh: Optional[str] = None,
    la_moi: Optional[bool] = None,
    la_hot: Optional[bool] = None,
    phien: Session = Depends(lay_phien)
):
    truy_van = phien.query(SanPham)
    
    if danh_muc:
        truy_van = truy_van.filter(SanPham.danh_muc == danh_muc)
    if gioi_tinh:
        truy_van = truy_van.filter(SanPham.gioi_tinh == gioi_tinh)
    if la_moi is not None:
        truy_van = truy_van.filter(SanPham.la_moi == la_moi)
    if la_hot is not None:
        truy_van = truy_van.filter(SanPham.la_hot == la_hot)
    
    return truy_van.offset(bo_qua).limit(gioi_han).all()


@bo_dinh_tuyen.get("/san-pham/{san_pham_id}", response_model=SanPhamPhanHoi, summary="Lấy chi tiết sản phẩm")
def lay_san_pham(san_pham_id: int, phien: Session = Depends(lay_phien)):
    san_pham = phien.query(SanPham).filter(SanPham.id == san_pham_id).first()
    if not san_pham:
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")
    return san_pham


@bo_dinh_tuyen.post("/san-pham", response_model=SanPhamPhanHoi, summary="Tạo sản phẩm mới")
def tao_san_pham(du_lieu: SanPhamTao, phien: Session = Depends(lay_phien)):
    # Kiểm tra mã sản phẩm đã tồn tại
    ton_tai = phien.query(SanPham).filter(SanPham.ma == du_lieu.ma).first()
    if ton_tai:
        raise HTTPException(status_code=400, detail="Mã sản phẩm đã tồn tại")
    
    san_pham = SanPham(**du_lieu.model_dump())
    phien.add(san_pham)
    phien.commit()
    phien.refresh(san_pham)
    return san_pham


@bo_dinh_tuyen.put("/san-pham/{san_pham_id}", response_model=SanPhamPhanHoi, summary="Cập nhật sản phẩm")
def cap_nhat_san_pham(san_pham_id: int, du_lieu: SanPhamCapNhat, phien: Session = Depends(lay_phien)):
    san_pham = phien.query(SanPham).filter(SanPham.id == san_pham_id).first()
    if not san_pham:
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")
    
    for truong, gia_tri in du_lieu.model_dump(exclude_unset=True).items():
        setattr(san_pham, truong, gia_tri)
    
    phien.commit()
    phien.refresh(san_pham)
    return san_pham


@bo_dinh_tuyen.delete("/san-pham/{san_pham_id}", summary="Xóa sản phẩm")
def xoa_san_pham(san_pham_id: int, phien: Session = Depends(lay_phien)):
    san_pham = phien.query(SanPham).filter(SanPham.id == san_pham_id).first()
    if not san_pham:
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")
    
    phien.delete(san_pham)
    phien.commit()
    return {"thong_bao": "Đã xóa sản phẩm thành công"}



# ============ NGƯỜI DÙNG API ============
@bo_dinh_tuyen.get("/nguoi-dung", response_model=List[NguoiDungPhanHoi], summary="Lấy danh sách người dùng")
def lay_danh_sach_nguoi_dung(
    bo_qua: int = Query(0, ge=0),
    gioi_han: int = Query(100, ge=1, le=1000),
    hoat_dong: Optional[bool] = None,
    phien: Session = Depends(lay_phien)
):
    truy_van = phien.query(NguoiDung)
    if hoat_dong is not None:
        truy_van = truy_van.filter(NguoiDung.hoat_dong == hoat_dong)
    return truy_van.offset(bo_qua).limit(gioi_han).all()


@bo_dinh_tuyen.get("/nguoi-dung/{nguoi_dung_id}", response_model=NguoiDungPhanHoi, summary="Lấy chi tiết người dùng")
def lay_nguoi_dung(nguoi_dung_id: int, phien: Session = Depends(lay_phien)):
    nguoi_dung = phien.query(NguoiDung).filter(NguoiDung.id == nguoi_dung_id).first()
    if not nguoi_dung:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
    return nguoi_dung


@bo_dinh_tuyen.post("/nguoi-dung", response_model=NguoiDungPhanHoi, summary="Tạo người dùng mới")
def tao_nguoi_dung(du_lieu: NguoiDungTao, phien: Session = Depends(lay_phien)):
    # Kiểm tra tên đăng nhập đã tồn tại
    ton_tai = phien.query(NguoiDung).filter(NguoiDung.ten_dang_nhap == du_lieu.ten_dang_nhap).first()
    if ton_tai:
        raise HTTPException(status_code=400, detail="Tên đăng nhập đã tồn tại")
    
    # Mã hóa mật khẩu
    du_lieu_dict = du_lieu.model_dump()
    mat_khau = du_lieu_dict.pop("mat_khau")
    du_lieu_dict["mat_khau_hash"] = ma_hoa.hash(mat_khau)
    
    nguoi_dung = NguoiDung(**du_lieu_dict)
    phien.add(nguoi_dung)
    phien.commit()
    phien.refresh(nguoi_dung)
    return nguoi_dung


@bo_dinh_tuyen.put("/nguoi-dung/{nguoi_dung_id}", response_model=NguoiDungPhanHoi, summary="Cập nhật người dùng")
def cap_nhat_nguoi_dung(nguoi_dung_id: int, du_lieu: NguoiDungCapNhat, phien: Session = Depends(lay_phien)):
    nguoi_dung = phien.query(NguoiDung).filter(NguoiDung.id == nguoi_dung_id).first()
    if not nguoi_dung:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
    
    for truong, gia_tri in du_lieu.model_dump(exclude_unset=True).items():
        setattr(nguoi_dung, truong, gia_tri)
    
    phien.commit()
    phien.refresh(nguoi_dung)
    return nguoi_dung


@bo_dinh_tuyen.delete("/nguoi-dung/{nguoi_dung_id}", summary="Xóa người dùng")
def xoa_nguoi_dung(nguoi_dung_id: int, phien: Session = Depends(lay_phien)):
    nguoi_dung = phien.query(NguoiDung).filter(NguoiDung.id == nguoi_dung_id).first()
    if not nguoi_dung:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
    
    phien.delete(nguoi_dung)
    phien.commit()
    return {"thong_bao": "Đã xóa người dùng thành công"}


# ============ ĐƠN HÀNG API ============
@bo_dinh_tuyen.get("/don-hang", response_model=List[DonHangPhanHoi], summary="Lấy danh sách đơn hàng")
def lay_danh_sach_don_hang(
    bo_qua: int = Query(0, ge=0),
    gioi_han: int = Query(100, ge=1, le=1000),
    trang_thai: Optional[str] = None,
    phien: Session = Depends(lay_phien)
):
    truy_van = phien.query(DonHang)
    if trang_thai:
        truy_van = truy_van.filter(DonHang.trang_thai == trang_thai)
    return truy_van.order_by(DonHang.ngay_dat.desc()).offset(bo_qua).limit(gioi_han).all()


@bo_dinh_tuyen.get("/don-hang/{don_hang_id}", response_model=DonHangPhanHoi, summary="Lấy chi tiết đơn hàng")
def lay_don_hang(don_hang_id: int, phien: Session = Depends(lay_phien)):
    don_hang = phien.query(DonHang).filter(DonHang.id == don_hang_id).first()
    if not don_hang:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")
    return don_hang


@bo_dinh_tuyen.post("/don-hang", response_model=DonHangPhanHoi, summary="Tạo đơn hàng mới")
def tao_don_hang(du_lieu: DonHangTao, phien: Session = Depends(lay_phien)):
    don_hang = DonHang(**du_lieu.model_dump())
    phien.add(don_hang)
    phien.commit()
    phien.refresh(don_hang)
    return don_hang


@bo_dinh_tuyen.put("/don-hang/{don_hang_id}", response_model=DonHangPhanHoi, summary="Cập nhật đơn hàng")
def cap_nhat_don_hang(don_hang_id: int, du_lieu: DonHangCapNhat, phien: Session = Depends(lay_phien)):
    don_hang = phien.query(DonHang).filter(DonHang.id == don_hang_id).first()
    if not don_hang:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")
    
    for truong, gia_tri in du_lieu.model_dump(exclude_unset=True).items():
        setattr(don_hang, truong, gia_tri)
    
    phien.commit()
    phien.refresh(don_hang)
    return don_hang


@bo_dinh_tuyen.delete("/don-hang/{don_hang_id}", summary="Xóa đơn hàng")
def xoa_don_hang(don_hang_id: int, phien: Session = Depends(lay_phien)):
    don_hang = phien.query(DonHang).filter(DonHang.id == don_hang_id).first()
    if not don_hang:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")
    
    phien.delete(don_hang)
    phien.commit()
    return {"thong_bao": "Đã xóa đơn hàng thành công"}


# ============ LIÊN HỆ API ============
@bo_dinh_tuyen.get("/lien-he", response_model=List[LienHePhanHoi], summary="Lấy danh sách liên hệ")
def lay_danh_sach_lien_he(
    bo_qua: int = Query(0, ge=0),
    gioi_han: int = Query(100, ge=1, le=1000),
    trang_thai: Optional[str] = None,
    phien: Session = Depends(lay_phien)
):
    truy_van = phien.query(LienHe)
    if trang_thai:
        truy_van = truy_van.filter(LienHe.trang_thai == trang_thai)
    return truy_van.order_by(LienHe.ngay_gui.desc()).offset(bo_qua).limit(gioi_han).all()


@bo_dinh_tuyen.post("/lien-he", response_model=LienHePhanHoi, summary="Gửi liên hệ mới")
def tao_lien_he(du_lieu: LienHeTao, phien: Session = Depends(lay_phien)):
    lien_he = LienHe(**du_lieu.model_dump())
    phien.add(lien_he)
    phien.commit()
    phien.refresh(lien_he)
    return lien_he


@bo_dinh_tuyen.put("/lien-he/{lien_he_id}", response_model=LienHePhanHoi, summary="Cập nhật trạng thái liên hệ")
def cap_nhat_lien_he(lien_he_id: int, du_lieu: LienHeCapNhat, phien: Session = Depends(lay_phien)):
    lien_he = phien.query(LienHe).filter(LienHe.id == lien_he_id).first()
    if not lien_he:
        raise HTTPException(status_code=404, detail="Không tìm thấy liên hệ")
    
    for truong, gia_tri in du_lieu.model_dump(exclude_unset=True).items():
        setattr(lien_he, truong, gia_tri)
    
    phien.commit()
    phien.refresh(lien_he)
    return lien_he


# ============ THƯ VIỆN ẢNH API ============
@bo_dinh_tuyen.get("/thu-vien-anh", response_model=List[ThuVienAnhPhanHoi], summary="Lấy danh sách ảnh")
def lay_danh_sach_anh(
    bo_qua: int = Query(0, ge=0),
    gioi_han: int = Query(100, ge=1, le=1000),
    phien: Session = Depends(lay_phien)
):
    return phien.query(ThuVienAnh).order_by(ThuVienAnh.thu_tu).offset(bo_qua).limit(gioi_han).all()


@bo_dinh_tuyen.post("/thu-vien-anh", response_model=ThuVienAnhPhanHoi, summary="Thêm ảnh mới")
def tao_anh(du_lieu: ThuVienAnhTao, phien: Session = Depends(lay_phien)):
    anh = ThuVienAnh(**du_lieu.model_dump())
    phien.add(anh)
    phien.commit()
    phien.refresh(anh)
    return anh


@bo_dinh_tuyen.put("/thu-vien-anh/{anh_id}", response_model=ThuVienAnhPhanHoi, summary="Cập nhật ảnh")
def cap_nhat_anh(anh_id: int, du_lieu: ThuVienAnhCapNhat, phien: Session = Depends(lay_phien)):
    anh = phien.query(ThuVienAnh).filter(ThuVienAnh.id == anh_id).first()
    if not anh:
        raise HTTPException(status_code=404, detail="Không tìm thấy ảnh")
    
    for truong, gia_tri in du_lieu.model_dump(exclude_unset=True).items():
        setattr(anh, truong, gia_tri)
    
    phien.commit()
    phien.refresh(anh)
    return anh


@bo_dinh_tuyen.delete("/thu-vien-anh/{anh_id}", summary="Xóa ảnh")
def xoa_anh(anh_id: int, phien: Session = Depends(lay_phien)):
    anh = phien.query(ThuVienAnh).filter(ThuVienAnh.id == anh_id).first()
    if not anh:
        raise HTTPException(status_code=404, detail="Không tìm thấy ảnh")
    
    phien.delete(anh)
    phien.commit()
    return {"thong_bao": "Đã xóa ảnh thành công"}



# ============ CHUYÊN GIA API ============
@bo_dinh_tuyen.get("/chuyen-gia", summary="Lấy danh sách chuyên gia")
def lay_danh_sach_chuyen_gia(phien: Session = Depends(lay_phien)):
    from sqlalchemy import text
    result = phien.execute(text("SELECT id, ten, chuc_vu, mo_ta, anh_url, thu_tu FROM chuyen_gia ORDER BY thu_tu"))
    chuyen_gias = []
    for r in result:
        chuyen_gias.append({
            "id": r[0],
            "ten": r[1],
            "chuc_vu": r[2],
            "mo_ta": r[3],
            "anh_url": r[4],
            "thu_tu": r[5]
        })
    return chuyen_gias


@bo_dinh_tuyen.post("/chuyen-gia", summary="Thêm chuyên gia mới")
def tao_chuyen_gia(
    ten: str,
    chuc_vu: str = None,
    mo_ta: str = None,
    anh_url: str = None,
    phien: Session = Depends(lay_phien)
):
    from sqlalchemy import text
    phien.execute(text("""
        INSERT INTO chuyen_gia (ten, chuc_vu, mo_ta, anh_url, thu_tu)
        VALUES (:ten, :chuc_vu, :mo_ta, :anh_url, 0)
    """), {"ten": ten, "chuc_vu": chuc_vu, "mo_ta": mo_ta, "anh_url": anh_url})
    phien.commit()
    return {"thong_bao": "Đã thêm chuyên gia thành công"}
