// --- Popup Login/Signup Modal Switch ---
document.addEventListener("DOMContentLoaded", function () {
  // Switch to signup form when clicking Sign up
  const signupLink = document.querySelector(".signup-link");
  if (signupLink) {
    signupLink.addEventListener("click", function (e) {
      e.preventDefault();
      showSignupForm();
    });
  }
});

function showSignupForm() {
  const modal = document.querySelector(".login-modal");
  if (!modal) return;
  modal.innerHTML = `
        <div class="login-header">
            <button class="close-btn" onclick="closeLogin()">&times;</button>
            <h2 class="login-title">Create Account</h2>
            <p class="login-subtitle">Sign up to get started</p>
        </div>
        <div class="login-body">
            <button class="google-btn" onclick="signInWithGoogle()">
                <svg class="google-icon" viewBox="0 0 24 24">
                    <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                    <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                    <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                    <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                </svg>
                Continue with Google
            </button>
            <div class="divider">
                <span>or continue with email</span>
            </div>
            <form class="login-form" method="post" action="/register">
                <input type="hidden" name="csrfmiddlewaretoken" value="${window.getCSRFToken ? window.getCSRFToken() : ''}">
                <div class="form-group">
                    <label class="form-label">Username</label>
                    <input type="text" name="username" class="form-input" placeholder="Enter a username" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Email</label>
                    <input type="email" name="email" class="form-input" placeholder="Enter your email" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Password</label>
                    <input type="password" name="password" class="form-input" placeholder="Create a password" required>
                </div>
                <button type="submit" class="login-btn">Sign Up</button>
            </form>
            <div class="login-footer">
                <p style="margin: 0; color: #6b7280; font-size: 14px;">
                    Already have an account?
                    <a href="#" class="login-link">Sign in</a>
                </p>
            </div>
        </div>
    `;
  // Add event for switching back to login
  const loginLink = modal.querySelector(".login-link");
  if (loginLink) {
    loginLink.addEventListener("click", function (e) {
      e.preventDefault();
      showLoginForm();
    });
  }
}

function showLoginForm() {
  const modal = document.querySelector(".login-modal");
  if (!modal) return;
  modal.innerHTML = `
    <div class="login-header">
      <button class="close-btn" onclick="closeLogin()">&times;</button>
      <h2 class="login-title">Welcome Back</h2>
      <p class="login-subtitle">Sign in to access your dashboard</p>
    </div>
    <div class="login-body">
      <button class="google-btn" onclick="signInWithGoogle()">
        <svg class="google-icon" viewBox="0 0 24 24">
          <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
          <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
          <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
          <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
        </svg>
        Continue with Google
      </button>
      <div class="divider">
        <span>or continue with email</span>
      </div>
      <form class="login-form" method="post" action="/login">
        <input type="hidden" name="csrfmiddlewaretoken" value="${window.getCSRFToken ? window.getCSRFToken() : ''}">
        <div class="form-group">
          <label class="form-label">Email</label>
          <input type="email" name="email" class="form-input" placeholder="Enter your email" required>
        </div>
        <div class="form-group">
          <label class="form-label">Password</label>
          <input type="password" name="password" class="form-input" placeholder="Enter your password" required>
        </div>
        <button type="submit" class="login-btn">Sign In</button>
      </form>
      <div class="login-footer">
        <p style="margin: 0; color: #6b7280; font-size: 14px;">
          Don't have an account? 
          <a href="#" class="signup-link">Sign up</a>
        </p>
      </div>
    </div>
  `;
  // Add event for switching to signup
  const signupLink = modal.querySelector(".signup-link");
  if (signupLink) {
    signupLink.addEventListener("click", function (e) {
      e.preventDefault();
      showSignupForm();
    });
  }
}
// Login Popup Functions
function openLogin() {
  const overlay = document.getElementById("loginOverlay");
  overlay.style.display = "flex";
  setTimeout(() => {
    overlay.classList.add("active");
  }, 10);
  document.body.style.overflow = "hidden";
}

