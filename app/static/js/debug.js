/**
 * Debug and troubleshooting utilities for StudyWAI
 * This script helps diagnose common frontend issues and attempts to apply fixes
 */

// Log debugging information to console
console.log('StudyWAI Debug Script loaded');

// Check if DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded');
    
    // Debug information
    console.log('User agent:', navigator.userAgent);
    console.log('Window dimensions:', window.innerWidth, 'x', window.innerHeight);
    
    // Check and report loaded resources
    checkResources();
    
    // Fix common issues
    fixCommonIssues();
    
    // Enhance error handling
    enhanceErrorHandling();
});

// Check if all required resources loaded properly
function checkResources() {
    // Check stylesheets
    const stylesheets = document.styleSheets;
    console.log(`Loaded ${stylesheets.length} stylesheets`);
    
    try {
        for (let i = 0; i < stylesheets.length; i++) {
            console.log(`Stylesheet ${i + 1}:`, stylesheets[i].href);
        }
    } catch (e) {
        console.warn('Could not access all stylesheet details:', e);
    }
    
    // Check scripts
    const scripts = document.scripts;
    console.log(`Loaded ${scripts.length} scripts`);
    
    try {
        Array.from(scripts).forEach((script, index) => {
            console.log(`Script ${index + 1}:`, script.src || 'inline script');
        });
    } catch (e) {
        console.warn('Could not access all script details:', e);
    }
    
    // Check for Bootstrap
    if (typeof bootstrap === 'undefined') {
        console.error('Bootstrap JavaScript not loaded!');
    } else {
        console.log('Bootstrap loaded successfully');
    }
}

// Fix common issues
function fixCommonIssues() {
    // Fix flashcard display issues
    fixFlashcardDisplay();
    
    // Fix interactive elements
    fixInteractiveElements();
    
    // Fix navigation issues
    fixNavigationIssues();
    
    // Enhance content loading
    enhanceContentLoading();
}

// Fix flashcard display issues
function fixFlashcardDisplay() {
    const flashcards = document.querySelectorAll('.flashcard-item');
    console.log(`Found ${flashcards.length} flashcard items`);
    
    if (flashcards.length === 0) {
        console.warn('No flashcards found, checking if data exists');
        
        // Check if we're on the flashcards page
        if (window.location.pathname === '/' || window.location.pathname === '/index') {
            const container = document.getElementById('flashcards-container');
            
            if (container) {
                console.log('Flashcard container exists, checking if empty state is properly shown');
                
                // Make sure the empty state is visible
                const emptyState = container.querySelector('.card');
                if (!emptyState) {
                    console.warn('Empty state not found, adding it');
                    
                    container.innerHTML = `
                        <div class="col-12">
                            <div class="card">
                                <div class="card-body text-center py-5">
                                    <div class="mb-3">
                                        <i class="fas fa-layer-group text-muted fa-4x"></i>
                                    </div>
                                    <h3 class="fw-bold">No Flashcards Yet</h3>
                                    <p class="text-muted">Create your first flashcard to get started!</p>
                                    <a href="/create" class="btn btn-primary">
                                        <i class="fas fa-plus me-2"></i> Create Flashcard
                                    </a>
                                </div>
                            </div>
                        </div>
                    `;
                }
            }
        }
    } else {
        // Make sure flashcards are visible
        flashcards.forEach(card => {
            card.style.display = 'block';
            card.classList.add('fade-in');
            
            // Make sure flip functionality works
            const innerCard = card.querySelector('.flashcard');
            if (innerCard) {
                innerCard.addEventListener('click', function(e) {
                    // Don't flip if clicking on action buttons
                    if (e.target.closest('.flashcard-actions')) {
                        return;
                    }
                    
                    // Toggle flipped class
                    this.classList.toggle('flipped');
                });
            }
        });
    }
}

// Fix interactive elements
function fixInteractiveElements() {
    // Fix tool cards
    const toolCards = document.querySelectorAll('.tool-card');
    console.log(`Found ${toolCards.length} tool cards`);
    
    toolCards.forEach(card => {
        const href = card.getAttribute('data-href');
        if (href) {
            card.style.cursor = 'pointer';
            card.addEventListener('click', function() {
                window.location.href = href;
            });
        }
    });
    
    // Make sure forms have proper submission handling
    const forms = document.querySelectorAll('form:not([data-no-loading])');
    console.log(`Found ${forms.length} forms`);
    
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            // Show loading spinner if available
            if (window.showLoading) {
                window.showLoading();
            } else {
                console.warn('Loading function not available');
            }
        });
    });
}

