// Handle Newsletter Form
const newsletterForm = document.querySelector('.newsletter-form');
if (newsletterForm) {
    newsletterForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const emailInput = newsletterForm.querySelector('input[type="email"]');
        if (emailInput.value) {
            // Here you would typically send this to your backend
            alert('Thank you for subscribing to our newsletter!');
            emailInput.value = '';
        }
    });
}
