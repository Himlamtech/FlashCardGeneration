/**
 * Animation utilities for FlashCard Generation app
 */

// Initialize animations when document is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeAnimations();
    initializeScrollEffects();
});

// Card animations
function initializeAnimations() {
    // Animate cards on page load
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 + (index * 100)); // Stagger the animations
    });
    
    // Add hover effects to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s ease';
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transition = 'all 0.3s ease';
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
        });
    });
    
    // Animation for flashcard flip
    const flipButtons = document.querySelectorAll('#flipBtn, #backFlipBtn');
    flipButtons.forEach(button => {
        button.addEventListener('click', function() {
            const wrapper = document.getElementById('flashcardWrapper');
            if (wrapper) {
                wrapper.style.transition = 'transform 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
            }
        });
    });
}

// Scroll-based animations
function initializeScrollEffects() {
    // Only run if IntersectionObserver is supported
    if ('IntersectionObserver' in window) {
        const appearOptions = {
            threshold: 0.15,
            rootMargin: '0px 0px -100px 0px'
        };
        
        const appearOnScroll = new IntersectionObserver(function(entries, observer) {
            entries.forEach(entry => {
                if (!entry.isIntersecting) return;
                
                entry.target.classList.add('fade-in-element');
                observer.unobserve(entry.target);
            });
        }, appearOptions);
        
        // Apply to elements with scroll-animate class
        document.querySelectorAll('.scroll-animate').forEach(element => {
            element.style.opacity = '0';
            element.style.transform = 'translateY(20px)';
            appearOnScroll.observe(element);
        });
    }
}

// Add pulse animation to an element
function addPulseEffect(element) {
    element.classList.add('pulse-animation');
    
    // Remove animation after it completes to allow it to be triggered again
    setTimeout(() => {
        element.classList.remove('pulse-animation');
    }, 1000);
}

// Add shake animation to an element
function addShakeEffect(element) {
    element.classList.add('shake-animation');
    
    // Remove animation after it completes
    setTimeout(() => {
        element.classList.remove('shake-animation');
    }, 800);
}

// Confetti animation for achievements
function showConfetti() {
    const confettiContainer = document.createElement('div');
    confettiContainer.classList.add('confetti-container');
    document.body.appendChild(confettiContainer);
    
    // Create confetti pieces
    for (let i = 0; i < 100; i++) {
        const confetti = document.createElement('div');
        confetti.classList.add('confetti');
        confetti.style.left = Math.random() * 100 + 'vw';
        confetti.style.animationDelay = Math.random() * 3 + 's';
        confetti.style.backgroundColor = getRandomColor();
        confettiContainer.appendChild(confetti);
    }
    
    // Remove confetti after animation completes
    setTimeout(() => {
        document.body.removeChild(confettiContainer);
    }, 6000);
}

// Get random color for confetti
function getRandomColor() {
    const colors = [
        '#f94144', '#f3722c', '#f8961e', 
        '#f9c74f', '#90be6d', '#43aa8b', 
        '#4d908e', '#577590', '#277da1'
    ];
    return colors[Math.floor(Math.random() * colors.length)];
} 