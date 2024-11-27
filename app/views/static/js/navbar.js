document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const navbar = document.querySelector('.navbar');
    const goldBar = document.querySelector('.gold-bar');
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');

    // Handle scroll behavior
    const handleScroll = () => {
        const currentScroll = window.pageYOffset;

        // Handle gold bar visibility
        if (currentScroll > 70) {
            goldBar?.classList.add('hidden');
            navbar?.classList.add('gold-bar-hidden');
        } else {
            goldBar?.classList.remove('hidden');
            navbar?.classList.remove('gold-bar-hidden');
        }

        // Handle navbar scroll state
        if (currentScroll > 120) {
            navbar.classList.add('scrolled');
            document.body.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('scrolled');
            document.body.classList.remove('navbar-scrolled');
        }
    };

    // Mobile menu handling
    let isMenuOpen = false;

    const toggleMenu = (show = null) => {
        isMenuOpen = show !== null ? show : !isMenuOpen;

        if (isMenuOpen) {
            navbarCollapse.classList.add('show');
            document.body.style.overflow = 'hidden';
            navbarToggler.setAttribute('aria-expanded', 'true');
        } else {
            navbarCollapse.classList.remove('show');
            document.body.style.overflow = '';
            navbarToggler.setAttribute('aria-expanded', 'false');
        }
    };

    if (navbarToggler && navbarCollapse) {
        // Toggle mobile menu
        navbarToggler.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleMenu();
        });

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (isMenuOpen &&
                !navbarCollapse.contains(e.target) &&
                !navbarToggler.contains(e.target)) {
                toggleMenu(false);
            }
        });

        // Close menu when clicking nav links
        navbarCollapse.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                toggleMenu(false);
            });
        });

        // Close menu on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && isMenuOpen) {
                toggleMenu(false);
            }
        });

        // Handle resize events
        window.addEventListener('resize', () => {
            if (window.innerWidth > 991.98 && isMenuOpen) {
                toggleMenu(false);
            }
        });
    }

    // Smooth scroll handling
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = document.querySelector(link.getAttribute('href'));
            if (target) {
                const navbarHeight = navbar.offsetHeight;
                const goldBarHeight = goldBar.offsetHeight;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset;

                window.scrollTo({
                    top: targetPosition - (navbarHeight + (goldBar.classList.contains('hidden') ? 0 : goldBarHeight)),
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add scroll listener only after preloader is gone
    window.addEventListener('load', () => {
        setTimeout(() => {
            window.addEventListener('scroll', handleScroll, { passive: true });
        }, 600); // Slightly longer than preloader fade
    });
});