function closeLogin() {
  const overlay = document.getElementById("loginOverlay");
  overlay.classList.remove("active");
  setTimeout(() => {
    overlay.style.display = "none";
    document.body.style.overflow = "auto";
  }, 300);
}

// Close on overlay click
document.addEventListener("DOMContentLoaded", function () {
  const overlay = document.getElementById("loginOverlay");
  if (overlay) {
    overlay.addEventListener("click", function (e) {
      if (e.target === this) {
        closeLogin();
      }
    });
  }
});

// Close on Escape key
document.addEventListener("keydown", function (e) {
  if (e.key === "Escape") {
    closeLogin();
  }
});


// // static/js/main.js

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute("href"));
    if (target) {
      target.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  });
});

//     // Intersection Observer for animations
//     const observerOptions = {
//         threshold: 0.1,
//         rootMargin: '0px 0px -50px 0px'
//     };

//     const observer = new IntersectionObserver(function(entries) {
//         entries.forEach(entry => {
//             if (entry.isIntersecting) {
//                 entry.target.classList.add('animate-fade-in');
//             }
//         });
//     }, observerOptions);

//     // Observe elements that should animate on scroll
//     document.querySelectorAll('.animate-on-scroll').forEach(el => {
//         observer.observe(el);
//     });

//     // Form validation helpers
//     function validateEmail(email) {
//         const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
//         return re.test(email);
//     }

//     function validateRequired(value) {
//         return value.trim().length > 0;
//     }

//     // Generic form validation
//     document.querySelectorAll('form').forEach(form => {
//         form.addEventListener('submit', function(e) {
//             let isValid = true;
//             const requiredFields = form.querySelectorAll('[required]');

//             requiredFields.forEach(field => {
//                 const value = field.value;
//                 const fieldType = field.type;
//                 let fieldValid = true;

//                 // Remove existing error styles
//                 field.classList.remove('border-red-500', 'focus:border-red-500');

//                 if (fieldType === 'email') {
//                     fieldValid = validateEmail(value);
//                 } else {
//                     fieldValid = validateRequired(value);
//                 }

//                 if (!fieldValid) {
//                     field.classList.add('border-red-500', 'focus:border-red-500');
//                     isValid = false;
//                 }
//             });

//             if (!isValid) {
//                 e.preventDefault();
//                 // Show error message or handle validation failure
//                 showNotification('Please fill in all required fields correctly.', 'error');
//             }
//         });
//     });

//     // Notification system
//     function showNotification(message, type = 'info') {
//         const notification = document.createElement('div');
//         notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg max-w-sm transition-all duration-300 transform translate-x-full`;

//         const typeClasses = {
//             success: 'bg-green-500 text-white',
//             error: 'bg-red-500 text-white',
//             warning: 'bg-yellow-500 text-white',
//             info: 'bg-blue-500 text-white'
//         };

//         notification.className += ` ${typeClasses[type] || typeClasses.info}`;
//         notification.innerHTML = `
//             <div class="flex items-center justify-between">
//                 <span>${message}</span>
//                 <button class="ml-4 text-white hover:text-gray-200" onclick="this.parentElement.parentElement.remove()">
//                     <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//                         <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
//                     </svg>
//                 </button>
//             </div>
//         `;

//         document.body.appendChild(notification);

//         // Animate in
//         setTimeout(() => {
//             notification.classList.remove('translate-x-full');
//         }, 10);

//         // Auto remove after 5 seconds
//         setTimeout(() => {
//             notification.classList.add('translate-x-full');
//             setTimeout(() => {
//                 if (notification.parentNode) {
//                     notification.parentNode.removeChild(notification);
//                 }
//             }, 300);
//         }, 5000);
//     }

//     // Expose notification function globally
//     window.showNotification = showNotification;

//     // Loading state helpers
//     function showLoading(button) {
//         const originalText = button.innerHTML;
//         button.innerHTML = `
//             <div class="flex items-center">
//                 <div class="spinner mr-2"></div>
//                 Loading...
//             </div>
//         `;
//         button.disabled = true;
//         button.dataset.originalText = originalText;
//     }

