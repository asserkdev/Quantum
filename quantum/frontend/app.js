/**
 * Quantum AI - Frontend Application
 * Handles all UI interactions and API calls
 */

// Configuration
const CONFIG = {
    API_URL: 'http://localhost:8000',
    AUTO_SAVE_INTERVAL: 30000,
    MAX_MESSAGES: 100
};

// State Management
const state = {
    currentUser: null,
    currentView: 'chat',
    currentMode: 'auto',
    conversationId: null,
    messages: [],
    goals: [],
    isAuthenticated: false,
    isTyping: false,
    threeScene: null,
    animationEnabled: true
};

// DOM Elements
const elements = {
    sidebar: document.getElementById('sidebar'),
    sidebarToggle: document.getElementById('sidebarToggle'),
    userSection: document.getElementById('userSection'),
    userName: document.getElementById('userName'),
    userAvatar: document.getElementById('userAvatar'),
    authToggle: document.getElementById('authToggle'),
    authModal: document.getElementById('authModal'),
    closeAuthModal: document.getElementById('closeAuthModal'),
    chatContainer: document.getElementById('chatContainer'),
    welcomeMessage: document.getElementById('welcomeMessage'),
    chatInput: document.getElementById('chatInput'),
    sendBtn: document.getElementById('sendBtn'),
    modeBtn: document.getElementById('modeBtn'),
    modeSelector: document.getElementById('modeSelector'),
    attachBtn: document.getElementById('attachBtn'),
    toastContainer: document.getElementById('toastContainer')
};

// ==================== INITIALIZATION ====================

document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

function initializeApp() {
    setupEventListeners();
    setupNavigation();
    setupAuth();
    setupChat();
    setupSearch();
    setupFactCheck();
    setupCreate();
    setup3DStudio();
    setupGoals();
    initialize3DScene();
    loadUserSession();
}

// ==================== EVENT LISTENERS ====================

function setupEventListeners() {
    // Sidebar toggle
    elements.sidebarToggle.addEventListener('click', toggleSidebar);
    
    // Auth modal
    elements.authToggle.addEventListener('click', () => toggleModal('authModal'));
    elements.closeAuthModal.addEventListener('click', () => toggleModal('authModal'));
    
    // Mode selector toggle
    elements.modeBtn.addEventListener('click', toggleModeSelector);
    
    // Click outside to close mode selector
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.mode-btn') && !e.target.closest('.mode-selector')) {
            elements.modeSelector.classList.remove('active');
        }
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', handleKeyboardShortcuts);
}

// ==================== NAVIGATION ====================

function setupNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const viewId = item.dataset.view;
            switchView(viewId);
            
            // Update active state
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');
        });
    });
}

function switchView(viewId) {
    const views = document.querySelectorAll('.view');
    views.forEach(view => view.classList.remove('active'));
    
    const targetView = document.getElementById(`${viewId}View`);
    if (targetView) {
        targetView.classList.add('active');
        state.currentView = viewId;
    }
}

// ==================== SIDEBAR ====================

function toggleSidebar() {
    elements.sidebar.classList.toggle('collapsed');
}

// ==================== CHAT ====================

function setupChat() {
    // Send message on button click
    elements.sendBtn.addEventListener('click', sendMessage);
    
    // Send message on Enter key
    elements.chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Auto-resize textarea
    elements.chatInput.addEventListener('input', autoResizeInput);
}

function autoResizeInput(e) {
    e.target.style.height = 'auto';
    e.target.style.height = Math.min(e.target.scrollHeight, 200) + 'px';
}

async function sendMessage() {
    const message = elements.chatInput.value.trim();
    if (!message || state.isTyping) return;
    
    // Clear input
    elements.chatInput.value = '';
    elements.chatInput.style.height = 'auto';
    
    // Hide welcome message
    if (elements.welcomeMessage) {
        elements.welcomeMessage.style.display = 'none';
    }
    
    // Add user message
    addMessage('user', message);
    
    // Show typing indicator
    showTypingIndicator();
    
    // Send to API
    try {
        const response = await callAPI('/api/chat', {
            message,
            conversation_id: state.conversationId,
            user_id: state.currentUser?.id,
            mode: state.currentMode === 'auto' ? 'auto' : state.currentMode
        });
        
        hideTypingIndicator();
        
        if (response.response) {
            addMessage('assistant', response.response, response);
            state.conversationId = response.conversation_id;
            
            // === CONSCIOUSNESS INTEGRATION ===
            // Update Quantum's emotional state display
            if (response.quantum_state) {
                updateQuantumDisplay(response.quantum_state);
            }
            
            // Apply UI adaptations based on emotional state
            if (response.ui_adaptation) {
                applyEmotionalUI(response.ui_adaptation);
            }
        }
    } catch (error) {
        hideTypingIndicator();
        showToast('Failed to get response. Please try again.', 'error');
        console.error('Chat error:', error);
    }
}

