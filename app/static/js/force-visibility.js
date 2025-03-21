/**
 * FORCE VISIBILITY SCRIPT
 * This script ensures content is always visible regardless of other scripts
 * It has higher priority overrides than any other script
 */

(function() {
    console.log("🔥 FORCE VISIBILITY SCRIPT ACTIVATED 🔥");
    
    // Immediately force visibility
    function forceContentVisible() {
        const content = document.getElementById('content');
        const container = document.querySelector('#content .container');
        
        // Force direct style on content div with !important
        if (content) {
            console.log("Forcing content visibility");
            content.setAttribute('style', 'display: block !important; opacity: 1 !important; visibility: visible !important; min-height: 100vh !important; z-index: 1 !important;');
            content.classList.add('force-visible');
        }
        
        // Force visibility on container
        if (container) {
            console.log("Forcing container visibility");
            container.setAttribute('style', 'display: block !important; opacity: 1 !important; visibility: visible !important;');
            container.classList.add('force-visible');
        }
    }
    
    // Run immediately
    forceContentVisible();
    
    // Run again after a very short delay
    setTimeout(forceContentVisible, 0);
    
    // Also run after DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            forceContentVisible();
            // Multiple runs to ensure it catches any late changes
            setTimeout(forceContentVisible, 100);
            setTimeout(forceContentVisible, 500);
        });
    }
    
    // Run when window loads too
    window.addEventListener('load', function() {
        forceContentVisible();
        // Keep running periodically for first few seconds
        setTimeout(forceContentVisible, 1000);
        setTimeout(forceContentVisible, 2000);
        setTimeout(forceContentVisible, 3000);
    });
    
    // Use MutationObserver to detect any attempts to hide content
    const observer = new MutationObserver(function() {
        forceContentVisible();
    });
    
    // Start observing once DOM is loaded
    if (document.readyState !== 'loading') {
        const content = document.getElementById('content');
        if (content) {
            observer.observe(document, { 
                childList: true, 
                subtree: true,
                attributes: true,
                attributeFilter: ['style', 'class'] 
            });
            console.log("Now watching for visibility changes");
        }
    } else {
        document.addEventListener('DOMContentLoaded', function() {
            const content = document.getElementById('content');
            if (content) {
                observer.observe(document, { 
                    childList: true, 
                    subtree: true,
                    attributes: true,
                    attributeFilter: ['style', 'class'] 
                });
                console.log("Now watching for visibility changes");
            }
        });
    }
    
    // Override any attempts to modify style
    const originalSetAttribute = Element.prototype.setAttribute;
    Element.prototype.setAttribute = function(name, value) {
        // If trying to hide content, prevent it
        if (this.id === 'content' || this.closest('#content') || this.closest('.container')) {
            if (name === 'style' && 
                (value.includes('display: none') || 
                 value.includes('visibility: hidden') || 
                 value.includes('opacity: 0'))) {
                console.warn('⚠️ Prevented attempt to hide content via setAttribute');
                return;
            }
        }
        return originalSetAttribute.call(this, name, value);
    };
    
    // Add CSS to force visibility
    const style = document.createElement('style');
    style.innerHTML = `
        #content, #content .container, #content * {
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
        }
        .force-visible {
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
        }
    `;
    document.head.appendChild(style);
    
    console.log("Force visibility script fully loaded");
})(); 