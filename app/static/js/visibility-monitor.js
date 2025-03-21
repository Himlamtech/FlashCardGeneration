/**
 * Visibility Monitor
 * Detects and logs any attempts to hide content to help with debugging
 */

(function() {
    console.log("👁️ Visibility Monitor Active");
    
    // Track content visibility state
    let contentWasVisible = false;
    let contentLastVisible = Date.now();
    let visibilityLog = [];
    
    // Create a debugging panel
    function createDebugPanel() {
        const panel = document.createElement('div');
        panel.id = 'visibility-debug-panel';
        panel.style.cssText = `
            position: fixed;
            bottom: 10px;
            right: 10px;
            background: rgba(0,0,0,0.8);
            color: #00ff00;
            font-family: monospace;
            padding: 10px;
            border-radius: 5px;
            z-index: 9999;
            max-height: 200px;
            overflow: auto;
            font-size: 12px;
        `;
        document.body.appendChild(panel);
        return panel;
    }
    
    // Check if content is visible and log any changes
    function checkContentVisibility() {
        const content = document.getElementById('content');
        
        if (!content) {
            logEvent("Content element not found!");
            return;
        }
        
        const isVisible = isElementVisible(content);
        
        if (contentWasVisible && !isVisible) {
            // Content just disappeared!
            const timeSinceLastVisible = Date.now() - contentLastVisible;
            const stackTrace = new Error().stack;
            logEvent(`CRITICAL: Content disappeared after ${timeSinceLastVisible}ms! Stack trace: ${stackTrace}`);
            
            // Force it back to visible
            forceVisible(content);
        } else if (!contentWasVisible && isVisible) {
            // Content has appeared
            logEvent("Content is now visible");
        }
        
        contentWasVisible = isVisible;
        if (isVisible) {
            contentLastVisible = Date.now();
        }
    }
    
    // Check if an element is visible
    function isElementVisible(element) {
        if (!element) return false;
        
        const style = window.getComputedStyle(element);
        return !(
            style.display === 'none' ||
            style.visibility === 'hidden' ||
            parseFloat(style.opacity) === 0
        );
    }
    
    // Force an element to be visible
    function forceVisible(element) {
        element.style.display = 'block';
        element.style.visibility = 'visible';
        element.style.opacity = '1';
        logEvent("Forced content back to visible state");
    }
    
    // Log an event to console and debug panel
    function logEvent(message) {
        const timestamp = new Date().toISOString().split('T')[1].split('.')[0];
        const logEntry = `[${timestamp}] ${message}`;
        
        console.log(`👁️ ${logEntry}`);
        visibilityLog.push(logEntry);
        
        // Update debug panel if it exists
        const panel = document.getElementById('visibility-debug-panel');
        if (panel) {
            panel.innerHTML = visibilityLog.slice(-10).join('<br>');
            panel.scrollTop = panel.scrollHeight;
        }
    }
    
    // Catch and log all errors
    window.addEventListener('error', function(event) {
        logEvent(`ERROR: ${event.message} at ${event.filename}:${event.lineno}`);
    });
    
    // Monitor DOM mutations for content visibility changes
    const observer = new MutationObserver(function(mutations) {
        let needsCheck = false;
        
        mutations.forEach(function(mutation) {
            if (mutation.target.id === 'content' || 
                (mutation.target.closest && mutation.target.closest('#content'))) {
                needsCheck = true;
                
                // Log what changed
                if (mutation.type === 'attributes') {
                    logEvent(`Content attribute changed: ${mutation.attributeName} = "${mutation.target.getAttribute(mutation.attributeName)}"`);
                } else if (mutation.type === 'childList') {
                    if (mutation.addedNodes.length) {
                        logEvent(`Content children added: ${mutation.addedNodes.length} nodes`);
                    }
                    if (mutation.removedNodes.length) {
                        logEvent(`Content children removed: ${mutation.removedNodes.length} nodes`);
                    }
                }
            }
        });
        
        if (needsCheck) {
            checkContentVisibility();
        }
    });
    
    // Initialize
    function init() {
        logEvent("Initializing visibility monitor");
        
        // Do initial check
        checkContentVisibility();
        
        // Create debug panel
        createDebugPanel();
        
        // Set up observer
        observer.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: ['style', 'class', 'hidden']
        });
        
        // Check periodically
        setInterval(checkContentVisibility, 1000);
        
        logEvent("Visibility monitor initialized");
    }
    
    // Run when DOM is loaded
    if (document.readyState !== 'loading') {
        init();
    } else {
        document.addEventListener('DOMContentLoaded', init);
    }
})(); 