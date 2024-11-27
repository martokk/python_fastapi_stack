// Preloader functionality
window.addEventListener('load', () => {
    // Force scroll to top
    window.scrollTo(0, 0);

    // Get elements
    const preloader = document.getElementById('preloader');
    const navbar = document.querySelector('.navbar');
    const goldBar = document.querySelector('.gold-bar');

    // Reset all navbar states
    navbar.classList.remove('scrolled', 'gold-bar-hidden');
    goldBar.classList.remove('hidden');
    document.body.classList.remove('navbar-scrolled');

    // Fade out preloader
    preloader.style.opacity = '0';

    setTimeout(() => {
        preloader.style.display = 'none';

        // Enable transitions after everything is set
        requestAnimationFrame(() => {
            navbar.style.transition = '';
            goldBar.style.transition = '';
        });
    }, 500);
});

// Disable transitions initially
document.addEventListener('DOMContentLoaded', () => {
    const navbar = document.querySelector('.navbar');
    const goldBar = document.querySelector('.gold-bar');

    navbar.style.transition = 'none';
    goldBar.style.transition = 'none';
});
