/**
 * StudyWAI - Animation and Interaction Scripts
 * Enhances the user interface with modern animations and effects
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add hover effects to cards
    const cards = document.querySelectorAll('.card, .flashcard');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 8px 25px rgba(0, 0, 0, 0.1)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = '';
            this.style.boxShadow = '';
        });
    });

    // Add staggered animations to lists
    const animateStaggered = (elements, className, delay = 100) => {
        elements.forEach((el, index) => {
            setTimeout(() => {
                el.classList.add(className);
            }, index * delay);
        });
    };

    // Animate section titles with slide-in effect
    const sectionTitles = document.querySelectorAll('.flashcard-section-title, h1, h2');
    animateStaggered(sectionTitles, 'fade-in-element', 150);

    // Add subtle animation to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });

    // Create a ripple effect on button clicks
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const rect = button.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const ripple = document.createElement('span');
            ripple.style.position = 'absolute';
            ripple.style.width = '0';
            ripple.style.height = '0';
            ripple.style.borderRadius = '50%';
            ripple.style.transform = 'translate(-50%, -50%)';
            ripple.style.background = 'rgba(255, 255, 255, 0.3)';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            
            button.appendChild(ripple);
            
            ripple.style.animation = 'ripple-effect 0.6s linear';
            ripple.addEventListener('animationend', function() {
                ripple.remove();
            });
        });
    });

    // Add keyframe animation for ripple effect to the document
    if (!document.querySelector('#ripple-animation')) {
        const style = document.createElement('style');
        style.id = 'ripple-animation';
        style.textContent = `
        @keyframes ripple-effect {
            0% {
                width: 0;
                height: 0;
                opacity: 0.5;
            }
            100% {
                width: 500px;
                height: 500px;
                opacity: 0;
            }
        }`;
        document.head.appendChild(style);
    }

    // Sidebar toggle animation enhancement
    const sidebarCollapse = document.getElementById('sidebarCollapse');
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');
    
    if (sidebarCollapse && sidebar && content) {
        sidebarCollapse.addEventListener('click', function() {
            sidebar.classList.toggle('active');
            content.classList.toggle('active');
            
            // Add rotation to the toggle icon
            const icon = this.querySelector('i');
            if (icon) {
                icon.style.transition = 'transform 0.3s ease';
                icon.style.transform = sidebar.classList.contains('active') ? 'rotate(180deg)' : '';
            }
        });
    }

    // Add subtle parallax effect to flashcards on mouse move
    const flashcards = document.querySelectorAll('.flashcard');
    flashcards.forEach(card => {
        card.addEventListener('mousemove', function(e) {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const deltaX = (x - centerX) / centerX;
            const deltaY = (y - centerY) / centerY;
            
            card.style.transition = 'transform 0.1s ease-out';
            card.style.transform = `perspective(1000px) rotateY(${deltaX * 2}deg) rotateX(${-deltaY * 2}deg)`;
        });
        
        card.addEventListener('mouseleave', function() {
            card.style.transition = 'transform 0.5s ease';
            card.style.transform = 'perspective(1000px) rotateY(0) rotateX(0)';
        });
    });

    // Add scroll reveal animation
    const revealElements = document.querySelectorAll('.ai-tool-container, .card, .flashcard');
    const revealOnScroll = function() {
        for (let i = 0; i < revealElements.length; i++) {
            const windowHeight = window.innerHeight;
            const elementTop = revealElements[i].getBoundingClientRect().top;
            const elementVisible = 150;
            
            if (elementTop < windowHeight - elementVisible) {
                revealElements[i].classList.add('fade-in-element');
            }
        }
    };
    
    window.addEventListener('scroll', revealOnScroll);
    revealOnScroll(); // Initial check
}); 