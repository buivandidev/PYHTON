from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from ..co_so_du_lieu import lay_csdl, DonHang as DonHangDB, ChiTietDonHang as ChiTietDonHangDB, SanPham as SanPhamDB

bo_dinh_tuyen = APIRouter(
    prefix="/api/don_hang",
    tags=["don_hang"]
)

# Pydantic models
class ChiTietDonHangTao(BaseModel):
    product_id: int
    quantity: int
    price: float
    loai: str = "mua"
    rental_days: int = 0

class DonHangTao(BaseModel):
    customer_name: str
    customer_email: str
    customer_phone: str
    shipping_address: str
    total_amount: float
    items: List[ChiTietDonHangTao]
    payment_method: str = "cod"
    delivery_type: str = "delivery"
    note: Optional[str] = None
    user_id: Optional[int] = None

class DonHangPhanHoi(BaseModel):
    id: int
    customer_name: str
    customer_email: str
    customer_phone: str
    shipping_address: str
    total_amount: float
    status: str
    order_date: datetime
    
    class Config:
        from_attributes = True

class DonHangCapNhat(BaseModel):
    status: Optional[str] = None

@bo_dinh_tuyen.post("/", response_model=DonHangPhanHoi)
def tao_don_hang(du_lieu: DonHangTao, csdl: Session = Depends(lay_csdl)):
    """Tạo đơn hàng mới"""
    # Tạo đơn hàng
    don_hang = DonHangDB(
        customer_name=du_lieu.customer_name,
        customer_email=du_lieu.customer_email,
        customer_phone=du_lieu.customer_phone,
        shipping_address=du_lieu.shipping_address,
        total_amount=du_lieu.total_amount,
        status="pending",
        user_id=du_lieu.user_id
    )
    csdl.add(don_hang)
    csdl.commit()
    csdl.refresh(don_hang)
    
    # Thêm chi tiết đơn hàng
    for item in du_lieu.items:
        chi_tiet = ChiTietDonHangDB(
            order_id=don_hang.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price
        )
        csdl.add(chi_tiet)
    
    csdl.commit()
    return don_hang

@bo_dinh_tuyen.get("/", response_model=List[DonHangPhanHoi])
def lay_danh_sach_don_hang(csdl: Session = Depends(lay_csdl)):
    """Lấy tất cả đơn hàng"""
    return csdl.query(DonHangDB).order_by(DonHangDB.order_date.desc()).all()

@bo_dinh_tuyen.get("/{id}", response_model=DonHangPhanHoi)
def lay_don_hang(id: int, csdl: Session = Depends(lay_csdl)):
    """Lấy chi tiết đơn hàng"""
    don_hang = csdl.query(DonHangDB).filter(DonHangDB.id == id).first()
    if not don_hang:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")
    return don_hang

@bo_dinh_tuyen.put("/{id}", response_model=DonHangPhanHoi)
def cap_nhat_don_hang(id: int, du_lieu: DonHangCapNhat, csdl: Session = Depends(lay_csdl)):
    """Cập nhật trạng thái đơn hàng"""
    don_hang = csdl.query(DonHangDB).filter(DonHangDB.id == id).first()
    if not don_hang:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")
    
    if du_lieu.status:
        don_hang.status = du_lieu.status
    
    csdl.commit()
    csdl.refresh(don_hang)
    return don_hang
