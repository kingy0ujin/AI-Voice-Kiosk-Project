const micBtn = document.getElementById('mic-btn');
const statusText = document.getElementById('status-text');
const chatContainer = document.getElementById('chat-container');
const textInputArea = document.getElementById('text-input-area');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

let recognition;
let isListening = false;
let isSyntheticVoicePlaying = false; // Prevent listening while speaking

// Initialize Web Speech API
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.lang = 'ko-KR'; // Korean
    recognition.interimResults = true; // Enable interim results for real-time feedback
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
        isListening = true;
        micBtn.classList.add('listening');
        statusText.textContent = "듣고 있어요... (말씀해 보세요)";
    };

    recognition.onend = () => {
        isListening = false;
        micBtn.classList.remove('listening');
        // Do not reset status text immediately if we processed a final result
        // statusText.textContent = "버튼을 누르고 말씀하세요..."; 
    };

    recognition.onresult = (event) => {
        let interimTranscript = '';
        let finalTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                finalTranscript += event.results[i][0].transcript;
            } else {
                interimTranscript += event.results[i][0].transcript;
            }
        }

        if (interimTranscript) {
            statusText.textContent = `[인식 중]: ${interimTranscript}`;
            statusText.style.color = "#a29bfe";
        }

        if (finalTranscript) {
            statusText.textContent = "답변을 생각하는 중...";
            console.log('Final Recognized:', finalTranscript);
            addMessage(finalTranscript, 'user');
            processUserMessage(finalTranscript);
        }
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error', event.error);
        statusText.textContent = "오류가 발생했습니다. 다시 시도해주세요.";
        // Show text input fallback on repeated errors or specific errors
        if (event.error === 'not-allowed' || event.error === 'service-not-allowed') {
            textInputArea.classList.remove('hidden');
            statusText.textContent = "마이크 사용이 차단되었습니다. 텍스트로 입력해주세요.";
        }
    };
} else {
    // Fallback for browsers without speech recognition
    textInputArea.classList.remove('hidden');
    micBtn.style.display = 'none';
    statusText.textContent = "이 브라우저는 음성 인식을 지원하지 않습니다.";
}

// Event Listeners
micBtn.addEventListener('click', () => {
    if (isListening) {
        recognition.stop();
    } else {
        recognition.start();
    }
});

sendBtn.addEventListener('click', () => {
    const text = userInput.value.trim();
    if (text) {
        addMessage(text, 'user');
        processUserMessage(text);
        userInput.value = '';
    }
});

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const text = userInput.value.trim();
        if (text) {
            addMessage(text, 'user');
            processUserMessage(text);
            userInput.value = '';
        }
    }
});

function addMessage(text, sender) {
    const chatContainer = document.getElementById('chat-container');
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}`;
    // Add custom attribute for CSS content
    msgDiv.setAttribute('data-sender', sender === 'user' ? '나' : 'AI 키오스크');

    msgDiv.innerHTML = `<div class="bubble">${text}</div>`;
    chatContainer.appendChild(msgDiv);

    // Auto scroll with delay
    setTimeout(() => {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }, 50);
}

async function processUserMessage(message) {
    statusText.textContent = "답변을 생각하는 중...";

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: message,
                cart: cart // Send current cart state
            })
        });

        const data = await response.json();

        if (data.status === "success") {
            // Process Commands first
            if (data.commands && data.commands.length > 0) {
                data.commands.forEach(cmd => {
                    if (cmd.type === 'add') {
                        // Map name to price (simple lookup)
                        const price = getPriceByName(cmd.item);
                        if (price > 0) addToCart(cmd.item, price);
                    } else if (cmd.type === 'remove') {
                        removeFromCart(cmd.item);
                    } else if (cmd.type === 'clear') {
                        clearCart();
                    }
                });
            }

            const botReply = data.response;
            addMessage(botReply, 'system');

            // Speak the response (TTS)
            speak(botReply);

            if (data.order_complete) {
                statusText.textContent = "주문이 완료되었습니다!";
                statusText.style.color = "#a29bfe";
                // Optionally disable controls
            } else {
                statusText.textContent = "버튼을 누르고 말씀하세요...";
            }

        } else {
            addMessage("죄송합니다. 오류가 발생했습니다.", 'system');
        }
    } catch (error) {
        console.error('API Error:', error);
        addMessage("서버 연결에 실패했습니다.", 'system');
    }
}

// Helper to get price
function getPriceByName(name) {
    const menu = {
        '불고기 버거': 5000,
        '치즈 버거': 5500,
        '새우 버거': 6000,
        '리얼 치즈 버거': 7000,
        '베이컨 버거': 6500,
        '감자튀김': 2000,
        '양파링': 2500,
        '치즈스틱': 2000,
        '콜라': 1500,
        '사이다': 1500,
        '오렌지 주스': 2500,
        '레모네이드': 3000
    };
    return menu[name] || 0;
}

function removeFromCart(name) {
    // Find index of item
    const index = cart.findIndex(item => item.name === name);
    if (index > -1) {
        cart.splice(index, 1);
        updateCartDisplay();
    }
}

// Cart Data
let cart = [];

function openTab(category) {
    // Hide all tab content
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    // Deactivate all tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));

    // Show selected and activate button
    document.getElementById(category).classList.add('active');
    document.querySelector(`.tab-btn[onclick="openTab('${category}')"]`).classList.add('active');
}

function addToCart(name, price) {
    cart.push({ name, price });
    updateCartDisplay();
    // Optional: Play a small sound or visual feedback
}

function clearCart() {
    cart = [];
    updateCartDisplay();
}

function updateCartDisplay() {
    const list = document.getElementById('cart-list');
    const totalEl = document.getElementById('total-price');

    list.innerHTML = '';

    if (cart.length === 0) {
        list.innerHTML = '<li class="empty-cart">선택된 메뉴가 없습니다.</li>';
        totalEl.textContent = '0원';
        return;
    }

    let total = 0;

    // Aggregate items
    const counts = {};
    const prices = {};

    cart.forEach(item => {
        counts[item.name] = (counts[item.name] || 0) + 1;
        prices[item.name] = item.price;
        total += item.price;
    });

    for (const [name, count] of Object.entries(counts)) {
        const li = document.createElement('li');
        li.className = 'cart-item';
        li.innerHTML = `
            <span>${name} x ${count}</span>
            <span>${(prices[name] * count).toLocaleString()}원</span>
        `;
        list.appendChild(li);
    }

    totalEl.textContent = `${total.toLocaleString()}원`;
}

function speak(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'ko-KR';
        // utterance.rate = 1.0;
        window.speechSynthesis.speak(utterance);
    }
}
