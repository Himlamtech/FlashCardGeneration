/**
 * Main JavaScript functionality for StudyWAI
 */
 
// Remove loading spinner when page is fully loaded
window.addEventListener('load', function() {
  const loadingContainer = document.querySelector('.loading-container');
  if (loadingContainer) {
    loadingContainer.style.opacity = '0';
    setTimeout(() => {
      loadingContainer.style.display = 'none';
    }, 300);
  }
});

// Handle flashcard flipping
document.addEventListener('DOMContentLoaded', function() {
  const flashcards = document.querySelectorAll('.flashcard');
  
  flashcards.forEach(card => {
    card.addEventListener('click', function(e) {
      // Don't flip if clicking action buttons
      if (e.target.closest('.flashcard-actions') || 
          e.target.closest('button') || 
          e.target.closest('a')) {
        return;
      }
      
      this.classList.toggle('flipped');
    });
  });
  
  // Add accessibility support for keyboard navigation
  const focusableElements = document.querySelectorAll('a, button, input, textarea, select, [tabindex]:not([tabindex="-1"])');
  
  focusableElements.forEach(element => {
    element.addEventListener('keydown', function(e) {
      // Enter key
      if (e.key === 'Enter') {
        e.preventDefault();
        element.click();
      }
    });
    
    // Add keyboard-focus class for better focus styles
    element.addEventListener('focus', function() {
      this.classList.add('keyboard-focus');
    });
    
    element.addEventListener('blur', function() {
      this.classList.remove('keyboard-focus');
    });
    
    // Remove keyboard-focus class on mouse click
    element.addEventListener('mousedown', function() {
      this.classList.remove('keyboard-focus');
    });
  });
});

// Add fade-in animations to elements
const animateElements = () => {
  const elementsToAnimate = document.querySelectorAll('.fade-in-element:not(.fade-in)');
  
  elementsToAnimate.forEach((element, index) => {
    // Stagger animation with a small delay
    setTimeout(() => {
      element.classList.add('fade-in');
    }, index * 100);
  });
};

// Run animations when page loads and after dynamic content changes
document.addEventListener('DOMContentLoaded', animateElements);

// Helper function to format dates
function formatDate(dateString) {
  const options = { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  };
  
  return new Date(dateString).toLocaleDateString(undefined, options);
}

// Initialize all date elements
document.addEventListener('DOMContentLoaded', function() {
  const dateElements = document.querySelectorAll('[data-date]');
  
  dateElements.forEach(element => {
    const date = element.getAttribute('data-date');
    if (date) {
      element.textContent = formatDate(date);
    }
  });
});

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