//     function hideLoading(button) {
//         button.innerHTML = button.dataset.originalText || 'Submit';
//         button.disabled = false;
//     }

//     // Expose loading helpers globally
//     window.showLoading = showLoading;
//     window.hideLoading = hideLoading;

//     // CSRF token helper for AJAX requests
//     function getCookie(name) {
//         let cookieValue = null;
//         if (document.cookie && document.cookie !== '') {
//             const cookies = document.cookie.split(';');
//             for (let i = 0; i < cookies.length; i++) {
//                 const cookie = cookies[i].trim();
//                 if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                     break;
//                 }
//             }
//         }
//         return cookieValue;
//     }

//     // Set up CSRF token for all AJAX requests
//     const csrftoken = getCookie('csrftoken');
//     if (csrftoken) {
//         // For jQuery if you're using it
//         if (typeof $ !== 'undefined') {
//             $.ajaxSetup({
//                 beforeSend: function(xhr, settings) {
//                     if (!this.crossDomain) {
//                         xhr.setRequestHeader("X-CSRFToken", csrftoken);
//                     }
//                 }
//             });
//         }
//     }

//     // Expose CSRF token helper
//     window.getCSRFToken = () => csrftoken;

//     // Utility function for making API calls
//     async function apiCall(url, options = {}) {
//         const defaultOptions = {
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': csrftoken,
//             },
//         };

//         const mergedOptions = {
//             ...defaultOptions,
//             ...options,
//             headers: {
//                 ...defaultOptions.headers,
//                 ...options.headers,
//             },
//         };

//         try {
//             const response = await fetch(url, mergedOptions);
//             if (!response.ok) {
//                 throw new Error(`HTTP error! status: ${response.status}`);
//             }
//             return await response.json();
//         } catch (error) {
//             console.error('API call failed:', error);
//             showNotification('An error occurred. Please try again.', 'error');
//             throw error;
//         }
//     }

//     // Expose API helper globally
//     window.apiCall = apiCall;

//     // Initialize any third-party libraries or additional functionality
//     console.log('Docent frontend initialized successfully');
// });

// static/js/main.js