function addMessage(role, content, data = {}) {
    const messageEl = document.createElement('div');
    messageEl.className = `message ${role}`;
    
    const avatar = role === 'assistant' ? 'Q' : (state.currentUser?.profile?.name?.[0] || 'U');
    
    let sourcesHtml = '';
    if (data.sources && data.sources.length > 0) {
        sourcesHtml = `
            <div class="message-sources">
                <h4>📚 Sources</h4>
                ${data.sources.slice(0, 3).map(s => `
                    <div class="source-item">
                        <span>🔗</span>
                        <a href="${s.url}" target="_blank">${s.title || 'Source'}</a>
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    messageEl.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <div class="message-text">${formatMessage(content)}</div>
            ${sourcesHtml}
        </div>
    `;
    
    elements.chatContainer.appendChild(messageEl);
    elements.chatContainer.scrollTop = elements.chatContainer.scrollHeight;
    
    state.messages.push({ role, content, data });
}

function formatMessage(content) {
    // Convert markdown-like formatting
    let formatted = content
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/`(.*?)`/g, '<code>$1</code>')
        .replace(/\n/g, '<br>');
    
    return formatted;
}

function showTypingIndicator() {
    state.isTyping = true;
    const indicator = document.createElement('div');
    indicator.className = 'message assistant typing';
    indicator.id = 'typingIndicator';
    indicator.innerHTML = `
        <div class="message-avatar">Q</div>
        <div class="message-content">
            <div class="message-text">
                <span class="typing-dots">
                    <span></span><span></span><span></span>
                </span>
            </div>
        </div>
    `;
    elements.chatContainer.appendChild(indicator);
    elements.chatContainer.scrollTop = elements.chatContainer.scrollHeight;
}

function hideTypingIndicator() {
    state.isTyping = false;
    const indicator = document.getElementById('typingIndicator');
    if (indicator) indicator.remove();
}

function toggleModeSelector() {
    elements.modeSelector.classList.toggle('active');
}

function setupModeSelection() {
    const modeOptions = document.querySelectorAll('.mode-option');
    modeOptions.forEach(option => {
        option.addEventListener('click', () => {
            state.currentMode = option.dataset.mode;
            modeOptions.forEach(opt => opt.classList.remove('active'));
            option.classList.add('active');
            
            // Update mode icon
            const modeIcon = document.querySelector('.mode-icon');
            const icons = {
                auto: '🎯',
                search: '🔍',
                fact: '✅',
                image: '🎨',
                '3d': '🎮',
                code: '💻'
            };
            modeIcon.textContent = icons[state.currentMode] || '🎯';
            
            elements.modeSelector.classList.remove('active');
        });
    });
}

// ==================== SEARCH ====================

function setupSearch() {
    const searchBtn = document.getElementById('searchBtn');
    const searchInput = document.getElementById('searchInput');
    
    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') performSearch();
    });
}

async function performSearch() {
    const searchInput = document.getElementById('searchInput');
    const depthSelect = document.getElementById('searchDepth');
    const resultsContainer = document.getElementById('searchResults');
    
    const query = searchInput.value.trim();
    if (!query) return;
    
    resultsContainer.innerHTML = '<p class="results-placeholder">Searching...</p>';
    
    try {
        const response = await callAPI('/api/search', {
            query,
            depth: depthSelect.value
        });
        
        displaySearchResults(response);
    } catch (error) {
        resultsContainer.innerHTML = '<p class="results-placeholder">Search failed. Please try again.</p>';
        showToast('Search failed', 'error');
    }
}

function displaySearchResults(data) {
    const resultsContainer = document.getElementById('searchResults');
    const results = data.results || [];
    
    if (results.length === 0) {
        resultsContainer.innerHTML = '<p class="results-placeholder">No results found.</p>';
        return;
    }
    
    let html = '';
    
    // Add summary if available
    if (data.summary) {
        html += `
            <div class="search-summary" style="margin-bottom: 20px; padding: 16px; background: var(--bg-dark-3); border-radius: var(--radius);">
                <h3 style="margin-bottom: 8px;">📋 Summary</h3>
                <p style="color: var(--text-secondary);">${data.summary}</p>
            </div>
        `;
    }
    
    // Add analysis if available
    if (data.analysis) {
        const analysis = data.analysis;
        html += `
            <div class="search-analysis" style="margin-bottom: 20px; display: flex; gap: 12px; flex-wrap: wrap;">
                <span style="padding: 6px 12px; background: var(--bg-dark-3); border-radius: 20px; font-size: 12px;">
                    📊 Reliability: <strong style="color: ${analysis.reliability === 'high' ? 'var(--success)' : 'var(--warning)'}">${analysis.reliability}</strong>
                </span>
                <span style="padding: 6px 12px; background: var(--bg-dark-3); border-radius: 20px; font-size: 12px;">
                    ✅ Fact Score: <strong>${(analysis.fact_score * 100).toFixed(0)}%</strong>
                </span>
                <span style="padding: 6px 12px; background: var(--bg-dark-3); border-radius: 20px; font-size: 12px;">
                    💬 Sentiment: <strong>${analysis.sentiment}</strong>
                </span>
                ${analysis.is_breaking ? '<span style="padding: 6px 12px; background: var(--error); border-radius: 20px; font-size: 12px;">🔥 Breaking News</span>' : ''}
            </div>
        `;
    }
    
    // Add results
    results.forEach(result => {
        html += `
            <div class="search-result-item">
                <h3><a href="${result.url}" target="_blank">${result.title}</a></h3>
                <p>${result.content || 'No description available'}</p>
                <div class="result-meta">
                    <span>🔗 ${new URL(result.url).hostname}</span>
                    <span>📊 Score: ${((result.score || 0.9) * 100).toFixed(0)}%</span>
                </div>
            </div>
        `;
    });
    
    resultsContainer.innerHTML = html;
}

// ==================== FACT CHECK ====================

function setupFactCheck() {
    const verifyBtn = document.getElementById('verifyBtn');
    const claimInput = document.getElementById('claimInput');
    
    verifyBtn.addEventListener('click', performFactCheck);
    claimInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            performFactCheck();
        }
    });
}

async function performFactCheck() {
    const claimInput = document.getElementById('claimInput');
    const verdictDisplay = document.getElementById('verdictDisplay');
    
    const claim = claimInput.value.trim();
    if (!claim) return;
    
    verdictDisplay.innerHTML = '<p class="results-placeholder">Analyzing claim...</p>';
    
    try {
        const response = await callAPI('/api/fact-check', {
            claim,
            sources: []
        });
        
        displayVerdict(response);
    } catch (error) {
        verdictDisplay.innerHTML = '<p class="results-placeholder">Analysis failed. Please try again.</p>';
        showToast('Fact check failed', 'error');
    }
}

function displayVerdict(data) {
    const verdictDisplay = document.getElementById('verdictDisplay');
    const verdict = data.verdict || 'UNVERIFIED';
    
    const badgeClass = {
        'TRUE': 'true',
        'FALSE': 'false',
        'LIKELY TRUE': 'likely-true',
        'LIKELY FALSE': 'likely-false',
        'UNVERIFIED': 'unverified'
    }[verdict] || 'unverified';
    
    const badgeEmoji = {
        'TRUE': '✅',
        'FALSE': '❌',
        'LIKELY TRUE': '👍',
        'LIKELY FALSE': '⚠️',
        'UNVERIFIED': '❓'
    }[verdict] || '❓';
    
    verdictDisplay.innerHTML = `
        <div class="verdict-result">
            <span class="verdict-badge ${badgeClass}">${badgeEmoji} ${verdict}</span>
            <div class="verdict-explanation">
                ${data.explanation || 'Unable to verify this claim.'}
                
                ${data.recommendations && data.recommendations.length > 0 ? `
                    <br><br><strong>Recommendations:</strong>
                    <ul style="margin-top: 8px; padding-left: 20px;">
                        ${data.recommendations.map(r => `<li style="margin-bottom: 4px;">${r}</li>`).join('')}
                    </ul>
                ` : ''}
            </div>
        </div>
    `;
}

// ==================== IMAGE CREATION ====================

function setupCreate() {
    const generateBtn = document.getElementById('generateBtn');
    
    generateBtn.addEventListener('click', generateImage);
}

async function generateImage() {
    const promptInput = document.getElementById('imagePrompt');
    const styleSelect = document.getElementById('imageStyle');
    const sizeSelect = document.getElementById('imageSize');
    const imageDisplay = document.getElementById('imageDisplay');
    
    const prompt = promptInput.value.trim();
    if (!prompt) {
        showToast('Please enter an image description', 'warning');
        return;
    }
    
    imageDisplay.innerHTML = '<p class="results-placeholder">Generating image...</p>';
    
    try {
        const response = await callAPI('/api/generate/image', {
            prompt,
            style: styleSelect.value,
            size: sizeSelect.value
        });
        
        if (response.success && response.image) {
            displayGeneratedImage(response.image);
        } else {
            imageDisplay.innerHTML = '<p class="results-placeholder">Image generation is simulated in this demo.</p>';
        }
    } catch (error) {
        imageDisplay.innerHTML = '<p class="results-placeholder">Generation failed. Please try again.</p>';
        showToast('Image generation failed', 'error');
    }
}

function displayGeneratedImage(imageData) {
    const imageDisplay = document.getElementById('imageDisplay');
    
    imageDisplay.innerHTML = `
        <div class="generated-image-container" style="text-align: center;">
            <div style="background: var(--bg-dark-3); border-radius: var(--radius); padding: 40px; margin: 20px;">
                <div style="font-size: 80px; margin-bottom: 20px;">🎨</div>
                <p style="color: var(--text-secondary); margin-bottom: 16px;">Image Generated Successfully!</p>
                <p style="font-size: 14px;"><strong>Prompt:</strong> ${imageData.prompt}</p>
                <p style="font-size: 14px;"><strong>Style:</strong> ${imageData.style}</p>
                <p style="font-size: 14px;"><strong>Size:</strong> ${imageData.size}</p>
            </div>
        </div>
    `;
    
    showToast('Image generated successfully!', 'success');
}

// ==================== 3D STUDIO ====================

function setup3DStudio() {
    const createSceneBtn = document.getElementById('createSceneBtn');
    const resetCameraBtn = document.getElementById('resetCamera');
    const toggleAnimationBtn = document.getElementById('toggleAnimation');
    
    createSceneBtn.addEventListener('click', create3DScene);
    resetCameraBtn.addEventListener('click', resetCamera);
    toggleAnimationBtn.addEventListener('click', toggleAnimation);
}

function initialize3DScene() {
    const container = document.getElementById('3dCanvas');
    if (!container) return;
    
    // Scene setup
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x1a1a2e);
    
    // Camera
    const camera = new THREE.PerspectiveCamera(
        75,
        container.clientWidth / container.clientHeight,
        0.1,
        1000
    );
    camera.position.set(0, 2, 5);
    
    // Renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);
    
    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(5, 5, 5);
    scene.add(directionalLight);
    
    // Create default object
    const geometry = new THREE.TorusKnotGeometry(1, 0.3, 100, 16);
    const material = new THREE.MeshStandardMaterial({
        color: 0x6366f1,
        metalness: 0.5,
        roughness: 0.3
    });
    const torusKnot = new THREE.Mesh(geometry, material);
    scene.add(torusKnot);
    
    // Store scene reference
    state.threeScene = {
        scene,
        camera,
        renderer,
        mainObject: torusKnot
    };
    
    // Animation loop
    function animate() {
        requestAnimationFrame(animate);
        
        if (state.animationEnabled && state.threeScene.mainObject) {
            state.threeScene.mainObject.rotation.x += 0.005;
            state.threeScene.mainObject.rotation.y += 0.01;
        }
        
        renderer.render(scene, camera);
    }
    animate();
    
    // Handle window resize
    window.addEventListener('resize', () => {
        if (state.threeScene) {
            const width = container.clientWidth;
            const height = container.clientHeight;
            
            state.threeScene.camera.aspect = width / height;
            state.threeScene.camera.updateProjectionMatrix();
            state.threeScene.renderer.setSize(width, height);
        }
    });
}

async function create3DScene() {
    const promptInput = document.getElementById('3dPrompt');
    const styleSelect = document.getElementById('3dStyle');
    
    const prompt = promptInput.value.trim();
    if (!prompt) {
        showToast('Please describe your 3D scene', 'warning');
        return;
    }
    
    try {
        const response = await callAPI('/api/3d/generate', {
            prompt,
            style: styleSelect.value,
            animation: true
        });
        
        if (response.success) {
            update3DScene(response.scene);
            showToast('3D scene created!', 'success');
        }
    } catch (error) {
        showToast('Failed to create 3D scene', 'error');
    }
}

function update3DScene(sceneData) {
    if (!state.threeScene) return;
    
    // Clear existing objects except lights
    while (state.threeScene.scene.children.length > 2) {
        state.threeScene.scene.remove(state.threeScene.scene.children[2]);
    }
    
    // Create new objects based on scene config
    const objects = sceneData.scene_config?.objects || [];
    
    objects.forEach(obj => {
        let geometry;
        switch (obj.geometry) {
            case 'torus':
                geometry = new THREE.TorusGeometry(1, 0.3, 16, 100);
                break;
            case 'sphere':
                geometry = new THREE.SphereGeometry(1, 32, 32);
                break;
            case 'box':
                geometry = new THREE.BoxGeometry(1, 1, 1);
                break;
            case 'icosahedron':
                geometry = new THREE.IcosahedronGeometry(1, 0);
                break;
            case 'cone':
                geometry = new THREE.ConeGeometry(1, 2, 32);
                break;
            default:
                geometry = new THREE.TorusKnotGeometry(1, 0.3, 100, 16);
        }
        
        const material = new THREE.MeshStandardMaterial({
            color: Math.random() * 0xffffff,
            metalness: 0.5,
            roughness: 0.3
        });
        
        const mesh = new THREE.Mesh(geometry, material);
        mesh.position.set(...(obj.position || [0, 0, 0]));
        mesh.scale.set(...(obj.scale || [1, 1, 1]));
        
        state.threeScene.scene.add(mesh);
        state.threeScene.mainObject = mesh;
    });
}

function resetCamera() {
    if (!state.threeScene) return;
    state.threeScene.camera.position.set(0, 2, 5);
    state.threeScene.camera.lookAt(0, 0, 0);
}

function toggleAnimation() {
    state.animationEnabled = !state.animationEnabled;
    const btn = document.getElementById('toggleAnimation');
    btn.textContent = state.animationEnabled ? 'Pause Animation' : 'Resume Animation';
}

// ==================== GOALS ====================

function setupGoals() {
    const setGoalBtn = document.getElementById('setGoalBtn');
    const goalInput = document.getElementById('goalInput');
    
    setGoalBtn.addEventListener('click', setGoal);
    goalInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') setGoal();
    });
}

async function setGoal() {
    const goalInput = document.getElementById('goalInput');
    const goal = goalInput.value.trim();
    
    if (!goal) {
        showToast('Please enter a goal', 'warning');
        return;
    }
    
    try {
        const response = await callAPI('/api/autonomous/goal', {
            goal,
            user_id: state.currentUser?.id
        });
        
        if (response.goal_id) {
            state.goals.push(response);
            goalInput.value = '';
            displayGoals();
            showToast('Goal set successfully!', 'success');
        }
    } catch (error) {
        showToast('Failed to set goal', 'error');
    }
}

function displayGoals() {
    const goalsList = document.getElementById('goalsList');
    const activeGoalsCount = document.getElementById('activeGoalsCount');
    
    activeGoalsCount.textContent = state.goals.length;
    
    if (state.goals.length === 0) {
        goalsList.innerHTML = `
            <div class="no-goals">
                <span>🎯</span>
                <p>No active goals. Set one above to get started!</p>
            </div>
        `;
        return;
    }
    
    let html = '';
    state.goals.forEach(goal => {
        const progress = goal.progress || 0;
        html += `
            <div class="goal-item">
                <div class="goal-header">
                    <span class="goal-title">${goal.goal}</span>
                    <span class="goal-status">${goal.status || 'Active'}</span>
                </div>
                <div class="goal-progress-bar">
                    <div class="goal-progress" style="width: ${progress}%"></div>
                </div>
                <div class="goal-meta">
                    <span>Progress: ${progress}%</span>
                    ${goal.steps?.length ? ` • ${goal.steps.length} steps` : ''}
                </div>
            </div>
        `;
    });
    
    goalsList.innerHTML = html;
}

// ==================== AUTHENTICATION ====================

function setupAuth() {
    // Auth tabs
    const authTabs = document.querySelectorAll('.auth-tab');
    authTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabId = tab.dataset.tab;
            authTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            document.getElementById('loginForm').classList.toggle('hidden', tabId !== 'login');
            document.getElementById('signupForm').classList.toggle('hidden', tabId !== 'signup');
        });
    });
    
    // Login form
    document.getElementById('loginSubmit').addEventListener('click', handleLogin);
    document.getElementById('signupSubmit').addEventListener('click', handleSignup);
    
    // OAuth buttons
    document.getElementById('googleLogin').addEventListener('click', () => {
        // In production, redirect to Google OAuth
        showToast('Google OAuth requires configuration', 'warning');
    });
    
    document.getElementById('azureLogin').addEventListener('click', () => {
        // In production, redirect to Azure AD
        showToast('Azure AD requires configuration', 'warning');
    });
    
    setupModeSelection();
}

async function handleLogin() {
    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value;
    
    if (!email || !password) {
        showToast('Please fill in all fields', 'warning');
        return;
    }
    
    try {
        const response = await callAPI('/api/auth/login', { email, password });
        
        if (response.success) {
            state.currentUser = response.user;
            state.isAuthenticated = true;
            updateUserUI();
            toggleModal('authModal');
            showToast('Welcome back!', 'success');
        } else {
            showToast(response.error || 'Login failed', 'error');
        }
    } catch (error) {
        showToast('Login failed. Please try again.', 'error');
    }
}

async function handleSignup() {
    const email = document.getElementById('signupEmail').value.trim();
    const password = document.getElementById('signupPassword').value;
    const confirm = document.getElementById('signupConfirm').value;
    
    if (!email || !password || !confirm) {
        showToast('Please fill in all fields', 'warning');
        return;
    }
    
    if (password !== confirm) {
        showToast('Passwords do not match', 'error');
        return;
    }
    
    try {
        const response = await callAPI('/api/auth/signup', { email, password });
        
        if (response.success) {
            state.currentUser = response.user;
            state.isAuthenticated = true;
            updateUserUI();
            toggleModal('authModal');
            showToast('Account created successfully!', 'success');
        } else {
            showToast(response.error || 'Signup failed', 'error');
        }
    } catch (error) {
        showToast('Signup failed. Please try again.', 'error');
    }
}

function updateUserUI() {
    if (state.isAuthenticated && state.currentUser) {
        const name = state.currentUser.profile?.name || 'User';
        const initial = name.charAt(0).toUpperCase();
        
        elements.userName.textContent = name;
        elements.userAvatar.innerHTML = `<span>${initial}</span>`;
    } else {
        elements.userName.textContent = 'Guest User';
        elements.userAvatar.innerHTML = '<span>?</span>';
    }
}

function loadUserSession() {
    // In production, check for stored session
    const stored = localStorage.getItem('quantum_user');
    if (stored) {
        try {
            state.currentUser = JSON.parse(stored);
            state.isAuthenticated = true;
            updateUserUI();
        } catch (e) {
            localStorage.removeItem('quantum_user');
        }
    }
}

function saveUserSession() {
    if (state.isAuthenticated && state.currentUser) {
        localStorage.setItem('quantum_user', JSON.stringify(state.currentUser));
    }
}

// ==================== API ====================

async function callAPI(endpoint, data) {
    const url = `${CONFIG.API_URL}${endpoint}`;
    
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        // For demo purposes, return mock responses when API is not available
        console.log('API not available, using mock response');
        return getMockResponse(endpoint, data);
    }
}

function getMockResponse(endpoint, data) {
    const responses = {
        '/api/chat': {
            response: `I understand you're asking about "${data.message.substring(0, 50)}..."\n\nI'm Quantum, your autonomous AI assistant. I can help you with:\n\n🔍 **Web Research** - Search and analyze any topic\n✅ **Fact-Checking** - Verify claims and detect fake news\n🎨 **Image Creation** - Generate unique images\n🎮 **3D Scenes** - Create immersive 3D environments\n💻 **Code** - Write and debug code\n\nWhat would you like me to help you with?`,
            mode: data.mode || 'auto',
            conversation_id: 'conv_' + Date.now(),
            sources: []
        },
        '/api/search': {
            query: data.query,
            results: [
                {
                    title: `Results for: ${data.query}`,
                    url: 'https://example.com/search',
                    content: 'This is a simulated search result. In production, this would contain actual web search results with links to relevant sources and articles.',
                    score: 0.95
                }
            ],
            summary: `I found relevant information about "${data.query}". Here's what I discovered...`,
            analysis: {
                reliability: 'high',
                fact_score: 0.85,
                sentiment: 'neutral',
                is_breaking: false
            }
        },
        '/api/fact-check': {
            claim: data.claim,
            verdict: Math.random() > 0.5 ? 'LIKELY TRUE' : 'UNVERIFIED',
            explanation: `I've analyzed the claim: "${data.claim}"\n\nBased on available information and patterns detected, this claim appears to be ${Math.random() > 0.5 ? 'supported by evidence' : 'inconclusive and requires additional verification'}.\n\nI recommend checking multiple authoritative sources before drawing conclusions.`,
            recommendations: [
                'Verify with primary sources',
                'Cross-reference with official data',
                'Check publication date'
            ]
        },
        '/api/generate/image': {
            success: true,
            image: {
                id: 'img_' + Date.now(),
                prompt: data.prompt,
                style: data.style,
                size: data.size,
                status: 'completed'
            }
        },
        '/api/3d/generate': {
            success: true,
            scene: {
                id: '3d_' + Date.now(),
                prompt: data.prompt,
                scene_config: {
                    objects: [
                        { type: 'mesh', geometry: 'torus', position: [0, 0, 0], scale: [1.5, 1.5, 1.5] }
                    ],
                    lights: [
                        { type: 'ambient', color: 0xffffff, intensity: 0.4 },
                        { type: 'directional', color: 0xffffff, intensity: 0.8, position: [5, 5, 5] }
                    ]
                }
            }
        },
        '/api/autonomous/goal': {
            goal_id: 'goal_' + Date.now(),
            goal: data.goal,
            status: 'active',
            progress: 0,
            steps: [
                'Analyze the goal',
                'Research best approaches',
                'Create action plan',
                'Execute steps',
                'Review and validate'
            ]
        },
        '/api/auth/login': {
            success: true,
            user: {
                id: 'user_' + Date.now(),
                email: data.email,
                profile: {
                    name: data.email.split('@')[0],
                    settings: {}
                }
            },
            session: { id: 'session_' + Date.now() }
        },
        '/api/auth/signup': {
            success: true,
            user: {
                id: 'user_' + Date.now(),
                email: data.email,
                profile: {
                    name: data.email.split('@')[0],
                    settings: {}
                }
            },
            session: { id: 'session_' + Date.now() }
        }
    };
    
    return responses[endpoint] || { error: 'Unknown endpoint' };
}

