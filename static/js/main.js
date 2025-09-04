// // static/js/main.js

// document.addEventListener('DOMContentLoaded', function() {
//     // Mobile menu functionality
//     const mobileMenuButton = document.querySelector('.mobile-menu-button');
//     const mobileMenu = document.querySelector('.mobile-menu');
    
//     if (mobileMenuButton && mobileMenu) {
//         mobileMenuButton.addEventListener('click', function() {
//             mobileMenu.classList.toggle('hidden');
            
//             // Toggle hamburger icon
//             const icon = mobileMenuButton.querySelector('svg');
//             if (mobileMenu.classList.contains('hidden')) {
//                 icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />';
//             } else {
//                 icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />';
//             }
//         });
//     }
    
//     // Smooth scrolling for anchor links
//     document.querySelectorAll('a[href^="#"]').forEach(anchor => {
//         anchor.addEventListener('click', function(e) {
//             e.preventDefault();
//             const target = document.querySelector(this.getAttribute('href'));
//             if (target) {
//                 target.scrollIntoView({
//                     behavior: 'smooth',
//                     block: 'start'
//                 });
//             }
//         });
//     });
    
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

document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu functionality
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
            
            // Toggle hamburger icon
            const icon = mobileMenuButton.querySelector('svg');
            if (mobileMenu.classList.contains('hidden')) {
                icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />';
            } else {
                icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />';
            }
        });
    }
    
    // FAQ functionality
    window.toggleFAQ = function(button) {
        const content = button.nextElementSibling;
        const icon = button.querySelector('.faq-icon');
        const allFAQs = document.querySelectorAll('.faq-content');
        const allIcons = document.querySelectorAll('.faq-icon');
        
        // Close all other FAQs
        allFAQs.forEach((faq, index) => {
            if (faq !== content) {
                faq.classList.add('hidden');
                allIcons[index].classList.remove('rotate-180');
            }
        });
        
        // Toggle current FAQ
        content.classList.toggle('hidden');
        icon.classList.toggle('rotate-180');
    };
    
    // Smooth scrolling for navigation links with offset for fixed header
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerOffset = 80; // Account for fixed header
                const elementPosition = target.offsetTop;
                const offsetPosition = elementPosition - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
                
                // Close mobile menu if open
                const mobileMenu = document.querySelector('.mobile-menu');
                if (mobileMenu && !mobileMenu.classList.contains('hidden')) {
                    mobileMenu.classList.add('hidden');
                    // Reset hamburger icon
                    const icon = document.querySelector('.mobile-menu-button svg');
                    if (icon) {
                        icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />';
                    }
                }
            }
        });
    });
    
    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
            }
        });
    }, observerOptions);
    
    // Observe elements that should animate on scroll
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
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
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            const requiredFields = form.querySelectorAll('[required]');
            
            requiredFields.forEach(field => {
                const value = field.value;
                const fieldType = field.type;
                let fieldValid = true;
                
                // Remove existing error styles
                field.classList.remove('border-red-500', 'focus:border-red-500');
                
                if (fieldType === 'email') {
                    fieldValid = validateEmail(value);
                } else {
                    fieldValid = validateRequired(value);
                }
                
                if (!fieldValid) {
                    field.classList.add('border-red-500', 'focus:border-red-500');
                    isValid = false;
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                // Show error message or handle validation failure
                showNotification('Please fill in all required fields correctly.', 'error');
            }
        });
    });
    
    // Notification system
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg max-w-sm transition-all duration-300 transform translate-x-full`;
        
        const typeClasses = {
            success: 'bg-green-500 text-white',
            error: 'bg-red-500 text-white',
            warning: 'bg-yellow-500 text-white',
            info: 'bg-blue-500 text-white'
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
            notification.classList.remove('translate-x-full');
        }, 10);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            notification.classList.add('translate-x-full');
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
        button.innerHTML = button.dataset.originalText || 'Submit';
        button.disabled = false;
    }
    
    // Expose loading helpers globally
    window.showLoading = showLoading;
    window.hideLoading = hideLoading;
    
    // CSRF token helper for AJAX requests
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Set up CSRF token for all AJAX requests
    const csrftoken = getCookie('csrftoken');
    if (csrftoken) {
        // For jQuery if you're using it
        if (typeof $ !== 'undefined') {
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });
        }
    }
    
    // Expose CSRF token helper
    window.getCSRFToken = () => csrftoken;
    
    // Utility function for making API calls
    async function apiCall(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
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
            console.error('API call failed:', error);
            showNotification('An error occurred. Please try again.', 'error');
            throw error;
        }
    }
    
    // Expose API helper globally
    window.apiCall = apiCall;
    
    // Initialize any third-party libraries or additional functionality
    console.log('Docent frontend initialized successfully');
});