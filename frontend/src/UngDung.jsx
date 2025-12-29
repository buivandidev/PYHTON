import { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import sal from 'sal.js';
import 'sal.js/dist/sal.css';
import DauTrang from './thanh_phan/DauTrang';
import ChanTrang from './thanh_phan/ChanTrang';
import ChatBox from './thanh_phan/ChatBox';
import HieuUngLaRoi from './thanh_phan/HieuUngLaRoi';
import HieuUngChuyenTrang from './thanh_phan/HieuUngChuyenTrang';
import CuonLenDau from './thanh_phan/CuonLenDau';
import TrangChu from './trang/TrangChu';
import SanPham from './trang/SanPham';
import ChiTietSanPham from './trang/ChiTietSanPham';
import DichVuTrangDiem from './trang/DichVuTrangDiem';
import LienHe from './trang/LienHe';
import ThuVien from './trang/ThuVien';
import ChonCombo from './trang/ChonCombo';
import TaiKhoan from './trang/TaiKhoan';
import DangNhap from './trang/DangNhap';
import DangKy from './trang/DangKy';
import GioHang from './trang/GioHang';
import DoiTacPortal from './trang/DoiTacPortal';
import Blog from './trang/Blog';
import ChiTietBlog from './trang/ChiTietBlog';
import AntiGravityLanding from './trang/AntiGravityLanding';
import ProductDetail from './trang/ProductDetail';
import GalleryDemo from './trang/GalleryDemo';
import CuonPhongTo from './trang/CuonPhongTo';
import DemoHieuUng from './trang/DemoHieuUng';

// Component to handle sal.js initialization on route change
function SalInitializer() {
  const location = useLocation();

  useEffect(() => {
    // Skip sal animations on home page
    if (location.pathname !== '/') {
      sal({
        threshold: 0.1,
        once: true,
      });
    }
  }, [location]);

  return null;
}

function UngDung() {
  return (
    <Router>
      <div className="App">
        <CuonLenDau />
        <SalInitializer />
        <HieuUngLaRoi />
        <HieuUngChuyenTrang />
        <DauTrang />
        <main>
          <Routes>
            <Route path="/" element={<TrangChu />} />
            <Route path="/san-pham" element={<SanPham />} />
            <Route path="/san-pham/:id" element={<ProductDetail />} />
            <Route path="/thu-vien" element={<ThuVien />} />
            <Route path="/dich-vu-trang-diem" element={<DichVuTrangDiem />} />
            <Route path="/chon-combo" element={<ChonCombo />} />
            <Route path="/lien-he" element={<LienHe />} />
            <Route path="/tai-khoan" element={<TaiKhoan />} />
            <Route path="/dang-nhap" element={<DangNhap />} />
            <Route path="/dang-ky" element={<DangKy />} />
            <Route path="/gio-hang" element={<GioHang />} />
            <Route path="/doi-tac-portal" element={<DoiTacPortal />} />
            <Route path="/blog" element={<Blog />} />
            <Route path="/blog/:slug" element={<ChiTietBlog />} />
            <Route path="/anti-gravity" element={<AntiGravityLanding />} />
            <Route path="/san-pham-demo" element={<ProductDetail />} />
            <Route path="/gallery-demo" element={<GalleryDemo />} />
            <Route path="/cuon-phong-to" element={<CuonPhongTo />} />
            <Route path="/demo-hieu-ung" element={<DemoHieuUng />} />
          </Routes>

        </main>
        <ChanTrang />
        <ChatBox />
      </div>
    </Router>
  );
}

export default UngDung;
