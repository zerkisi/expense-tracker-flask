function checkPasswordStrength() {
    const passwordInput = document.getElementById("password");
    const bar = document.getElementById("strength-bar");
    const text = document.getElementById("strength-text");

    if (!passwordInput || !bar || !text) {
        return;
    }

    const password = passwordInput.value;
    let score = 0;

    if (password.length >= 8) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[a-z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) score++;

    if (score <= 2) {
        bar.style.width = "33%";
        bar.style.background = "#ef4444";
        text.innerText = "Weak password";
    } else if (score <= 4) {
        bar.style.width = "66%";
        bar.style.background = "#f59e0b";
        text.innerText = "Medium password";
    } else {
        bar.style.width = "100%";
        bar.style.background = "#22c55e";
        text.innerText = "Strong password";
    }
}
