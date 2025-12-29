import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';

export default function HieuUngChuyenTrang() {
    const location = useLocation();
    const [dangChuyenTrang, setDangChuyenTrang] = useState(false);
    const [hienThi, setHienThi] = useState(false);

    useEffect(() => {
        // Bắt đầu hiệu ứng khi route thay đổi
        setHienThi(true);
        setDangChuyenTrang(true);

        // Fade out sau 400ms
        const timer1 = setTimeout(() => {
            setDangChuyenTrang(false);
        }, 400);

        // Ẩn hoàn toàn sau 800ms
        const timer2 = setTimeout(() => {
            setHienThi(false);
        }, 800);

        return () => {
            clearTimeout(timer1);
            clearTimeout(timer2);
        };
    }, [location.pathname]);

    if (!hienThi) return null;

    return (
        <div
            style={{
                position: 'fixed',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                zIndex: 9999,
                pointerEvents: 'none',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                background: dangChuyenTrang 
                    ? 'rgba(255, 255, 255, 0.95)' 
                    : 'rgba(255, 255, 255, 0)',
                transition: 'background 0.4s ease-out'
            }}
        >
            {/* Logo IVIE */}
            <div
                style={{
                    opacity: dangChuyenTrang ? 1 : 0,
                    transform: dangChuyenTrang ? 'scale(1)' : 'scale(0.8)',
                    transition: 'all 0.3s ease-out',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    gap: '16px'
                }}
            >
                <span
                    style={{
                        fontSize: '48px',
                        fontWeight: 700,
                        color: '#c9a86c',
                        fontFamily: 'Playfair Display, serif',
                        letterSpacing: '8px'
                    }}
                >
                    IVIE
                </span>
                
                {/* Loading dots */}
                <div style={{ display: 'flex', gap: '8px' }}>
                    {[0, 1, 2].map((i) => (
                        <div
                            key={i}
                            style={{
                                width: '8px',
                                height: '8px',
                                borderRadius: '50%',
                                background: '#c9a86c',
                                animation: `pulse 1s ease-in-out ${i * 0.15}s infinite`
                            }}
                        />
                    ))}
                </div>
            </div>

            <style>{`
                @keyframes pulse {
                    0%, 100% { opacity: 0.3; transform: scale(0.8); }
                    50% { opacity: 1; transform: scale(1.2); }
                }
            `}</style>
        </div>
    );
}
