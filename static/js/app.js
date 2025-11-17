// Dropdown functionality
function toggleDropdown() {
  const dropdown = document.getElementById('dropdownMenu');
  const profile = document.querySelector('.user-profile');

  dropdown.classList.toggle('active');
  profile.classList.toggle('dropdown-active');
}

// Close dropdown when clicking outside
document.addEventListener('click', function (event) {
  const dropdown = document.getElementById('dropdownMenu');
  const profile = document.querySelector('.user-profile');

  if (!profile.contains(event.target)) {
    dropdown.classList.remove('active');
    profile.classList.remove('dropdown-active');
  }
});

// Logout function
function logout() {
  window.location.href = "/logout";
}

// Check if user session is still valid
function checkSession() {
  fetch('/dashboard', {
    method: 'GET',
    headers: {
      'Cache-Control': 'no-cache',
      'Pragma': 'no-cache'
    }
  })
    .then(response => {
      if (response.redirected && response.url.includes('/login')) {
        // Session expired, redirect to login
        window.location.href = "/";
      }
    })
    .catch(error => {
      console.log('Session check failed:', error);
    });
}

// Toast auto-remove functionality
function initToasts() {
  // Close button functionality
  document.querySelectorAll('.toast-close').forEach(btn => {
    btn.addEventListener('click', function () {
      const toast = this.parentElement;
      toast.style.display = 'none';
    });
  });

  // Auto hide after 5 seconds
  setTimeout(() => {
    document.querySelectorAll('.toast').forEach(toast => {
      toast.style.display = 'none';
    });
  }, 5000);
}

// Tab switching functionality for login/register
function switchTab(tabName) {
  const tabs = document.querySelectorAll('.tab');
  const contents = document.querySelectorAll('.form-content');

  tabs.forEach(tab => tab.classList.remove('active'));
  contents.forEach(content => content.classList.remove('active'));

  event.target.classList.add('active');
  document.getElementById(tabName).classList.add('active');

  const title = document.getElementById('sideTitle');
  const description = document.getElementById('sideDescription');

  if (tabName === 'register') {
    title.textContent = 'Join Our Community';
    description.textContent = 'Create your account and start your journey with us. Discover endless possibilities ahead.';
  } else {
    title.textContent = 'Welcome Back!';
    description.textContent = 'Step into your account and unlock a world of possibilities. Your journey continues here.';
  }
}

// OTP input handling
function handleOTPInput(event) {
  const input = event.target;
  const value = input.value;

  // Only allow numbers
  if (!/^\d*$/.test(value)) {
    input.value = value.replace(/\D/g, '');
    return;
  }

  // Move to next input if current is filled
  if (value.length === 1) {
    const nextInput = input.nextElementSibling;
    if (nextInput && nextInput.classList.contains('otp-input')) {
      nextInput.focus();
    }
  }

  // Move to previous input if backspace pressed and current is empty
  if (event.key === 'Backspace' && value.length === 0) {
    const prevInput = input.previousElementSibling;
    if (prevInput && prevInput.classList.contains('otp-input')) {
      prevInput.focus();
    }
  }
}

// Initialize all functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function () {
  // Initialize toasts
  initToasts();

  // Only run session checks on dashboard pages
  if (window.location.pathname === '/dashboard' || document.querySelector('.user-profile')) {
    // Check session on page load
    checkSession();

    // Check session when page becomes visible (user comes back from another tab)
    document.addEventListener('visibilitychange', function () {
      if (!document.hidden) {
        checkSession();
      }
    });

    // Check session periodically (every 2 minutes)
    setInterval(checkSession, 120000);
  }

  // Add enter key support for OTP inputs
  const otpInputs = document.querySelectorAll('.otp-input');
  if (otpInputs.length > 0) {
    otpInputs.forEach(input => {
      input.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
          event.preventDefault();
          // Find and submit the form
          const form = this.closest('form');
          if (form) {
            form.submit();
          }
        }
      });
    });
  }

  // Add loading states to buttons
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    form.addEventListener('submit', function () {
      const submitBtn = this.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.innerHTML = '<span>Loading...</span>';
        submitBtn.disabled = true;
      }
    });
  });
});

// Social login button handlers
function handleGoogleLogin() {
  alert('Google login would be implemented here');
  
}

function handleFacebookLogin() {
  alert('Facebook login would be implemented here');
  
}

// Add social login event listeners
document.addEventListener('DOMContentLoaded', function () {
  const googleButtons = document.querySelectorAll('.social-btn');
  googleButtons.forEach(btn => {
    if (btn.textContent.includes('Google')) {
      btn.addEventListener('click', handleGoogleLogin);
    } else if (btn.textContent.includes('Facebook')) {
      btn.addEventListener('click', handleFacebookLogin);
    }
  });
});

// Utility function to show custom toasts (for future use)
function showToast(message, type = 'success') {
  const toastContainer = document.getElementById('toast-container');
  if (!toastContainer) return;

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `
        <span>${message}</span>
        <button class="toast-close">&times;</button>
    `;

  toastContainer.appendChild(toast);

  // Add close functionality
  const closeBtn = toast.querySelector('.toast-close');
  closeBtn.addEventListener('click', () => {
    toast.style.display = 'none';
  });

  // Auto remove after 5 seconds
  setTimeout(() => {
    if (toast.parentElement) {
      toast.style.display = 'none';
    }
  }, 5000);
}

// Form validation enhancement
function enhanceFormValidation() {
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    const inputs = form.querySelectorAll('input[required]');
    inputs.forEach(input => {
      input.addEventListener('invalid', function () {
        this.style.borderColor = '#ef4444';
      });

      input.addEventListener('input', function () {
        if (this.checkValidity()) {
          this.style.borderColor = '#8b5cf6';
        }
      });
    });
  });
}

// Initialize form validation when DOM is loaded
document.addEventListener('DOMContentLoaded', enhanceFormValidation);

// Password strength indicator (for register form)
function initPasswordStrength() {
  const passwordInput = document.querySelector('input[name="password"]');
  if (!passwordInput) return;

  passwordInput.addEventListener('input', function () {
    const password = this.value;
    const strengthIndicator = document.getElementById('password-strength');

    if (!strengthIndicator) return;

    let strength = 0;
    let feedback = '';

    if (password.length >= 8) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;

    switch (strength) {
      case 0:
      case 1:
        feedback = 'Very Weak';
        strengthIndicator.style.color = '#ef4444';
        break;
      case 2:
        feedback = 'Weak';
        strengthIndicator.style.color = '#f59e0b';
        break;
      case 3:
        feedback = 'Medium';
        strengthIndicator.style.color = '#eab308';
        break;
      case 4:
        feedback = 'Strong';
        strengthIndicator.style.color = '#84cc16';
        break;
      case 5:
        feedback = 'Very Strong';
        strengthIndicator.style.color = '#10b981';
        break;
    }

    strengthIndicator.textContent = feedback;
  });
}

// Initialize password strength when DOM is loaded
document.addEventListener('DOMContentLoaded', initPasswordStrength);