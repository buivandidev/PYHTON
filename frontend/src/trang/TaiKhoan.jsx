import React, { useState, useEffect } from 'react';
import { useToast } from '../thanh_phan/Toast';
import { nguoiDungAPI } from '../api/nguoi_dung';
import NutBam from '../thanh_phan/NutBam';
import '../styles/auth.css';

const TaiKhoan = () => {
    const [user, setUser] = useState(null);
    const [donHangs, setDonHangs] = useState([]);
    const [activeTab, setActiveTab] = useState('profile');
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        full_name: '',
        email: '',
        phone: '',
        address: '',
        password: ''
    });
    const { addToast } = useToast();

    useEffect(() => {
        const savedUser = localStorage.getItem('ivie_user');
        const token = localStorage.getItem('ivie_token');
        if (savedUser) {
            const userData = JSON.parse(savedUser);
            setUser(userData);
            setFormData({
                full_name: userData.full_name || '',
                email: userData.email || '',
                phone: userData.phone || '',
                address: userData.address || '',
                password: ''
            });
        }
        if (token) {
            fetchOrders(token);
        }
    }, []);

    const fetchOrders = async (token) => {
        try {
            console.log("Fetching orders with token:", token);
            const res = await nguoiDungAPI.layDonHang(token);
            console.log("Orders response:", res.data);
            // Handle cả trường hợp res.data là array hoặc object
            const orders = Array.isArray(res.data) ? res.data : (res.data?.orders || res.data?.value || []);
            console.log("Parsed orders:", orders);
            setDonHangs(orders);
        } catch (error) {
            console.error("Lỗi lấy đơn hàng:", error);
            console.error("Error response:", error.response?.data);
            setDonHangs([]);
        }
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleUpdate = async (e) => {
        e.preventDefault();
        setLoading(true);
        const token = localStorage.getItem('ivie_token');
        try {
            const cleanedData = { ...formData };
            if (!cleanedData.password) delete cleanedData.password;

            const res = await nguoiDungAPI.capNhatProfile(cleanedData, token);
            localStorage.setItem('ivie_user', JSON.stringify(res.data));
            setUser(res.data);
            window.dispatchEvent(new Event('authChange'));
            addToast({ message: "Cập nhật thông tin thành công!", type: "success" });
        } catch (error) {
            addToast({ message: "Lỗi cập nhật thông tin.", type: "error" });
        } finally {
            setLoading(false);
        }
    };

    if (!user) return <div className="container" style={{ padding: '100px 0', textAlign: 'center' }}>Vui lòng đăng nhập để xem thông tin.</div>;

    // Debug: log khi render
    console.log("Rendering TaiKhoan, activeTab:", activeTab, "donHangs:", donHangs);

    return (
        <div className="auth-container" style={{ marginTop: '100px', maxWidth: '800px' }}>
            <div className="auth-card">
                <div className="account-tabs" style={{ display: 'flex', gap: '20px', marginBottom: '30px', borderBottom: '1px solid #eee' }}>
                    <button
                        onClick={() => setActiveTab('profile')}
                        style={{ padding: '10px 20px', background: 'none', border: 'none', borderBottom: activeTab === 'profile' ? '2px solid #d4af37' : 'none', color: activeTab === 'profile' ? '#d4af37' : '#666', fontWeight: 'bold', cursor: 'pointer' }}
                    >
                        Thông tin cá nhân
                    </button>
                    <button
                        onClick={() => setActiveTab('orders')}
                        style={{ padding: '10px 20px', background: 'none', border: 'none', borderBottom: activeTab === 'orders' ? '2px solid #d4af37' : 'none', color: activeTab === 'orders' ? '#d4af37' : '#666', fontWeight: 'bold', cursor: 'pointer' }}
                    >
                        Đơn hàng của tôi ({donHangs.length})
                    </button>
                </div>

                {activeTab === 'profile' ? (
                    <form onSubmit={handleUpdate} className="auth-form">
                        <div className="form-group">
                            <label>Họ và Tên</label>
                            <input name="full_name" value={formData.full_name} onChange={handleChange} />
                        </div>
                        <div className="form-group">
                            <label>Số điện thoại</label>
                            <input name="phone" value={formData.phone} onChange={handleChange} />
                        </div>
                        <div className="form-group">
                            <label>Địa chỉ</label>
                            <input name="address" value={formData.address} onChange={handleChange} />
                        </div>
                        <div className="form-group">
                            <label>Email</label>
                            <input name="email" value={formData.email} onChange={handleChange} />
                        </div>
                        <div className="form-group">
                            <label>Mật khẩu mới (để trống nếu không đổi)</label>
                            <input type="password" name="password" value={formData.password} onChange={handleChange} />
                        </div>
                        <NutBam type="submit" loading={loading} style={{ width: '100%' }}>
                            CẬP NHẬT THÔNG TIN
                        </NutBam>
                    </form>
                ) : (
                    <div className="order-history">
                        {donHangs && donHangs.length > 0 ? (
                            donHangs.map(order => (
                                <div key={order.id} style={{ padding: '15px', border: '1px solid #eee', borderRadius: '8px', marginBottom: '15px', background: '#fff' }}>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
                                        <span style={{ fontWeight: 'bold', color: '#333' }}>Mã đơn: #{order.id}</span>
                                        <span style={{ 
                                            color: order.status === 'delivered' ? '#28a745' : 
                                                   order.status === 'processing' ? '#007bff' : 
                                                   order.status === 'cancelled' ? '#dc3545' : '#d4af37',
                                            fontWeight: 'bold'
                                        }}>
                                            {order.status === 'pending' ? '⏳ Chờ xử lý' :
                                             order.status === 'processing' ? '🔄 Đang xử lý' :
                                             order.status === 'shipped' ? '🚚 Đang giao' :
                                             order.status === 'delivered' ? '✅ Đã giao' :
                                             order.status === 'cancelled' ? '❌ Đã hủy' : order.status}
                                        </span>
                                    </div>
                                    <div style={{ fontSize: '0.9rem', color: '#666', marginBottom: '5px' }}>
                                        📅 Ngày đặt: {order.order_date ? new Date(order.order_date).toLocaleDateString('vi-VN') : 'N/A'}
                                    </div>
                                    <div style={{ fontSize: '0.9rem', color: '#666', marginBottom: '5px' }}>
                                        📍 Địa chỉ: {order.shipping_address}
                                    </div>
                                    <div style={{ textAlign: 'right', fontWeight: 'bold', marginTop: '10px', color: '#d4af37', fontSize: '1.1rem' }}>
                                        Tổng: {(order.total_amount || 0).toLocaleString()}đ
                                    </div>
                                </div>
                            ))
                        ) : (
                            <p style={{ textAlign: 'center', color: '#666' }}>Bạn chưa có đơn hàng nào.</p>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
};

export default TaiKhoan;
