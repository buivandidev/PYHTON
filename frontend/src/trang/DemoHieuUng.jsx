import { Link } from 'react-router-dom';
import HieuUngHat from '../thanh_phan/HieuUngHat';

export default function DemoHieuUng() {
    return (
        <div style={{ 
            minHeight: '100vh',
            background: '#fff',
            padding: '40px'
        }}>
            {/* Hero Card */}
            <div style={{
                position: 'relative',
                width: '100%',
                maxWidth: '1400px',
                height: '700px',
                margin: '0 auto',
                background: '#000',
                borderRadius: '24px',
                overflow: 'hidden'
            }}>
                <HieuUngHat particleCount={200} />

                {/* Content overlay - pointerEvents none để mouse đi qua xuống canvas */}
                <div style={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    zIndex: 10,
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'center',
                    padding: '50px',
                    pointerEvents: 'none'
                }}>
                    <h1 style={{
                        color: '#fff',
                        fontSize: '42px',
                        fontWeight: 400,
                        lineHeight: 1.2,
                        marginBottom: '30px'
                    }}>
                        Download Google<br/>
                        Antigravity for<br/>
                        Windows
                    </h1>
                    
                    <div style={{ display: 'flex', gap: '12px', pointerEvents: 'auto' }}>
                        <button style={{
                            padding: '12px 24px',
                            background: '#fff',
                            color: '#000',
                            fontSize: '14px',
                            fontWeight: 500,
                            borderRadius: '50px',
                            border: 'none',
                            cursor: 'pointer'
                        }}>
                            Download for x64
                        </button>
                        <button style={{
                            padding: '12px 24px',
                            background: '#333',
                            color: '#fff',
                            fontSize: '14px',
                            fontWeight: 500,
                            borderRadius: '50px',
                            border: 'none',
                            cursor: 'pointer'
                        }}>
                            Download for ARM64
                        </button>
                    </div>
                </div>
            </div>

            {/* Footer */}
            <footer style={{
                maxWidth: '900px',
                margin: '60px auto 0',
                display: 'flex',
                justifyContent: 'space-between',
                flexWrap: 'wrap',
                gap: '40px'
            }}>
                <div>
                    <h2 style={{ fontSize: '24px', fontWeight: 300, color: '#000' }}>
                        Experience liftoff
                    </h2>
                </div>
                <div style={{ display: 'flex', gap: '60px' }}>
                    <div>
                        <h3 style={{ fontSize: '14px', fontWeight: 600, marginBottom: '16px' }}>Product</h3>
                        <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                            <li style={{ marginBottom: '8px' }}><a href="#" style={{ color: '#666', fontSize: '14px', textDecoration: 'none' }}>Download</a></li>
                            <li style={{ marginBottom: '8px' }}><a href="#" style={{ color: '#666', fontSize: '14px', textDecoration: 'none' }}>Product</a></li>
                            <li style={{ marginBottom: '8px' }}><a href="#" style={{ color: '#666', fontSize: '14px', textDecoration: 'none' }}>Docs</a></li>
                        </ul>
                    </div>
                    <div>
                        <h3 style={{ fontSize: '14px', fontWeight: 600, marginBottom: '16px' }}>Resources</h3>
                        <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                            <li style={{ marginBottom: '8px' }}><a href="#" style={{ color: '#666', fontSize: '14px', textDecoration: 'none' }}>Blog</a></li>
                            <li style={{ marginBottom: '8px' }}><a href="#" style={{ color: '#666', fontSize: '14px', textDecoration: 'none' }}>Pricing</a></li>
                        </ul>
                    </div>
                </div>
            </footer>

            <div style={{ textAlign: 'center', marginTop: '40px' }}>
                <Link to="/" style={{ color: '#888', fontSize: '14px', textDecoration: 'none' }}>
                    ← Quay về trang chủ IVIE
                </Link>
            </div>
        </div>
    );
}