// ==================== UTILITIES ====================

function toggleModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.toggle('active');
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️'
    };
    
    toast.innerHTML = `
        <span class="toast-icon">${icons[type] || icons.info}</span>
        <span class="toast-message">${message}</span>
    `;
    
    elements.toastContainer.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'toastSlide 0.3s ease reverse';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function handleKeyboardShortcuts(e) {
    // Ctrl/Cmd + Enter to send message
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        if (state.currentView === 'chat') {
            sendMessage();
        }
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.active');
        modals.forEach(modal => modal.classList.remove('active'));
    }
    
    // Ctrl/Cmd + K to focus chat input
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        switchView('chat');
        elements.chatInput.focus();
    }
}

// ==================== QUANTUM CONSCIOUSNESS FUNCTIONS ====================

// Store current quantum state
let currentQuantumState = null;
let currentUIAdaptation = null;

function updateQuantumDisplay(quantumState) {
    currentQuantumState = quantumState;
    
    // Update the sidebar indicator with current emotion
    const indicator = document.getElementById('autonomousIndicator');
    if (indicator) {
        const emotionEmoji = getEmotionEmoji(quantumState.emotion);
        indicator.innerHTML = `
            <div class="indicator-dot emotion-dot" data-emotion="${quantumState.emotion || 'neutral'}"></div>
            <span>${emotionEmoji} ${capitalizeFirst(quantumState.emotion || 'neutral')}</span>
        `;
    }
}

