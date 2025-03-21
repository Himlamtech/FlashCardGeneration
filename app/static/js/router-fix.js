/**
 * StudyWAI - URL Router Fix
 * Handles routing issues and prevents URL hash fragments from causing problems
 */

// Expose functions globally to ensure they're accessible
window.studywaiRouter = {
    // Clean URL if it has a hash fragment
    cleanUrl: function() {
        if (window.location.hash) {
            console.log("Cleaning URL with hash:", window.location.href);
            const cleanUrl = window.location.pathname;
            try {
                history.replaceState(null, '', cleanUrl);
                console.log("URL cleaned to:", cleanUrl);
                return true;
            } catch (e) {
                console.error("Error cleaning URL:", e);
                return false;
            }
        }
        return false;
    },
    
    // Fix links with hash fragments
    fixHashLinks: function() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            // Skip bootstrap toggles
            if (anchor.getAttribute('data-bs-toggle')) return;
            
            // Replace # links with javascript:void(0)
            if (anchor.getAttribute('href') === '#') {
                anchor.setAttribute('href', 'javascript:void(0);');
                console.log("Fixed empty hash link");
            }
        });
    },
    
    // Setup navigation handling
    setupNavigation: function() {
        document.addEventListener('click', function(e) {
            // Find closest anchor tag if clicked on child element
            const anchor = e.target.closest('a');
            if (!anchor) return;
            
            const href = anchor.getAttribute('href');
            
            // Skip external links, javascript: links, and bootstrap toggles
            if (!href || 
                href.startsWith('http') || 
                href.startsWith('javascript:') || 
                anchor.getAttribute('data-bs-toggle')) {
                return;
            }
            
            // Skip if modifier keys are pressed
            if (e.ctrlKey || e.metaKey || e.shiftKey) return;
            
            // Handle hash links properly
            if (href.startsWith('#')) {
                e.preventDefault();
                const targetId = href.substring(1);
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({ behavior: 'smooth' });
                }
                return;
            }
        });
    },
    
    // Initialize all fixes
    init: function() {
        console.log("Router fix initializing");
        this.cleanUrl();
        
        // Wait for DOM to be ready for the rest
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.fixHashLinks();
                this.setupNavigation();
                console.log("Router fix initialized");
            });
        } else {
            this.fixHashLinks();
            this.setupNavigation();
            console.log("Router fix initialized (DOM already loaded)");
        }
    }
};

// Initialize router fixes
window.studywaiRouter.init(); 