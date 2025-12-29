import { useEffect, useRef } from 'react';

export default function HieuUngHat({ particleCount = 80, nenTrang = false }) {
    const canvasRef = useRef(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        // Tối ưu: dùng 2d context với các options tốt nhất
        const ctx = canvas.getContext('2d', { 
            alpha: false,
            desynchronized: true 
        });
        
        let animationId;
        let particles = [];
        let mouse = { x: -9999, y: -9999 };
        let isMouseActive = false;
        let mouseIdleTimer = null;
        
        const REPULSION_RADIUS = 150;
        const ROTATION_SPEED = 0.0003;
        
        // Cache các giá trị tính toán
        let centerX, centerY, maxRadius;

        const resize = () => {
            const parent = canvas.parentElement;
            if (!parent) return;
            
            // Tối ưu: set size trực tiếp
            const dpr = Math.min(window.devicePixelRatio || 1, 2);
            const width = parent.offsetWidth;
            const height = parent.offsetHeight;
            
            canvas.width = width * dpr;
            canvas.height = height * dpr;
            canvas.style.width = width + 'px';
            canvas.style.height = height + 'px';
            ctx.scale(dpr, dpr);
            
            centerX = width / 2;
            centerY = height / 2;
            maxRadius = Math.min(width, height) * 0.9;
            
            initParticles(width, height);
        };

        const initParticles = (width, height) => {
            particles = [];
            const sizes = [1, 1.5, 2, 2.5, 3, 3.5, 4];
            
            for (let i = 0; i < particleCount; i++) {
                let x, y;
                
                if (nenTrang) {
                    const angle = Math.random() * Math.PI * 2;
                    const radius = Math.random() * maxRadius;
                    x = centerX + Math.cos(angle) * radius;
                    y = centerY + Math.sin(angle) * radius;
                } else {
                    x = Math.random() * width;
                    y = Math.random() * height;
                }
                
                const baseSize = sizes[i % sizes.length];
                
                // Pre-calculate color string để tránh tính toán trong loop
                const hue = nenTrang ? (200 + Math.random() * 30) : (200 + Math.random() * 60);
                const brightness = nenTrang ? (55 + Math.random() * 25) : (60 + Math.random() * 30);
                
                particles.push({
                    x, y,
                    homeX: x,
                    homeY: y,
                    vx: 0,
                    vy: 0,
                    size: baseSize,
                    baseSize: baseSize,
                    color: `hsl(${hue}, 80%, ${brightness}%)`
                });
            }
        };

        const animate = () => {
            const width = canvas.width / (window.devicePixelRatio || 1);
            const height = canvas.height / (window.devicePixelRatio || 1);
            
            // Clear canvas
            ctx.fillStyle = nenTrang ? '#fff' : '#000';
            ctx.fillRect(0, 0, width, height);

            const len = particles.length;
            
            for (let i = 0; i < len; i++) {
                const p = particles[i];

                // Mouse repulsion - tối ưu với squared distance
                const dx = p.x - mouse.x;
                const dy = p.y - mouse.y;
                const distSq = dx * dx + dy * dy;
                const radiusSq = REPULSION_RADIUS * REPULSION_RADIUS;

                if (distSq < radiusSq && distSq > 0) {
                    const dist = Math.sqrt(distSq);
                    const force = (REPULSION_RADIUS - dist) / REPULSION_RADIUS;
                    const angle = Math.atan2(dy, dx);
                    p.vx += Math.cos(angle) * force * 2;
                    p.vy += Math.sin(angle) * force * 2;
                }

                // Xoay khi không có mouse
                if (!isMouseActive) {
                    const dxC = p.homeX - centerX;
                    const dyC = p.homeY - centerY;
                    const radius = Math.sqrt(dxC * dxC + dyC * dyC);
                    const currentAngle = Math.atan2(dyC, dxC) + ROTATION_SPEED;
                    p.homeX = centerX + radius * Math.cos(currentAngle);
                    p.homeY = centerY + radius * Math.sin(currentAngle);
                }

                // Spring physics - mượt hơn
                p.vx += (p.homeX - p.x) * 0.02;
                p.vy += (p.homeY - p.y) * 0.02;
                p.vx *= 0.92;
                p.vy *= 0.92;
                p.x += p.vx;
                p.y += p.vy;

                // Vẽ hạt - batch drawing
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size, 0, 6.283185);
                ctx.fillStyle = p.color;
                ctx.fill();
            }

            animationId = requestAnimationFrame(animate);
        };

        const handleMouseMove = (e) => {
            const rect = canvas.getBoundingClientRect();
            mouse.x = e.clientX - rect.left;
            mouse.y = e.clientY - rect.top;
            isMouseActive = true;
            
            if (mouseIdleTimer) clearTimeout(mouseIdleTimer);
            mouseIdleTimer = setTimeout(() => {
                isMouseActive = false;
            }, 1500);
        };

        const handleMouseLeave = () => {
            mouse.x = -9999;
            mouse.y = -9999;
            isMouseActive = false;
        };

        resize();
        animate();

        window.addEventListener('resize', resize);
        
        const parent = canvas.parentElement;
        if (parent) {
            parent.addEventListener('mousemove', handleMouseMove, { passive: true });
            parent.addEventListener('mouseleave', handleMouseLeave, { passive: true });
        }

        return () => {
            cancelAnimationFrame(animationId);
            if (mouseIdleTimer) clearTimeout(mouseIdleTimer);
            window.removeEventListener('resize', resize);
            if (parent) {
                parent.removeEventListener('mousemove', handleMouseMove);
                parent.removeEventListener('mouseleave', handleMouseLeave);
            }
        };
    }, [particleCount, nenTrang]);

    return (
        <canvas
            ref={canvasRef}
            style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                background: nenTrang ? '#fff' : '#000',
                borderRadius: 'inherit',
                zIndex: 1
            }}
        />
    );
}
