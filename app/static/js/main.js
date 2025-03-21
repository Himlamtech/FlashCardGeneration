/**
 * Main JavaScript functionality for FlashCard Generation app
 */

document.addEventListener('DOMContentLoaded', function() {
    // Sidebar toggle functionality
    const sidebarCollapse = document.getElementById('sidebarCollapse');
    if (sidebarCollapse) {
        sidebarCollapse.addEventListener('click', function() {
            document.getElementById('sidebar').classList.toggle('active');
            document.getElementById('content').classList.toggle('active');
        });
    }

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize AI tool modals
    setupAITools();

    // Add fade-in animation to elements when they become visible
    animateOnScroll();
});

// Set up AI tool modals and their functionality
function setupAITools() {
    // Create modal elements for AI tools
    createAIModals();
    
    // Add event listeners for AI tool links
    setupAIToolListeners();
}

// Create modal elements for Grammar Check, Translation, and Summarize
function createAIModals() {
    // Create Grammar Check Modal
    const grammarModal = createModal(
        'grammarModal',
        'Grammar Check',
        `<form id="grammarForm">
            <div class="mb-3">
                <label for="grammarText" class="form-label">Enter text to check:</label>
                <textarea id="grammarText" class="form-control" rows="5" required></textarea>
            </div>
            <button type="submit" class="btn btn-primary">
                <span class="spinner-border spinner-border-sm d-none" role="status" aria-hidden="true"></span>
                Check Grammar
            </button>
        </form>
        <div id="grammarResult" class="mt-4 d-none">
            <h6>Corrected Text:</h6>
            <div class="card">
                <div class="card-body" id="grammarCorrected"></div>
            </div>
        </div>`
    );
    
    // Create Translation Modal
    const translateModal = createModal(
        'translateModal',
        'Translation',
        `<form id="translateForm">
            <div class="mb-3">
                <label for="translateText" class="form-label">Enter text to translate:</label>
                <textarea id="translateText" class="form-control" rows="5" required></textarea>
            </div>
            <div class="mb-3">
                <label for="targetLanguage" class="form-label">Target Language:</label>
                <select id="targetLanguage" class="form-select" required>
                    <option value="fr">French</option>
                    <option value="es">Spanish</option>
                    <option value="de">German</option>
                    <option value="it">Italian</option>
                    <option value="ja">Japanese</option>
                    <option value="zh">Chinese</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary">
                <span class="spinner-border spinner-border-sm d-none" role="status" aria-hidden="true"></span>
                Translate
            </button>
        </form>
        <div id="translateResult" class="mt-4 d-none">
            <h6>Translation:</h6>
            <div class="card">
                <div class="card-body" id="translatedText"></div>
            </div>
        </div>`
    );
    
    // Create Summarize Modal
    const summarizeModal = createModal(
        'summarizeModal',
        'Summarize Text',
        `<form id="summarizeForm">
            <div class="mb-3">
                <label for="summarizeText" class="form-label">Enter text to summarize:</label>
                <textarea id="summarizeText" class="form-control" rows="5" required></textarea>
            </div>
            <button type="submit" class="btn btn-primary">
                <span class="spinner-border spinner-border-sm d-none" role="status" aria-hidden="true"></span>
                Summarize
            </button>
        </form>
        <div id="summarizeResult" class="mt-4 d-none">
            <h6>Summary:</h6>
            <div class="card">
                <div class="card-body" id="summarizedText"></div>
            </div>
        </div>`
    );
    
    // Append modals to document body
    document.body.appendChild(grammarModal);
    document.body.appendChild(translateModal);
    document.body.appendChild(summarizeModal);
}

