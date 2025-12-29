import { useState, useEffect, useRef } from 'react';
import { motion, useScroll, useTransform } from 'framer-motion';
import { thuVienAPI, layUrlHinhAnh } from '../api/khach_hang';
import BoSuuTapGach from '../thanh_phan/BoSuuTapGach';
import HieuUngHat from '../thanh_phan/HieuUngHat';

const ThuVien = () => {
    const [danhSachAnh, setDanhSachAnh] = useState([]);
    const [dangTai, setDangTai] = useState(true);
    const phanHeroRef = useRef(null);

    // Hiệu ứng cuộn cho phần hero
    const { scrollYProgress: tienTrinhCuon } = useScroll({
        target: phanHeroRef,
        offset: ["start start", "end start"]
    });

    const tiLe = useTransform(tienTrinhCuon, [0, 1], [1, 1.5]);
    const doMo = useTransform(tienTrinhCuon, [0, 0.5, 1], [1, 1, 0.3]);
    const doMoChu = useTransform(tienTrinhCuon, [0, 0.3, 0.6], [1, 1, 0]);

    useEffect(() => {
        layDuLieuThuVien();
    }, []);

    const layDuLieuThuVien = async () => {
        try {
            const phanHoi = await thuVienAPI.layTatCa();
            setDanhSachAnh(phanHoi.data);
        } catch (loi) {
            console.error('Lỗi tải thư viện:', loi);
        } finally {
            setDangTai(false);
        }
    };

    const danhSachAnhGallery = danhSachAnh.map(item => ({
        url: layUrlHinhAnh(item.image_url),
        moTa: item.title || 'IVIE Studio - Khoảnh khắc hạnh phúc'
    }));

    // Hiệu ứng chữ
    const hieuUngTieuDe = {
        anDi: { opacity: 0 },
        hienThi: {
            opacity: 1,
            transition: {
                staggerChildren: 0.08,
            },
        },
    };

    const hieuUngChuCai = {
        anDi: { opacity: 0, y: 50 },
        hienThi: {
            opacity: 1,
            y: 0,
            transition: {
                duration: 0.5,
                ease: [0.25, 0.46, 0.45, 0.94],
            },
        },
    };

    const tieuDe = "Thư Viện Ảnh IVIE STUDIO";

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100">
            {/* Khung hiệu ứng hạt ở đầu trang */}
            <section style={{ 
                padding: '120px 20px 40px',
                background: '#fff',
                position: 'relative',
                overflow: 'hidden'
            }}>
                <div style={{
                    position: 'relative',
                    width: '100%',
                    maxWidth: '100%',
                    height: '700px',
                    margin: '0 auto',
                    background: '#fff',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                }}>
                    <HieuUngHat particleCount={800} nenTrang={true} />
                    
                    {/* Content overlay căn giữa */}
                    <div style={{
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        right: 0,
                        bottom: 0,
                        zIndex: 10,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        justifyContent: 'center',
                        padding: '50px',
                        pointerEvents: 'none',
                        textAlign: 'center'
                    }}>
                        <h1 style={{
                            color: '#1a1a1a',
                            fontSize: '52px',
                            fontWeight: 700,
                            lineHeight: 1.2,
                            marginBottom: '16px',
                            fontFamily: 'system-ui, -apple-system, sans-serif'
                        }}>
                            Thư Viện Ảnh IVIE
                        </h1>
                        <p style={{
                            color: '#666',
                            fontSize: '18px',
                            maxWidth: '400px',
                            marginBottom: '30px'
                        }}>
                            Khoảnh khắc hạnh phúc của các cặp đôi
                        </p>
                        <div style={{ display: 'flex', gap: '16px', pointerEvents: 'auto' }}>
                            <a href="/lien-he" style={{
                                padding: '14px 28px',
                                background: '#1a1a1a',
                                color: '#fff',
                                fontSize: '14px',
                                fontWeight: 600,
                                borderRadius: '8px',
                                border: 'none',
                                cursor: 'pointer',
                                textDecoration: 'none'
                            }}>
                                Đặt Lịch Chụp
                            </a>
                            <a href="/san-pham" style={{
                                padding: '14px 28px',
                                background: 'transparent',
                                color: '#1a1a1a',
                                fontSize: '14px',
                                fontWeight: 600,
                                borderRadius: '8px',
                                border: 'none',
                                cursor: 'pointer',
                                textDecoration: 'none'
                            }}>
                                Xem Sản Phẩm →
                            </a>
                        </div>
                    </div>
                </div>
            </section>

            {/* Phần Gallery */}
            <div className="py-12" style={{ marginTop: '80px' }}>
                <div className="container mx-auto px-4">
                {/* Phần đầu với hiệu ứng chữ */}
                <div className="text-center mb-12 relative">
                    {/* Ảnh nền cho hiệu ứng chữ */}
                    <div className="absolute inset-0 -z-10 opacity-5">
                        <div
                            className="w-full h-full bg-cover bg-center"
                            style={{
                                backgroundImage: 'url(https://images.unsplash.com/photo-1519741497674-611481863552?w=1200)',
                            }}
                        />
                    </div>

                    {/* Tiêu đề với hiệu ứng */}
                    <motion.h1
                        className="text-4xl md:text-6xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-gray-900 via-[#b59410] to-gray-900"
                        variants={hieuUngTieuDe}
                        initial="anDi"
                        animate="hienThi"
                    >
                        {tieuDe.split('').map((kyTu, viTri) => (
                            <motion.span key={viTri} variants={hieuUngChuCai}>
                                {kyTu === ' ' ? '\u00A0' : kyTu}
                            </motion.span>
                        ))}
                    </motion.h1>

                    {/* Phụ đề với hiệu ứng fade-in */}
                    <motion.p
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, delay: 0.5 }}
                        className="text-lg text-gray-600 max-w-2xl mx-auto"
                    >
                        Khoảnh khắc hạnh phúc của các cặp đôi - Nơi lưu giữ những kỷ niệm đẹp nhất
                    </motion.p>

                    {/* Các nhãn với hiệu ứng lần lượt */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, delay: 0.7 }}
                        className="mt-6 flex items-center justify-center gap-3 flex-wrap text-sm text-gray-500"
                    >
                        {[
                            { bieuTuong: '📸', noiDung: `${danhSachAnh.length} ảnh` },
                            { bieuTuong: '✨', noiDung: 'Bố cục Gạch' },
                            { bieuTuong: '💝', noiDung: 'Khoảnh khắc đẹp' },
                        ].map((nhan, viTri) => (
                            <motion.span
                                key={viTri}
                                initial={{ opacity: 0, scale: 0.8 }}
                                animate={{ opacity: 1, scale: 1 }}
                                transition={{ duration: 0.5, delay: 0.9 + viTri * 0.1 }}
                                whileHover={{ scale: 1.05, y: -2 }}
                                className="px-4 py-2 bg-white rounded-full shadow-sm hover:shadow-md transition-all cursor-pointer"
                            >
                                {nhan.bieuTuong} {nhan.noiDung}
                            </motion.span>
                        ))}
                    </motion.div>

                    {/* Đường trang trí */}
                    <motion.div
                        initial={{ scaleX: 0 }}
                        animate={{ scaleX: 1 }}
                        transition={{ duration: 1, delay: 1.2 }}
                        className="w-24 h-1 bg-gradient-to-r from-transparent via-[#b59410] to-transparent mx-auto mt-8"
                    />
                </div>

                {/* Nội dung Gallery */}
                {dangTai ? (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="flex flex-col items-center justify-center py-20"
                    >
                        <motion.div
                            animate={{ rotate: 360 }}
                            transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                            className="w-12 h-12 border-4 border-[#b59410] border-t-transparent rounded-full mb-4"
                        />
                        <p className="text-gray-600">Đang tải bộ sưu tập ảnh...</p>
                    </motion.div>
                ) : danhSachAnh.length > 0 ? (
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, delay: 0.3 }}
                        className="bg-white/50 backdrop-blur-sm rounded-2xl shadow-xl p-6"
                    >
                        <BoSuuTapGach danhSachAnh={danhSachAnhGallery} />
                    </motion.div>
                ) : (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="text-center py-20 bg-white rounded-2xl shadow-lg"
                    >
                        <motion.div
                            animate={{ y: [0, -10, 0] }}
                            transition={{ duration: 2, repeat: Infinity }}
                            className="text-6xl mb-4"
                        >
                            📷
                        </motion.div>
                        <p className="text-gray-500 text-lg">Chưa có ảnh trong thư viện</p>
                        <p className="text-gray-400 text-sm mt-2">
                            Hãy quay lại sau để xem những khoảnh khắc đẹp
                        </p>
                    </motion.div>
                )}

                {/* Thông tin cuối trang */}
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.8, delay: 1.5 }}
                    className="text-center mt-12 py-8 border-t border-gray-200"
                >
                    <p className="text-gray-600 mb-2">
                        💡 <strong>Mẹo:</strong> Di chuột vào ảnh để xem hiệu ứng, click để phóng to
                    </p>
                    <p className="text-gray-500 text-sm">
                        © 2024 IVIE STUDIO - Lưu giữ khoảnh khắc hạnh phúc
                    </p>
                </motion.div>
            </div>
        </div>

            {/* Phần Hero với hiệu ứng cuộn phóng to - đã dời xuống cuối */}
            <div ref={phanHeroRef} className="relative h-[200vh]">
                <div className="sticky top-0 h-screen flex items-center justify-center overflow-hidden bg-gradient-to-br from-[#f8f6f3] to-[#e8e4df]">
                    
                    {/* Nền trang trí */}
                    <motion.div 
                        className="absolute inset-0 opacity-10"
                        style={{ opacity: useTransform(tienTrinhCuon, [0, 0.5], [0.1, 0.3]) }}
                    >
                        <div className="absolute top-20 left-20 w-64 h-64 bg-[#b59410] rounded-full blur-3xl" />
                        <div className="absolute bottom-20 right-20 w-96 h-96 bg-[#d4af37] rounded-full blur-3xl" />
                    </motion.div>

                    {/* Ảnh Hero chính với hiệu ứng phóng to */}
                    {danhSachAnh.length > 0 && (
                        <motion.div
                            style={{ scale: tiLe, opacity: doMo }}
                            className="relative z-10"
                        >
                            <img
                                src={layUrlHinhAnh(danhSachAnh[0].image_url)}
                                alt="Thư viện IVIE Studio"
                                className="w-[500px] h-[700px] object-cover rounded-lg shadow-2xl"
                            />
                            <div className="absolute inset-0 bg-gradient-to-t from-black/20 via-transparent to-transparent rounded-lg" />
                        </motion.div>
                    )}

                    {/* Chữ tiêu đề */}
                    <motion.div
                        style={{ opacity: doMoChu }}
                        className="absolute top-1/4 left-1/2 transform -translate-x-1/2 text-center z-20"
                    >
                        <h1 className="text-6xl md:text-8xl font-serif text-[#2c2c2c] mb-4 tracking-wider">
                            IVIE STUDIO
                        </h1>
                        <p className="text-xl md:text-2xl text-[#6b6b6b] font-light tracking-widest">
                            Thư Viện Khoảnh Khắc Hạnh Phúc
                        </p>
                    </motion.div>

                    {/* Chỉ báo cuộn */}
                    <motion.div
                        style={{ opacity: useTransform(tienTrinhCuon, [0, 0.2], [1, 0]) }}
                        className="absolute bottom-10 left-1/2 transform -translate-x-1/2 z-20"
                    >
                        <motion.div
                            animate={{ y: [0, 10, 0] }}
                            transition={{ duration: 1.5, repeat: Infinity }}
                            className="flex flex-col items-center"
                        >
                            <span className="text-[#6b6b6b] text-sm mb-2 tracking-widest">CUỘN XUỐNG</span>
                            <svg className="w-6 h-6 text-[#b59410]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                            </svg>
                        </motion.div>
                    </motion.div>

                    {/* Thanh tiến trình */}
                    <motion.div
                        className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-[#b59410] to-[#d4af37] origin-left z-30"
                        style={{ scaleX: tienTrinhCuon }}
                    />
                </div>
            </div>
        </div>
    );
};

export default ThuVien;
