from fastapi import APIRouter, Depends, Query, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
from datetime import datetime
from ..co_so_du_lieu import lay_csdl, SanPham as SanPhamDB, DanhGia as DanhGiaDB
from ..mo_hinh import SanPham, SanPhamTao, SanPhamCapNhat, DanhGia, DanhGiaCoBan

bo_dinh_tuyen = APIRouter(
    prefix="/api/san_pham",
    tags=["san_pham"]
)

@bo_dinh_tuyen.get("/", response_model=List[SanPham])
def lay_danh_sach_san_pham(
    danh_muc: Optional[str] = Query(None, description="Lọc theo danh mục: wedding_modern, traditional, vest"),
    sub_category: Optional[str] = Query(None, description="Lọc theo tiểu mục"),
    gioi_tinh: Optional[str] = Query(None, description="Lọc theo giới tính: male, female"),
    sort_by: Optional[str] = Query(None, description="Sắp xếp: price_asc, price_desc, hot, new"),
    csdl: Session = Depends(lay_csdl)
):
    """Lấy tất cả sản phẩm với bộ lọc và sắp xếp tùy chọn"""
    truy_van = csdl.query(SanPhamDB)
    
    if danh_muc:
        # Support combined categories like 'vest'
        truy_van = truy_van.filter(SanPhamDB.category == danh_muc)
    if sub_category:
        truy_van = truy_van.filter(SanPhamDB.sub_category == sub_category)
    if gioi_tinh:
        truy_van = truy_van.filter(SanPhamDB.gender == gioi_tinh)
    
    # Sorting logic
    if sort_by == "price_asc":
        truy_van = truy_van.order_by(SanPhamDB.rental_price_day.asc())
    elif sort_by == "price_desc":
        truy_van = truy_van.order_by(SanPhamDB.rental_price_day.desc())
    elif sort_by == "hot":
        truy_van = truy_van.order_by(SanPhamDB.is_hot.desc())
    elif sort_by == "new":
        truy_van = truy_van.order_by(SanPhamDB.is_new.desc(), SanPhamDB.id.desc())
    else:
        # Default sort by ID desc
        truy_van = truy_van.order_by(SanPhamDB.id.desc())
    
    return truy_van.all()


@bo_dinh_tuyen.get("/{id_san_pham}", response_model=SanPham)
def lay_san_pham(id_san_pham: int, csdl: Session = Depends(lay_csdl)):
    """Lấy sản phẩm cụ thể theo ID"""
    san_pham = csdl.query(SanPhamDB).filter(SanPhamDB.id == id_san_pham).first()
    if not san_pham:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")
    return san_pham

@bo_dinh_tuyen.post("/", response_model=SanPham)
def tao_san_pham(san_pham: SanPhamTao, csdl: Session = Depends(lay_csdl)):
    """Tạo sản phẩm mới (dành cho admin)"""
    san_pham_moi = SanPhamDB(**san_pham.dict())
    csdl.add(san_pham_moi)
    csdl.commit()
    csdl.refresh(san_pham_moi)
    return san_pham_moi

@bo_dinh_tuyen.put("/{id_san_pham}", response_model=SanPham)
def cap_nhat_san_pham(id_san_pham: int, san_pham: SanPhamCapNhat, csdl: Session = Depends(lay_csdl)):
    """Cập nhật sản phẩm (dành cho admin)"""
    san_pham_cu = csdl.query(SanPhamDB).filter(SanPhamDB.id == id_san_pham).first()
    if not san_pham_cu:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")
    
    du_lieu_cap_nhat = san_pham.dict(exclude_unset=True)
    for khoa, gia_tri in du_lieu_cap_nhat.items():
        setattr(san_pham_cu, khoa, gia_tri)
    
    csdl.commit()
    csdl.refresh(san_pham_cu)
    return san_pham_cu

@bo_dinh_tuyen.delete("/{id_san_pham}")
def xoa_san_pham(id_san_pham: int, csdl: Session = Depends(lay_csdl)):
    """Xóa sản phẩm (dành cho admin)"""
    san_pham = csdl.query(SanPhamDB).filter(SanPhamDB.id == id_san_pham).first()
    if not san_pham:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")
    
    csdl.delete(san_pham)
    csdl.commit()
    return {"thong_bao": "Đã xóa sản phẩm thành công"}