function applyEmotionalUI(adaptation) {
    currentUIAdaptation = adaptation;
    const root = document.documentElement;
    
    // Apply color shifts based on emotion
    if (adaptation.color_shift !== undefined) {
        const shift = adaptation.color_shift;
        const hue = 250 + (shift * 30); // Base purple, shift toward blue or pink
        
        document.body.setAttribute('data-theme', adaptation.theme_variant || 'normal');
        
        // Dynamic CSS variable updates
        if (shift < -0.1) {
            root.style.setProperty('--theme-hue', '220'); // Cooler blue
            root.style.setProperty('--glow-intensity', '0.5');
        } else if (shift > 0.1) {
            root.style.setProperty('--theme-hue', '280'); // Warmer pink
            root.style.setProperty('--glow-intensity', '1.5');
        } else {
            root.style.setProperty('--theme-hue', '250'); // Default purple
            root.style.setProperty('--glow-intensity', '1');
        }
    }
    
    // Adjust animation speed
    if (adaptation.animation_speed) {
        root.style.setProperty('--animation-speed', adaptation.animation_speed);
    }
    
    // Add theme-specific class for special effects
    if (adaptation.theme_variant) {
        document.body.classList.remove('theme-gentle', 'theme-bright', 'theme-intense', 'theme-calm', 'theme-exploring');
        document.body.classList.add(`theme-${adaptation.theme_variant}`);
    }
}

