/**
 * StudyWAI - Visibility Fix
 * Ensures the application remains visible and prevents content from disappearing
 */

// Immediate execution to ensure content visibility
(function() {
    console.log("Visibility fix running");
    
    // Function to ensure content stays visible
    function ensureContentVisible() {
        const contentArea = document.getElementById('content');
        const mainContainer = document.querySelector('#content .container');
        
        if (contentArea) {
            // Ensure the content area is visible
            contentArea.style.display = 'block';
            contentArea.style.opacity = '1';
            contentArea.style.visibility = 'visible';
            
            // Add a class to make it easier to debug
            contentArea.classList.add('visibility-fixed');
            
            console.log("Content area visibility enforced");
        } else {
            console.error("Content area not found");
        }
        
        if (mainContainer) {
            // Ensure main container is visible
            mainContainer.style.display = 'block';
            mainContainer.style.opacity = '1';
            mainContainer.style.visibility = 'visible';
            console.log("Main container visibility enforced");
        }
    }
    
    // Run immediately
    if (document.readyState === 'loading') {
        // If the document is still loading, add event listener
        document.addEventListener('DOMContentLoaded', function() {
            ensureContentVisible();
            // Run again after a short delay to catch any late changes
            setTimeout(ensureContentVisible, 100);
            setTimeout(ensureContentVisible, 500);
            setTimeout(ensureContentVisible, 1000);
        });
    } else {
        // If DOMContentLoaded has already fired
        ensureContentVisible();
        // Run again after a short delay to catch any late changes
        setTimeout(ensureContentVisible, 100);
        setTimeout(ensureContentVisible, 500);
        setTimeout(ensureContentVisible, 1000);
    }
    
    // Override any functions that might hide content
    const originalAddClass = Element.prototype.classList.add;
    Element.prototype.classList.add = function(...classes) {
        // Check if trying to hide content
        if (this.id === 'content' && 
            (classes.includes('d-none') || 
             classes.includes('hidden') || 
             classes.includes('invisible'))) {
            console.warn('Prevented hiding content area');
            return;
        }
        return originalAddClass.apply(this, classes);
    };
    
    // Detect and prevent style changes that hide content
    const originalSetProperty = CSSStyleDeclaration.prototype.setProperty;
    CSSStyleDeclaration.prototype.setProperty = function(propertyName, value, priority) {
        // Check if trying to hide content via style
        if (this.parentElement && 
            (this.parentElement.id === 'content' || 
             this.parentElement.closest('#content .container')) && 
            (propertyName === 'display' && value === 'none' || 
             propertyName === 'opacity' && value === '0' || 
             propertyName === 'visibility' && value === 'hidden')) {
            console.warn(`Prevented hiding content area via style: ${propertyName} = ${value}`);
            return;
        }
        return originalSetProperty.call(this, propertyName, value, priority);
    };
    
    // Create a MutationObserver to watch for changes
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'attributes' && 
                mutation.attributeName === 'style' &&
                (mutation.target.id === 'content' || 
                 mutation.target.closest('#content .container'))) {
                ensureContentVisible();
            }
        });
    });
    
    // Start observing once the DOM is loaded
    document.addEventListener('DOMContentLoaded', function() {
        const contentArea = document.getElementById('content');
        if (contentArea) {
            observer.observe(contentArea, { 
                attributes: true,
                subtree: true,
                attributeFilter: ['style', 'class']
            });
            console.log("Observing content area for visibility changes");
        }
    });
})(); 