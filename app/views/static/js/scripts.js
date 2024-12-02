// Initialize AOS
AOS.init({
    duration: 1000,
    once: true,
    offset: 100,
    easing: 'cubic-bezier(0.175, 0.885, 0.32, 1.275)' // Smooth easing

});


// Handle window resize
window.addEventListener('resize', () => {
    AOS.refresh();
});