document.addEventListener("DOMContentLoaded", function () {
  // Mobile menu functionality
  const mobileMenuButton = document.querySelector(".mobile-menu-button");
  const mobileMenu = document.querySelector(".mobile-menu");

  if (mobileMenuButton && mobileMenu) {
    mobileMenuButton.addEventListener("click", function () {
      mobileMenu.classList.toggle("hidden");

      // Toggle hamburger icon
      const icon = mobileMenuButton.querySelector("svg");
      if (mobileMenu.classList.contains("hidden")) {
        icon.innerHTML =
          '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />';
      } else {
        icon.innerHTML =
          '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />';
      }
    });
  }

  // FAQ functionality
  window.toggleFAQ = function (button) {
    const content = button.nextElementSibling;
    const icon = button.querySelector(".faq-icon");
    const allFAQs = document.querySelectorAll(".faq-content");
    const allIcons = document.querySelectorAll(".faq-icon");

    // Close all other FAQs
    allFAQs.forEach((faq, index) => {
      if (faq !== content) {
        faq.classList.add("hidden");
        allIcons[index].classList.remove("rotate-180");
      }
    });

    // Toggle current FAQ
    content.classList.toggle("hidden");
    icon.classList.toggle("rotate-180");
  };

  // Smooth scrolling for navigation links with offset for fixed header
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        const headerOffset = 80; // Account for fixed header
        const elementPosition = target.offsetTop;
        const offsetPosition = elementPosition - headerOffset;

        const middlePosition =
          absoluteElementTop -
          window.innerHeight / 2 +
          target.offsetHeight / 2 -
          headerOffset;

        window.scrollTo({
          top: offsetPosition,
          behavior: "smooth",
        });

        // Close mobile menu if open
        const mobileMenu = document.querySelector(".mobile-menu");
        if (mobileMenu && !mobileMenu.classList.contains("hidden")) {
          mobileMenu.classList.add("hidden");
          // Reset hamburger icon
          const icon = document.querySelector(".mobile-menu-button svg");
          if (icon) {
            icon.innerHTML =
              '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />';
          }
        }
      }
    });
  });

  // Intersection Observer for animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  };

  const observer = new IntersectionObserver(function (entries) {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("animate-fade-in");
      }
    });
  }, observerOptions);

  // Observe elements that should animate on scroll
  document.querySelectorAll(".animate-on-scroll").forEach((el) => {
    observer.observe(el);
  });

  // Form validation helpers
  function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  }

  function validateRequired(value) {
    return value.trim().length > 0;
  }

  // Generic form validation
  document.querySelectorAll("form").forEach((form) => {
    form.addEventListener("submit", function (e) {
      let isValid = true;
      const requiredFields = form.querySelectorAll("[required]");

      requiredFields.forEach((field) => {
        const value = field.value;
        const fieldType = field.type;
        let fieldValid = true;

        // Remove existing error styles
        field.classList.remove("border-red-500", "focus:border-red-500");

        if (fieldType === "email") {
          fieldValid = validateEmail(value);
        } else {
          fieldValid = validateRequired(value);
        }

        if (!fieldValid) {
          field.classList.add("border-red-500", "focus:border-red-500");
          isValid = false;
        }
      });

      if (!isValid) {
        e.preventDefault();
        // Show error message or handle validation failure
        showNotification(
          "Please fill in all required fields correctly.",
          "error"
        );
      }
    });
  });

  // Notification system
  function showNotification(message, type = "info") {
    const notification = document.createElement("div");
    notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg max-w-sm transition-all duration-300 transform translate-x-full`;

    const typeClasses = {
      success: "bg-green-500 text-white",
      error: "bg-red-500 text-white",
      warning: "bg-yellow-500 text-white",
      info: "bg-blue-500 text-white",
    };

    notification.className += ` ${typeClasses[type] || typeClasses.info}`;
    notification.innerHTML = `
            <div class="flex items-center justify-between">
                <span>${message}</span>
                <button class="ml-4 text-white hover:text-gray-200" onclick="this.parentElement.parentElement.remove()">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                </button>
            </div>
        `;

    document.body.appendChild(notification);

    // Animate in
    setTimeout(() => {
      notification.classList.remove("translate-x-full");
    }, 10);

    // Auto remove after 5 seconds
    setTimeout(() => {
      notification.classList.add("translate-x-full");
      setTimeout(() => {
        if (notification.parentNode) {
          notification.parentNode.removeChild(notification);
        }
      }, 300);
    }, 5000);
  }

  // Expose notification function globally
  window.showNotification = showNotification;

  // Loading state helpers
  function showLoading(button) {
    const originalText = button.innerHTML;
    button.innerHTML = `
            <div class="flex items-center">
                <div class="spinner mr-2"></div>
                Loading...
            </div>
        `;
    button.disabled = true;
    button.dataset.originalText = originalText;
  }

  function hideLoading(button) {
    button.innerHTML = button.dataset.originalText || "Submit";
    button.disabled = false;
  }

  // Expose loading helpers globally
  window.showLoading = showLoading;
  window.hideLoading = hideLoading;

  // CSRF token helper for AJAX requests
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // Set up CSRF token for all AJAX requests
  const csrftoken = getCookie("csrftoken");
  if (csrftoken) {
    // For jQuery if you're using it
    if (typeof $ !== "undefined") {
      $.ajaxSetup({
        beforeSend: function (xhr, settings) {
          if (!this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
        },
      });
    }
  }

  // Expose CSRF token helper
  window.getCSRFToken = () => csrftoken;

  // Utility function for making API calls
  async function apiCall(url, options = {}) {
    const defaultOptions = {
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
    };

    const mergedOptions = {
      ...defaultOptions,
      ...options,
      headers: {
        ...defaultOptions.headers,
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, mergedOptions);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error("API call failed:", error);
      showNotification("An error occurred. Please try again.", "error");
      throw error;
    }
  }

  // Expose API helper globally
  window.apiCall = apiCall;

  // Initialize any third-party libraries or additional functionality
  console.log("Docent frontend initialized successfully");
});