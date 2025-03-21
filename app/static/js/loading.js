/**
 * StudyWAI - Loading Animations
 * Provides enhanced loading animations for all API requests
 */

document.addEventListener('DOMContentLoaded', function() {
    // Global loading spinner
    const createLoadingSpinner = () => {
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
    };

    // Add spinner to body when forms are submitted
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        // Skip forms that have their own loading handling
        if (form.classList.contains('skip-loading-handler')) return;
        
        form.addEventListener('submit', function(e) {
            if (this.method === 'post' && !this.getAttribute('data-no-loading')) {
                const spinner = createLoadingSpinner();
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

    // Button loading state
    const actionButtons = document.querySelectorAll('.btn-action');
    actionButtons.forEach(button => {
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

    // Enhanced fetch function with loading indicators
    window.fetchWithLoading = (url, options = {}) => {
        const spinner = createLoadingSpinner();
        document.body.appendChild(spinner);
        
        return fetch(url, options)
            .then(response => {
                document.body.removeChild(spinner);
                return response;
            })
            .catch(error => {
                document.body.removeChild(spinner);
                throw error;
            });
    };

    // Add CSS if not already present
    if (!document.getElementById('loading-styles')) {
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
    }
}); 