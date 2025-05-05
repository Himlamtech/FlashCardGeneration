/**
 * Header Fixer Script - fixes content-type headers for various file types
 * This script should be loaded in the head of the document
 */

(function() {
  // Fix content-type headers for fonts and other resources
  if ('serviceWorker' in navigator && navigator.serviceWorker.controller) {
    const fontExtensions = ['woff', 'woff2', 'ttf', 'eot', 'otf'];
    const fontMimeTypes = {
      'woff': 'font/woff',
      'woff2': 'font/woff2',
      'ttf': 'font/ttf',
      'eot': 'application/vnd.ms-fontobject',
      'otf': 'font/otf'
    };
    
    // Override fetch for font files to fix content-type headers
    const originalFetch = window.fetch;
    window.fetch = function(input, init) {
      // Check if this is a font file request
      if (typeof input === 'string') {
        const url = new URL(input, window.location.href);
        const extension = url.pathname.split('.').pop().toLowerCase();
        
        if (fontExtensions.includes(extension)) {
          // Create new init object with proper headers
          const newInit = init || {};
          newInit.headers = new Headers(newInit.headers || {});
          
          // Add proper content-type header without charset
          if (fontMimeTypes[extension]) {
            newInit.headers.set('Accept', fontMimeTypes[extension]);
          }
          
          return originalFetch(input, newInit);
        }
      }
      
      // Default fetch behavior
      return originalFetch(input, init);
    };
    
    // Tell service worker to add proper headers for fonts
    navigator.serviceWorker.controller.postMessage({
      action: 'add-content-type-mappings',
      mappings: fontMimeTypes
    });
  }
  
  // Add meta tags for security
  const metaTags = [
    { name: 'referrer', content: 'same-origin' },
    { 'http-equiv': 'X-UA-Compatible', content: 'IE=edge,chrome=1' },
    { 'http-equiv': 'Content-Security-Policy', content: "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://code.jquery.com https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; img-src 'self' data: https:; connect-src 'self';" },
    { 'http-equiv': 'X-Content-Type-Options', content: 'nosniff' }
  ];
  
  // Add meta tags to document head
  metaTags.forEach(attributes => {
    const meta = document.createElement('meta');
    for (const key in attributes) {
      meta.setAttribute(key, attributes[key]);
    }
    document.head.appendChild(meta);
  });
})(); 