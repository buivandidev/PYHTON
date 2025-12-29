import { useState, useEffect } from 'react';
import { sanPhamAPI, lienHeAPI, layUrlHinhAnh } from '../api/khach_hang';
import NutBam from '../thanh_phan/NutBam';
import { useToast } from '../thanh_phan/Toast';
import '../styles/combo.css';

export const DANH_SACH_GOI = [
    {
        id: 1,
        ten: 'COMBO KHỞI ĐẦU',
        gia: 2000000,
        gioi_han: 2,
        mo_ta: 'Gói cơ bản cho các cặp đôi',
        quyen_loi: [
            '2 Váy Cưới tùy chọn',
            '2 Bộ Vest Nam tùy chọn',
            'Miễn phí giặt ủi',
            'Hỗ trợ chỉnh sửa kích cỡ'
        ],
        hinh_anh: 'https://images.unsplash.com/photo-1594552072238-b8a33785b261?auto=format&fit=crop&q=80&w=600'
    },
    {
        id: 2,
        ten: 'COMBO TIẾT KIỆM',
        gia: 5000000,
        gioi_han: 5,
        mo_ta: 'Sự lựa chọn phổ biến nhất',
        quyen_loi: [
            '5 Váy Cưới tùy chọn',
            '5 Bộ Vest Nam tùy chọn',
            'Phụ kiện đi kèm miễn phí',
            'Giữ đồ trong 3 ngày'
        ],
        hinh_anh: 'https://images.unsplash.com/photo-1583939003579-730e3918a45a?auto=format&fit=crop&q=80&w=600',
        noi_bat: true
    },
    {
        id: 3,
        ten: 'COMBO VIP TOÀN NĂNG',
        gia: 15000000,
        gioi_han: 7,
        mo_ta: 'Trọn gói ngày cưới hoàn hảo',
        quyen_loi: [
            '7 Váy Cưới tùy chọn (bao gồm dòng Luxury)',
            '7 Bộ Vest Nam cao cấp',
            'Trang điểm cô dâu & mẹ uyên ương',
            'Chụp ảnh Pre-wedding & Tiệc cưới',
            'Quay phim phóng sự cưới',
            'Miễn phí chỉnh sửa ảnh & dựng phim'
        ],
        hinh_anh: 'https://images.unsplash.com/photo-1511285560982-1351cdeb9821?auto=format&fit=crop&q=80&w=600'
    }
];

