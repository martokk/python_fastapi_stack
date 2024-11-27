// const scrollElements = document.querySelectorAll('.gold-scroll, .silver-scroll, .black-scroll');

// let ticking = false;

// function handleScroll() {
//     if (!ticking) {
//         window.requestAnimationFrame(() => {
//             scrollElements.forEach((element) => {
//                 const rect = element.getBoundingClientRect();

//                 // Calculate the element's vertical position within the viewport
//                 const viewportHeight = window.innerHeight;
//                 const elementMid = rect.top + rect.height / 2; // Middle of the element
//                 const gradientPosition = (elementMid / viewportHeight) * 100;

//                 // Set the background-position based on the element's position
//                 element.style.backgroundPosition = `50% ${gradientPosition}%`;
//             });

//             ticking = false;
//         });

//         ticking = true;
//     }
// }

// // Add scroll listener
// window.addEventListener('scroll', handleScroll);
// // Trigger an initial update to position gradients
// handleScroll();
