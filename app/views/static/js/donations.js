// Handle donation amounts
const donationButtons = document.querySelectorAll('.donation-amount');

donationButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Remove active class from all buttons
        donationButtons.forEach(btn => btn.classList.remove('active'));

        // Add active class to clicked button
        button.classList.add('active');

        // Handle custom amount
        if (button.textContent === 'Custom') {
            const amount = prompt('Enter custom amount:', '');
            if (amount !== null && !isNaN(amount) && amount > 0) {
                button.textContent = `$${parseFloat(amount).toFixed(2)}`;
            } else {
                button.classList.remove('active');
            }
        }
    });
});

// Facebook Button Handler
const facebookButton = document.querySelector('.btn-facebook');
if (facebookButton) {
    facebookButton.addEventListener('click', (e) => {
        e.preventDefault();
        // Replace with your actual Facebook page URL
        window.open('https://www.facebook.com/YourPage', '_blank');
    });
}
