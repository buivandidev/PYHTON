import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import NutBam from '../thanh_phan/NutBam';
import '../styles/cart.css';

const GioHang = () => {
    const [cartItems, setCartItems] = useState([]);
    const [customerInfo, setCustomerInfo] = useState({
        name: '',
        phone: '',
        email: '',
        address: '',
        date: '',
        note: ''
    });
    const [isSubmitted, setIsSubmitted] = useState(false);

    useEffect(() => {
        const savedCart = JSON.parse(localStorage.getItem('ivie_cart') || '[]');
        setCartItems(savedCart);
    }, []);

    const updateQuantity = (id, delta, loai) => {
        const newCart = cartItems.map(item => {
            if (item.id === id && (item.loai || 'mua') === (loai || 'mua')) {
                const newQty = Math.max(1, (item.quantity || 1) + delta);
                // Giới hạn số lượng theo so_luong nếu có
                const maxQty = item.so_luong || 10;
                return { ...item, quantity: Math.min(newQty, maxQty) };
            }
            return item;
        });
        setCartItems(newCart);
        localStorage.setItem('ivie_cart', JSON.stringify(newCart));
    };

    const removeItem = (id, loai) => {
        const newCart = cartItems.filter(item => !(item.id === id && (item.loai || 'mua') === (loai || 'mua')));
        setCartItems(newCart);
        localStorage.setItem('ivie_cart', JSON.stringify(newCart));
    };

    const getOrderSummary = () => {
        const subtotal = cartItems.reduce((total, item) => {
            const price = item.price_to_use || item.rental_price_day;
            return total + (price * (item.quantity || 1));
        }, 0);

        let discountPercent = 0;
        let gift = null;

        if (subtotal >= 15000000) {
            discountPercent = 15;
            gift = "Bó hoa cưới cao cấp (Trị giá 1.000.000đ)";
        } else if (subtotal >= 10000000) {
            discountPercent = 10;
        } else if (subtotal >= 5000000) {
            discountPercent = 5;
        }

        const discountValue = (subtotal * discountPercent) / 100;
        const finalTotal = subtotal - discountValue;

        return { subtotal, discountPercent, discountValue, finalTotal, gift };
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const summary = getOrderSummary();
        console.log("Order submitted:", { customerInfo, cartItems, summary });
        setIsSubmitted(true);
        localStorage.removeItem('ivie_cart');
        setCartItems([]);
    };

    if (isSubmitted) {
        return (
            <div className="container" style={{ padding: '4rem 0', textAlign: 'center' }}>
                <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>🎉</div>
                <h2>Đặt Hàng Thành Công!</h2>
                <p>Cảm ơn bạn đã lựa chọn IVIE Studio. Chúng tôi sẽ liên hệ lại sớm nhất.</p>
                <Link to="/">
                    <NutBam variant="primary" style={{ marginTop: '2rem' }}>Về Trang Chủ</NutBam>
                </Link>
            </div>
        );
    }

    if (cartItems.length === 0) {
        return (
            <div className="container" style={{ padding: '4rem 0', textAlign: 'center' }}>
                <h2>Giỏ Hàng Trống</h2>
                <p>Bạn chưa chọn sản phẩm nào.</p>
                <Link to="/san-pham">
                    <NutBam variant="primary" style={{ marginTop: '2rem' }}>Xem Sản Phẩm</NutBam>
                </Link>
            </div>
        );
    }

    return (
        <div className="cart-page section">
            <div className="container">
                <h1 className="section-title">Giỏ Hàng Của Bạn</h1>

                <div className="cart-grid">
                    <div className="cart-items">
                        {cartItems.map(item => (
                            <div key={`${item.id}-${item.loai || 'mua'}`} className="cart-item" style={item.loai === 'thue' ? {border: '2px solid #3b82f6', background: '#eff6ff'} : {}}>
                                {item.loai === 'thue' && (
                                    <div style={{
                                        position: 'absolute', top: '-10px', left: '10px',
                                        background: '#3b82f6', color: '#fff', padding: '4px 12px',
                                        borderRadius: '12px', fontSize: '0.75rem', fontWeight: '600'
                                    }}>
                                        🏷️ THUÊ {item.rental_days} NGÀY
                                    </div>
                                )}
                                {item.loai === 'mua' && (
                                    <div style={{
                                        position: 'absolute', top: '-10px', left: '10px',
                                        background: '#f97316', color: '#fff', padding: '4px 12px',
                                        borderRadius: '12px', fontSize: '0.75rem', fontWeight: '600'
                                    }}>
                                        🛒 MUA
                                    </div>
                                )}
                                <img src={item.image_url?.startsWith('http') ? item.image_url : `http://localhost:8000${item.image_url}`} alt={item.name} className="cart-item-img" onError={(e) => e.target.src = 'https://placehold.co/100'} />
                                <div className="cart-item-info">
                                    <h3>{item.name}</h3>
                                    <p className="item-code">#{item.code}</p>
                                    {item.so_luong !== undefined && item.so_luong <= 3 && (
                                        <p style={{color: '#d70018', fontSize: '0.85rem', fontWeight: '600', margin: '4px 0'}}>
                                            ⚠️ Chỉ còn {item.so_luong} sản phẩm
                                        </p>
                                    )}
                                    {item.loai === 'thue' ? (
                                        <p className="item-price" style={{color: '#3b82f6', fontWeight: '700'}}>
                                            {new Intl.NumberFormat('vi-VN').format(item.price_to_use || item.rental_price_day * item.rental_days)}đ 
                                            <span style={{fontSize: '0.8rem', fontWeight: '400'}}> / {item.rental_days} ngày</span>
                                        </p>
                                    ) : (
                                        <p className="item-price" style={{color: '#f97316', fontWeight: '700'}}>
                                            {new Intl.NumberFormat('vi-VN').format(item.purchase_price || item.price_to_use)}đ
                                        </p>
                                    )}
                                </div>
                                <div className="cart-item-actions">
                                    <div className="quantity-control">
                                        <button onClick={() => updateQuantity(item.id, -1, item.loai)}>-</button>
                                        <span>{item.quantity || 1}</span>
                                        <button 
                                            onClick={() => updateQuantity(item.id, 1, item.loai)}
                                            disabled={(item.quantity || 1) >= (item.so_luong || 10)}
                                            style={{opacity: (item.quantity || 1) >= (item.so_luong || 10) ? 0.5 : 1, cursor: (item.quantity || 1) >= (item.so_luong || 10) ? 'not-allowed' : 'pointer'}}
                                        >+</button>
                                    </div>
                                    <button onClick={() => removeItem(item.id, item.loai)} className="remove-btn">Xóa</button>
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className="cart-summary">
                        <h3>Thông Tin Đặt Hàng</h3>
                        <form onSubmit={handleSubmit} className="order-form">
                            <div className="form-group">
                                <label>Họ và Tên</label>
                                <input
                                    type="text"
                                    required
                                    value={customerInfo.name}
                                    onChange={e => setCustomerInfo({ ...customerInfo, name: e.target.value })}
                                />
                            </div>
                            <div className="form-group">
                                <label>Email</label>
                                <input
                                    type="email"
                                    required
                                    value={customerInfo.email}
                                    onChange={e => setCustomerInfo({ ...customerInfo, email: e.target.value })}
                                />
                            </div>
                            <div className="form-group">
                                <label>Số Điện Thoại</label>
                                <input
                                    type="tel"
                                    required
                                    value={customerInfo.phone}
                                    onChange={e => setCustomerInfo({ ...customerInfo, phone: e.target.value })}
                                />
                            </div>
                            <div className="form-group">
                                <label>Địa Chỉ Nhận Hàng</label>
                                <input
                                    type="text"
                                    required
                                    value={customerInfo.address}
                                    onChange={e => setCustomerInfo({ ...customerInfo, address: e.target.value })}
                                />
                            </div>
                            <div className="form-group">
                                <label>Ngày Dự Kiến</label>
                                <input
                                    type="date"
                                    required
                                    value={customerInfo.date}
                                    onChange={e => setCustomerInfo({ ...customerInfo, date: e.target.value })}
                                />
                            </div>
                            <div className="cart-total-details">
                                <div className="summary-row">
                                    <span>Tạm tính:</span>
                                    <span>{new Intl.NumberFormat('vi-VN').format(getOrderSummary().subtotal)}đ</span>
                                </div>

                                {getOrderSummary().discountPercent > 0 && (
                                    <div className="summary-row discount">
                                        <span>Giảm giá ({getOrderSummary().discountPercent}%):</span>
                                        <span>-{new Intl.NumberFormat('vi-VN').format(getOrderSummary().discountValue)}đ</span>
                                    </div>
                                )}

                                {getOrderSummary().gift && (
                                    <div className="summary-row gift">
                                        <span>Quà tặng:</span>
                                        <span>{getOrderSummary().gift}</span>
                                    </div>
                                )}

                                <div className="summary-row final">
                                    <span>Tổng cộng:</span>
                                    <span className="total-price">{new Intl.NumberFormat('vi-VN').format(getOrderSummary().finalTotal)}đ</span>
                                </div>
                            </div>
                            <NutBam variant="primary" type="submit" className="btn-block">GỬI YÊU CẦU</NutBam>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default GioHang;
