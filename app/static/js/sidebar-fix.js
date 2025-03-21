/**
 * StudyWAI - Sidebar Fix
 * Ensures the sidebar doesn't interfere with the content visibility
 */

window.studywaiSidebar = {
    initialized: false,
    
    // Initialize sidebar toggle without affecting content
    setupSidebarToggle: function() {
        console.log("Setting up sidebar toggle (fixed version)");
        const sidebarBtn = document.getElementById('sidebarCollapse');
        const sidebar = document.getElementById('sidebar');
        
        if (sidebarBtn && sidebar) {
            // Remove any existing click handlers (important!)
            const newBtn = sidebarBtn.cloneNode(true);
            sidebarBtn.parentNode.replaceChild(newBtn, sidebarBtn);
            
            newBtn.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Toggle sidebar only, not content
                sidebar.classList.toggle('active');
                
                // Safe way to adjust content margins without hiding it
                const content = document.getElementById('content');
                if (content) {
                    if (sidebar.classList.contains('active')) {
                        content.style.marginLeft = "0";
                        content.style.width = "100%";
                    } else {
                        content.style.marginLeft = "280px";
                        content.style.width = "calc(100% - 280px)";
                    }
                }
                
                // Animate the toggle icon
                const icon = this.querySelector('i');
                if (icon) {
                    icon.style.transition = 'transform 0.3s ease';
                    icon.style.transform = sidebar.classList.contains('active') ? 'rotate(180deg)' : '';
                }
                
                console.log("Sidebar toggled without touching content visibility");
            });
        }
    },
    
    // Setup the collapsible submenu
    setupSubmenu: function() {
        const toggles = document.querySelectorAll('.flashcard-toggle');
        toggles.forEach(toggle => {
            toggle.addEventListener('click', function() {
                const target = document.querySelector(this.getAttribute('data-bs-target'));
                if (target) {
                    const isExpanded = this.getAttribute('aria-expanded') === 'true';
                    this.setAttribute('aria-expanded', !isExpanded);
                    
                    if (isExpanded) {
                        target.classList.remove('show');
                    } else {
                        target.classList.add('show');
                    }
                    
                    // Toggle icon
                    const icon = this.querySelector('.submenu-icon');
                    if (icon) {
                        if (isExpanded) {
                            icon.style.transform = 'rotate(-90deg)';
                        } else {
                            icon.style.transform = '';
                        }
                    }
                }
            });
        });
    },
    
    // Initialize the sidebar fixes
    init: function() {
        if (this.initialized) return;
        console.log("Sidebar fix initializing");
        
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.setupSidebarToggle();
                this.setupSubmenu();
                this.initialized = true;
                console.log("Sidebar fix initialized");
            });
        } else {
            this.setupSidebarToggle();
            this.setupSubmenu();
            this.initialized = true;
            console.log("Sidebar fix initialized (DOM already loaded)");
        }
    }
};

// Run immediately
window.studywaiSidebar.init(); 