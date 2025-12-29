import streamlit as st
import requests
import os
from dotenv import load_dotenv
import pandas as pd
from PIL import Image
import io
from datetime import datetime

load_dotenv()

API_URL = os.getenv("VITE_API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="IVIE Wedding Admin", layout="wide", page_icon="🏯")

# CSS custom for minimalist B&W Dark Theme
st.markdown("""
    <style>
    /* Dark Theme Logic is handled by top-level config usually, but we enforce some styles */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    .main {
        background-color: #000000;
    }
    
    /* Buttons: White border, black bg, white text for minimalist look */
    .stButton>button { 
        width: 100%;
        background-color: #000000;
        color: #ffffff;
        border: 1px solid #333;
        border-radius: 4px;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        border-color: #ffffff;
        color: #ffffff;
    }

    /* Inputs */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stNumberInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #111;
        color: white;
        border: 1px solid #333;
    }
    
    /* Headers */
    h1, h2, h3, h4 {
        color: #ffffff !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 300;
    }
    
    /* Remove default streamlit branding if possible (limited via CSS) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Status indicators - Monochrome */
    .status-badge {
        font-size: 0.8em;
        padding: 2px 6px;
        border: 1px solid #333;
        border-radius: 4px;
        background: #111;
    }
    
    /* Product row */
    .product-row {
        border-bottom: 1px solid #222;
        padding: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

st.title("IVIE STUDIO ADMIN")

with st.sidebar:
    choice = st.selectbox("MENU QUẢN TRỊ", [
        "📊 Tổng quan",
        "🛒 Quản lý Đơn hàng",
        "📞 Liên hệ khách hàng",
        "💬 Tư vấn khách hàng",
        "⏳ Duyệt Đánh Giá",
        "🖼️ Quản lý Banner",
        "👗 Quản lý Sản phẩm",
        "🤝 Đối tác & Khiếu nại",
        "📁 Thư viện ảnh mẫu",
        "✨ Dịch vụ Chuyên gia",
        "📰 Blog & Tin tức",
        "🏠 Nội dung Trang chủ"
    ])



# --- Helpers ---
@st.cache_data(show_spinner=False)
def fetch_api_data(endpoint):
    """Cached version for GET requests"""
    url = f"{API_URL}{endpoint}"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.json()
        return None
    except Exception:
        return None

def call_api(method, endpoint, data=None, files=None, clear_cache=True):
    url = f"{API_URL}{endpoint}"
    try:
        with st.spinner("Đang xử lý..."):
            if method == "GET":
                if not clear_cache: # If we explicitly want cached data
                    return fetch_api_data(endpoint)
                res = requests.get(url)
            elif method == "POST":
                res = requests.post(url, json=data, files=files)
            elif method == "PUT":
                res = requests.put(url, json=data)
            elif method == "PATCH":
                res = requests.patch(url, json=data)
            elif method == "DELETE":
                res = requests.delete(url)
            
            if res.status_code in [200, 201]:
                if method != "GET" and clear_cache:
                    st.cache_data.clear() # Invalidate cache on mutations
                return res.json()
            else:
                st.error(f"Lỗi API ({res.status_code}): {res.text}")
                return None
    except Exception as e:
        st.error(f"Lỗi kết nối: {e}")
        return None

def upload_image(uploaded_file):
    if uploaded_file is not None:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        url = f"{API_URL}/api/tap_tin/upload"
        try:
            res = requests.post(url, files=files)
            if res.status_code == 200:
                return res.json().get("url")
            st.error("Lỗi tải ảnh lên")
        except Exception as e:
            st.error(f"Lỗi kết nối tải ảnh: {e}")
    return None

def lay_url_anh(path):
    if not path: return "https://placehold.co/400x300/000000/ffffff?text=No+Image"
    if path.startswith("http"): return path
    if not path.startswith("/"):
        path = "/" + path
    return f"{API_URL}{path}"

def cap_nhat_trang_thai_lien_he(id_lien_he, status):
    url = f"{API_URL}/api/lien_he/{id_lien_he}/status"
    try:
        res = requests.patch(url, json={"status": status})
        if res.status_code == 200:
            return res.json()
        else:
            st.error(f"Lỗi: {res.text}")
            return None
    except Exception as e:
        st.error(f"Lỗi kết nối: {e}")
        return None

# --- UI Sections ---
def ui_lien_he():
    st.header("Quản lý Liên hệ")
    contacts = call_api("GET", "/api/lien_he/", clear_cache=False)
    if not contacts:
        st.info("Chưa có liên hệ nào.")
        return

    search = st.text_input("Tìm kiếm", placeholder="Nhập tên, email...")
    status_filter = st.selectbox("Lọc trạng thái", ["Tất cả", "Chưa xử lý", "Đã xử lý"])
    
    filtered = contacts
    if search:
        filtered = [c for c in filtered if search.lower() in str(c).lower()]
    if status_filter == "Chưa xử lý":
        filtered = [c for c in filtered if c.get('status') == 'pending']
    elif status_filter == "Đã xử lý":
        filtered = [c for c in filtered if c.get('status') != 'pending']
        
    st.write(f"Hiển thị: {len(filtered)}")
    
    for c in filtered:
        with st.container(border=True):
            c1, c2, c3 = st.columns([4, 2, 1])
            with c1:
                st.write(f"**{c.get('name')}** | {c.get('phone')} | {c.get('email')}")
                st.write(f"📍 **Địa chỉ:** {c.get('address', 'Chưa cung cấp')}")
                st.caption(c.get('message'))
            with c2:
                curr_status = c.get('status', 'pending')
                new_status = st.selectbox("", ["pending", "contacted", "completed"], 
                                        index=["pending", "contacted", "completed"].index(curr_status) if curr_status in ["pending", "contacted", "completed"] else 0,
                                        key=f"st_{c['id']}", label_visibility="collapsed")
                if new_status != curr_status:
                    if st.button("LƯU", key=f"save_{c['id']}"):
                        if cap_nhat_trang_thai_lien_he(c['id'], new_status):
                            st.toast("Đã cập nhật trạng thái!")
                            st.rerun()
            with c3:
                if st.button("XÓA", key=f"del_{c['id']}"):
                    if call_api("DELETE", f"/api/lien_he/{c['id']}"):
                        st.toast("Đã xóa liên hệ")
                        st.rerun()

def ui_banner():
    st.header("Quản lý Banner")
    t1, t2 = st.tabs(["DANH SÁCH", "THÊM MỚI"])
    
    with t2:
        with st.form("new_bn"):
            title = st.text_input("Tiêu đề")
            sub = st.text_input("Mô tả phụ")
            img = st.file_uploader("Ảnh Banner", type=["jpg", "png"])
            if st.form_submit_button("THÊM BANNER"):
                url = upload_image(img)
                if url:
                    if call_api("POST", "/api/banner/", data={
                        "title": title, "subtitle": sub, "image_url": url, "is_active": True, "order": 0
                    }):
                        st.toast("Đã thêm banner")
                        st.rerun()
    
    with t1:
        banners = call_api("GET", "/api/banner/tat_ca", clear_cache=False)
        if banners:
            for b in banners:
                with st.container(border=True):
                    c1, c2, c3 = st.columns([1, 3, 1])
                    with c1:
                        st.image(lay_url_anh(b['image_url']))
                    with c2:
                        st.write(f"**{b.get('title')}**")
                        st.caption(b.get('subtitle'))
                    with c3:
                        if st.button("XÓA", key=f"del_bn_{b['id']}"):
                            if call_api("DELETE", f"/api/banner/{b['id']}"):
                                st.toast("Đã xóa banner")
                                st.rerun()

def ui_san_pham():
    st.header("Quản lý Sản phẩm")
    t1, t2 = st.tabs(["DANH SÁCH", "THÊM MỚI"])
    
    # Định nghĩa tiểu mục theo danh mục
    tieu_muc_theo_danh_muc = {
        "wedding_modern": [
            ("all", "Tất cả váy cưới"),
            ("xoe", "Váy Xòe"),
            ("duoi_ca", "Váy Đuôi Cá"),
            ("ngan", "Váy Ngắn"),
        ],
        "vest": [
            ("all", "Tất cả Vest"),
            ("hien_dai", "Vest Hiện Đại"),
            ("han_quoc", "Vest Hàn Quốc"),
        ],
        "aodai": [
            ("all", "Tất cả Áo Dài"),
            ("nam", "Áo Dài Nam"),
            ("nu", "Áo Dài Nữ"),
        ],
    }
    
    with t2:
        st.subheader("📝 Thêm mẫu váy mới")
        with st.form("add_prod"):
            # THÔNG TIN CƠ BẢN
            st.markdown("### 📋 Thông tin cơ bản")
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Tên sản phẩm *", placeholder="VD: Váy Cưới Thanh Lịch")
                code = st.text_input("Mã sản phẩm (SKU) *", placeholder="VD: VD-M001")
                cat = st.selectbox("Danh mục *", ["wedding_modern", "vest", "aodai"], 
                                 format_func=lambda x: {"wedding_modern": "👰 Váy cưới hiện đại", "vest": "🤵 Vest", "aodai": "👘 Áo dài"}[x])
            with c2:
                # Tiểu mục động theo danh mục
                sub_cat_options = tieu_muc_theo_danh_muc.get(cat, [("all", "Tất cả")])
                sub_cat = st.selectbox("Tiểu mục *", 
                                      options=[x[0] for x in sub_cat_options],
                                      format_func=lambda x: dict(sub_cat_options).get(x, x))
                gender = st.selectbox("Giới tính", ["female", "male", "unisex"], 
                                    format_func=lambda x: {"female": "👰 Nữ", "male": "🤵 Nam", "unisex": "👫 Unisex"}[x])
                is_hot = st.checkbox("🔥 Đánh dấu sản phẩm HOT")
            
            # SỐ LƯỢNG VÀ TRẠNG THÁI
            st.markdown("### 📦 Số lượng & Trạng thái")
            c1, c2 = st.columns(2)
            with c1:
                so_luong = st.number_input("Số lượng tồn kho *", min_value=0, value=10, step=1)
            with c2:
                het_hang = st.checkbox("❌ Đánh dấu HẾT HÀNG")
            
            # GIÁ CẢ
            st.markdown("### 💰 Giá cả")
            c1, c2, c3 = st.columns(3)
            with c1:
                price_day = st.number_input("Giá thuê/ngày (VNĐ) *", min_value=0, value=1000000, step=100000)
            with c2:
                price_week = st.number_input("Giá thuê/tuần (VNĐ)", min_value=0, value=int(price_day * 5), step=100000)
            with c3:
                price_buy = st.number_input("Giá mua (VNĐ)", min_value=0, value=int(price_day * 20), step=500000)
            
            # CHI TIẾT SẢN PHẨM
            st.markdown("### 🎨 Chi tiết sản phẩm")
            c1, c2 = st.columns(2)
            with c1:
                fabric = st.text_input("Loại vải", placeholder="VD: Ren cao cấp, Lụa Satin")
                color = st.text_input("Màu sắc", placeholder="VD: Trắng, Kem, Hồng pastel")
            with c2:
                sizes = st.multiselect("Size có sẵn *", 
                                      options=["XS", "S", "M", "L", "XL", "XXL", "Free Size"],
                                      default=["S", "M", "L"])
                makeup_tone = st.text_area("Gợi ý tông makeup", placeholder="VD: Tông nude tự nhiên, môi hồng nhẹ", height=80)
            
            description = st.text_area("Mô tả chi tiết sản phẩm", 
                                      placeholder="Mô tả về thiết kế, phong cách, đặc điểm nổi bật...", 
                                      height=120)
            
            # HÌNH ẢNH
            st.markdown("### 📸 Hình ảnh sản phẩm")
            st.info("💡 Mẹo: Ảnh đại diện sẽ là Váy Mẫu 1. Chỉ cần thêm 3 ảnh mẫu còn lại (Mẫu 2, 3, 4)")
            
            img_file = st.file_uploader("🖼️ Ảnh đại diện - Váy Mẫu 1 (bắt buộc) *", type=["jpg", "png", "jpeg", "webp"], 
                                       help="Ảnh này sẽ là Váy Mẫu 1 và hiển thị trên danh sách sản phẩm")
            
            if img_file:
                st.image(img_file, caption="Xem trước Váy Mẫu 1 (Ảnh đại diện)", width=300)
            
            st.markdown("#### 🎨 3 Ảnh mẫu còn lại (Váy Mẫu 2, 3, 4)")
            st.caption("Upload 3 ảnh để có đủ 4 thumbnail cho khách hàng xem")
            
            col_img2, col_img3, col_img4 = st.columns(3)
            
            with col_img2:
                img_mau_2 = st.file_uploader("📷 Váy Mẫu 2", type=["jpg", "png", "jpeg", "webp"], key="mau2")
                if img_mau_2:
                    st.image(img_mau_2, use_container_width=True)
            
            with col_img3:
                img_mau_3 = st.file_uploader("📷 Váy Mẫu 3", type=["jpg", "png", "jpeg", "webp"], key="mau3")
                if img_mau_3:
                    st.image(img_mau_3, use_container_width=True)
            
            with col_img4:
                img_mau_4 = st.file_uploader("📷 Váy Mẫu 4", type=["jpg", "png", "jpeg", "webp"], key="mau4")
                if img_mau_4:
                    st.image(img_mau_4, use_container_width=True)
            
            st.markdown("---")
            st.markdown("#### 🖼️ Bộ sưu tập ảnh bổ sung (tùy chọn)")
            st.caption("Nếu muốn thêm nhiều ảnh khác ngoài 4 ảnh mẫu ở trên")
            
            gallery_files = st.file_uploader("Chọn thêm ảnh cho bộ sưu tập", 
                                            accept_multiple_files=True, 
                                            type=["jpg", "png", "jpeg", "webp"],
                                            help="Các ảnh bổ sung sẽ được thêm vào gallery")
            
            if gallery_files:
                st.write(f"✅ Đã chọn {len(gallery_files)} ảnh bổ sung")
                cols = st.columns(min(len(gallery_files), 4))
                for idx, f in enumerate(gallery_files[:4]):
                    with cols[idx]:
                        st.image(f, caption=f"Ảnh {idx+1}", use_container_width=True)
                if len(gallery_files) > 4:
                    st.caption(f"... và {len(gallery_files) - 4} ảnh khác")
            
            # PHỤ KIỆN KÈM THEO (Optional)
            st.markdown("### 🎀 Phụ kiện kèm theo (tùy chọn)")
            with st.expander("Thêm phụ kiện"):
                acc1_name = st.text_input("Tên phụ kiện 1", placeholder="VD: Vai nơ")
                acc1_price = st.number_input("Giá phụ kiện 1", min_value=0, value=0, step=10000)
                
                acc2_name = st.text_input("Tên phụ kiện 2", placeholder="VD: Lúp voan")
                acc2_price = st.number_input("Giá phụ kiện 2", min_value=0, value=0, step=10000)
                
                acc3_name = st.text_input("Tên phụ kiện 3", placeholder="VD: Găng tay ren")
                acc3_price = st.number_input("Giá phụ kiện 3", min_value=0, value=0, step=10000)
            
            st.markdown("---")
            submit_col1, submit_col2 = st.columns([3, 1])
            with submit_col2:
                submitted = st.form_submit_button("✨ THÊM SẢN PHẨM", use_container_width=True, type="primary")
            
            if submitted:
                # Validation
                if not name or not code or not img_file:
                    st.error("⚠️ Vui lòng điền đầy đủ các trường bắt buộc (*)")
                else:
                    with st.spinner("Đang tải ảnh lên..."):
                        # Upload ảnh đại diện (Váy Mẫu 1)
                        url = upload_image(img_file)
                        
                        # Upload 3 ảnh mẫu còn lại (Mẫu 2, 3, 4)
                        # Gallery sẽ bao gồm: [ảnh đại diện, mẫu 2, mẫu 3, mẫu 4]
                        gallery_urls = [url] if url else []  # Mẫu 1 = ảnh đại diện
                        mau_images = [img_mau_2, img_mau_3, img_mau_4]
                        
                        for idx, mau_img in enumerate(mau_images):
                            if mau_img:
                                u = upload_image(mau_img)
                                if u: 
                                    gallery_urls.append(u)
                                    st.success(f"✅ Đã tải Váy Mẫu {idx+2}")
                        
                        # Upload các ảnh bổ sung từ gallery
                        if gallery_files:
                            progress_bar = st.progress(0)
                            for idx, f in enumerate(gallery_files):
                                u = upload_image(f)
                                if u: gallery_urls.append(u)
                                progress_bar.progress((idx + 1) / len(gallery_files))
                            progress_bar.empty()
                    
                    if url:
                        # Prepare accessories data
                        accessories = []
                        if acc1_name and acc1_price > 0:
                            accessories.append({"name": acc1_name, "price": acc1_price})
                        if acc2_name and acc2_price > 0:
                            accessories.append({"name": acc2_name, "price": acc2_price})
                        if acc3_name and acc3_price > 0:
                            accessories.append({"name": acc3_name, "price": acc3_price})
                        
                        data = {
                            "name": name, 
                            "code": code, 
                            "category": cat, 
                            "sub_category": sub_cat,
                            "rental_price_day": price_day, 
                            "rental_price_week": price_week,
                            "purchase_price": price_buy,
                            "image_url": url,
                            "gallery_images": gallery_urls,
                            "gender": gender,
                            "fabric_type": fabric or "Cao cấp",
                            "color": color or "Đa dạng",
                            "recommended_size": ", ".join(sizes) if sizes else "Đủ size",
                            "makeup_tone": makeup_tone or "Tự nhiên",
                            "description": description or "",
                            "is_hot": is_hot,
                            "so_luong": so_luong,
                            "het_hang": het_hang,
                            "accessories": accessories
                        }
                        if call_api("POST", "/api/san_pham/", data=data):
                            st.success(f"✅ Đã thêm sản phẩm mới thành công! ({len(gallery_urls)} ảnh mẫu)")
                            st.balloons()
                            st.rerun()
                    else:
                        st.error("❌ Lỗi khi tải ảnh lên. Vui lòng thử lại.")


    with t1:
        prods = call_api("GET", "/api/san_pham/", clear_cache=False)
        if prods:
            # THANH TÌM KIẾM VÀ LỌC
            st.markdown("### 🔍 Tìm kiếm & Lọc")
            col_search, col_cat, col_hot, col_sort = st.columns([3, 2, 1, 2])
            
            with col_search:
                search_term = st.text_input("🔎 Tìm kiếm", placeholder="Tên, mã sản phẩm...", label_visibility="collapsed")
            
            with col_cat:
                filter_cat = st.selectbox("Danh mục", ["Tất cả", "wedding_modern", "vest", "aodai"],
                                         format_func=lambda x: {"Tất cả": "📦 Tất cả", "wedding_modern": "👰 Váy cưới", "vest": "🤵 Vest", "aodai": "👘 Áo dài"}.get(x, x))
            
            with col_hot:
                filter_hot = st.checkbox("🔥 Chỉ HOT")
            
            with col_sort:
                sort_by = st.selectbox("Sắp xếp", ["Mới nhất", "Tên A-Z", "Tên Z-A", "Giá tăng", "Giá giảm"])
            
            # Lọc tiểu mục theo danh mục đã chọn
            if filter_cat != "Tất cả":
                sub_cat_filter_options = {
                    "wedding_modern": ["Tất cả", "xoe", "duoi_ca", "ngan"],
                    "vest": ["Tất cả", "hien_dai", "han_quoc"],
                    "aodai": ["Tất cả", "nam", "nu"],
                }
                sub_cat_labels = {
                    "Tất cả": "Tất cả tiểu mục",
                    "xoe": "Váy Xòe", "duoi_ca": "Váy Đuôi Cá", "ngan": "Váy Ngắn",
                    "hien_dai": "Vest Hiện Đại", "han_quoc": "Vest Hàn Quốc",
                    "nam": "Áo Dài Nam", "nu": "Áo Dài Nữ",
                }
                filter_sub = st.selectbox("Tiểu mục", 
                                         sub_cat_filter_options.get(filter_cat, ["Tất cả"]),
                                         format_func=lambda x: sub_cat_labels.get(x, x))
            else:
                filter_sub = "Tất cả"
            
            # LỌC DỮ LIỆU
            filtered_prods = prods.copy()
            
            # Lọc theo tìm kiếm
            if search_term:
                search_lower = search_term.lower()
                filtered_prods = [p for p in filtered_prods if 
                                 search_lower in p.get('name', '').lower() or 
                                 search_lower in p.get('code', '').lower()]
            
            # Lọc theo danh mục
            if filter_cat != "Tất cả":
                filtered_prods = [p for p in filtered_prods if p.get('category') == filter_cat]
            
            # Lọc theo tiểu mục
            if filter_sub != "Tất cả":
                filtered_prods = [p for p in filtered_prods if p.get('sub_category') == filter_sub]
            
            # Lọc theo HOT
            if filter_hot:
                filtered_prods = [p for p in filtered_prods if p.get('is_hot', False)]
            
            # Sắp xếp
            if sort_by == "Tên A-Z":
                filtered_prods.sort(key=lambda x: x.get('name', '').lower())
            elif sort_by == "Tên Z-A":
                filtered_prods.sort(key=lambda x: x.get('name', '').lower(), reverse=True)
            elif sort_by == "Giá tăng":
                filtered_prods.sort(key=lambda x: x.get('rental_price_day', 0))
            elif sort_by == "Giá giảm":
                filtered_prods.sort(key=lambda x: x.get('rental_price_day', 0), reverse=True)
            elif sort_by == "Mới nhất":
                filtered_prods.reverse()  # Giả sử API trả về theo thứ tự cũ nhất trước
            
            # XUẤT EXCEL
            col_info, col_export = st.columns([3, 1])
            with col_info:
                st.text(f"📊 Hiển thị: {len(filtered_prods)}/{len(prods)} sản phẩm")
            with col_export:
                if st.button("📥 XUẤT EXCEL", use_container_width=True):
                    # Tạo DataFrame
                    export_data = []
                    for p in filtered_prods:
                        export_data.append({
                            "Mã SP": p.get('code', ''),
                            "Tên sản phẩm": p.get('name', ''),
                            "Danh mục": p.get('category', ''),
                            "Tiểu mục": p.get('sub_category', ''),
                            "Giá thuê/ngày": p.get('rental_price_day', 0),
                            "Giá thuê/tuần": p.get('rental_price_week', 0),
                            "Giá mua": p.get('purchase_price', 0),
                            "Loại vải": p.get('fabric_type', ''),
                            "Màu sắc": p.get('color', ''),
                            "Size": p.get('recommended_size', ''),
                            "HOT": "Có" if p.get('is_hot', False) else "Không",
                            "Giới tính": p.get('gender', '')
                        })
                    
                    df = pd.DataFrame(export_data)
                    
                    # Tạo file Excel trong memory
                    from io import BytesIO
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False, sheet_name='Sản phẩm')
                    output.seek(0)
                    
                    # Download button
                    st.download_button(
                        label="💾 Tải xuống",
                        data=output,
                        file_name=f"danh_sach_san_pham_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            
            st.markdown("---")
            h1, h2, h3, h4 = st.columns([1, 2, 1, 1])
            h1.write("**ẢNH**")
            h2.write("**THÔNG TIN**")
            h3.write("**GIÁ THUÊ**")
            h4.write("**HÀNH ĐỘNG**")
            st.markdown("---")
            
            for p in filtered_prods:
                edit_key = f"edit_{p['id']}"
                is_editing = st.session_state.get(edit_key, False)
                
                with st.container():
                    if is_editing:
                        with st.form(f"form_edit_{p['id']}"):
                            c1, c2, c3, c4 = st.columns([1, 2, 1, 1])
                            with c1:
                                st.image(lay_url_anh(p['image_url']), use_container_width=True)
                                new_img = st.file_uploader("Đổi ảnh đại diện (Váy Mẫu 1)", type=["jpg", "png", "jpeg", "webp"], key=f"u_{p['id']}")
                                
                                st.markdown("**📸 4 Ảnh mẫu hiện tại:**")
                                st.caption("Mẫu 1 = Ảnh đại diện")
                                current_gallery = p.get('gallery_images', [])
                                if current_gallery:
                                    # Hiển thị ảnh đại diện + 3 ảnh mẫu
                                    st.image(lay_url_anh(p['image_url']), caption="Mẫu 1 (Đại diện)", use_container_width=True)
                                    for idx, g in enumerate(current_gallery[1:4]):  # Bỏ qua ảnh đầu (trùng với đại diện)
                                        st.image(lay_url_anh(g), caption=f"Mẫu {idx+2}", use_container_width=True)
                                else:
                                    st.caption("Chưa có ảnh mẫu")
                                
                                st.markdown("**🔄 Cập nhật 3 ảnh mẫu còn lại:**")
                                st.caption("Mẫu 1 = Ảnh đại diện ở trên")
                                edit_mau_2 = st.file_uploader("Váy Mẫu 2", type=["jpg", "png", "jpeg", "webp"], key=f"em2_{p['id']}")
                                edit_mau_3 = st.file_uploader("Váy Mẫu 3", type=["jpg", "png", "jpeg", "webp"], key=f"em3_{p['id']}")
                                edit_mau_4 = st.file_uploader("Váy Mẫu 4", type=["jpg", "png", "jpeg", "webp"], key=f"em4_{p['id']}")
                                
                                st.caption("💡 Chỉ upload ảnh nào muốn thay đổi. Để trống = giữ nguyên ảnh cũ")
                            with c2:
                                new_name = st.text_input("Tên", value=p['name'])
                                new_code = st.text_input("Mã", value=p['code'])
                                new_cat = st.selectbox("Danh mục", ["wedding_modern", "vest", "aodai"], 
                                                     index=["wedding_modern", "vest", "aodai"].index(p['category']) if p['category'] in ["wedding_modern", "vest", "aodai"] else 0,
                                                     key=f"cat_{p['id']}")
                                
                                # Tiểu mục động theo danh mục
                                sub_options_edit = {
                                    "wedding_modern": ["", "xoe", "duoi_ca", "ngan"],
                                    "vest": ["", "hien_dai", "han_quoc"],
                                    "aodai": ["", "nam", "nu"],
                                }
                                sub_labels_edit = {
                                    "": "-- Chọn tiểu mục --",
                                    "xoe": "👗 Váy Xòe", "duoi_ca": "👗 Váy Đuôi Cá", "ngan": "👗 Váy Ngắn",
                                    "hien_dai": "🤵 Vest Hiện Đại", "han_quoc": "🤵 Vest Hàn Quốc",
                                    "nam": "👔 Áo Dài Nam", "nu": "👘 Áo Dài Nữ",
                                }
                                current_sub = p.get('sub_category', '')
                                sub_opts = sub_options_edit.get(new_cat, [""])
                                sub_idx = sub_opts.index(current_sub) if current_sub in sub_opts else 0
                                new_sub = st.selectbox("Tiểu mục", sub_opts, index=sub_idx,
                                                      format_func=lambda x: sub_labels_edit.get(x, x),
                                                      key=f"sub_{p['id']}")

                            with c3:
                                new_price = st.number_input("Giá thuê ngày", value=float(p['rental_price_day']))
                                new_price_buy = st.number_input("Giá mua", value=float(p.get('purchase_price', 0)))
                                new_hot = st.checkbox("Hot", value=p.get('is_hot', False), key=f"hot_{p['id']}")
                                new_so_luong = st.number_input("Số lượng", min_value=0, value=int(p.get('so_luong', 10)), key=f"sl_{p['id']}")
                                new_het_hang = st.checkbox("Hết hàng", value=p.get('het_hang', False), key=f"hh_{p['id']}")
                                st.markdown("---")
                                new_fabric = st.text_input("Loại vải", value=p.get('fabric_type', ''))
                                new_color = st.text_input("Màu sắc", value=p.get('color', ''))
                                # Chuyển size từ string thành list
                                current_sizes = [s.strip() for s in (p.get('recommended_size', '') or '').split(',') if s.strip()]
                                all_sizes = ["XS", "S", "M", "L", "XL", "XXL", "Free Size"]
                                new_size_list = st.multiselect("Size có sẵn", 
                                                              options=all_sizes,
                                                              default=[s for s in current_sizes if s in all_sizes],
                                                              key=f"size_{p['id']}")
                                new_size = ", ".join(new_size_list) if new_size_list else "Đủ size"
                                new_makeup = st.text_area("Tông makeup", value=p.get('makeup_tone', ''))
                            with c4:
                                if st.form_submit_button("LƯU"):
                                    img_url = p['image_url']
                                    if new_img:
                                        uploaded = upload_image(new_img)
                                        if uploaded: img_url = uploaded
                                    
                                    # Xử lý 3 ảnh mẫu (Mẫu 2, 3, 4)
                                    # Gallery = [ảnh đại diện, mẫu 2, mẫu 3, mẫu 4, ...]
                                    gallery_urls = [img_url]  # Mẫu 1 = ảnh đại diện
                                    new_mau_images = [edit_mau_2, edit_mau_3, edit_mau_4]
                                    old_gallery = p.get('gallery_images', [])
                                    
                                    # Xử lý 3 ảnh mẫu còn lại
                                    for idx, mau_img in enumerate(new_mau_images):
                                        if mau_img:
                                            u = upload_image(mau_img)
                                            if u: 
                                                gallery_urls.append(u)
                                                st.success(f"✅ Đã cập nhật Váy Mẫu {idx+2}")
                                        else:
                                            # Giữ ảnh cũ nếu không upload mới (bỏ qua ảnh đầu vì đó là ảnh đại diện)
                                            if idx + 1 < len(old_gallery):
                                                gallery_urls.append(old_gallery[idx + 1])
                                    
                                    # Thêm các ảnh bổ sung còn lại (nếu có)
                                    if len(old_gallery) > 4:
                                        gallery_urls.extend(old_gallery[4:])
                                    
                                    up_data = {
                                        "name": new_name, "code": new_code, "category": new_cat, "sub_category": new_sub,
                                        "rental_price_day": new_price, "image_url": img_url,
                                        "gallery_images": gallery_urls,
                                        "is_hot": new_hot, "gender": p['gender'],
                                        "purchase_price": new_price_buy,
                                        "rental_price_week": p.get('rental_price_week', new_price * 5),
                                        "fabric_type": new_fabric, "color": new_color,
                                        "recommended_size": new_size, "makeup_tone": new_makeup,
                                        "so_luong": new_so_luong, "het_hang": new_het_hang
                                    }
                                    if call_api("PUT", f"/api/san_pham/{p['id']}", data=up_data):
                                        st.session_state[edit_key] = False
                                        st.toast(f"Đã cập nhật sản phẩm (4 ảnh mẫu)")
                                        st.rerun()
                                if st.form_submit_button("HỦY"):
                                    st.session_state[edit_key] = False
                                    st.rerun()
                    else:
                        c1, c2, c3, c4 = st.columns([1, 2, 1, 1])
                        with c1:
                            st.image(lay_url_anh(p['image_url']), use_container_width=True)
                        with c2:
                            st.write(f"**{p['code']}**")
                            st.write(p['name'])
                            if p.get('is_hot'): st.caption("🔥 Sản phẩm Hot")
                        with c3:
                            st.write(f"**{p['rental_price_day']:,.0f}đ**")
                        with c4:
                            b_edit, b_del = st.columns(2)
                            if b_edit.button("SỬA", key=f"btn_edit_{p['id']}"):
                                st.session_state[edit_key] = True
                                st.rerun()
                            if b_del.button("XÓA", key=f"dp_{p['id']}"):
                                if call_api("DELETE", f"/api/san_pham/{p['id']}"):
                                    st.toast("Đã xóa sản phẩm")
                                    st.rerun()
                    st.markdown("<div style='border-bottom: 1px solid #222; margin: 10px 0;'></div>", unsafe_allow_html=True)

def ui_thu_vien():
    st.header("Quản lý Thư viện")
    t1, t2 = st.tabs(["DANH SÁCH", "THÊM MỚI"])
    with t2:
        img_file = st.file_uploader("Chọn ảnh")
        if st.button("TẢI LÊN"):
            url = upload_image(img_file)
            if url:
                if call_api("POST", "/api/thu_vien/", data={"image_url": url, "title": "", "order": 0}):
                    st.toast("Đã tải ảnh lên thư viện")
                    st.rerun()
    with t1:
        gal = call_api("GET", "/api/thu_vien/", clear_cache=False)
        if gal:
            cols = st.columns(4)
            for idx, item in enumerate(gal):
                with cols[idx % 4]:
                    st.image(lay_url_anh(item['image_url']), use_container_width=True)
                    if st.button("XÓA", key=f"dg_{item['id']}"):
                        if call_api("DELETE", f"/api/thu_vien/{item['id']}"):
                            st.toast("Đã xóa ảnh")
                            st.rerun()

def ui_dich_vu_chuyen_gia():
    st.header("Chuyên gia & Dịch vụ")
    t_ex, t_sv = st.tabs(["CHUYÊN GIA", "GÓI DỊCH VỤ"])
    with t_ex:
        with st.expander("THÊM CHUYÊN GIA"):
            with st.form("add_ex"):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("Tên chuyên gia")
                    title = st.text_input("Danh hiệu (VD: Chuyên viên Makeup)")
                    category = st.selectbox("Loại chuyên gia", ["makeup", "photo"], format_func=lambda x: "💄 Trang điểm" if x == "makeup" else "📸 Quay chụp")
                with col2:
                    years_exp = st.number_input("Số năm kinh nghiệm", min_value=1, value=3)
                    price = st.number_input("Giá booking (VNĐ)", min_value=100000, value=1000000, step=100000)
                    location = st.text_input("Khu vực làm việc", value="Hà Nội")
                level = st.selectbox("Cấp bậc", ["senior", "master", "top_artist"], format_func=lambda x: {"senior": "Senior", "master": "Master", "top_artist": "Top Artist"}[x])
                is_top = st.checkbox("Đánh dấu là TOP Artist (nổi bật)")
                img_f = st.file_uploader("Ảnh đại diện")
                if st.form_submit_button("THÊM CHUYÊN GIA"):
                    url = upload_image(img_f)
                    if url:
                        data = {
                            "name": name, "title": title, "image_url": url, 
                            "years_experience": years_exp, "brides_count": years_exp * 50,
                            "category": category, "level": level, 
                            "location": location, "price": price, "is_top": is_top,
                            "specialties": ["Cưới", "Sự kiện"]
                        }
                        if call_api("POST", "/api/dich_vu/chuyen_gia", data=data):
                            st.toast("Đã thêm chuyên gia mới!")
                            st.rerun()
        exps = call_api("GET", "/api/dich_vu/chuyen_gia", clear_cache=False)
        if exps:
            for e in exps:
                edit_key_ex = f"edit_ex_{e['id']}"
                is_editing_ex = st.session_state.get(edit_key_ex, False)
                with st.container(border=True):
                    if is_editing_ex:
                        with st.form(f"edit_ex_form_{e['id']}"):
                            c1, c2 = st.columns([1, 2])
                            with c1:
                                st.image(lay_url_anh(e['image_url']))
                                new_img_ex = st.file_uploader("Đổi ảnh", type=["jpg", "png"], key=f"ue_{e['id']}")
                            with c2:
                                en_name = st.text_input("Tên", value=e['name'])
                                en_title = st.text_input("Danh hiệu", value=e['title'])
                                en_cat = st.selectbox("Loại", ["makeup", "photo"], index=0 if e.get('category') == 'makeup' else 1)
                                en_level = st.selectbox("Level", ["senior", "master", "top_artist"], index=0)
                                en_loc = st.text_input("Khu vực", value=e.get('location', 'Hà Nội'))
                                en_price = st.number_input("Giá (Booking)", value=float(e.get('price', 1000000)))
                                en_top = st.checkbox("Top Artist", value=e.get('is_top', False))
                            if st.form_submit_button("LƯU"):
                                img_url = e['image_url']
                                if new_img_ex:
                                    u = upload_image(new_img_ex); 
                                    if u: img_url = u
                                up_data = {"name": en_name, "title": en_title, "image_url": img_url, "category": en_cat, "level": en_level, "location": en_loc, "price": en_price, "is_top": en_top, "years_experience": e['years_experience'], "brides_count": e['brides_count']}
                                if call_api("PUT", f"/api/dich_vu/chuyen_gia/{e['id']}", data=up_data):
                                    st.session_state[edit_key_ex] = False; st.toast("Đã cập nhật"); st.rerun()
                    else:
                        c1, c2, c3, c4 = st.columns([1, 2, 1, 1])
                        with c1: st.image(lay_url_anh(e['image_url']))
                        with c2: st.write(f"**{e['name']}**"); st.caption(e['title'])
                        with c3: st.write(f"{float(e.get('price', 1000000)):,.0f}đ")
                        with c4:
                            if st.button("SỬA", key=f"e_ex_{e['id']}"): st.session_state[edit_key_ex] = True; st.rerun()
                            if st.button("XOÁ", key=f"dex_{e['id']}"):
                                if call_api("DELETE", f"/api/dich_vu/chuyen_gia/{e['id']}"): st.toast("Đã xóa"); st.rerun()
    with t_sv:
        svs = call_api("GET", "/api/dich_vu/", clear_cache=False)
        if svs:
            for s in svs:
                with st.container(border=True):
                    st.write(f"**{s['name']}**")
                    if st.button("XÓA", key=f"d_sv_{s['id']}"):
                        if call_api("DELETE", f"/api/dich_vu/{s['id']}"): st.toast("Đã xóa"); st.rerun()

def ui_tu_van_khach_hang():
    st.header("Trò chuyện hỗ trợ khách hàng")
    st.markdown("""
        <style>
        .chat-container { display: flex; flex-direction: column; gap: 10px; padding: 20px; background: #111; border-radius: 8px; height: 500px; overflow-y: auto; border: 1px solid #333; }
        .msg { max-width: 80%; padding: 8px 12px; border-radius: 12px; font-size: 0.9em; line-height: 1.4; }
        .msg-user { align-self: flex-start; background: #222; color: #eee; border: 1px solid #444; }
        .msg-admin { align-self: flex-end; background: #ffffff; color: #000; }
        .chat-time { font-size: 0.7em; opacity: 0.6; margin-top: 4px; }
        </style>
    """, unsafe_allow_html=True)
    col_users, col_chat = st.columns([1, 2])
    with col_users:
        sessions = call_api("GET", "/api/chat/admin/cac_phien_chat", clear_cache=False)
        selected_user_id = st.session_state.get("selected_chat_user", None)
        if sessions:
            for s in sessions:
                if st.button(f"{s['full_name'] or s['username']}", key=f"user_chat_{s['id']}", use_container_width=True):
                    st.session_state.selected_chat_user = s['id']
                    st.rerun()
    with col_chat:
        if selected_user_id:
            history = call_api("GET", f"/api/chat/admin/lich_su/{selected_user_id}", clear_cache=False)
            if history:
                chat_html = '<div class="chat-container">'
                for m in history:
                    cls = "msg-admin" if m["is_from_admin"] else "msg-user"
                    chat_html += f'<div class="msg {cls}">{m["tin_nhan"]}</div>'
                chat_html += '</div>'
                st.markdown(chat_html, unsafe_allow_html=True)
            with st.form("reply_form", clear_on_submit=True):
                reply_text = st.text_area("Nhập tin nhắn...")
                if st.form_submit_button("GỬI"):
                    if call_api("POST", f"/api/chat/admin/tra_loi/{selected_user_id}", data={"tin_nhan": reply_text}):
                        st.toast("Đã gửi"); st.rerun()

def ui_duyet_danh_gia():
    st.header("⏳ Quản lý Đánh giá chờ duyệt")
    
    # Nút refresh
    if st.button("🔄 Tải lại"):
        st.cache_data.clear()
        st.rerun()
    
    pending = call_api("GET", "/api/san_pham/admin/danh_gia_cho_duyet", clear_cache=False)
    
    if pending is None:
        st.error("Không thể kết nối API. Kiểm tra backend đang chạy.")
    elif len(pending) == 0:
        st.info("🎉 Không có đánh giá nào đang chờ duyệt!")
    else:
        st.success(f"Có {len(pending)} đánh giá đang chờ duyệt")
        for dg in pending:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{dg.get('user_name', 'Ẩn danh')}** - ⭐ {dg.get('rating', 0)}/5")
                    st.write(f"📦 Sản phẩm ID: {dg.get('product_id')}")
                    st.caption(dg.get('comment', 'Không có nhận xét'))
                    if dg.get('image_url'):
                        st.image(lay_url_anh(dg['image_url']), width=100)
                with col2:
                    if st.button(f"✅ Duyệt", key=f"duyet_{dg['id']}"):
                        if call_api("POST", f"/api/san_pham/admin/duyet_danh_gia/{dg['id']}"):
                            st.toast("Đã duyệt đánh giá!")
                            st.rerun()
                    if st.button(f"❌ Xóa", key=f"xoa_{dg['id']}"):
                        if call_api("DELETE", f"/api/san_pham/admin/xoa_danh_gia/{dg['id']}"):
                            st.toast("Đã xóa đánh giá!")
                            st.rerun()

def ui_doi_tac_khieu_nai():
    st.header("🤝 Quản lý Đối tác & Khiếu nại")
    tab1, tab2 = st.tabs(["HỒ SƠ ĐỐI TÁC", "KHIẾU NẠI KHÁCH HÀNG"])
    
    with tab1:
        apps = call_api("GET", "/api/doi_tac/admin/danh_sach")

        if not apps:
            st.info("Chưa có hồ sơ đối tác nào.")
        else:
            for app in apps:
                with st.container(border=True):
                    c1, c2 = st.columns([2, 1])
                    with c1:
                        st.write(f"**{app['full_name']}** ({app['partner_type']})")
                        st.write(f"📞 {app['phone']} | ✉️ {app['email']}")
                        st.write(f"💼 Kinh nghiệm: {app['experience']}")
                        if app['portfolio_url']: st.write(f"🔗 [Portfolio]({app['portfolio_url']})")
                        if app['cv_url']:
                            st.image(f"http://localhost:8000{app['cv_url']}", caption="Ảnh CV / Portfolio", width=300)
                    with c2:
                        curr_status = app['status']
                        st.write(f"Trạng thái hiện tại: **{curr_status}**")
                        new_status = st.selectbox("Cập nhật trạng thái", ["pending", "interviewing", "accepted", "rejected"], 
                                                index=["pending", "interviewing", "accepted", "rejected"].index(curr_status), key=f"status_{app['id']}")
                        reply = st.text_area("Phản hồi cho đối tác", key=f"reply_{app['id']}")
                        contract = ""
                        if new_status == "accepted":
                            contract = st.text_area("Nội dung hợp đồng & Điều khoản", value="CHƯƠNG TRÌNH HỢP TÁC IVIE...\n1. Trách nhiệm...\n2. Quyền lợi...", key=f"contract_{app['id']}")
                        
                        if st.button("CẬP NHẬT HỒ SƠ", key=f"btn_{app['id']}", type="primary"):
                            params = {"status": new_status, "reply": reply, "contract": contract}
                            try:
                                res = requests.post(f"{API_URL}/api/doi_tac/admin/{app['id']}/phe_duyet", params=params)
                                if res.status_code == 200:
                                    st.toast("Đã cập nhật!")
                                    st.cache_data.clear()
                                    st.rerun()
                                else:
                                    st.error(f"Lỗi API ({res.status_code}): {res.text}")
                            except Exception as e:
                                st.error(f"Lỗi kết nối: {e}")

    with tab2:
        complaints = call_api("GET", "/api/doi_tac/admin/khieu_nai")

        if not complaints:
            st.info("Không có khiếu nại nào.")
        else:
            for kn in complaints:
                with st.container(border=True):
                    st.write(f"**{kn['title']}** - Status: {kn['status']}")
                    st.write(f"Người gửi: {kn['customer_name']} ({kn['customer_phone']})")
                    st.write(f"Nội dung: {kn['content']}")
                    if kn['admin_reply']:
                        st.info(f"Đã phản hồi: {kn['admin_reply']}")
                    else:
                        rep = st.text_input("Câu trả lời của Admin", key=f"rep_kn_{kn['id']}")
                        if st.button("GỬI PHẢN HỒI", key=f"btn_kn_{kn['id']}"):
                            res = requests.post(f"{API_URL}/api/doi_tac/admin/khieu_nai/{kn['id']}/tra_loi", params={"reply": rep})
                            if res.status_code == 200:
                                st.toast("Đã phản hồi"); st.rerun()

def ui_blog():
    st.header("📰 Quản lý Blog & Tin tức")
    t1, t2 = st.tabs(["DANH SÁCH BÀI VIẾT", "THÊM BÀI VIẾT MỚI"])
    
    with t2:
        with st.form("new_blog"):
            title = st.text_input("Tiêu đề bài viết")
            category = st.selectbox("Danh mục", ["tips", "news", "wedding-story"], format_func=lambda x: {"tips": "💡 Mẹo cưới", "news": "📰 Tin tức", "wedding-story": "💕 Câu chuyện cưới"}[x])
            excerpt = st.text_area("Tóm tắt ngắn", height=80)
            content = st.text_area("Nội dung bài viết (hỗ trợ HTML)", height=300)
            img = st.file_uploader("Ảnh bìa", type=["jpg", "png", "webp"])
            is_published = st.checkbox("Xuất bản ngay", value=False)
            
            if st.form_submit_button("TẠO BÀI VIẾT"):
                img_url = upload_image(img) if img else None
                data = {
                    "title": title,
                    "excerpt": excerpt, 
                    "content": content,
                    "image_url": img_url,
                    "category": category,
                    "is_published": is_published
                }
                if call_api("POST", "/api/blog/", data=data):
                    st.toast("Đã tạo bài viết mới!")
                    st.rerun()
    
    with t1:
        posts = call_api("GET", "/api/blog/?published_only=false", clear_cache=False)
        if posts:
            for p in posts:
                with st.container(border=True):
                    c1, c2, c3 = st.columns([1, 3, 1])
                    with c1:
                        if p.get('image_url'):
                            st.image(lay_url_anh(p['image_url']), use_container_width=True)
                    with c2:
                        status_badge = "✅ Đã xuất bản" if p.get('is_published') else "📝 Bản nháp"
                        st.write(f"**{p['title']}** {status_badge}")
                        st.caption(f"📁 {p['category']} | 👁️ {p['views']} lượt xem")
                        st.text(p.get('excerpt', '')[:100] + "..." if p.get('excerpt') else "")
                    with c3:
                        if st.button("XÓA", key=f"del_blog_{p['id']}"):
                            if call_api("DELETE", f"/api/blog/{p['id']}"):
                                st.toast("Đã xóa bài viết")
                                st.rerun()
                        if not p.get('is_published'):
                            if st.button("XUẤT BẢN", key=f"pub_{p['id']}"):
                                data = {
                                    "title": p['title'], "excerpt": p.get('excerpt', ''),
                                    "content": p['content'], "image_url": p.get('image_url'),
                                    "category": p['category'], "is_published": True
                                }
                                if call_api("PUT", f"/api/blog/{p['id']}", data=data):
                                    st.toast("Đã xuất bản!")
                                    st.rerun()
        else:
            st.info("Chưa có bài viết nào.")

def ui_don_hang():
    st.header("🛒 Quản lý Đơn hàng")
    
    # Nút refresh
    if st.button("🔄 Làm mới danh sách"):
        st.cache_data.clear()
        st.rerun()
    
    # Lấy danh sách đơn hàng - không cache để luôn lấy dữ liệu mới nhất
    don_hang_list = call_api("GET", "/api/don_hang/", clear_cache=True)
    
    if not don_hang_list:
        st.info("Chưa có đơn hàng nào.")
        return
    
    # Bộ lọc
    col1, col2 = st.columns(2)
    with col1:
        search = st.text_input("🔍 Tìm kiếm", placeholder="Tên, SĐT, email...")
    with col2:
        status_filter = st.selectbox("Trạng thái", ["Tất cả", "Chờ xử lý", "Đang xử lý", "Đã giao", "Đã hủy"])
    
    # Lọc dữ liệu
    filtered = don_hang_list
    if search:
        filtered = [d for d in filtered if search.lower() in str(d).lower()]
    if status_filter == "Chờ xử lý":
        filtered = [d for d in filtered if d.get('status') == 'pending']
    elif status_filter == "Đang xử lý":
        filtered = [d for d in filtered if d.get('status') == 'processing']
    elif status_filter == "Đã giao":
        filtered = [d for d in filtered if d.get('status') == 'delivered']
    elif status_filter == "Đã hủy":
        filtered = [d for d in filtered if d.get('status') == 'cancelled']
    
    st.write(f"📦 Tổng: **{len(filtered)}** đơn hàng")
    
    # Hiển thị đơn hàng
    for dh in filtered:
        status = dh.get('status', 'pending')
        status_color = {
            'pending': '🟡',
            'processing': '🔵', 
            'shipped': '🟣',
            'delivered': '🟢',
            'cancelled': '🔴'
        }.get(status, '⚪')
        status_text = {
            'pending': 'Chờ xử lý',
            'processing': 'Đang xử lý',
            'shipped': 'Đang giao',
            'delivered': 'Đã giao',
            'cancelled': 'Đã hủy'
        }.get(status, status)
        
        with st.container(border=True):
            c1, c2, c3 = st.columns([3, 2, 1])
            with c1:
                st.write(f"**#{dh.get('id')}** - {dh.get('customer_name')}")
                st.write(f"📞 {dh.get('customer_phone')} | ✉️ {dh.get('customer_email')}")
                st.write(f"📍 {dh.get('shipping_address')}")
            with c2:
                st.write(f"💰 **{dh.get('total_amount', 0):,.0f}đ**")
                st.write(f"{status_color} {status_text}")
                # Ngày đặt
                order_date = dh.get('order_date', '')
                if order_date:
                    st.caption(f"🕐 {order_date[:16] if len(order_date) > 16 else order_date}")
            with c3:
                new_status = st.selectbox(
                    "Cập nhật",
                    ["pending", "processing", "shipped", "delivered", "cancelled"],
                    index=["pending", "processing", "shipped", "delivered", "cancelled"].index(status) if status in ["pending", "processing", "shipped", "delivered", "cancelled"] else 0,
                    key=f"status_{dh['id']}",
                    format_func=lambda x: {'pending': 'Chờ xử lý', 'processing': 'Đang xử lý', 'shipped': 'Đang giao', 'delivered': 'Đã giao', 'cancelled': 'Đã hủy'}.get(x, x),
                    label_visibility="collapsed"
                )
                if new_status != status:
                    if st.button("💾 Lưu", key=f"save_{dh['id']}"):
                        if call_api("PUT", f"/api/don_hang/{dh['id']}", data={"status": new_status}):
                            st.toast("Đã cập nhật trạng thái!")
                            st.rerun()

# --- Main Layout ---
if "Tổng quan" in choice:
    st.header("Tổng quan")
    # Fetch statistics from new API
    stats = call_api("GET", "/api/thong_ke/tong_quan", clear_cache=False)
    if stats:
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("🛍️ SẢN PHẨM", stats.get('tong_san_pham', 0))
        with c2: st.metric("📦 ĐƠN HÀNG", stats.get('tong_don_hang', 0))
        with c3: st.metric("👤 NGƯỜI DÙNG", stats.get('tong_nguoi_dung', 0))
        with c4: st.metric("📞 LIÊN HỆ MỚI", stats.get('lien_he_chua_xu_ly', 0))
        
        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("💰 DOANH THU", f"{stats.get('tong_doanh_thu', 0):,.0f}đ")
        with c2:
            st.metric("⏳ ĐƠN CHỜ XỬ LÝ", stats.get('don_hang_cho_xu_ly', 0))
    else:
        products = call_api("GET", "/api/san_pham/", clear_cache=False)
        contacts = call_api("GET", "/api/lien_he/", clear_cache=False)
        c1, c2 = st.columns(2)
        with c1: st.metric("TỔNG SẢN PHẨM", len(products) if products else 0)
        with c2: st.metric("LIÊN HỆ MỚI", len([c for c in (contacts or []) if c.get('status') == 'pending']))

elif "Liên hệ" in choice: ui_lien_he()
elif "Đơn hàng" in choice: ui_don_hang()
elif "Tư vấn" in choice: ui_tu_van_khach_hang()
elif "Duyệt Đánh Giá" in choice: ui_duyet_danh_gia()
elif "Banner" in choice: ui_banner()
elif "Sản phẩm" in choice: ui_san_pham()
elif "Đối tác" in choice: ui_doi_tac_khieu_nai()
elif "Thư viện" in choice: ui_thu_vien()
elif "Dịch vụ" in choice: ui_dich_vu_chuyen_gia()
elif "Blog" in choice: ui_blog()
elif "Nội dung Trang chủ" in choice:
    st.header("Nội dung Trang chủ")
    
    tab1, tab2, tab3 = st.tabs(["📖 Câu chuyện IVIE", "⭐ Dịch vụ Cao Cấp", "✨ Điểm nhấn"])
    
    # === TAB 1: CÂU CHUYỆN IVIE (about_us) ===
    with tab1:
        st.subheader("📖 Quản lý phần Câu chuyện IVIE")
        
        # Lấy dữ liệu hiện tại
        about_data = call_api("GET", "/api/noi_dung/gioi_thieu", clear_cache=False)
        
        with st.form("form_about"):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("**Ảnh hiện tại:**")
                if about_data and about_data.get('image_url'):
                    st.image(lay_url_anh(about_data['image_url']), use_container_width=True)
                else:
                    st.info("Chưa có ảnh")
                
                new_about_img = st.file_uploader("📷 Tải ảnh mới", type=["jpg", "png", "jpeg", "webp"], key="about_img")
                if new_about_img:
                    st.image(new_about_img, caption="Xem trước", use_container_width=True)
            
            with col2:
                about_title = st.text_input("Tiêu đề", value=about_data.get('title', 'Câu Chuyện Của IVIE') if about_data else 'Câu Chuyện Của IVIE')
                about_subtitle = st.text_input("Phụ đề", value=about_data.get('subtitle', 'Hơn 10 năm kinh nghiệm') if about_data else 'Hơn 10 năm kinh nghiệm')
                about_desc = st.text_area("Mô tả", value=about_data.get('description', '') if about_data else '', height=150)
                
                st.markdown("**Thống kê:**")
                c1, c2, c3 = st.columns(3)
                with c1:
                    stat1_num = st.text_input("Số 1", value=about_data.get('stat1_number', '500+') if about_data else '500+')
                    stat1_label = st.text_input("Nhãn 1", value=about_data.get('stat1_label', 'Cặp Đôi') if about_data else 'Cặp Đôi')
                with c2:
                    stat2_num = st.text_input("Số 2", value=about_data.get('stat2_number', '10+') if about_data else '10+')
                    stat2_label = st.text_input("Nhãn 2", value=about_data.get('stat2_label', 'Năm Kinh Nghiệm') if about_data else 'Năm Kinh Nghiệm')
                with c3:
                    stat3_num = st.text_input("Số 3", value=about_data.get('stat3_number', '100%') if about_data else '100%')
                    stat3_label = st.text_input("Nhãn 3", value=about_data.get('stat3_label', 'Hài Lòng') if about_data else 'Hài Lòng')
            
            if st.form_submit_button("💾 LƯU CÂU CHUYỆN", use_container_width=True):
                img_url = about_data.get('image_url', '') if about_data else ''
                if new_about_img:
                    uploaded = upload_image(new_about_img)
                    if uploaded:
                        img_url = uploaded
                
                update_data = {
                    "title": about_title,
                    "subtitle": about_subtitle,
                    "description": about_desc,
                    "image_url": img_url,
                    "stat1_number": stat1_num,
                    "stat1_label": stat1_label,
                    "stat2_number": stat2_num,
                    "stat2_label": stat2_label,
                    "stat3_number": stat3_num,
                    "stat3_label": stat3_label
                }
                
                if call_api("PUT", "/api/noi_dung/gioi_thieu", data=update_data):
                    st.success("✅ Đã cập nhật Câu chuyện IVIE!")
                    st.rerun()
    
    # === TAB 2: DỊCH VỤ CAO CẤP (home_highlights) ===
    with tab2:
        st.subheader("⭐ Quản lý 3 Dịch vụ Cao Cấp")
        st.caption("3 card dịch vụ hiển thị trên trang chủ")
        
        # Lấy dữ liệu điểm nhấn
        highlights = call_api("GET", "/api/noi_dung/diem_nhan", clear_cache=False)
        if not highlights:
            highlights = []
        
        # Đảm bảo có đủ 3 item
        while len(highlights) < 3:
            highlights.append({"id": None, "title": "", "description": "", "image_url": ""})
        
        service_names = ["📷 Nhiếp Ảnh Nghệ Thuật", "💄 Trang Điểm Cô Dâu", "👗 Váy Cưới Thiết Kế"]
        
        for idx, (hl, svc_name) in enumerate(zip(highlights[:3], service_names)):
            st.markdown(f"### {svc_name}")
            with st.form(f"form_highlight_{idx}"):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    if hl.get('image_url'):
                        st.image(lay_url_anh(hl['image_url']), use_container_width=True)
                    else:
                        st.info("Chưa có ảnh")
                    
                    new_hl_img = st.file_uploader(f"📷 Tải ảnh mới", type=["jpg", "png", "jpeg", "webp"], key=f"hl_img_{idx}")
                    if new_hl_img:
                        st.image(new_hl_img, caption="Xem trước", use_container_width=True)
                
                with col2:
                    hl_title = st.text_input("Tiêu đề", value=hl.get('title', ''), key=f"hl_title_{idx}")
                    hl_desc = st.text_area("Mô tả", value=hl.get('description', ''), key=f"hl_desc_{idx}", height=100)
                    hl_order = st.number_input("Thứ tự", value=hl.get('order', idx), key=f"hl_order_{idx}")
                
                if st.form_submit_button(f"💾 LƯU DỊCH VỤ {idx + 1}", use_container_width=True):
                    img_url = hl.get('image_url', '')
                    if new_hl_img:
                        uploaded = upload_image(new_hl_img)
                        if uploaded:
                            img_url = uploaded
                    
                    update_data = {
                        "title": hl_title,
                        "description": hl_desc,
                        "image_url": img_url,
                        "order": hl_order
                    }
                    
                    if hl.get('id'):
                        # Cập nhật
                        if call_api("PUT", f"/api/noi_dung/diem_nhan/{hl['id']}", data=update_data):
                            st.success(f"✅ Đã cập nhật {svc_name}!")
                            st.rerun()
                    else:
                        # Thêm mới
                        if call_api("POST", "/api/noi_dung/diem_nhan", data=update_data):
                            st.success(f"✅ Đã thêm {svc_name}!")
                            st.rerun()
            
            st.markdown("---")
    
    # === TAB 3: ĐIỂM NHẤN KHÁC ===
    with tab3:
        st.subheader("✨ Quản lý các điểm nhấn khác")
        st.info("Thêm các điểm nhấn bổ sung cho trang chủ")
        
        with st.form("form_new_highlight"):
            st.markdown("**Thêm điểm nhấn mới:**")
            new_title = st.text_input("Tiêu đề")
            new_desc = st.text_area("Mô tả")
            new_img = st.file_uploader("Ảnh", type=["jpg", "png", "jpeg", "webp"])
            new_order = st.number_input("Thứ tự", value=10)
            
            if st.form_submit_button("➕ THÊM ĐIỂM NHẤN"):
                img_url = ""
                if new_img:
                    img_url = upload_image(new_img) or ""
                
                if call_api("POST", "/api/noi_dung/diem_nhan", data={
                    "title": new_title,
                    "description": new_desc,
                    "image_url": img_url,
                    "order": new_order
                }):
                    st.success("✅ Đã thêm điểm nhấn mới!")
                    st.rerun()
        
        # Danh sách điểm nhấn hiện có
        st.markdown("### Danh sách điểm nhấn")
        all_highlights = call_api("GET", "/api/noi_dung/diem_nhan", clear_cache=False)
        if all_highlights:
            for hl in all_highlights:
                with st.container(border=True):
                    c1, c2, c3 = st.columns([1, 3, 1])
                    with c1:
                        if hl.get('image_url'):
                            st.image(lay_url_anh(hl['image_url']), use_container_width=True)
                    with c2:
                        st.write(f"**{hl.get('title', 'Không có tiêu đề')}**")
                        st.caption(hl.get('description', ''))
                    with c3:
                        if st.button("🗑️ XÓA", key=f"del_hl_{hl['id']}"):
                            if call_api("DELETE", f"/api/noi_dung/diem_nhan/{hl['id']}"):
                                st.success("Đã xóa!")
                                st.rerun()
        else:
            st.info("Chưa có điểm nhấn nào")
