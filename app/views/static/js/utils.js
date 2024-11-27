// Back to Top Button
const backToTopButton = document.getElementById('backToTop');

window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        backToTopButton.classList.add('show');
    } else {
        backToTopButton.classList.remove('show');
    }
});

backToTopButton.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// // Service Cards Hover Effect
// const serviceCards = document.querySelectorAll('.service-card');
// serviceCards.forEach(card => {
//     card.addEventListener('mouseenter', () => {
//         card.style.transform = 'translateY(-10px)';
//     });

//     card.addEventListener('mouseleave', () => {
//         card.style.transform = 'translateY(0)';
//     });
// });
