/**
 * StudyWAI - Main Script File
 */

// Create a namespace to avoid conflicts
window.studywaiMain = {
    initialized: false,
    
    // Update footer year
    updateFooterYear: function() {
        const footerYear = document.querySelector('footer p');
        if (footerYear) {
            const currentYear = new Date().getFullYear();
            footerYear.innerHTML = footerYear.innerHTML.replace('{{ now.year }}', currentYear);
        }
    },
    
    // Set up animations for elements
    setupAnimations: function() {
        // Add animation class to elements when they appear in viewport
        const animatables = document.querySelectorAll('.animate-on-scroll');
        if ('IntersectionObserver' in window && animatables.length > 0) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('fade-in-element');
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.1 });
            
            animatables.forEach(element => {
                observer.observe(element);
            });
        } else {
            // Fallback for browsers without IntersectionObserver
            animatables.forEach(element => {
                element.classList.add('fade-in-element');
            });
        }
        
        // Add animation class to cards when they appear in viewport
        const cards = document.querySelectorAll('.card');
        if ('IntersectionObserver' in window && cards.length > 0) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('fade-in-element');
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.1 });
            
            cards.forEach(card => {
                observer.observe(card);
            });
        }
    },
    
    // Make flashcards interactive
    setupFlashcards: function() {
        const flashcards = document.querySelectorAll('.flashcard');
        flashcards.forEach(card => {
            card.addEventListener('click', function() {
                this.classList.toggle('flipped');
            });
        });
    },
    
    // Set up auto-hiding alerts
    setupAlerts: function() {
        setTimeout(() => {
            document.querySelectorAll('.alert').forEach(alert => {
                if (alert && typeof bootstrap !== 'undefined') {
                    const bsAlert = new bootstrap.Alert(alert);
                    bsAlert.close();
                }
            });
        }, 5000);
    },
    
    // Set up form validation
    setupFormValidation: function() {
        const forms = document.querySelectorAll('form:not([data-validation-handled])');
        forms.forEach(form => {
            form.setAttribute('data-validation-handled', 'true');
            form.addEventListener('submit', function(event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                
                form.classList.add('was-validated');
            }, false);
        });
    },
    
    // Set up sidebar toggle
    setupSidebar: function() {
        const sidebarToggle = document.getElementById('sidebarCollapse');
        if (sidebarToggle) {
            sidebarToggle.addEventListener('click', function() {
                document.getElementById('sidebar').classList.toggle('active');
                document.getElementById('content').classList.toggle('active');
            });
        }
    },
    
    // Initialize all functionality
    init: function() {
        if (this.initialized) {
            console.log("Main script already initialized, skipping");
            return;
        }
        
        console.log("Main script initializing...");
        
        // Important: Make sure content is visible
        this.ensureContentVisible();
        
        // Set up event listeners
        this.setupEventListeners();
        
        // Initialize interactive elements
        this.initializeFlashcards();
        
        // Setup animations
        this.setupFadeIn();
        
        // Setup delete confirmation
        this.setupDeleteHandlers();
        
        this.initialized = true;
        console.log("Main script initialized");
        
        // Run another visibility check after everything else
        setTimeout(() => this.ensureContentVisible(), 100);
        setTimeout(() => this.ensureContentVisible(), 500);
        setTimeout(() => this.ensureContentVisible(), 1000);
    },
    
    // Make absolutely sure content is visible
    ensureContentVisible: function() {
        console.log("Ensuring content visibility from main script");
        const content = document.getElementById('content');
        const container = document.querySelector('#content .container');
        
        if (content) {
            content.style.display = 'block';
            content.style.opacity = '1';
            content.style.visibility = 'visible';
        }
        
        if (container) {
            container.style.display = 'block';
            container.style.opacity = '1';
            container.style.visibility = 'visible';
        }
    },
    
    // Setup proper delete confirmation handling
    setupDeleteHandlers: function() {
        // Fix delete confirmation modal issues
        const deleteButtons = document.querySelectorAll('.delete-button, button[type="submit"][formaction*="delete"], form[action*="delete"] button[type="submit"]');
        
        deleteButtons.forEach(button => {
            // Remove any existing click handlers to prevent duplicates
            const newButton = button.cloneNode(true);
            button.parentNode.replaceChild(newButton, button);
            
            newButton.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                // Get the form or create fallback path
                const form = this.closest('form');
                const deleteUrl = form ? form.action : this.getAttribute('formaction') || this.getAttribute('data-action');
                
                if (!deleteUrl) {
                    console.error('Delete URL not found');
                    return;
                }
                
                // Create or use existing confirmation
                let confirmDialog = document.getElementById('deleteConfirmDialog');
                if (!confirmDialog) {
                    confirmDialog = document.createElement('div');
                    confirmDialog.id = 'deleteConfirmDialog';
                    confirmDialog.className = 'modal fade';
                    confirmDialog.innerHTML = `
                        <div class="modal-dialog">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title">Confirm Deletion</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    <p>Are you sure you want to delete this item?</p>
                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                                    <button type="button" class="btn btn-danger" id="confirmDeleteBtn">Delete</button>
                                </div>
                            </div>
                        </div>
                    `;
                    document.body.appendChild(confirmDialog);
                }
                
                // Initialize modal if Bootstrap is available
                let modal;
                if (typeof bootstrap !== 'undefined') {
                    modal = new bootstrap.Modal(confirmDialog);
                    modal.show();
                } else {
                    // Fallback if bootstrap isn't loaded yet
                    confirmDialog.style.display = 'block';
                }
                
                // Set up confirmation button
                const confirmBtn = document.getElementById('confirmDeleteBtn');
                if (confirmBtn) {
                    // Remove existing listeners
                    const newConfirmBtn = confirmBtn.cloneNode(true);
                    confirmBtn.parentNode.replaceChild(newConfirmBtn, confirmBtn);
                    
                    newConfirmBtn.addEventListener('click', function() {
                        try {
                            if (form) {
                                // If we have a form, submit it
                                form.submit();
                            } else {
                                // Otherwise create a form and submit it
                                const dynamicForm = document.createElement('form');
                                dynamicForm.method = 'POST';
                                dynamicForm.action = deleteUrl;
                                document.body.appendChild(dynamicForm);
                                dynamicForm.submit();
                            }
                        } catch (err) {
                            console.error('Error during delete:', err);
                            window.location.href = deleteUrl; // Fallback direct navigation
                        }
                    });
                }
            });
        });
    },
    
    // Set up event listeners for the app
    setupEventListeners: function() {
        // Initialize flashcards when clicking on them
        document.addEventListener('click', event => {
            const flashcard = event.target.closest('.flip-card');
            if (flashcard) {
                flashcard.classList.toggle('flipped');
            }
        });
        
        // Don't let sidebar toggle affect content visibility
        const sidebarCollapse = document.getElementById('sidebarCollapse');
        if (sidebarCollapse) {
            const originalHandler = sidebarCollapse.onclick;
            sidebarCollapse.onclick = (e) => {
                if (originalHandler) originalHandler(e);
                // Make sure content is visible regardless
                setTimeout(() => this.ensureContentVisible(), 10);
            };
        }
    },
    
    // Initialize flashcards
    initializeFlashcards: function() {
        document.querySelectorAll('.flip-card').forEach(card => {
            card.addEventListener('click', function() {
                this.classList.toggle('flipped');
            });
        });
    },
    
    // Set up fade-in animations
    setupFadeIn: function() {
        if ('IntersectionObserver' in window) {
            const fadeElems = document.querySelectorAll('.fade-in-element');
            const fadeObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('fade-in');
                        fadeObserver.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.1 });
            
            fadeElems.forEach(elem => fadeObserver.observe(elem));
        } else {
            // Fallback for browsers without IntersectionObserver
            document.querySelectorAll('.fade-in-element').forEach(elem => {
                elem.classList.add('fade-in');
            });
        }
    }
};

// Run on document ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => window.studywaiMain.init());
} else {
    window.studywaiMain.init();
}

// Also run on window load to be safe
window.addEventListener('load', () => window.studywaiMain.init()); 