import AlbumThongMinh from '../thanh_phan/AlbumThongMinh';
import GanTheSanPham, { duLieuTheMau } from '../thanh_phan/GanTheSanPham';
import ThanhTruotTruocSau from '../thanh_phan/ThanhTruotTruocSau';
import BoSuuTapGach from '../thanh_phan/BoSuuTapGach';
import BoSuuTapDanXen from '../thanh_phan/BoSuuTapDanXen';
import BoSuuTapTiLeVang, { duLieuAnhTiLeVangMau } from '../thanh_phan/BoSuuTapTiLeVang';

const GalleryDemo = () => {
  // Sample data for Smart Album Gallery
  const galleryImages = [
    {
      url: 'https://images.unsplash.com/photo-1519741497674-611481863552?w=800',
      caption: 'Váy Cưới Công Chúa - Bộ sưu tập Xuân 2024',
    },
    {
      url: 'https://images.unsplash.com/photo-1594552072238-6d4f0a7c3c8e?w=800',
      caption: 'Váy Cưới Đuôi Cá - Phong cách Hiện Đại',
    },
    {
      url: 'https://images.unsplash.com/photo-1606800052052-a08af7148866?w=800',
      caption: 'Váy Cưới Tối Giản - Thanh Lịch & Sang Trọng',
    },
    {
      url: 'https://images.unsplash.com/photo-1583939003579-730e3918a45a?w=800',
      caption: 'Váy Cưới Vintage - Phong cách Cổ Điển',
    },
    {
      url: 'https://images.unsplash.com/photo-1591604466107-ec97de577aff?w=800',
      caption: 'Váy Cưới Boho - Tự Do & Phóng Khoáng',
    },
    {
      url: 'https://images.unsplash.com/photo-1595777216528-071e0127ccf4?w=800',
      caption: 'Váy Cưới Ren - Tinh Tế & Quyến Rũ',
    },
    {
      url: 'https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=800',
      caption: 'Váy Cưới A-Line - Dáng Chữ A Cổ Điển',
    },
    {
      url: 'https://images.unsplash.com/photo-1525562723836-dca67a71d5f1?w=800',
      caption: 'Váy Cưới Ball Gown - Lộng Lẫy Hoàng Gia',
    },
    {
      url: 'https://images.unsplash.com/photo-1522673607200-164d1b6ce486?w=800',
      caption: 'Váy Cưới Sheath - Ôm Sát Quyến Rũ',
    },
    {
      url: 'https://images.unsplash.com/photo-1465495976277-4387d4b0b4c6?w=800',
      caption: 'Váy Cưới Empire - Eo Cao Thanh Thoát',
    },
    {
      url: 'https://images.unsplash.com/photo-1502635385003-ee1e6a1a742d?w=800',
      caption: 'Váy Cưới Tea Length - Ngắn Trẻ Trung',
    },
    {
      url: 'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=800',
      caption: 'Váy Cưới Off-Shoulder - Vai Trần Gợi Cảm',
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            IVIE STUDIO Gallery Components
          </h1>
          <p className="text-gray-600">
            Trải nghiệm các tính năng gallery hiện đại và tương tác
          </p>
        </div>

        {/* Section 1: Smart Album Gallery */}
        <section className="mb-20">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              Album Thông Minh
            </h2>
            <p className="text-gray-600">
              Click vào ảnh để xem phóng to với hiệu ứng mượt mà
            </p>
          </div>
          <AlbumThongMinh danhSachAnh={galleryImages} />
        </section>

        {/* Section 3: Masonry Gallery */}
        <section className="mb-20">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              Bộ Sưu Tập Gạch
            </h2>
            <p className="text-gray-600">
              Ảnh đứng và ảnh ngang tự nhiên, hover để zoom và tăng sáng
            </p>
          </div>
          <BoSuuTapGach danhSachAnh={galleryImages} />
        </section>

        {/* Section 4: Alternating Layout */}
        <section className="mb-20">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              Bộ Sưu Tập Đan Xen
            </h2>
            <p className="text-gray-600">
              Bố cục đảo chiều mỗi hàng với hiệu ứng fade-in on scroll
            </p>
          </div>
          <BoSuuTapDanXen danhSachAnh={galleryImages} />
        </section>

        {/* Section 5: Golden Ratio Gallery */}
        <section className="mb-20">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              Bộ Sưu Tập Tỉ Lệ Vàng
            </h2>
            <p className="text-gray-600">
              Ảnh theo tỉ lệ 3:2 và 2:3 với viền vàng sang trọng
            </p>
          </div>
          <BoSuuTapTiLeVang danhSachAnh={duLieuAnhTiLeVangMau} />
        </section>

        {/* Section 6: Image Tagging */}
        <section className="mb-20">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              Gắn Thẻ Sản Phẩm
            </h2>
            <p className="text-gray-600">
              Click vào các điểm sáng để khám phá sản phẩm
            </p>
          </div>
          <GanTheSanPham
            duongDanAnh="https://images.unsplash.com/photo-1519741497674-611481863552?w=1200"
            danhSachThe={duLieuTheMau}
          />
        </section>

        {/* Section 3: Before & After Slider */}
        <section className="mb-20">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              Thanh Trượt Trước & Sau
            </h2>
            <p className="text-gray-600">
              Kéo thanh trượt để so sánh ảnh trước và sau chỉnh sửa
            </p>
          </div>
          <ThanhTruotTruocSau
            anhTruoc="https://images.unsplash.com/photo-1519741497674-611481863552?w=1200"
            anhSau="https://images.unsplash.com/photo-1519741497674-611481863552?w=1200&sat=-100&brightness=1.2"
            moTa="Chỉnh sửa váy cưới"
          />
        </section>

        {/* Footer */}
        <div className="text-center py-8 border-t border-gray-200">
          <p className="text-gray-600">
            © 2024 IVIE STUDIO - Crafted with ❤️ using React & Tailwind CSS
          </p>
        </div>
      </div>
    </div>
  );
};

export default GalleryDemo;
