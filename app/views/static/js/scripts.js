// Initialize AOS
AOS.init({
    duration: 1000,
    once: true,
    offset: 100,
    easing: 'cubic-bezier(0.175, 0.885, 0.32, 1.275)' // Smooth easing

});

// Import all modules
import './counters.js';
import './donations.js';
import './forms.js';
import './navbar.js';
import './preloader.js';
import './scroll-effect.js';
import './utils.js';
// Handle window resize
window.addEventListener('resize', () => {
    AOS.refresh();
});
