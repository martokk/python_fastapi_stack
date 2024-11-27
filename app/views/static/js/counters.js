// Counter animation with optimized performance
const startCounters = () => {
    const counters = document.querySelectorAll('.counter-value');
    const ANIMATION_DURATION = 1000; // 1 second animation
    const FRAME_RATE = 60; // 60 FPS
    const FRAMES = ANIMATION_DURATION / (1000 / FRAME_RATE);

    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-count'));
        const increment = target / FRAMES;
        let current = 0;
        let frame = 0;

        const updateCount = () => {
            frame++;
            current += increment;

            if (frame <= FRAMES) {
                counter.innerText = Math.round(current).toLocaleString();
                requestAnimationFrame(updateCount);
            } else {
                counter.innerText = target.toLocaleString();
            }
        };

        requestAnimationFrame(updateCount);
    });
};

// Start counters when they come into view
const observerCallback = (entries) => {
    entries.forEach(entry => {
        // Only start once when element comes into view
        if (entry.isIntersecting) {
            startCounters();
            observer.unobserve(entry.target); // Stop observing after animation starts
        }
    });
};

const observer = new IntersectionObserver(observerCallback, {
    threshold: 0.5
});

const counterSection = document.querySelector('.counter');
if (counterSection) {
    observer.observe(counterSection);
}
