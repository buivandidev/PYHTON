from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from ..co_so_du_lieu import lay_csdl, NguoiDung as NguoiDungDB, DonHang as DonHangDB, MaGiamGia as MaGiamGiaDB
from ..mo_hinh import (
    NguoiDungTao, NguoiDung as NguoiDungSchema, 
    NguoiDungCapNhat, DonHang as DonHangSchema, MaGiamGia as MaGiamGiaSchema
)
from ..bao_mat import bam_mat_khau, xac_minh_mat_khau, tao_token_truy_cap
from jose import jwt, JWTError
from decouple import config
from pydantic import BaseModel
from typing import Optional
import traceback
import os

bo_dinh_tuyen = APIRouter(
    prefix="/api/nguoi_dung",
    tags=["nguoi_dung"]
)

SECRET_KEY = config('SECRET_KEY', default='secret_key_mac_dinh_rat_dai_va_bao_mat_123')
ALGORITHM = "HS256"

def lay_user_tu_token(token: str, csdl: Session):
    """Giải mã token và lấy user"""
    if not token:
        raise HTTPException(status_code=401, detail="Token không được cung cấp")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token không hợp lệ")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token không hợp lệ")
    
    user = csdl.query(NguoiDungDB).filter(NguoiDungDB.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Người dùng không tồn tại")
    return user

# Alias cho tương thích ngược với các file khác
def lay_user_hien_tai(token: str, csdl: Session):
    return lay_user_tu_token(token, csdl)

class DangNhapForm(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: NguoiDungSchema

@bo_dinh_tuyen.post("/dang_ky", response_model=NguoiDungSchema)
def dang_ky(du_lieu: NguoiDungTao, csdl: Session = Depends(lay_csdl)):
    """Đăng ký người dùng mới"""
    # Kiểm tra username đã tồn tại chưa
    db_user = csdl.query(NguoiDungDB).filter(NguoiDungDB.username == du_lieu.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Tên đăng nhập đã tồn tại")
    
    # Kiểm tra email đã tồn tại chưa (nếu có cung cấp)
    if du_lieu.email:
        db_email = csdl.query(NguoiDungDB).filter(NguoiDungDB.email == du_lieu.email).first()
        if db_email:
            raise HTTPException(status_code=400, detail="Email đã được sử dụng")
    
    # Tạo người dùng mới
    mat_khau_ma_hoa = bam_mat_khau(du_lieu.password)
    user_moi = NguoiDungDB(
        username=du_lieu.username,
        email=du_lieu.email,
        full_name=du_lieu.full_name,
        phone=du_lieu.phone,
        address=du_lieu.address,
        hashed_password=mat_khau_ma_hoa,
        is_active=True
    )
    csdl.add(user_moi)
    csdl.commit()
    csdl.refresh(user_moi)
    return user_moi

@bo_dinh_tuyen.post("/dang_nhap", response_model=Token)
def dang_nhap(du_lieu: DangNhapForm, csdl: Session = Depends(lay_csdl)):
    """Đăng nhập và lấy token"""
    user = csdl.query(NguoiDungDB).filter(NguoiDungDB.username == du_lieu.username).first()
    if not user or not xac_minh_mat_khau(du_lieu.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập hoặc mật khẩu không chính xác",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = tao_token_truy_cap(du_lieu={"sub": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@bo_dinh_tuyen.put("/cap_nhat", response_model=NguoiDungSchema)
def cap_nhat_profile(du_lieu: NguoiDungCapNhat, authorization: Optional[str] = Header(None, alias="Authorization"), csdl: Session = Depends(lay_csdl)):
    """Cập nhật thông tin cá nhân"""
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]
    user = lay_user_tu_token(token, csdl)
    
    if du_lieu.full_name:
        user.full_name = du_lieu.full_name
    if du_lieu.phone:
        user.phone = du_lieu.phone
    if du_lieu.address:
        user.address = du_lieu.address
    if du_lieu.email:
        user.email = du_lieu.email
    if du_lieu.password:
        user.hashed_password = bam_mat_khau(du_lieu.password)
        
    csdl.commit()
    csdl.refresh(user)
    return user

@bo_dinh_tuyen.get("/don_hang")
def lay_lich_su_don_hang(authorization: Optional[str] = Header(None, alias="Authorization"), csdl: Session = Depends(lay_csdl)):
    """Lấy danh sách đơn hàng của người dùng"""
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]
    user = lay_user_tu_token(token, csdl)
    # Trả về danh sách đơn hàng dạng dict
    orders = csdl.query(DonHangDB).filter(DonHangDB.user_id == user.id).order_by(DonHangDB.order_date.desc()).all()
    return [
        {
            "id": o.id,
            "customer_name": o.customer_name,
            "customer_email": o.customer_email,
            "customer_phone": o.customer_phone,
            "shipping_address": o.shipping_address,
            "total_amount": o.total_amount,
            "status": o.status,
            "order_date": o.order_date.isoformat() if o.order_date else None
        }
        for o in orders
    ]

@bo_dinh_tuyen.post("/kiem_tra_giam_gia")
def kiem_tra_giam_gia(authorization: Optional[str] = Header(None, alias="Authorization"), csdl: Session = Depends(lay_csdl)):
    """Kiểm tra quyền lợi giảm giá 5% cho khách cũ"""
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]
    user = lay_user_tu_token(token, csdl)
    
    # Kiểm tra xem có đơn hàng thành công nào chưa
    don_hang_cu = csdl.query(DonHangDB).filter(
        DonHangDB.user_id == user.id,
        DonHangDB.status.in_(['processing', 'shipped', 'delivered'])
    ).first()
    
    if don_hang_cu:
        return {"co_the_giam": True, "phan_tram": 5.0, "message": "Bạn là khách hàng thân thiết, được giảm 5%!"}
    
    return {"co_the_giam": False, "phan_tram": 0, "message": "Giảm giá 5% cho lần mua hàng sau."}
