/**
 * Chatbot functionality for FlashCard Generation app
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeChatbot();
});

// Initialize the chatbot UI and functionality
function initializeChatbot() {
    // Create chatbot widget
    createChatbotUI();
    
    // Set up event listeners
    setupChatbotEvents();
}

// Create chatbot UI elements
function createChatbotUI() {
    // Create chatbot widget button
    const chatbotWidget = document.createElement('div');
    chatbotWidget.classList.add('chatbot-widget');
    chatbotWidget.innerHTML = '<i class="bi bi-chat-dots"></i>';
    document.body.appendChild(chatbotWidget);
    
    // Create chatbot container
    const chatbotContainer = document.createElement('div');
    chatbotContainer.classList.add('chatbot-container');
    chatbotContainer.id = 'chatbotContainer';
    
    chatbotContainer.innerHTML = `
        <div class="chatbot-header">
            <h5><i class="bi bi-robot me-2"></i>FlashCard Assistant</h5>
            <button class="chatbot-close" id="chatbotClose">&times;</button>
        </div>
        <div class="chatbot-messages" id="chatbotMessages"></div>
        <div class="chatbot-input-container">
            <input type="text" class="chatbot-input" id="chatbotInput" placeholder="Ask me anything...">
            <button class="chatbot-send" id="chatbotSend">
                <i class="bi bi-send"></i>
            </button>
        </div>
    `;
    
    document.body.appendChild(chatbotContainer);
    
    // Add welcome message
    setTimeout(() => {
        addBotMessage("👋 Hi there! I'm your FlashCard Assistant. How can I help you today?");
        
        // Add quick action buttons
        const quickActions = document.createElement('div');
        quickActions.classList.add('chatbot-quick-actions');
        quickActions.innerHTML = `
            <button class="chatbot-quick-action" data-action="create">Create a flashcard</button>
            <button class="chatbot-quick-action" data-action="study">Start studying</button>
            <button class="chatbot-quick-action" data-action="help">How to use</button>
        `;
        
        const messagesContainer = document.getElementById('chatbotMessages');
        messagesContainer.appendChild(quickActions);
        
        // Add event listeners to quick action buttons
        document.querySelectorAll('.chatbot-quick-action').forEach(button => {
            button.addEventListener('click', function() {
                const action = this.getAttribute('data-action');
                handleQuickAction(action);
            });
        });
    }, 500);
}

// Set up event listeners for chatbot interactions
function setupChatbotEvents() {
    // Toggle chatbot visibility when widget is clicked
    document.querySelector('.chatbot-widget').addEventListener('click', function() {
        const chatbotContainer = document.getElementById('chatbotContainer');
        chatbotContainer.classList.toggle('open');
        
        // Focus input when opened
        if (chatbotContainer.classList.contains('open')) {
            document.getElementById('chatbotInput').focus();
        }
    });
    
    // Close chatbot when close button is clicked
    document.getElementById('chatbotClose').addEventListener('click', function() {
        document.getElementById('chatbotContainer').classList.remove('open');
    });
    
    // Send message when send button is clicked
    document.getElementById('chatbotSend').addEventListener('click', sendUserMessage);
    
    // Send message when Enter key is pressed in input
    document.getElementById('chatbotInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendUserMessage();
        }
    });
}

// Send user message to the chatbot
function sendUserMessage() {
    const input = document.getElementById('chatbotInput');
    const message = input.value.trim();
    
    if (message) {
        // Add user message to chat
        addUserMessage(message);
        
        // Clear input
        input.value = '';
        
        // Show typing indicator
        showTypingIndicator();
        
        // Process user message and generate response
        setTimeout(() => {
            hideTypingIndicator();
            processChatbotResponse(message);
        }, 1000 + Math.random() * 1000); // Random delay for realism
    }
}

// Add a user message to the chat
function addUserMessage(message) {
    const messagesContainer = document.getElementById('chatbotMessages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('chatbot-message', 'chatbot-message-user');
    messageElement.textContent = message;
    messagesContainer.appendChild(messageElement);
    
    // Scroll to bottom
    scrollToBottom();
}

// Add a bot message to the chat
function addBotMessage(message) {
    const messagesContainer = document.getElementById('chatbotMessages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('chatbot-message', 'chatbot-message-bot');
    messageElement.innerHTML = message;
    messagesContainer.appendChild(messageElement);
    
    // Scroll to bottom
    scrollToBottom();
}

// Show typing indicator
function showTypingIndicator() {
    const messagesContainer = document.getElementById('chatbotMessages');
    const typingIndicator = document.createElement('div');
    typingIndicator.id = 'typingIndicator';
    typingIndicator.classList.add('chatbot-message', 'chatbot-message-bot', 'typing-indicator');
    typingIndicator.innerHTML = '<span></span><span></span><span></span>';
    messagesContainer.appendChild(typingIndicator);
    
    // Scroll to bottom
    scrollToBottom();
}

// Hide typing indicator
function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Scroll the chat to the bottom
function scrollToBottom() {
    const messagesContainer = document.getElementById('chatbotMessages');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Process user message and generate a response
function processChatbotResponse(message) {
    // Convert to lowercase for easier comparison
    const lowerMessage = message.toLowerCase();
    
    // Check for keywords and respond accordingly
    if (lowerMessage.includes('hello') || lowerMessage.includes('hi') || lowerMessage.includes('hey')) {
        addBotMessage("Hello! How can I assist you with your flashcards today?");
    }
    else if (lowerMessage.includes('bye') || lowerMessage.includes('goodbye')) {
        addBotMessage("Goodbye! If you need more help with your flashcards, just open the chat again.");
    }
    else if (lowerMessage.includes('thank')) {
        addBotMessage("You're welcome! I'm happy to help. Is there anything else you'd like to know?");
    }
    else if (lowerMessage.includes('create') || lowerMessage.includes('new card') || lowerMessage.includes('make card')) {
        addBotMessage("To create a new flashcard, click on the <b>Create Cards</b> link in the sidebar or use this button: <a href='/create' class='btn btn-sm btn-primary mt-2'>Create Flashcard</a>");
    }
    else if (lowerMessage.includes('study') || lowerMessage.includes('review')) {
        addBotMessage("Ready to study? Click on the <b>Study</b> link in the sidebar or use this button: <a href='/study' class='btn btn-sm btn-primary mt-2'>Start Studying</a>");
    }
    else if (lowerMessage.includes('delete')) {
        addBotMessage("To delete a flashcard, go to the home page and find the flashcard you want to remove. Then click the Delete button on that card.");
    }
    else if (lowerMessage.includes('edit') || lowerMessage.includes('change')) {
        addBotMessage("To edit a flashcard, go to the home page, find the card you want to modify, and click the Edit button.");
    }
    else if (lowerMessage.includes('help') || lowerMessage.includes('how to')) {
        showHelpGuide();
    }
    else if (lowerMessage.includes('grammar') || lowerMessage.includes('check grammar')) {
        addBotMessage("You can use our Grammar Check tool by clicking on <b>Grammar Check</b> in the sidebar. It will help you fix any grammatical errors in your text.");
    }
    else if (lowerMessage.includes('translate') || lowerMessage.includes('translation')) {
        addBotMessage("Need to translate something? Click on <b>Translation</b> in the sidebar to use our translation tool.");
    }
    else if (lowerMessage.includes('summarize') || lowerMessage.includes('summary')) {
        addBotMessage("Our Summarize tool can help condense long text. Click on <b>Summarize</b> in the sidebar to use it.");
    }
    else if (lowerMessage.includes('tip') || lowerMessage.includes('advice')) {
        showRandomTip();
    }
    else {
        // General response for any other query
        addBotMessage("I'm not sure I understand. Would you like help with creating flashcards, studying, or using our AI tools?");
        
        // Add quick action buttons again
        const quickActions = document.createElement('div');
        quickActions.classList.add('chatbot-quick-actions');
        quickActions.innerHTML = `
            <button class="chatbot-quick-action" data-action="create">Create a flashcard</button>
            <button class="chatbot-quick-action" data-action="study">Start studying</button>
            <button class="chatbot-quick-action" data-action="help">How to use</button>
        `;
        
        const messagesContainer = document.getElementById('chatbotMessages');
        messagesContainer.appendChild(quickActions);
        
        // Add event listeners to quick action buttons
        document.querySelectorAll('.chatbot-quick-action').forEach(button => {
            button.addEventListener('click', function() {
                const action = this.getAttribute('data-action');
                handleQuickAction(action);
            });
        });
    }
}

// Handle quick action button clicks
function handleQuickAction(action) {
    switch(action) {
        case 'create':
            addUserMessage("I want to create a flashcard");
            showTypingIndicator();
            
            setTimeout(() => {
                hideTypingIndicator();
                addBotMessage("Great! You can create a new flashcard by clicking the <b>Create Cards</b> link in the sidebar or this button: <a href='/create' class='btn btn-sm btn-primary mt-2'>Create Flashcard</a>");
                addBotMessage("For the best flashcards, make sure to write clear questions and comprehensive answers. You can also use our AI tools to help generate content!");
            }, 1000);
            break;
            
        case 'study':
            addUserMessage("I want to study");
            showTypingIndicator();
            
            setTimeout(() => {
                hideTypingIndicator();
                addBotMessage("Ready to study? You can start by clicking the <b>Study</b> link in the sidebar or this button: <a href='/study' class='btn btn-sm btn-primary mt-2'>Start Studying</a>");
                addBotMessage("Tip: When studying, use the difficulty ratings (Easy, Medium, Hard) to help with spaced repetition learning. Focus more on the cards you find difficult.");
            }, 1000);
            break;
            
        case 'help':
            addUserMessage("How do I use this app?");
            showTypingIndicator();
            
            setTimeout(() => {
                hideTypingIndicator();
                showHelpGuide();
            }, 1000);
            break;
    }
}

// Show help guide with app instructions
function showHelpGuide() {
    const helpGuide = `
        <h6 class="mb-2">FlashCard App Guide:</h6>
        <ul class="ps-3">
            <li><b>Create flashcards</b> - Go to Create Cards page and fill out the form</li>
            <li><b>Study</b> - Go to Study page and flip through your cards</li>
            <li><b>AI Tools</b> - Use Grammar Check, Translation, and Summarize from the sidebar</li>
            <li><b>Edit cards</b> - Go to home page and click Edit on any card</li>
            <li><b>Delete cards</b> - Go to home page and click Delete on any card</li>
        </ul>
        <p>Is there something specific you need help with?</p>
    `;
    
    addBotMessage(helpGuide);
}

// Show a random study tip
function showRandomTip() {
    const tips = [
        "Try to create flashcards with simple, clear questions for the best results.",
        "Use spaced repetition - study hard cards more frequently than easier ones.",
        "Write answers in your own words to improve understanding and retention.",
        "Review your flashcards regularly, not just before exams.",
        "Try to create visual associations to help remember difficult concepts.",
        "Use our AI tools to help generate content or check your grammar.",
        "Organize your flashcards with tags for better organization.",
        "Test yourself actively rather than just reading through the cards.",
        "Study in short, focused sessions rather than long marathons.",
        "Combine your flashcards with other study methods for the best learning."
    ];
    
    const randomTip = tips[Math.floor(Math.random() * tips.length)];
    addBotMessage(`<b>Study Tip:</b> ${randomTip}`);
} 