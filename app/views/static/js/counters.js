// Counter animation
const startCounters = () => {
    const counters = document.querySelectorAll('.counter-value');

    counters.forEach(counter => {
        const updateCount = () => {
            const target = parseInt(counter.getAttribute('data-count'));
            const count = parseInt(counter.innerText);
            const increment = target / 100;

            if (count < target) {
                counter.innerText = Math.ceil(count + increment);
                setTimeout(updateCount, 10);
            } else {
                counter.innerText = target.toLocaleString();
            }
        };
        updateCount();
    });
};

// Start counters when they come into view
const observerCallback = (entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            startCounters();
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