// Create a modal element with given ID, title, and content
function createModal(id, title, bodyContent) {
    const modalDiv = document.createElement('div');
    modalDiv.classList.add('modal', 'fade');
    modalDiv.id = id;
    modalDiv.setAttribute('tabindex', '-1');
    modalDiv.setAttribute('aria-labelledby', `${id}Label`);
    modalDiv.setAttribute('aria-hidden', 'true');
    
    modalDiv.innerHTML = `
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="${id}Label">${title}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    ${bodyContent}
                </div>
            </div>
        </div>
    `;
    
    return modalDiv;
}

// Set up event listeners for AI tool links
function setupAIToolListeners() {
    // Grammar Check modal
    const grammarCheck = document.getElementById('grammarCheck');
    if (grammarCheck) {
        grammarCheck.addEventListener('click', function(e) {
            e.preventDefault();
            const modal = new bootstrap.Modal(document.getElementById('grammarModal'));
            modal.show();
        });
    }
    
    // Translation modal
    const translation = document.getElementById('translation');
    if (translation) {
        translation.addEventListener('click', function(e) {
            e.preventDefault();
            const modal = new bootstrap.Modal(document.getElementById('translateModal'));
            modal.show();
        });
    }
    
    // Summarize modal
    const summarize = document.getElementById('summarize');
    if (summarize) {
        summarize.addEventListener('click', function(e) {
            e.preventDefault();
            const modal = new bootstrap.Modal(document.getElementById('summarizeModal'));
            modal.show();
        });
    }
    
    // Set up form submission handlers for each AI tool
    setupAIFormHandlers();
}

// Set up form submission handlers for AI tools
function setupAIFormHandlers() {
    // Grammar Check form submission
    const grammarForm = document.getElementById('grammarForm');
    if (grammarForm) {
        grammarForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const text = document.getElementById('grammarText').value;
            const spinner = this.querySelector('.spinner-border');
            const submitBtn = this.querySelector('button[type="submit"]');
            
            spinner.classList.remove('d-none');
            submitBtn.disabled = true;
            
            fetch('/api/check-grammar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: text })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('grammarCorrected').textContent = data.corrected_text;
                document.getElementById('grammarResult').classList.remove('d-none');
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            })
            .finally(() => {
                spinner.classList.add('d-none');
                submitBtn.disabled = false;
            });
        });
    }
    
    // Translation form submission
    const translateForm = document.getElementById('translateForm');
    if (translateForm) {
        translateForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const text = document.getElementById('translateText').value;
            const targetLang = document.getElementById('targetLanguage').value;
            const spinner = this.querySelector('.spinner-border');
            const submitBtn = this.querySelector('button[type="submit"]');
            
            spinner.classList.remove('d-none');
            submitBtn.disabled = true;
            
            fetch('/api/translate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: text, target_language: targetLang })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('translatedText').textContent = data.translated_text;
                document.getElementById('translateResult').classList.remove('d-none');
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            })
            .finally(() => {
                spinner.classList.add('d-none');
                submitBtn.disabled = false;
            });
        });
    }
    
    // Summarize form submission
    const summarizeForm = document.getElementById('summarizeForm');
    if (summarizeForm) {
        summarizeForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const text = document.getElementById('summarizeText').value;
            const spinner = this.querySelector('.spinner-border');
            const submitBtn = this.querySelector('button[type="submit"]');
            
            spinner.classList.remove('d-none');
            submitBtn.disabled = true;
            
            fetch('/api/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: text })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('summarizedText').textContent = data.summary;
                document.getElementById('summarizeResult').classList.remove('d-none');
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            })
            .finally(() => {
                spinner.classList.add('d-none');
                submitBtn.disabled = false;
            });
        });
    }
}

// Add scroll animation for elements
function animateOnScroll() {
    // Add the animation class to elements with fade-in-element class
    const fadeElements = document.querySelectorAll('.fade-in-element');
    
    // Create the Intersection Observer
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target); // Stop observing after animation
            }
        });
    }, {
        threshold: 0.1 // Trigger when 10% of element is visible
    });
    
    // Observe each element
    fadeElements.forEach(element => {
        observer.observe(element);
    });
} 