import api from './khach_hang';

export const nguoiDungAPI = {
    dangKy: (duLieu) => api.post('/api/nguoi_dung/dang_ky', duLieu),
    dangNhap: (duLieu) => api.post('/api/nguoi_dung/dang_nhap', duLieu),
    layDonHang: (token) => api.get('/api/nguoi_dung/don_hang', {
        headers: { 'Authorization': `Bearer ${token}` }
    }),
    capNhatProfile: (duLieu, token) => api.put('/api/nguoi_dung/cap_nhat', duLieu, {
        headers: { 'Authorization': `Bearer ${token}` }
    }),
    kiemTraGiamGia: (token) => api.post('/api/nguoi_dung/kiem_tra_giam_gia', {}, {
        headers: { 'Authorization': `Bearer ${token}` }
    }),
};