const ChonCombo = () => {
    const [buoc, setBuoc] = useState(1);
    const [goiDaChon, setGoiDaChon] = useState(null);
    const [vayNu, setVayNu] = useState([]);
    const [vestNam, setVestNam] = useState([]);
    const [chonNu, setChonNu] = useState([]);
    const [chonNam, setChonNam] = useState([]);
    const [dangTai, setDangTai] = useState(false);
    const { addToast } = useToast();

    // Form state
    const [thongTin, setThongTin] = useState({
        ten: '', email: '', sdt: '', ngayCuoi: '', ghiChu: ''
    });
    const [trangThaiGui, setTrangThaiGui] = useState('idle');

    useEffect(() => {
        taiDuLieu();
    }, []);

    const taiDuLieu = async () => {
        setDangTai(true);
        try {
            const [nuRes, namRes] = await Promise.all([
                sanPhamAPI.layTatCa({ gioi_tinh: 'female' }),
                sanPhamAPI.layTatCa({ gioi_tinh: 'male' })
            ]);
            setVayNu(nuRes.data);
            setVestNam(namRes.data);
        } catch (error) {
            console.error('Lỗi tải sản phẩm:', error);
        } finally {
            setDangTai(false);
        }
    };

    const chonGoiDichVu = (goi) => {
        setGoiDaChon(goi);
        setChonNu([]); // Reset selection when changing package
        setChonNam([]);
        setBuoc(2);
        window.scrollTo(0, 0);
    };

    const xuLyChon = (item, danhSachDaChon, setDanhSachDaChon) => {
        const daCo = danhSachDaChon.find(i => i.id === item.id);
        if (daCo) {
            setDanhSachDaChon(danhSachDaChon.filter(i => i.id !== item.id));
        } else {
            if (danhSachDaChon.length < goiDaChon.gioi_han) {
                setDanhSachDaChon([...danhSachDaChon, item]);
            } else {
                addToast({ message: `Gói ${goiDaChon.ten} chỉ được chọn tối đa ${goiDaChon.gioi_han} sản phẩm mỗi loại.`, type: 'info' });
            }
        }
    };

    const xuLyGui = async (e) => {
        e.preventDefault();
        setTrangThaiGui('sending');

        const sanPhamChon = [
            ...chonNu.map(i => `[Nữ] ${i.name} (#${i.code})`),
            ...chonNam.map(i => `[Nam] ${i.name} (#${i.code})`)
        ].join('\n');

        const noiDungTinNhan = `
YÊU CẦU ĐẶT COMBO: ${goiDaChon.ten.toUpperCase()}
Giá trị gói: ${new Intl.NumberFormat('vi-VN').format(goiDaChon.gia)}đ
---------------------------
Ngày cưới dự kiến: ${thongTin.ngayCuoi}

DANH SÁCH SẢN PHẨM ĐÃ CHỌN (${chonNu.length} Váy + ${chonNam.length} Vest):
${sanPhamChon}

Ghi chú thêm: ${thongTin.ghiChu}
        `.trim();

        try {
            await lienHeAPI.gui({
                name: thongTin.ten,
                email: thongTin.email,
                phone: thongTin.sdt,
                message: noiDungTinNhan
            });
            setTrangThaiGui('success');
        } catch (error) {
            console.error(error);
            setTrangThaiGui('error');
        }
    };

    const StepIndicator = () => (
        <div className="combo-steps">
            {[1, 2, 3, 4].map(s => (
                <div key={s} className={`step-indicator ${buoc === s ? 'active' : ''} ${buoc > s ? 'completed' : ''}`}>
                    <div className="step-number">{s}</div>
                    <span className="step-text">
                        {s === 1 ? 'Chọn Gói' : s === 2 ? 'Chọn Váy' : s === 3 ? 'Chọn Vest' : 'Xác nhận'}
                    </span>
                </div>
            ))}
        </div>
    );

    if (trangThaiGui === 'success') {
        return (
            <div className="combo-page">
                <div className="container" style={{ textAlign: 'center', paddingTop: '100px' }}>
                    <h2 style={{ color: 'green' }}>Đăng Ký Thành Công!</h2>
                    <p>Cảm ơn bạn đã lựa chọn gói <strong>{goiDaChon?.ten}</strong>.</p>
                    <p>Chúng tôi sẽ sớm liên hệ lại để xác nhận lịch thử đồ.</p>
                    <NutBam onClick={() => window.location.href = '/'} style={{ marginTop: '20px' }}>Về Trang Chủ</NutBam>
                </div>
            </div>
        );
    }

    return (
        <div className="combo-page">
            <section className="combo-hero">
                <div className="container">
                    <h1 className="page-title">Gói Dịch Vụ Cưới</h1>
                    <p className="page-subtitle">Giải pháp trọn gói, tiết kiệm tối đa</p>
                    <StepIndicator />
                </div>
            </section>

            <div className="combo-content">
                {/* BƯỚC 1: CHỌN GÓI */}
                {buoc === 1 && (
                    <div className="combo-intro fade-in">
                        <div className="pricing-grid">
                            {DANH_SACH_GOI.map(goi => (
                                <div key={goi.id} className={`pricing-card ${goi.noi_bat ? 'featured' : ''}`}>
                                    {goi.noi_bat && <div className="pricing-badge">BÁN CHẠY NHẤT</div>}
                                    <div className="pricing-image" style={{ backgroundImage: `url(${goi.hinh_anh})` }}></div>
                                    <div className="pricing-content">
                                        <h3 className="pricing-title">{goi.ten}</h3>
                                        <div className="pricing-price">{new Intl.NumberFormat('vi-VN').format(goi.gia)}đ</div>
                                        <p className="pricing-desc">{goi.mo_ta}</p>
                                        <ul className="pricing-features">
                                            {goi.quyen_loi.map((ql, idx) => (
                                                <li key={idx}>{ql}</li>
                                            ))}
                                        </ul>
                                        <NutBam
                                            variant="outline"
                                            className="btn-block"
                                            onClick={() => chonGoiDichVu(goi)}
                                        >
                                            CHỌN GÓI NÀY
                                        </NutBam>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* BƯỚC 2: CHỌN VÁY NỮ */}
                {buoc === 2 && (
                    <div className="selection-step fade-in">
                        <div className="selection-header">
                            <div>
                                <h3>Chọn Váy ({goiDaChon.gioi_han} mẫu)</h3>
                                <p style={{ fontSize: '14px', color: '#666' }}>Gói: {goiDaChon.ten}</p>
                            </div>
                            <span className="selection-counter">Đã chọn: {chonNu.length}/{goiDaChon.gioi_han}</span>
                        </div>
                        {dangTai ? <div className="loading">Đang tải sản phẩm...</div> : (
                            <div className="selection-grid">
                                {vayNu.map(sp => (
                                    <div
                                        key={sp.id}
                                        className={`selection-item ${chonNu.find(i => i.id === sp.id) ? 'selected' : ''}`}
                                        onClick={() => xuLyChon(sp, chonNu, setChonNu)}
                                    >
                                        <div className="selection-item-image">
                                            <img src={layUrlHinhAnh(sp.image_url)} alt={sp.name} />
                                        </div>
                                        <div className="selection-item-info">
                                            <h4>{sp.name}</h4>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                        <div className="combo-actions">
                            <NutBam variant="outline" onClick={() => setBuoc(1)}>CHỌN LẠI GÓI</NutBam>
                            <NutBam onClick={() => setBuoc(3)}>TIẾP TỤC: CHỌN VEST</NutBam>
                        </div>
                    </div>
                )}

                {/* BƯỚC 3: CHỌN VEST NAM */}
                {buoc === 3 && (
                    <div className="selection-step fade-in">
                        <div className="selection-header">
                            <div>
                                <h3>Chọn Vest ({goiDaChon.gioi_han} mẫu)</h3>
                                <p style={{ fontSize: '14px', color: '#666' }}>Gói: {goiDaChon.ten}</p>
                            </div>
                            <span className="selection-counter">Đã chọn: {chonNam.length}/{goiDaChon.gioi_han}</span>
                        </div>
                        {dangTai ? <div className="loading">Đang tải sản phẩm...</div> : (
                            <div className="selection-grid">
                                {vestNam.map(sp => (
                                    <div
                                        key={sp.id}
                                        className={`selection-item ${chonNam.find(i => i.id === sp.id) ? 'selected' : ''}`}
                                        onClick={() => xuLyChon(sp, chonNam, setChonNam)}
                                    >
                                        <div className="selection-item-image">
                                            <img src={layUrlHinhAnh(sp.image_url)} alt={sp.name} />
                                        </div>
                                        <div className="selection-item-info">
                                            <h4>{sp.name}</h4>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                        <div className="combo-actions">
                            <NutBam variant="outline" onClick={() => setBuoc(2)}>QUAY LẠI</NutBam>
                            <NutBam onClick={() => setBuoc(4)}>XEM LẠI & GỬI YÊU CẦU</NutBam>
                        </div>
                    </div>
                )}

                {/* BƯỚC 4: XÁC NHẬN */}
                {buoc === 4 && (
                    <div className="confirmation-step fade-in">
                        <div className="summary-container">
                            <div className="summary-list">
                                <div className="selected-package-summary">
                                    <h3>{goiDaChon.ten}</h3>
                                    <div className="package-price">{new Intl.NumberFormat('vi-VN').format(goiDaChon.gia)}đ</div>
                                    <ul>
                                        {goiDaChon.quyen_loi.map((ql, idx) => (
                                            <li key={idx}>{ql}</li>
                                        ))}
                                    </ul>
                                </div>

                                <h4 style={{ marginTop: '20px' }}>Váy Cưới Đã Chọn ({chonNu.length})</h4>
                                <div className="selected-items-review">
                                    {chonNu.map(i => (
                                        <div key={i.id} className="review-item">
                                            <img src={layUrlHinhAnh(i.image_url)} alt={i.name} />
                                        </div>
                                    ))}
                                </div>
                                <hr style={{ margin: '20px 0', border: '0', borderTop: '1px solid #eee' }} />
                                <h4>Vest Nam Đã Chọn ({chonNam.length})</h4>
                                <div className="selected-items-review">
                                    {chonNam.map(i => (
                                        <div key={i.id} className="review-item">
                                            <img src={layUrlHinhAnh(i.image_url)} alt={i.name} />
                                        </div>
                                    ))}
                                </div>
                            </div>

                            <div className="combo-form">
                                <h3>Thông Tin Của Bạn</h3>
                                <form onSubmit={xuLyGui}>
                                    <div className="form-group">
                                        <label>Họ và Tên</label>
                                        <input
                                            required
                                            value={thongTin.ten}
                                            onChange={e => setThongTin({ ...thongTin, ten: e.target.value })}
                                            placeholder="Nhập họ tên của bạn"
                                        />
                                    </div>
                                    <div className="form-group">
                                        <label>Số Điện Thoại</label>
                                        <input
                                            required
                                            value={thongTin.sdt}
                                            onChange={e => setThongTin({ ...thongTin, sdt: e.target.value })}
                                            placeholder="Số điện thoại liên hệ"
                                        />
                                    </div>
                                    <div className="form-group">
                                        <label>Email</label>
                                        <input
                                            type="email"
                                            required
                                            value={thongTin.email}
                                            onChange={e => setThongTin({ ...thongTin, email: e.target.value })}
                                            placeholder="Email nhận báo giá"
                                        />
                                    </div>
                                    <div className="form-group">
                                        <label>Ngày Cưới Dự Kiến</label>
                                        <input
                                            type="date"
                                            value={thongTin.ngayCuoi}
                                            onChange={e => setThongTin({ ...thongTin, ngayCuoi: e.target.value })}
                                        />
                                    </div>
                                    <div className="form-group">
                                        <label>Ghi Chú Thêm</label>
                                        <textarea
                                            rows="3"
                                            value={thongTin.ghiChu}
                                            onChange={e => setThongTin({ ...thongTin, ghiChu: e.target.value })}
                                            placeholder="Bạn có yêu cầu gì đặc biệt không?"
                                        ></textarea>
                                    </div>

                                    <NutBam type="submit" disabled={trangThaiGui === 'sending'} className="btn-block">
                                        {trangThaiGui === 'sending' ? 'ĐANG GỬI...' : 'HOÀN TẤT ĐĂNG KÝ'}
                                    </NutBam>
                                    {trangThaiGui === 'error' && <p style={{ color: 'red', marginTop: '10px' }}>Có lỗi xảy ra, vui lòng thử lại sau.</p>}
                                </form>
                            </div>
                        </div>
                        <div className="combo-actions">
                            <NutBam variant="outline" onClick={() => setBuoc(3)}>QUAY LẠI</NutBam>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default ChonCombo;