# Endpoints for Reviews
@bo_dinh_tuyen.get("/{id_san_pham}/danh_gia", response_model=List[DanhGia])
def lay_danh_gia_san_pham(id_san_pham: int, csdl: Session = Depends(lay_csdl)):
    """Lấy danh sách đánh giá ĐÃ DUYỆT của một sản phẩm"""
    return csdl.query(DanhGiaDB).filter(
        DanhGiaDB.product_id == id_san_pham,
        DanhGiaDB.is_approved == True # Only approved
    ).order_by(DanhGiaDB.created_at.desc()).all()

def quet_virus_gia_lap(file_path: str) -> bool:
    """
    Giả lập quá trình quét virus và mã độc.
    Trong thực tế, bạn có thể tích hợp API của ClamAV hoặc VirusTotal tại đây.
    """
    import time
    # Giả lập thời gian quét
    time.sleep(0.5) 
    
    # Kiểm tra phần mở rộng tệp tin cơ bản như một lớp bảo mật
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.webp']:
        return False # Tệp tin không hợp lệ/nghi ngờ
        
    # Giả lập log quét thành công
    print(f"--- [SECURITY SCAN] Đang quét tệp tin: {file_path} ---")
    print(f"--- [SECURITY SCAN] Kết quả: AN TOÀN ---")
    return True

@bo_dinh_tuyen.post("/{id_san_pham}/danh_gia", response_model=DanhGia)
async def gui_danh_gia_san_pham(
    id_san_pham: int, 
    user_name: str = Form(...),
    rating: int = Form(...),
    comment: str = Form(None),
    image: UploadFile = File(None),
    csdl: Session = Depends(lay_csdl)
):
    """Gửi đánh giá mới (luôn đợi Admin duyệt)"""
    try:
        from fastapi import HTTPException
        import traceback
        
        image_url = None
        
        if image and image.filename:
            # 1. Lưu và quét bảo mật (vẫn quét để đảm bảo server an toàn)
            folder = "tep_tin/danh_gia"
            os.makedirs(folder, exist_ok=True)
            
            ext = os.path.splitext(image.filename)[1]
            filename = f"dg_{id_san_pham}_{datetime.now().timestamp()}{ext}"
            filepath = os.path.join(folder, filename)
            
            with open(filepath, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            
            # Quét virus gia lập
            security_passed = quet_virus_gia_lap(filepath)
            
            if security_passed:
                image_url = f"/{folder}/{filename}"
            else:
                if os.path.exists(filepath):
                    os.remove(filepath)
                raise HTTPException(status_code=403, detail="Tệp tin bị từ chối bởi hệ thống bảo mật")

        # 2. Tạo đánh giá với trạng thái CHƯA DUYỆT (is_approved=False)
        danh_gia_moi = DanhGiaDB(
            product_id=id_san_pham,
            user_name=user_name,
            rating=rating,
            comment=comment,
            image_url=image_url,
            is_approved=False # Phải đợi admin duyệt
        )
        csdl.add(danh_gia_moi)
        csdl.commit()
        csdl.refresh(danh_gia_moi)
        return danh_gia_moi
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

# Admin Moderation Routes
@bo_dinh_tuyen.get("/admin/danh_gia_cho_duyet", response_model=List[DanhGia])
def lay_danh_gia_cho_duyet(csdl: Session = Depends(lay_csdl)):
    """Lấy danh sách đánh giá đang chờ duyệt"""
    return csdl.query(DanhGiaDB).filter(DanhGiaDB.is_approved == False).all()

@bo_dinh_tuyen.post("/admin/duyet_danh_gia/{id_danh_gia}")
def duyet_danh_gia(id_danh_gia: int, csdl: Session = Depends(lay_csdl)):
    """Duyệt một đánh giá"""
    dg = csdl.query(DanhGiaDB).filter(DanhGiaDB.id == id_danh_gia).first()
    if not dg:
        return {"loi": "Không tìm thấy đánh giá"}
    dg.is_approved = True
    csdl.commit()
    return {"thong_bao": "Đã duyệt đánh giá thành công"}

@bo_dinh_tuyen.delete("/admin/xoa_danh_gia/{id_danh_gia}")
def xoa_danh_gia(id_danh_gia: int, csdl: Session = Depends(lay_csdl)):
    """Xóa đánh giá (từ chối)"""
    dg = csdl.query(DanhGiaDB).filter(DanhGiaDB.id == id_danh_gia).first()
    if not dg:
        return {"loi": "Không tìm thấy đánh giá"}
    csdl.delete(dg)
    csdl.commit()
    return {"thong_bao": "Đã xóa đánh giá"}
