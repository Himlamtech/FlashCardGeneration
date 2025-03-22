/**
 * Loading and page transition utilities
 */

// Create and show loading spinner
function showLoading() {
    // Check if loading container already exists
    if (document.querySelector('.loading-container')) return;
    
    // Create loading container
    const loadingContainer = document.createElement('div');
    loadingContainer.classList.add('loading-container');
    
    // Create loading spinner
    const loadingSpinner = document.createElement('div');
    loadingSpinner.classList.add('loading-spinner');
    
    // Append spinner to container
    loadingContainer.appendChild(loadingSpinner);
    
    // Append container to body
    document.body.appendChild(loadingContainer);
}

// Hide and remove loading spinner
function hideLoading() {
    const loadingContainer = document.querySelector('.loading-container');
    if (!loadingContainer) return;
    
    // Fade out loading container
    loadingContainer.style.opacity = '0';
    
    // Remove after transition
    setTimeout(() => {
        loadingContainer.remove();
    }, 300);
}

// Show loading spinner when navigating between pages
document.addEventListener('DOMContentLoaded', function() {
    // Add loading indicator to all internal links except for form actions
    const internalLinks = document.querySelectorAll('a[href^="/"]:not([href^="#"]):not([target="_blank"])');
    
    internalLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Skip if modifier keys are pressed
            if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
            
            // Skip if this is part of a form action
            if (link.closest('form')) return;
            
            e.preventDefault();
            
            // Show loading spinner
            showLoading();
            
            // Navigate to the link after a short delay for the spinner to be visible
            setTimeout(() => {
                window.location.href = link.href;
            }, 100);
        });
    });
    
    // Hide loading when page is fully loaded
    window.addEventListener('load', hideLoading);
});

// Add loading indicator for form submissions
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form:not([data-no-loading])');
    
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            // Show loading spinner
            showLoading();
        });
    });
});

// Create and show loading spinner during AJAX requests
let activeRequests = 0;

// Setup AJAX request interceptor
function setupAjaxLoadingInterceptor() {
    // Check if XMLHttpRequest exists and hasn't been patched already
    if (window.XMLHttpRequest && !window.XMLHttpRequest._patched) {
        const originalOpen = XMLHttpRequest.prototype.open;
        const originalSend = XMLHttpRequest.prototype.send;
        
        // Override open method
        XMLHttpRequest.prototype.open = function() {
            this._ajaxLoadingInterceptor = true;
            return originalOpen.apply(this, arguments);
        };
        
        // Override send method
        XMLHttpRequest.prototype.send = function() {
            if (this._ajaxLoadingInterceptor) {
                activeRequests++;
                
                if (activeRequests === 1) {
                    showLoading();
                }
                
                const originalOnReadyStateChange = this.onreadystatechange;
                this.onreadystatechange = function() {
                    if (this.readyState === 4) {
                        activeRequests--;
                        
                        if (activeRequests === 0) {
                            hideLoading();
                        }
                    }
                    
                    if (originalOnReadyStateChange) {
                        originalOnReadyStateChange.apply(this, arguments);
                    }
                };
            }
            
            return originalSend.apply(this, arguments);
        };
        
        // Mark as patched
        window.XMLHttpRequest._patched = true;
    }
    
    // Also handle fetch requests if fetch is available
    if (window.fetch && !window._fetchPatched) {
        const originalFetch = window.fetch;
        
        window.fetch = function() {
            activeRequests++;
            
            if (activeRequests === 1) {
                showLoading();
            }
            
            return originalFetch.apply(this, arguments)
                .then(response => {
                    activeRequests--;
                    
                    if (activeRequests === 0) {
                        hideLoading();
                    }
                    
                    return response;
                })
                .catch(error => {
                    activeRequests--;
                    
                    if (activeRequests === 0) {
                        hideLoading();
                    }
                    
                    throw error;
                });
        };
        
        // Mark as patched
        window._fetchPatched = true;
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    setupAjaxLoadingInterceptor();
}); 