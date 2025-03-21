/**
 * StudyWAI - Debug Console
 * This script checks if all our namespaces are properly initialized
 */

console.log('==== StudyWAI Debug Console ====');
console.log('Checking for initialized namespaces:');

// Check main functionality
if (window.studywaiMain && window.studywaiMain.initialized) {
    console.log('✅ Main script (script.js) initialized correctly');
} else {
    console.error('❌ Main script not initialized properly!', window.studywaiMain);
}

// Check router functionality
if (window.studywaiRouter) {
    console.log('✅ Router script (router-fix.js) initialized correctly');
} else {
    console.error('❌ Router script not initialized properly!');
}

// Check loading functionality
if (window.studywaiLoading && window.studywaiLoading.initialized) {
    console.log('✅ Loading script (loading.js) initialized correctly');
} else {
    console.error('❌ Loading script not initialized properly!', window.studywaiLoading);
}

// Check for dependency conflicts
console.log('\nChecking for potential conflicts:');

// Check Bootstrap
if (typeof bootstrap !== 'undefined' && bootstrap.Modal) {
    console.log('✅ Bootstrap loaded correctly');
} else {
    console.error('❌ Bootstrap not loaded properly!');
}

// Check jQuery if being used
if (typeof jQuery !== 'undefined') {
    console.log('✅ jQuery loaded correctly (version ' + jQuery.fn.jquery + ')');
} else {
    console.log('jQuery not loaded (may be intentional)');
}

// Check DOM mutations
const observer = new MutationObserver((mutations) => {
    // Just checking if observer can be created
});
if (observer) {
    console.log('✅ MutationObserver available');
    observer.disconnect();
} else {
    console.error('❌ MutationObserver not available!');
}

// Check for console errors
if (console.error.toString().includes('native code')) {
    console.log('✅ Console API available');
} else {
    console.error('❌ Console API may be overridden!');
}

console.log('\nDOM Ready State:', document.readyState);
console.log('URL Path:', window.location.pathname);
console.log('URL Hash:', window.location.hash || '(none)');
console.log('==== Debug Complete ===='); 