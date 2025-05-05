/**
 * Service Worker for StudyWAI
 * Handles caching and cache headers for better performance and browser compatibility
 */

const CACHE_NAME = 'studywai-cache-v1';
const urlsToCache = [
  '/static/css/styles.css',
  '/static/css/forced-styles.css',
  '/static/js/script.js',
  '/static/js/animation.js',
  '/static/js/debug.js',
  '/static/img/favicon.ico'
];

// Security headers to add to responses
const securityHeaders = {
  'Cache-Control': 'public, max-age=31536000',
  'X-Content-Type-Options': 'nosniff'
};

// Content type mappings for different file extensions
let contentTypeMappings = {
  'css': 'text/css',
  'js': 'application/javascript',
  'html': 'text/html',
  'json': 'application/json',
  'png': 'image/png',
  'jpg': 'image/jpeg',
  'jpeg': 'image/jpeg',
  'gif': 'image/gif',
  'svg': 'image/svg+xml',
  'ico': 'image/x-icon',
  'woff': 'font/woff',
  'woff2': 'font/woff2',
  'ttf': 'font/ttf',
  'eot': 'application/vnd.ms-fontobject',
  'otf': 'font/otf'
};

// Install event - cache core assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  
  // Ensure the service worker takes control immediately
  return self.clients.claim();
});

/**
 * Fix headers and add proper content types
 * @param {Response} response - Original response
 * @param {string} extension - File extension
 * @returns {Promise<Response>} - Response with fixed headers
 */
const fixResponseHeaders = async (response, extension) => {
  // Create new headers
  const headers = new Headers(response.headers);
  
  // Add security headers
  Object.keys(securityHeaders).forEach(key => {
    headers.set(key, securityHeaders[key]);
  });
  
  // Set proper content-type header based on file extension
  if (contentTypeMappings[extension]) {
    // Handle special cases for fonts to ensure proper MIME types
    if (['woff', 'woff2', 'ttf', 'eot', 'otf'].includes(extension)) {
      headers.set('Content-Type', contentTypeMappings[extension]);
      
      // Add CORS headers for font files
      headers.set('Access-Control-Allow-Origin', '*');
    } else {
      headers.set('Content-Type', contentTypeMappings[extension]);
    }
  }
  
  // Create a new response with the updated headers
  const responseBody = await response.clone().blob();
  return new Response(responseBody, {
    status: response.status,
    statusText: response.statusText,
    headers: headers
  });
};

// Fetch event - serve cached content when offline
self.addEventListener('fetch', event => {
  // Only apply cache strategy to GET requests
  if (event.request.method !== 'GET') return;
  
  // Extract file extension from URL
  const url = new URL(event.request.url);
  const extension = url.pathname.split('.').pop().toLowerCase();
  
  // Handle static assets with a cache-first strategy
  if (event.request.url.includes('/static/')) {
    event.respondWith(
      caches.match(event.request)
        .then(async cachedResponse => {
          // Return cached response if found with fixed headers
          if (cachedResponse) {
            return fixResponseHeaders(cachedResponse, extension);
          }
          
          // Otherwise fetch from network
          try {
            const networkResponse = await fetch(event.request);
            
            // Don't cache if response is not valid
            if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic') {
              return networkResponse;
            }
            
            // Fix headers
            const enhancedResponse = await fixResponseHeaders(networkResponse, extension);
            
            // Cache the enhanced response
            const responseToCache = enhancedResponse.clone();
            caches.open(CACHE_NAME)
              .then(cache => {
                cache.put(event.request, responseToCache);
              });
            
            return enhancedResponse;
          } catch (error) {
            console.error('Fetch failed:', error);
            // If network fails and we don't have a cached response, return a fallback
            return new Response('Network error, cannot fetch resource', { 
              status: 503, 
              headers: { 'Content-Type': 'text/plain' }
            });
          }
        })
    );
  }
});

// Handle message from main thread
self.addEventListener('message', event => {
  if (event.data && event.data.action === 'add-cache-headers') {
    // Add custom headers to security headers
    if (event.data.headers) {
      Object.assign(securityHeaders, event.data.headers);
    }
  }
  
  // Update content type mappings
  if (event.data && event.data.action === 'add-content-type-mappings') {
    if (event.data.mappings) {
      Object.assign(contentTypeMappings, event.data.mappings);
    }
  }
  
  // Skip waiting to immediately activate a new service worker
  if (event.data && event.data.action === 'skipWaiting') {
    self.skipWaiting();
  }
}); 