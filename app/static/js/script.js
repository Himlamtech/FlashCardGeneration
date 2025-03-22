document.addEventListener('DOMContentLoaded', function() {
    // Initialize components
    initFlashcards();
    initSidebar();
    initFlashMessages();
    initAnimations();
    initDarkMode();
    initForms();
    initToolCards();
    
    // Remove loading screen if present
    const loadingScreen = document.querySelector('.loading-container');
    if (loadingScreen) {
        setTimeout(() => {
            loadingScreen.style.opacity = '0';
            setTimeout(() => {
                loadingScreen.remove();
            }, 300);
        }, 300);
    }
});

/**
 * Initialize flashcard interactions
 */
function initFlashcards() {
    const flashcards = document.querySelectorAll('.flashcard');
    
    flashcards.forEach(card => {
        card.addEventListener('click', function(e) {
            // Don't flip if clicking on action buttons
            if (e.target.closest('.flashcard-actions')) {
                return;
            }
            
            // Toggle flipped class
            this.classList.toggle('flipped');
        });
    });
    
    // Study mode navigation
    const nextBtn = document.querySelector('.study-next');
    const prevBtn = document.querySelector('.study-prev');
    const studyContainer = document.querySelector('.study-container');
    
    if (nextBtn && prevBtn && studyContainer) {
        let currentIndex = 0;
        const totalCards = flashcards.length;
        
        // Update counter display
        const updateCounter = () => {
            const counter = document.querySelector('.study-counter');
            if (counter) {
                counter.textContent = `${currentIndex + 1}/${totalCards}`;
            }
        };
        
        // Show current card
        const showCard = (index) => {
            flashcards.forEach((card, i) => {
                if (i === index) {
                    card.style.display = 'block';
                    // Reset flip state
                    card.classList.remove('flipped');
                } else {
                    card.style.display = 'none';
                }
            });
            updateCounter();
        };
        
        // Initialize
        if (totalCards > 0) {
            showCard(0);
        }
        
        // Next button
        nextBtn.addEventListener('click', () => {
            currentIndex = (currentIndex + 1) % totalCards;
            showCard(currentIndex);
        });
        
        // Previous button
        prevBtn.addEventListener('click', () => {
            currentIndex = (currentIndex - 1 + totalCards) % totalCards;
            showCard(currentIndex);
        });
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (document.querySelector('.study-container:focus-within')) {
                if (e.key === 'ArrowRight') {
                    nextBtn.click();
                } else if (e.key === 'ArrowLeft') {
                    prevBtn.click();
                } else if (e.key === ' ' || e.key === 'Enter') {
                    // Toggle flip with spacebar or enter
                    const currentCard = flashcards[currentIndex];
                    if (currentCard) {
                        currentCard.classList.toggle('flipped');
                    }
                }
            }
        });
    }
}

/**
 * Initialize sidebar interactions
 */
function initSidebar() {
    const toggleBtn = document.querySelector('.mobile-nav-toggle');
    const sidebar = document.querySelector('.app-sidebar');
    
    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', () => {
            sidebar.classList.toggle('show');
        });
        
        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', (e) => {
            if (window.innerWidth <= 768 && 
                sidebar.classList.contains('show') && 
                !sidebar.contains(e.target) && 
                !toggleBtn.contains(e.target)) {
                sidebar.classList.remove('show');
            }
        });
    }
    
    // Collapsible sub-menus
    const dropdownLinks = document.querySelectorAll('.nav-link.has-dropdown');
    
    dropdownLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            this.classList.toggle('collapsed');
            
            const submenu = this.nextElementSibling;
            if (submenu && submenu.classList.contains('nav-submenu')) {
                if (submenu.style.maxHeight) {
                    submenu.style.maxHeight = null;
                } else {
                    submenu.style.maxHeight = submenu.scrollHeight + 'px';
                }
            }
        });
    });
}

/**
 * Initialize flash messages with auto-dismiss
 */
function initFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(message => {
        // Add close button
        const closeBtn = document.createElement('button');
        closeBtn.classList.add('close');
        closeBtn.innerHTML = '&times;';
        closeBtn.addEventListener('click', () => {
            message.remove();
        });
        message.appendChild(closeBtn);
        
        // Auto dismiss after 5 seconds
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });
}

/**
 * Initialize animations for elements
 */
function initAnimations() {
    // Elements that should fade in when visible
    const fadeElements = document.querySelectorAll('.fade-in-element');
    
    if ('IntersectionObserver' in window) {
        const fadeObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                    fadeObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });
        
        fadeElements.forEach(el => {
            fadeObserver.observe(el);
        });
    } else {
        // Fallback for browsers that don't support IntersectionObserver
        fadeElements.forEach(el => {
            el.classList.add('fade-in');
        });
    }
    
    // Add page transition class to the body
    document.body.classList.add('page-transition');
}

/**
 * Initialize dark mode toggle
 */
function initDarkMode() {
    const darkModeToggle = document.querySelector('.dark-mode-toggle');
    
    // Check for saved theme preference or respect OS preference
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // Set initial theme
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.documentElement.setAttribute('data-theme', 'dark');
        if (darkModeToggle) {
            darkModeToggle.classList.add('active');
        }
    }
    
    // Toggle theme when button is clicked
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            darkModeToggle.classList.toggle('active');
        });
    }
}

/**
 * Initialize form validations and enhancements
 */
function initForms() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        // Add loading state when form is submitted
        form.addEventListener('submit', function() {
            this.classList.add('form-submitting');
            
            const submitBtn = this.querySelector('[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm mr-2" role="status" aria-hidden="true"></span> Processing...';
                submitBtn.disabled = true;
                
                // Store original text for restoration on error
                submitBtn.dataset.originalText = originalText;
            }
        });
        
        // Basic form validation
        const requiredInputs = form.querySelectorAll('[required]');
        requiredInputs.forEach(input => {
            input.addEventListener('invalid', function(e) {
                e.preventDefault();
                this.classList.add('is-invalid');
                
                // Restore submit button state
                const submitBtn = form.querySelector('[type="submit"]');
                if (submitBtn && submitBtn.dataset.originalText) {
                    submitBtn.innerHTML = submitBtn.dataset.originalText;
                    submitBtn.disabled = false;
                }
                
                form.classList.remove('form-submitting');
            });
            
            input.addEventListener('input', function() {
                this.classList.remove('is-invalid');
            });
        });
    });
}

/**
 * Initialize tool cards interactions
 */
function initToolCards() {
    const toolCards = document.querySelectorAll('.tool-card');
    
    toolCards.forEach(card => {
        card.addEventListener('click', function() {
            const href = this.getAttribute('data-href');
            if (href) {
                window.location.href = href;
            }
        });
    });
} 