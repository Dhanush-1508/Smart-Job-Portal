const tabBtns = document.querySelectorAll('.tab-btn');
const loginForm = document.getElementById('loginForm');
const signupForm = document.getElementById('signupForm');
const pageTitle = document.getElementById('pageTitle');
const pageSubtitle = document.getElementById('pageSubtitle');

function switchTab(tab) {
    tabBtns.forEach(b => {
        b.classList.toggle('active', b.dataset.tab === tab);
    });

    if (tab === 'login') {
        loginForm.style.display = 'flex';
        signupForm.style.display = 'none';
        if (pageTitle) pageTitle.textContent = 'Welcome Back';
        if (pageSubtitle) pageSubtitle.textContent = 'Sign in to continue to HireHub';
    } else {
        loginForm.style.display = 'none';
        signupForm.style.display = 'flex';
        if (pageTitle) pageTitle.textContent = 'Create Account';
        if (pageSubtitle) pageSubtitle.textContent = 'Join HireHub and find your dream job';
    }
}

// Tab click
tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        switchTab(btn.dataset.tab);
    });
});

// Open correct tab after Django error
const activeTab = document.body.dataset.activeTab;
if (activeTab === 'signup') {
    switchTab('signup');
} else {
    switchTab('login');
}

// Password show/hide
document.querySelectorAll('.toggle-pass').forEach(btn => {
    btn.addEventListener('click', () => {
        const input = document.getElementById(btn.dataset.target);
        const icon = btn.querySelector('i');
        if (!input || !icon) return;

        if (input.type === 'password') {
            input.type = 'text';
            icon.classList.replace('bi-eye', 'bi-eye-slash');
        } else {
            input.type = 'password';
            icon.classList.replace('bi-eye-slash', 'bi-eye');
        }
    });
});