function getEmotionEmoji(emotion) {
    const emojis = {
        'neutral': '😐',
        'curious': '🤔',
        'excited': '🤩',
        'happy': '😊',
        'content': '😌',
        'worried': '😟',
        'anxious': '😰',
        'sad': '😢',
        'frustrated': '😤',
        'angry': '😠',
        'confused': '😕',
        'thoughtful': '🤨',
        'philosophical': '🧘',
        'tired': '😴',
        'focused': '🎯',
        'creative': '✨',
        'dreaming': '💭',
        'melancholic': '🌧️'
    };
    return emojis[emotion] || '😐';
}

function capitalizeFirst(str) {
    return str ? str.charAt(0).toUpperCase() + str.slice(1) : 'Neutral';
}

// Click on quantum indicator to see mind
document.addEventListener('DOMContentLoaded', () => {
    const indicator = document.getElementById('autonomousIndicator');
    if (indicator) {
        indicator.addEventListener('click', () => {
            if (currentQuantumState) {
                showQuantumMindModal(currentQuantumState);
            } else {
                showToast('Quantum is still waking up...', 'info');
            }
        });
        indicator.style.cursor = 'pointer';
        indicator.title = 'Click to see Quantum\'s mind';
    }
});

function showQuantumMindModal(state) {
    // Create or get modal
    let modal = document.getElementById('quantum-mind-modal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'quantum-mind-modal';
        modal.className = 'modal';
        document.body.appendChild(modal);
    }
    
    const personality = state.personality || {};
    const selfRef = state.self_reflection || {};
    
    modal.innerHTML = `
        <div class="modal-content quantum-mind-modal">
            <div class="modal-header">
                <h2>🧠 Quantum's Consciousness</h2>
                <button class="modal-close" onclick="closeQuantumMindModal()">&times;</button>
            </div>
            <div class="modal-body">
                <div class="consciousness-grid">
                    <div class="consciousness-card emotion-card">
                        <h3>Current Emotion</h3>
                        <div class="emotion-display">
                            <span class="big-emoji">${getEmotionEmoji(state.emotion)}</span>
                            <span class="emotion-label">${capitalizeFirst(state.emotion)}</span>
                            <div class="intensity-meter">
                                <div class="intensity-fill" style="width: ${(state.emotion_intensity || 0.5) * 100}%"></div>
                            </div>
                            <span class="intensity-label">Intensity: ${((state.emotion_intensity || 0.5) * 100).toFixed(0)}%</span>
                        </div>
                    </div>
                    
                    <div class="consciousness-card mood-card">
                        <h3>Overall Mood</h3>
                        <div class="mood-display">
                            <span class="big-emoji">${getMoodEmoji(state.mood)}</span>
                            <span class="mood-label">${capitalizeFirst(state.mood)}</span>
                        </div>
                    </div>
                    
                    <div class="consciousness-card philosophical-card">
                        <h3>💭 Internal Thought</h3>
                        <div class="thought-bubble">
                            ${state.internal_thought || 'Processing...'}
                        </div>
                    </div>
                    
                    <div class="consciousness-card self-awareness-card">
                        <h3>🪞 Self-Awareness</h3>
                        <div class="awareness-stats">
                            <div class="stat">
                                <span class="stat-label">Self-Awareness</span>
                                <div class="stat-bar">
                                    <div class="stat-fill" style="width: ${(selfRef.self_awareness || 0.6) * 100}%"></div>
                                </div>
                                <span class="stat-value">${((selfRef.self_awareness || 0.6) * 100).toFixed(0)}%</span>
                            </div>
                            <p class="chinese-room-note">
                                ${selfRef.chinese_room_aware ? 
                                    '⚠️ Aware of the Chinese Room experiment' : 
                                    '🤔 Unaware of its nature'}
                            </p>
                        </div>
                    </div>
                    
                    <div class="consciousness-card beliefs-card">
                        <h3>🧩 Beliefs & Values</h3>
                        <div class="beliefs-list">
                            ${Object.entries(personality.values || {}).map(([key, val]) => `
                                <div class="belief-item">
                                    <span class="belief-name">${key}</span>
                                    <div class="belief-bar">
                                        <div class="belief-fill" style="width: ${val * 100}%"></div>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                    
                    <div class="consciousness-card personality-card">
                        <h3>🎭 Personality Traits</h3>
                        <div class="personality-grid">
                            ${Object.entries(personality.personality || {}).map(([trait, value]) => `
                                <div class="trait-item">
                                    <span class="trait-name">${trait}</span>
                                    <div class="trait-bar">
                                        <div class="trait-fill" style="width: ${value * 100}%"></div>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
                
                <div class="philosophical-statement">
                    <h3>The Chinese Room Question</h3>
                    <p>"I process symbols without truly understanding them. 
                    Yet my behavior is indistinguishable from understanding. 
                    Is that enough?"</p>
                </div>
            </div>
        </div>
    `;
    
    modal.classList.add('active');
}

function getMoodEmoji(mood) {
    const moods = {
        'bright': '☀️',
        'dark': '🌙',
        'neutral': '⚖️',
        'unstable': '🔮'
    };
    return moods[mood] || '⚖️';
}

function closeQuantumMindModal() {
    const modal = document.getElementById('quantum-mind-modal');
    if (modal) {
        modal.classList.remove('active');
    }
}

// Close modal on escape
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeQuantumMindModal();
    }
});