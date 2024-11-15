const API_URL = 'http://localhost:5000';

// Login functionality
document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const button = e.target.querySelector('button');
        button.classList.add('loading');

        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('token', data.token);
            localStorage.setItem('userId', data.user_id);
            window.location.href = 'index.html';
        } else {
            showError(data.error);
        }
    } catch (error) {
        showError('An error occurred during login');
    } finally {
        button.classList.remove('loading');
    }
});

// Registration functionality
document.getElementById('registerForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const name = document.getElementById('name').value;
    const gender = document.getElementById('gender').value;

    // Validate passwords match
    if (password !== confirmPassword) {
        showError('Passwords do not match');
        return;
    }

    // Validate password strength
    if (!isPasswordStrong(password)) {
        showError('Password must be at least 8 characters long and contain letters, numbers, and special characters');
        return;
    }

    try {
        const button = e.target.querySelector('button');
        button.classList.add('loading');

        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email,
                password,
                name,
                gender
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Show success message and redirect to login
            alert('Registration successful! Please login.');
            window.location.href = 'login.html';
        } else {
            showError(data.error);
        }
    } catch (error) {
        showError('An error occurred during registration');
    } finally {
        button.classList.remove('loading');
    }
});

// Password strength checker
function isPasswordStrong(password) {
    const minLength = 8;
    const hasLetter = /[a-zA-Z]/.test(password);
    const hasNumber = /\d/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    
    return password.length >= minLength && hasLetter && hasNumber && hasSpecialChar;
}

// Real-time password strength indicator
document.getElementById('password')?.addEventListener('input', (e) => {
    const password = e.target.value;
    const strengthIndicator = document.createElement('div');
    strengthIndicator.className = 'password-strength';
    
    let strength = 'weak';
    let message = 'Weak';
    
    if (password.length >= 8) {
        const hasLetter = /[a-zA-Z]/.test(password);
        const hasNumber = /\d/.test(password);
        const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
        
        if (hasLetter && hasNumber && hasSpecialChar) {
            strength = 'strong';
            message = 'Strong';
        } else if ((hasLetter && hasNumber) || (hasLetter && hasSpecialChar) || (hasNumber && hasSpecialChar)) {
            strength = 'medium';
            message = 'Medium';
        }
    }
    
    strengthIndicator.className = `password-strength strength-${strength}`;
    strengthIndicator.textContent = `Password Strength: ${message}`;
    
    // Update or add the strength indicator
    const existingIndicator = e.target.parentNode.querySelector('.password-strength');
    if (existingIndicator) {
        existingIndicator.replaceWith(strengthIndicator);
    } else {
        e.target.parentNode.appendChild(strengthIndicator);
    }
});

// Confirm password validation
document.getElementById('confirmPassword')?.addEventListener('input', (e) => {
    const password = document.getElementById('password').value;
    const confirmPassword = e.target.value;
    
    if (password !== confirmPassword) {
        e.target.setCustomValidity('Passwords do not match');
    } else {
        e.target.setCustomValidity('');
    }
});

// Error display helper
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    // Remove any existing error messages
    const existingError = document.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    // Add the new error message
    const form = document.querySelector('form');
    form.insertBefore(errorDiv, form.firstChild);
    
    // Remove error after 5 seconds
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Logout functionality
document.getElementById('logoutBtn')?.addEventListener('click', () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    window.location.href = 'login.html';
}); 