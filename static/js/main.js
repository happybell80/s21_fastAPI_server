// goosefarminvesting main JS file

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded - initializing...');

    // Debug elements
    console.log('Mobile menu button:', document.getElementById('mobile-menu'));
    console.log('Nav menu:', document.getElementById('nav-menu'));

    // Smooth scrolling for anchor links (revised to avoid invalid selectors)
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            
            // Skip empty anchors or language toggles
            if (href === "#" || this.closest('.language-dropdown')) {
                return; // Allow default event handling for language toggles
            }
            
            // Only proceed if there's a valid ID to scroll to
            if (href.length > 1) { // Must be longer than just "#"
                e.preventDefault(); // Only prevent default if we'll handle scrolling
                try {
                    const targetElement = document.querySelector(href);
                    if (targetElement) {
                        targetElement.scrollIntoView({
                            behavior: 'smooth'
                        });
                    }
                } catch (error) {
                    console.error("Invalid selector:", href);
                }
            }
        });
    });

    // Add active class to nav links based on current page
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('nav ul li a');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active');
        }
    });

    // Add animation to the CTA buttons on scroll
    const ctaButtons = document.querySelectorAll('.btn');
    if (ctaButtons.length > 0) {
        window.addEventListener('scroll', function() {
            ctaButtons.forEach(button => {
                if (isElementInViewport(button)) {
                    button.classList.add('animate');
                }
            });
        });
    }

    // Helper function to check if element is in viewport
    function isElementInViewport(el) {
        const rect = el.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    // Mobile menu toggle
    const mobileMenuBtn = document.getElementById('mobile-menu');
    const navMenu = document.getElementById('nav-menu');
    
    if (mobileMenuBtn && navMenu) {
        console.log('Menu elements found and initialized');
        mobileMenuBtn.addEventListener('click', function(e) {
            console.log('Menu toggle clicked');
            e.preventDefault();
            e.stopPropagation();
            navMenu.classList.toggle('active');
            mobileMenuBtn.classList.toggle('active');
            console.log('Nav menu class list after toggle:', navMenu.classList);
        });
    } else {
        console.error('Menu elements not found! mobile-menu:', mobileMenuBtn, 'nav-menu:', navMenu);
    }
    
    // Language toggle functionality
    const languageBtn = document.getElementById('language-btn');
    const languageDropdown = document.getElementById('language-dropdown');
    const languageOptions = document.querySelectorAll('.language-dropdown a');
    
    // Default language from browser or set to 'en'
    let currentLang = localStorage.getItem('preferredLanguage') || 'en';
    
    // Show/hide language dropdown
    if (languageBtn) {
        languageBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            languageDropdown.classList.toggle('show');
        });
    }
    
    // Handle language selection
    languageOptions.forEach(option => {
        option.addEventListener('click', function(e) {
            e.preventDefault();
            const lang = this.getAttribute('data-lang');
            setLanguage(lang);
            
            // Remove active class from all options
            languageOptions.forEach(opt => opt.classList.remove('active'));
            
            // Add active class to selected option
            this.classList.add('active');
            
            // Hide dropdown
            languageDropdown.classList.remove('show');
        });
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (languageDropdown && languageDropdown.classList.contains('show')) {
            if (!languageDropdown.contains(e.target) && e.target !== languageBtn) {
                languageDropdown.classList.remove('show');
            }
        }
    });
    
    // Function to set language
    function setLanguage(lang) {
        currentLang = lang;
        localStorage.setItem('preferredLanguage', lang);
        
        // Redirect to language-specific page
        if (lang === 'ko') {
            // Check if we're already on a Korean page
            if (!window.location.pathname.includes('/ko/')) {
                // Generate Korean URL - add /ko/ to the path
                const currentPath = window.location.pathname;
                const koPath = currentPath === '/' ? '/ko/' : `/ko${currentPath}`;
                window.location.href = koPath;
            }
        } else {
            // English - remove /ko/ from path if present
            if (window.location.pathname.includes('/ko/')) {
                const enPath = window.location.pathname.replace('/ko', '');
                window.location.href = enPath || '/';
            }
        }
    }
    
    // Initialize language UI based on current language
    function initLanguage() {
        // Mark the current language as active in the dropdown
        languageOptions.forEach(option => {
            if (option.getAttribute('data-lang') === currentLang) {
                option.classList.add('active');
            } else {
                option.classList.remove('active');
            }
        });
    }
    
    // Initialize language
    initLanguage();
}); 