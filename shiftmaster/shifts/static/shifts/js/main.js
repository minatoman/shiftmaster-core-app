// ShiftMaster Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeApp();
});

function initializeApp() {
    // PWA Installation
    initializePWA();
    
    // Mobile optimizations
    initializeMobileOptimizations();
    
    // Form enhancements
    initializeFormEnhancements();
    
    // Notifications
    initializeNotifications();
    
    // Theme handling
    initializeTheme();
}

// PWA Installation
function initializePWA() {
    let deferredPrompt;
    
    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
        showInstallBanner();
    });
    
    function showInstallBanner() {
        const banner = document.createElement('div');
        banner.className = 'pwa-install-banner';
        banner.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <strong>ShiftMasterをインストール</strong>
                    <br><small>ホーム画面に追加してアプリのように使用</small>
                </div>
                <div>
                    <button class="btn btn-light btn-sm me-2" id="installBtn">インストール</button>
                    <button class="btn btn-outline-light btn-sm" id="dismissBtn">×</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(banner);
        
        setTimeout(() => {
            banner.classList.add('show');
        }, 1000);
        
        document.getElementById('installBtn').addEventListener('click', () => {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then((choiceResult) => {
                    deferredPrompt = null;
                    banner.remove();
                });
            }
        });
        
        document.getElementById('dismissBtn').addEventListener('click', () => {
            banner.remove();
        });
    }
}

// Mobile optimizations
function initializeMobileOptimizations() {
    // Touch event handling
    if ('ontouchstart' in window) {
        document.body.classList.add('touch-device');
    }
    
    // Viewport height fix for mobile browsers
    function setVH() {
        let vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
    }
    
    setVH();
    window.addEventListener('resize', setVH);
    window.addEventListener('orientationchange', setVH);
    
    // Prevent zoom on input focus (iOS)
    const inputs = document.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            if (window.DevicePixelRatio > 1) {
                input.style.fontSize = '16px';
            }
        });
    });
}

// Form enhancements
function initializeFormEnhancements() {
    // Auto-resize textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', autoResize);
        autoResize.call(textarea);
    });
    
    function autoResize() {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    }
    
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // Date input enhancements
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        // Set min date to today if not already set
        if (!input.min) {
            input.min = new Date().toISOString().split('T')[0];
        }
    });
}

// Notifications
function initializeNotifications() {
    // Request notification permission
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
    }
    
    // Auto-dismiss alerts
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentNode) {
                alert.classList.add('fade');
                setTimeout(() => {
                    alert.remove();
                }, 300);
            }
        }, 5000);
    });
}

// Theme handling
function initializeTheme() {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
    
    function applyTheme(isDark) {
        document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
    }
    
    applyTheme(prefersDark.matches);
    prefersDark.addListener(e => applyTheme(e.matches));
}

// Utility functions
const Utils = {
    // Debounce function
    debounce: function(func, delay) {
        let timeoutId;
        return function (...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => func.apply(this, args), delay);
        };
    },
    
    // Format time
    formatTime: function(date) {
        return date.toLocaleTimeString('ja-JP', {
            hour: '2-digit',
            minute: '2-digit'
        });
    },
    
    // Format date
    formatDate: function(date) {
        return date.toLocaleDateString('ja-JP', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            weekday: 'long'
        });
    },
    
    // Show loading
    showLoading: function(element) {
        const spinner = document.createElement('div');
        spinner.className = 'spinner';
        spinner.setAttribute('data-loading', 'true');
        element.appendChild(spinner);
    },
    
    // Hide loading
    hideLoading: function(element) {
        const spinner = element.querySelector('[data-loading="true"]');
        if (spinner) {
            spinner.remove();
        }
    },
    
    // Show notification
    showNotification: function(title, message, type = 'info') {
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification(title, {
                body: message,
                icon: '/static/shifts/img/icon-192x192.png',
                badge: '/static/shifts/img/icon-72x72.png'
            });
        }
        
        // Fallback to in-app notification
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 300px;';
        notification.innerHTML = `
            <strong>${title}</strong><br>${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }
};

// Service Worker registration
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/shifts/js/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// Export utils for use in other scripts
window.ShiftMasterUtils = Utils;
