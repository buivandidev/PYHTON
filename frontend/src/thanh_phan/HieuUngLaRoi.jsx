import { useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';

const HieuUngLaRoi = () => {
    const location = useLocation();
    const canvasRef = useRef(null);
    const ctxRef = useRef(null);
    const animationRef = useRef(null);
    const leavesRef = useRef([]);
    const leafPathRef = useRef(null);
    const sizeRef = useRef({ width: 0, height: 0 });

    // Physics & Scroll State
    const scrollState = useRef({
        targetSpeed: 0,
        currentSpeed: 0,
        lastScrollY: 0,
        isScrolling: false
    });

    // Time State
    const timeRef = useRef({
        lastFrameTime: 0
    });

    // Check home page & admin/auth pages to exclude effect
    const excludeRoutes = [
        '/',
        '/index.html',
        '/doi-tac-portal',
        '/dang-nhap',
        '/dang-ky',
        '/tai-khoan',
        '/gio-hang'
    ];
    const shouldHide = excludeRoutes.some(route => location.pathname === route || location.pathname.startsWith('/doi-tac-portal'));

    useEffect(() => {
        if (shouldHide) return;

        const canvas = canvasRef.current;
        if (!canvas) return;

        const ctx = canvas.getContext('2d', { alpha: true }); // optimize alpha
        ctxRef.current = ctx;
        let width = window.innerWidth;
        let height = window.innerHeight;
        sizeRef.current = { width, height };

        // High DPI handling
        const dpr = window.devicePixelRatio || 1;
        canvas.width = width * dpr;
        canvas.height = height * dpr;
        ctx.scale(dpr, dpr);
        canvas.style.width = `${width}px`;
        canvas.style.height = `${height}px`;

        const handleResize = () => {
            width = window.innerWidth;
            height = window.innerHeight;
            sizeRef.current = { width, height };
            canvas.width = width * dpr;
            canvas.height = height * dpr;
            ctx.scale(dpr, dpr);
            canvas.style.width = `${width}px`;
            canvas.style.height = `${height}px`;
        };

        window.addEventListener('resize', handleResize);

        // Init leaves
        const leafCount = 30;
        const leaves = [];
        const leafPath = new Path2D("M20 0C20 0 25 10 25 20C25 35 15 40 10 40C0 40 -5 30 0 15C2 5 20 0 20 0Z");
        leafPathRef.current = leafPath;

        for (let i = 0; i < leafCount; i++) {
            leaves.push(createLeaf(width, height));
        }
        leavesRef.current = leaves;

        // Scroll Handler with Velocity Calculation
        const handleScroll = () => {
            const currentScrollY = window.scrollY;
            const delta = Math.abs(currentScrollY - scrollState.current.lastScrollY);

            // Limit max additional speed to avoid chaos
            // Scroll delta is usually usually large, so we dampen it significantly
            scrollState.current.targetSpeed = Math.min(delta * 0.8, 12);

            scrollState.current.lastScrollY = currentScrollY;
            scrollState.current.isScrolling = true;

            // Reset scrolling state after a delay if no more scroll events
            if (scrollState.current.timeout) clearTimeout(scrollState.current.timeout);
            scrollState.current.timeout = setTimeout(() => {
                scrollState.current.isScrolling = false;
                scrollState.current.targetSpeed = 0;
            }, 100);
        };

        window.addEventListener('scroll', handleScroll);

        // Animation Loop
        const render = (timestamp) => {
            const ctx = ctxRef.current;
            const leafPath = leafPathRef.current;
            const { width, height } = sizeRef.current;
            if (!ctx || !leafPath || !width || !height) return;
            if (!timeRef.current.lastFrameTime) timeRef.current.lastFrameTime = timestamp;

            // Calculate Delta Time (in seconds)
            // Limit delta time to avoid huge jumps if tab was inactive
            const dt = Math.min((timestamp - timeRef.current.lastFrameTime) / 1000, 0.1);
            timeRef.current.lastFrameTime = timestamp;

            ctx.clearRect(0, 0, width, height);

            // Smooth Scroll Speed Interpolation (Lerp)
            // If scrolling, approach target quickly. If stopped, decay slowly.
            const lerpFactor = scrollState.current.isScrolling ? 0.2 : 0.05;
            scrollState.current.currentSpeed += (scrollState.current.targetSpeed - scrollState.current.currentSpeed) * lerpFactor;

            // Global scroll influence scaling
            // Base speed is handled in leaf properties. This adds extra purely from scroll.
            // We multiply by 60 to normalize scroll speed relative to 60fps physics if needed, 
            // but since we use dt, we just treat speed as pixels/second effectively.
            // Actually, let's treat Leaf.speed as pixels/frame @ 60fps (~pixels per 16ms).
            // So pixel_per_second = speed * 60.
            const scrollInfluence = scrollState.current.currentSpeed * 60 * dt;

            leavesRef.current.forEach(leaf => {
                // Physics Update
                // Base fall speed + Scroll acceleration
                const moveY = (leaf.speed * 60 * dt) + scrollInfluence;
                leaf.y += moveY;

                // Sway logic: sin(angle)
                // angle changes over time
                leaf.angle += leaf.swaySpeed * 60 * dt;
                const swayOffset = Math.sin(leaf.angle) * leaf.swayAmp * 60 * dt;
                leaf.x += swayOffset;

                // Rotation
                leaf.rotation += leaf.rotationSpeed * 60 * dt;

                // Boundary Check
                if (leaf.y > height + 50) {
                    resetLeaf(leaf, width);
                }

                // Render
                ctx.save();
                ctx.translate(leaf.x, leaf.y);
                ctx.rotate(leaf.rotation * Math.PI / 180);
                ctx.scale(leaf.scale, leaf.scale);

                ctx.fillStyle = `rgba(212, 175, 55, ${leaf.opacity})`;
                ctx.fill(leafPath);

                ctx.restore();
            });

            animationRef.current = requestAnimationFrame(render);
        };

        animationRef.current = requestAnimationFrame(render);

        return () => {
            window.removeEventListener('resize', handleResize);
            window.removeEventListener('scroll', handleScroll);
            if (animationRef.current) cancelAnimationFrame(animationRef.current);
            if (scrollState.current.timeout) clearTimeout(scrollState.current.timeout);
        };
    }, [shouldHide]);

    if (shouldHide) return null;

    return (
        <canvas
            ref={canvasRef}
            style={{
                position: 'fixed',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                pointerEvents: 'none',
                zIndex: -1
            }}
        />
    );
};

// Helper Functions
function createLeaf(w, h) {
    return {
        x: Math.random() * w,
        y: Math.random() * h - h, // Start random off-screen or on-screen

        // Physics properties
        speed: 0.5 + Math.random() * 1.0,  // Base fall speed (approx pixels/frame at 60fps)

        // Sway properties
        angle: Math.random() * Math.PI * 2, // Initial phase
        swaySpeed: 0.02 + Math.random() * 0.03, // How fast it sways back and forth
        swayAmp: 0.5 + Math.random() * 1.0, // How far it sways

        // Appearance
        scale: 0.5 + Math.random() * 0.5,
        opacity: 0.85 + Math.random() * 0.15,
        rotation: Math.random() * 360,
        rotationSpeed: (Math.random() - 0.5) * 2
    };
}

function resetLeaf(leaf, w) {
    leaf.x = Math.random() * w;
    leaf.y = -60; // Reset above screen
    leaf.speed = 0.5 + Math.random() * 1.0;
    leaf.opacity = 0.85 + Math.random() * 0.15;
}

export default HieuUngLaRoi;