// Fix navigation issues
function fixNavigationIssues() {
    // Make sure mobile navigation works
    const toggleBtn = document.querySelector('.mobile-nav-toggle');
    const sidebar = document.querySelector('.app-sidebar');
    
    if (toggleBtn && sidebar) {
        console.log('Fixing mobile navigation');
        
        toggleBtn.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });
        
        // Make sure links are working
        const navLinks = sidebar.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href && !link.classList.contains('has-dropdown')) {
                link.addEventListener('click', function(e) {
                    e.preventDefault();
                    
                    // Show loading
                    if (window.showLoading) {
                        window.showLoading();
                    }
                    
                    // Navigate
                    setTimeout(() => {
                        window.location.href = href;
                    }, 100);
                });
            }
        });
    }
}

// Enhance content loading
function enhanceContentLoading() {
    // Make sure loading spinner is removed properly
    const loadingScreen = document.querySelector('.loading-container');
    if (loadingScreen) {
        console.log('Removing any stuck loading screens');
        
        setTimeout(() => {
            loadingScreen.style.opacity = '0';
            setTimeout(() => {
                loadingScreen.remove();
            }, 300);
        }, 300);
    }
    
    // Add fade-in animation to main content
    const contentWrapper = document.querySelector('.content-wrapper');
    if (contentWrapper) {
        contentWrapper.classList.add('fade-in');
    }
}

// Enhance error handling
function enhanceErrorHandling() {
    // Add global error handler
    window.addEventListener('error', function(e) {
        console.error('Global error caught:', e.message, 'at', e.filename, 'line', e.lineno);
        
        // Hide loading spinner if an error occurs
        if (window.hideLoading) {
            window.hideLoading();
        }
    });
    
    // Catch unhandled promise rejections
    window.addEventListener('unhandledrejection', function(e) {
        console.error('Unhandled Promise Rejection:', e.reason);
        
        // Hide loading spinner if an error occurs
        if (window.hideLoading) {
            window.hideLoading();
        }
    });
    
    // Patch fetch to ensure loading spinner is removed on error
    if (window.fetch && !window._debugFetchPatched) {
        const originalFetch = window.fetch;
        
        window.fetch = function() {
            return originalFetch.apply(this, arguments)
                .catch(error => {
                    console.error('Fetch error caught:', error);
                    
                    // Hide loading spinner
                    if (window.hideLoading) {
                        window.hideLoading();
                    }
                    
                    throw error;
                });
        };
        
        window._debugFetchPatched = true;
    }
}

// Fix any CSS issues
function fixCSSIssues() {
    // Create a style tag to fix any critical CSS issues
    const styleFixTag = document.createElement('style');
    styleFixTag.textContent = `
        /* Fix flashcard display issues */
        .flashcard {
            perspective: 1000px;
            width: 100%;
            height: 220px;
            margin-bottom: 1rem;
        }
        
        .flashcard-inner {
            position: relative;
            width: 100%;
            height: 100%;
            text-align: center;
            transition: transform 0.6s;
            transform-style: preserve-3d;
        }
        
        .flashcard.flipped .flashcard-inner {
            transform: rotateY(180deg);
        }
        
        .flashcard-front, .flashcard-back {
            position: absolute;
            width: 100%;
            height: 100%;
            -webkit-backface-visibility: hidden; /* Safari */
            backface-visibility: hidden;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 1.5rem;
        }
        
        .flashcard-front {
            background: linear-gradient(135deg, var(--primary-light), var(--primary-color));
            color: white;
        }
        
        .flashcard-back {
            background-color: white;
            color: var(--dark-color);
            transform: rotateY(180deg);
            text-align: left;
            overflow-y: auto;
        }
        
        /* Fix animation issues */
        .fade-in {
            animation: fadeIn ease-in 0.5s;
            animation-fill-mode: backwards;
        }
        
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(10px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        
        /* Fix mobile issues */
        @media (max-width: 768px) {
            .main-content {
                margin-left: 0;
            }
            
            .content-wrapper {
                padding: 1rem;
            }
        }
    `;
    
    document.head.appendChild(styleFixTag);
}

// Run CSS fixes after everything else
setTimeout(fixCSSIssues, 500); 