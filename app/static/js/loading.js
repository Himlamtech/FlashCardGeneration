/**
 * StudyWAI - Loading Animations
 * Provides enhanced loading animations for all API requests
 */

// Create a namespace to avoid conflicts
window.studywaiLoading = {
    initialized: false,
    
    // Create a loading spinner element
    createLoadingSpinner: function() {
        const spinner = document.createElement('div');
        spinner.classList.add('global-spinner');
        spinner.innerHTML = `
            <div class="spinner-overlay">
                <div class="spinner-container">
                    <div class="spinner"></div>
                    <p class="mt-3">Processing your request...</p>
                </div>
            </div>
        `;
        return spinner;
    },
    
    // Handle form submissions
    setupFormHandlers: function() {
        const forms = document.querySelectorAll('form:not([data-loading-handled])');
        forms.forEach(form => {
            // Skip forms that have their own loading handling
            if (form.classList.contains('skip-loading-handler')) return;
            
            // Mark this form as handled to prevent duplicate event listeners
            form.setAttribute('data-loading-handled', 'true');
            
            form.addEventListener('submit', function(e) {
                if (this.method === 'post' && !this.getAttribute('data-no-loading')) {
                    const spinner = window.studywaiLoading.createLoadingSpinner();
                    document.body.appendChild(spinner);
                    
                    // Auto-remove after 30 seconds to prevent indefinite loading
                    setTimeout(() => {
                        if (document.body.contains(spinner)) {
                            document.body.removeChild(spinner);
                        }
                    }, 30000);
                }
            });
        });
    },
    
    // Handle button loading states
    setupButtonHandlers: function() {
        const actionButtons = document.querySelectorAll('.btn-action:not([data-loading-handled])');
        actionButtons.forEach(button => {
            button.setAttribute('data-loading-handled', 'true');
            
            button.addEventListener('click', function() {
                if (this.getAttribute('data-loading-text')) {
                    const originalHTML = this.innerHTML;
                    const loadingText = this.getAttribute('data-loading-text');
                    
                    this.innerHTML = `
                        <span class="spinner-border spinner-border-sm me-2" 
                              role="status" aria-hidden="true"></span>
                        ${loadingText}
                    `;
                    this.disabled = true;
                    
                    // Store original content for restoration
                    this.setAttribute('data-original-html', originalHTML);
                    
                    // Auto-restore after 30 seconds to prevent indefinite loading
                    setTimeout(() => {
                        if (this.disabled && this.getAttribute('data-original-html')) {
                            this.innerHTML = this.getAttribute('data-original-html');
                            this.disabled = false;
                        }
                    }, 30000);
                }
            });
        });
    },
    
    // Create enhanced fetch function
    setupFetchWithLoading: function() {
        window.fetchWithLoading = (url, options = {}) => {
            const spinner = window.studywaiLoading.createLoadingSpinner();
            document.body.appendChild(spinner);
            
            return fetch(url, options)
                .then(response => {
                    document.body.removeChild(spinner);
                    return response;
                })
                .catch(error => {
                    if (document.body.contains(spinner)) {
                        document.body.removeChild(spinner);
                    }
                    throw error;
                });
        };
    },
    
    // Add CSS for loading animations
    addStyles: function() {
        if (document.getElementById('loading-styles')) return;
        
        const style = document.createElement('style');
        style.id = 'loading-styles';
        style.textContent = `
            .global-spinner {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 9999;
            }
            
            .spinner-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.5);
                display: flex;
                justify-content: center;
                align-items: center;
            }
            
            .spinner-container {
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            }
            
            .spinner {
                width: 50px;
                height: 50px;
                border: 5px solid #f3f3f3;
                border-top: 5px solid var(--primary-color, #4a6bff);
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin: 0 auto;
            }
            
            .btn-loading {
                position: relative;
                pointer-events: none;
            }
            
            .btn-loading:after {
                content: "";
                position: absolute;
                width: 16px;
                height: 16px;
                top: calc(50% - 8px);
                left: calc(50% - 8px);
                border: 2px solid rgba(255, 255, 255, 0.7);
                border-radius: 50%;
                border-top: 2px solid #fff;
                animation: spin 0.6s linear infinite;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .fade-in {
                animation: fadeIn 0.5s;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
        `;
        document.head.appendChild(style);
    },
    
    // Initialize loading functionality
    init: function() {
        if (this.initialized) return;
        console.log("Loading JS initializing");
        
        this.addStyles();
        
        // Setup immediately if DOM is ready, otherwise wait
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.setupFormHandlers();
                this.setupButtonHandlers();
                this.setupFetchWithLoading();
                this.initialized = true;
                console.log("Loading JS initialized");
            });
        } else {
            this.setupFormHandlers();
            this.setupButtonHandlers();
            this.setupFetchWithLoading();
            this.initialized = true;
            console.log("Loading JS initialized (DOM already loaded)");
        }
    }
};

// Initialize loading functionality
window.studywaiLoading.init(); 