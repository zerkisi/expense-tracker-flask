function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");

    if (document.body.classList.contains("dark-mode")) {
        localStorage.setItem("theme", "dark");
    } else {
        localStorage.setItem("theme", "light");
    }
}

window.onload = function () {
    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
    }
};

function checkPasswordStrength() {
    const password = document.getElementById("password").value;
    const bar = document.getElementById("strength-bar");
    const text = document.getElementById("strength-text");

    if (!bar || !text) {
        return;
    }

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