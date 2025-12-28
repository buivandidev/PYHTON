import { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import './Header.css';
import ThanhTimKiem from './ThanhTimKiem';
import NutBam from './NutBam';

const DauTrang = () => {
    const [user, setUser] = useState(null);
    const [menuOpen, setMenuOpen] = useState(false);
    const [searchOpen, setSearchOpen] = useState(false);
    const location = useLocation();
    const navigate = useNavigate();

    useEffect(() => {
        const checkAuth = () => {
            const savedUser = localStorage.getItem('ivie_user');
            if (savedUser) {
                setUser(JSON.parse(savedUser));
            } else {
                setUser(null);
            }
        };

        checkAuth();
        window.addEventListener('authChange', checkAuth);
        return () => window.removeEventListener('authChange', checkAuth);
    }, []);

    const logout = () => {
        localStorage.removeItem('ivie_token');
        localStorage.removeItem('ivie_user');
        setUser(null);
        navigate('/');
        window.dispatchEvent(new Event('authChange'));
    };

    const isActive = (path) => location.pathname === path;

    return (
        <header className="header" id="header">
            <div className="container">
                <div className="header-content">
                    <div className="logo">
                        <Link to="/">
                            <span className="logo-text">IVIE</span>
                        </Link>
                    </div>

                    <nav className={`nav ${menuOpen ? 'active' : ''}`} id="nav-menu">
                        <ul className="nav-list">
                            <li>
                                <Link
                                    to="/"
                                    className={`nav-link ${isActive('/') ? 'active' : ''}`}
                                    onClick={() => setMenuOpen(false)}
                                >
                                    TRANG CHỦ
                                </Link>
                            </li>
                            <li>
                                <Link
                                    to="/san-pham"
                                    className={`nav-link ${isActive('/san-pham') ? 'active' : ''}`}
                                    onClick={() => setMenuOpen(false)}
                                >
                                    SẢN PHẨM
                                </Link>
                            </li>
                            <li>
                                <Link
                                    to="/thu-vien"
                                    className={`nav-link ${isActive('/thu-vien') ? 'active' : ''}`}
                                    onClick={() => setMenuOpen(false)}
                                >
                                    THƯ VIỆN
                                </Link>
                            </li>
                            <li>
                                <Link
                                    to="/dich-vu-trang-diem"
                                    className={`nav-link ${isActive('/dich-vu-trang-diem') ? 'active' : ''}`}
                                    onClick={() => setMenuOpen(false)}
                                >
                                    DỊCH VỤ TRANG ĐIỂM
                                </Link>
                            </li>
                            <li>
                                <Link
                                    to="/chon-combo"
                                    className={`nav-link ${isActive('/chon-combo') ? 'active' : ''}`}
                                    onClick={() => setMenuOpen(false)}
                                >
                                    GÓI DỊCH VỤ
                                </Link>
                            </li>
                            <li>
                                <Link
                                    to="/lien-he"
                                    className={`nav-link ${isActive('/lien-he') ? 'active' : ''}`}
                                    onClick={() => setMenuOpen(false)}
                                >
                                    LIÊN HỆ
                                </Link>
                            </li>
                            <li>
                                <Link
                                    to="/blog"
                                    className={`nav-link ${isActive('/blog') ? 'active' : ''}`}
                                    onClick={() => setMenuOpen(false)}
                                >
                                    BLOG
                                </Link>
                            </li>
                        </ul>
                    </nav>

                    <div className="header-actions">
                        <button className="search-btn" aria-label="Tìm kiếm" onClick={() => setSearchOpen(true)}>
                            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                                <path d="M9 17A8 8 0 1 0 9 1a8 8 0 0 0 0 16zM19 19l-4.35-4.35" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                            </svg>
                        </button>
                        <Link to="/gio-hang" className="cart-btn" aria-label="Giỏ hàng" style={{ color: 'inherit', display: 'flex', alignItems: 'center', justifyContent: 'center', width: '40px', height: '40px' }}>
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                <circle cx="9" cy="21" r="1"></circle>
                                <circle cx="20" cy="21" r="1"></circle>
                                <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
                            </svg>
                        </Link>


                        {user ? (
                            <div className="user-menu-container">
                                <span className="user-name" style={{color: '#c9a86c'}}>Chào, {user.full_name.split(' ')[0]}</span>
                                <div className="user-dropdown">
                                    <Link to="/tai-khoan" className="dropdown-item">Tài khoản của tôi</Link>
                                    <button onClick={logout} className="logout-btn">Đăng xuất</button>
                                </div>
                            </div>
                        ) : (
                            <div className="auth-btns">
                                <Link to="/dang-nhap" className="auth-link">Đăng nhập</Link>
                                <span className="separator">/</span>
                                <Link to="/dang-ky" className="auth-link">Đăng ký</Link>
                            </div>
                        )}
                        <button
                            className={`menu-toggle ${menuOpen ? 'active' : ''}`}
                            onClick={() => setMenuOpen(!menuOpen)}
                            aria-label="Menu"
                        >
                            <span></span>
                            <span></span>
                            <span></span>
                        </button>
                    </div>
                </div>
            </div>
            <ThanhTimKiem isOpen={searchOpen} onClose={() => setSearchOpen(false)} />
        </header>
    );
};

export default DauTrang;
