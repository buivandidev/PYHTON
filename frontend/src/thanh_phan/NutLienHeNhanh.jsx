import { useState } from 'react';
import './NutLienHeNhanh.css';

const NutLienHeNhanh = () => {
    const [moRong, setMoRong] = useState(false);

    const zaloSDT = '0793919384';
    const messengerLink = 'https://www.facebook.com/di.di.717541';
    const hotline = '0793919384';

    return (
        <div className={`floating-contact ${moRong ? 'expanded' : ''}`}>
            <div className="contact-buttons">
                <a
                    href={`https://zalo.me/${zaloSDT}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="contact-btn zalo-btn"
                    title="Chat Zalo"
                >
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2C6.48 2 2 5.58 2 10c0 2.29 1.12 4.33 2.88 5.64L2 22l6.36-2.88C9.67 20.88 11.71 22 14 22c5.42 0 10-3.58 10-8S17.42 2 12 2zm0 16c-1.38 0-2.68-.35-3.82-.97l-.24-.14-2.54.55.55-2.54-.14-.24C5.35 14.68 5 13.38 5 12c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7z"/>
                    </svg>
                    <span>Zalo</span>
                </a>
                <a
                    href={messengerLink}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="contact-btn messenger-btn"
                    title="Chat Messenger"
                >
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 0C5.373 0 0 4.925 0 11c0 2.153.741 4.24 2.107 5.93L0 24l7.437-2.053C9.05 22.516 10.5 22.8 12 22.8c6.627 0 12-4.925 12-11S18.627 0 12 0zm0 20.4c-1.3 0-2.55-.25-3.7-.7l-.35-.1-3.65 1.01.97-3.55-.1-.35C4.2 15.75 3.6 13.4 3.6 11c0-4.75 3.85-8.6 8.6-8.6s8.6 3.85 8.6 8.6-3.85 8.6-8.6 8.6z"/>
                    </svg>
                    <span>Messenger</span>
                </a>
                <a
                    href={`tel:${hotline}`}
                    className="contact-btn phone-btn"
                    title="Gọi ngay"
                >
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
                    </svg>
                    <span>Gọi</span>
                </a>
            </div>
            <button
                className="contact-toggle"
                onClick={() => setMoRong(!moRong)}
                aria-label="Mở/Đóng liên hệ nhanh"
            >
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                    {moRong ? (
                        <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                    ) : (
                        <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
                    )}
                </svg>
            </button>
        </div>
    );
};

export default NutLienHeNhanh;






