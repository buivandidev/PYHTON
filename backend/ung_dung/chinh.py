from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .co_so_du_lieu import khoi_tao_csdl
from .dinh_tuyen import (
    san_pham, dich_vu, lien_he, tap_tin, 
    noi_dung, banner, thu_vien, nguoi_dung, chat, doi_tac,
    blog, yeu_thich, thong_ke, api_pg
)

import os
from dotenv import load_dotenv

load_dotenv()

ung_dung = FastAPI(
    title="IVIE Wedding Studio API (Tiếng Việt)",
    description="API cho website IVIE Wedding Studio",
    version="1.0.0"
)

# Cấu hình CORS
# Cấu hình CORS
# Cho phép tất cả các nguồn trong môi trường phát triển để tránh lỗi cổng (port)
nguon_goc = ["*"]

ung_dung.add_middleware(
    CORSMiddleware,
    allow_origins=nguon_goc,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gắn thư mục tĩnh cho hình ảnh (để Admin panel và API có thể truy cập)
# Đường dẫn tính từ backend/ung_dung/chinh.py -> ../../frontend/public/images
thu_muc_anh = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/public/images"))
if os.path.exists(thu_muc_anh):
    ung_dung.mount("/images", StaticFiles(directory=thu_muc_anh), name="images")
else:
    print(f"Lưu ý: Không tìm thấy thư mục ảnh tại {thu_muc_anh}")

# Gắn thư mục tep_tin cho ảnh người dùng tải lên
thu_muc_tep_tin = "tep_tin"
os.makedirs(thu_muc_tep_tin, exist_ok=True)
ung_dung.mount("/tep_tin", StaticFiles(directory=thu_muc_tep_tin), name="tep_tin")

# Bao gồm các bộ định tuyến
ung_dung.include_router(san_pham.bo_dinh_tuyen)
ung_dung.include_router(dich_vu.bo_dinh_tuyen)
ung_dung.include_router(lien_he.bo_dinh_tuyen)
ung_dung.include_router(tap_tin.bo_dinh_tuyen)
ung_dung.include_router(banner.bo_dinh_tuyen)
ung_dung.include_router(noi_dung.bo_dinh_tuyen)
ung_dung.include_router(thu_vien.bo_dinh_tuyen)
ung_dung.include_router(nguoi_dung.bo_dinh_tuyen)
ung_dung.include_router(chat.bo_dinh_tuyen)
ung_dung.include_router(doi_tac.bo_dinh_tuyen)
ung_dung.include_router(blog.bo_dinh_tuyen)
ung_dung.include_router(yeu_thich.bo_dinh_tuyen)
ung_dung.include_router(thong_ke.bo_dinh_tuyen)
ung_dung.include_router(api_pg.bo_dinh_tuyen)


@ung_dung.on_event("startup")
def su_kien_khoi_dong():
    """Khởi tạo cơ sở dữ liệu khi khởi động"""
    khoi_tao_csdl()

@ung_dung.get("/")
def doc_goc():
    return {
        "thong_bao": "Chào mừng đến với API IVIE Wedding Studio",
        "tai_lieu": "/docs",
        "phien_ban": "1.0.0"
    }

@ung_dung.get("/suckhoe")
def kiem_tra_suc_khoe():
    return {"trang_thai": "khoe_manh"}
