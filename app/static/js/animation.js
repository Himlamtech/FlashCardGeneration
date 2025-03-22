/**
 * Animation functions for StudyWAI application
 * This script handles animations and interactions across the application
 */

document.addEventListener('DOMContentLoaded', function() {
    initDarkMode();
    initAnimations();
    initParticles();
    initCountAnimations();
});

/**
 * Initialize dark mode functionality
 */
function initDarkMode() {
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            const html = document.documentElement;
            
            if (html.getAttribute('data-theme') === 'dark') {
                html.setAttribute('data-theme', 'light');
                localStorage.setItem('theme', 'light');
                this.innerHTML = '<i class="fas fa-moon me-2"></i>Dark Mode';
            } else {
                html.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
                this.innerHTML = '<i class="fas fa-sun me-2"></i>Light Mode';
            }
        });
        
        // Set initial state based on localStorage or system preference
        const savedTheme = localStorage.getItem('theme');
        
        if (savedTheme) {
            document.documentElement.setAttribute('data-theme', savedTheme);
            
            if (savedTheme === 'dark') {
                darkModeToggle.innerHTML = '<i class="fas fa-sun me-2"></i>Light Mode';
            } else {
                darkModeToggle.innerHTML = '<i class="fas fa-moon me-2"></i>Dark Mode';
            }
        } else {
            // Check system preference
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                document.documentElement.setAttribute('data-theme', 'dark');
                darkModeToggle.innerHTML = '<i class="fas fa-sun me-2"></i>Light Mode';
                localStorage.setItem('theme', 'dark');
            }
        }
    }
}

/**
 * Initialize animations for various elements
 */
function initAnimations() {
    // Set up fade-in animations for various elements
    if ('IntersectionObserver' in window) {
        const fadeElements = document.querySelectorAll('.fade-in-element');
        
        const fadeObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                    fadeObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });
        
        fadeElements.forEach(el => {
            fadeObserver.observe(el);
        });
    } else {
        // Fallback for browsers that don't support IntersectionObserver
        const fadeElements = document.querySelectorAll('.fade-in-element');
        fadeElements.forEach(el => {
            el.classList.add('fade-in');
        });
    }
    
    // Add fade-in class to flashcard items with small delay between each
    const flashcardItems = document.querySelectorAll('.flashcard-item');
    flashcardItems.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('fade-in');
        }, 50 * index);
    });
}

/**
 * Initialize background particle effect if canvas exists
 */
function initParticles() {
    const canvas = document.getElementById('particles-canvas');
    
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    let particles = [];
    
    // Resize canvas to full width
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    
    // Create a particle
    function Particle(x, y, size, speedX, speedY, color) {
        this.x = x;
        this.y = y;
        this.size = size;
        this.speedX = speedX;
        this.speedY = speedY;
        this.color = color;
        
        this.update = function() {
            this.x += this.speedX;
            this.y += this.speedY;
            
            // Bounce off edges
            if (this.x < 0 || this.x > canvas.width) {
                this.speedX = -this.speedX;
            }
            
            if (this.y < 0 || this.y > canvas.height) {
                this.speedY = -this.speedY;
            }
        };
        
        this.draw = function() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.fill();
        };
    }
    
    // Initialize particles
    function initParticlesArray() {
        particles = [];
        const particleCount = 30;
        const colors = ['rgba(62, 104, 255, 0.3)', 'rgba(0, 184, 121, 0.3)', 'rgba(255, 184, 0, 0.3)'];
        
        for (let i = 0; i < particleCount; i++) {
            const size = Math.random() * 5 + 1;
            const x = Math.random() * canvas.width;
            const y = Math.random() * canvas.height;
            const speedX = (Math.random() - 0.5) * 0.5;
            const speedY = (Math.random() - 0.5) * 0.5;
            const color = colors[Math.floor(Math.random() * colors.length)];
            
            particles.push(new Particle(x, y, size, speedX, speedY, color));
        }
    }
    
    // Animation loop
    function animate() {
        // Only run animation when visible in viewport
        const rect = canvas.getBoundingClientRect();
        if (
            rect.bottom < 0 ||
            rect.top > window.innerHeight ||
            rect.right < 0 ||
            rect.left > window.innerWidth
        ) {
            requestAnimationFrame(animate);
            return;
        }
        
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        for (let i = 0; i < particles.length; i++) {
            particles[i].update();
            particles[i].draw();
        }
        
        requestAnimationFrame(animate);
    }
    
    // Handle window resize
    window.addEventListener('resize', function() {
        resizeCanvas();
        initParticlesArray();
    });
    
    // Initialize
    resizeCanvas();
    initParticlesArray();
    animate();
}

/**
 * Initialize count animations for statistics
 */
function initCountAnimations() {
    const countElements = document.querySelectorAll('.count-animation');
    
    countElements.forEach(element => {
        const target = parseInt(element.getAttribute('data-count'), 10);
        const duration = 1500; // ms
        const start = 0;
        const startTime = performance.now();
        
        function updateCount(currentTime) {
            const elapsedTime = currentTime - startTime;
            
            if (elapsedTime > duration) {
                element.textContent = target;
                return;
            }
            
            const progress = elapsedTime / duration;
            const currentCount = Math.floor(progress * (target - start) + start);
            
            element.textContent = currentCount;
            
            requestAnimationFrame(updateCount);
        }
        
        requestAnimationFrame(updateCount);
    });
}

// Initialize typing effect for headers
function initTypingEffect() {
    const typingElements = document.querySelectorAll('.typing-effect');
    
    typingElements.forEach(element => {
        const text = element.getAttribute('data-text');
        if (!text) return;
        
        element.textContent = '';
        let charIndex = 0;
        
        function typeChar() {
            if (charIndex < text.length) {
                element.textContent += text.charAt(charIndex);
                charIndex++;
                setTimeout(typeChar, Math.random() * 50 + 50); // Random delay for natural effect
            }
        }
        
        // Start typing when element is in view
        if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        setTimeout(typeChar, 500); // Slight delay before typing starts
                        observer.unobserve(element);
                    }
                });
            });
            
            observer.observe(element);
        } else {
            // Fallback
            setTimeout(typeChar, 500);
        }
    });
}

// Initialize hover effect for cards
function initHoverEffect() {
    const hoverCards = document.querySelectorAll('.hover-card');
    
    hoverCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left; // x position within the element
            const y = e.clientY - rect.top; // y position within the element
            
            // Calculate rotation based on mouse position
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;
            
            // Apply transform
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
        });
        
        // Reset transform when mouse leaves
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0)';
        });
    });
}

// Initialize all animations when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize animations on pages that need them
    const currentPath = window.location.pathname;
    
    // Particle effect only on homepage
    if (currentPath === '/' || currentPath === '/index.html') {
        initParticles();
    }
    
    // These animations are used across the site
    initTypingEffect();
    initHoverEffect();
}); 