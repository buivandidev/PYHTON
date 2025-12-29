import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Products API (API Sản phẩm)
export const sanPhamAPI = {
    layTatCa: (params) => api.get('/api/san_pham', { params, headers: { 'Cache-Control': 'no-cache' } }),
    layTheoId: (id) => api.get(`/api/san_pham/${id}`, { headers: { 'Cache-Control': 'no-cache' } }),
    layDanhGia: (id) => api.get(`/api/san_pham/${id}/danh_gia`),
    guiDanhGia: (id, formData) => api.post(`/api/san_pham/${id}/danh_gia`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
    }),

    // Admin Review Moderation
    adminLayDanhGiaChoDuyet: () => api.get('/api/san_pham/admin/danh_gia_cho_duyet'),
    adminDuyetDanhGia: (id) => api.post(`/api/san_pham/admin/duyet_danh_gia/${id}`),
    adminXoaDanhGia: (id) => api.delete(`/api/san_pham/admin/xoa_danh_gia/${id}`),
};

// Services API (API Dịch vụ)
export const dichVuAPI = {
    layTatCa: () => api.get('/api/dich_vu'),
    layChuyenGia: () => api.get('/api/dich_vu/chuyen_gia'),
    layChuyenGiaTheoId: (id) => api.get(`/api/dich_vu/chuyen_gia/${id}`),
};

// Contact API (API Liên hệ)
export const lienHeAPI = {
    gui: (duLieu) => api.post('/api/lien_he', duLieu),
    datLich: (duLieu) => api.post('/api/lien_he/dat_lich', duLieu),
};

// Banner API
export const bannerAPI = {
    layTatCa: () => api.get('/api/banner/'),
};

// Gallery API (API Thư viện)
export const thuVienAPI = {
    layTatCa: () => api.get('/api/thu_vien/'),
};

// Partner API (API Đối tác)
export const doiTacAPI = {
    dangKy: (duLieu, user_id) => api.post(`/api/doi_tac/dang_ky?user_id=${user_id}`, duLieu),
    layHoSo: (user_id) => api.get(`/api/doi_tac/ho_so/${user_id}`),
    adminLayDanhSach: () => api.get('/api/doi_tac/admin/danh_sach'),
    adminPheDuyet: (id, params) => api.post(`/api/doi_tac/admin/${id}/phe_duyet`, null, { params }),
};

// Complaint API (API Khiếu nại)
export const khieuNaiAPI = {
    gui: (duLieu, user_id) => api.post(`/api/doi_tac/khieu_nai${user_id ? `?user_id=${user_id}` : ''}`, duLieu),
    adminLayDanhSach: () => api.get('/api/doi_tac/admin/khieu_nai'),
    adminTraLoi: (id, reply) => api.post(`/api/doi_tac/admin/khieu_nai/${id}/tra_loi?reply=${encodeURIComponent(reply)}`),
};

// Order API (API Đơn hàng)
export const donHangAPI = {
    tao: (duLieu) => api.post('/api/don_hang/', duLieu),
    layTatCa: () => api.get('/api/don_hang/'),
    layTheoId: (id) => api.get(`/api/don_hang/${id}`),
    capNhat: (id, duLieu) => api.put(`/api/don_hang/${id}`, duLieu),
};


// Nội dung trang chủ
export const noiDungAPI = {
    layGioiThieu: () => api.get('/api/noi_dung/gioi_thieu'),
    layDiemNhan: () => api.get('/api/noi_dung/diem_nhan'),
};

// Helper to get image URL
export const layUrlHinhAnh = (duongDan) => {
    if (!duongDan) return 'https://placehold.co/400x600/e5e5e5/333?text=No+Image';
    if (duongDan.startsWith('http')) return duongDan;
    // Nếu là ảnh trong thư mục public của frontend
    if (duongDan.startsWith('/images')) return duongDan;
    // Ngược lại, giả định là ảnh từ backend api
    return `${API_BASE_URL}${duongDan}`;
};

export default api;
