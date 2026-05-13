// Toast Notification System
// Teal background, white text, appears in the site (not browser alert)

function showToast(message, type = 'success', duration = 3000) {
    // Remove any existing toasts
    const existingToasts = document.querySelectorAll('.toast-notification');
    existingToasts.forEach(toast => toast.remove());
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = 'toast-notification fixed top-20 right-4 z-[9999] animate-slide-in';
    
    // Set colors based on type
    let bgColor, icon;
    switch(type) {
        case 'success':
            bgColor = 'bg-gradient-to-r from-teal-700 to-teal-600';
            icon = '✓';
            break;
        case 'error':
            bgColor = 'bg-gradient-to-r from-red-600 to-red-500';
            icon = '✕';
            break;
        case 'warning':
            bgColor = 'bg-gradient-to-r from-orange-600 to-orange-500';
            icon = '⚠';
            break;
        case 'info':
            bgColor = 'bg-gradient-to-r from-blue-600 to-blue-500';
            icon = 'ℹ';
            break;
        default:
            bgColor = 'bg-gradient-to-r from-teal-700 to-teal-600';
            icon = '✓';
    }
    
    toast.innerHTML = `
        <div class="${bgColor} text-white px-6 py-4 rounded-lg shadow-2xl flex items-center gap-3 min-w-[300px] max-w-[500px]">
            <span class="text-2xl">${icon}</span>
            <span class="flex-1 font-medium">${message}</span>
            <button onclick="this.closest('.toast-notification').remove()" class="text-white hover:text-slate-200 text-xl leading-none">×</button>
        </div>
    `;
    
    // Add to document
    document.body.appendChild(toast);
    
    // Auto remove after duration
    setTimeout(() => {
        toast.style.animation = 'slide-out 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

// Confirmation dialog with teal styling - returns a Promise
function showConfirm(message, options = {}) {
    return new Promise((resolve) => {
        // Remove any existing modals first
        const existingModal = document.getElementById('confirmModal');
        if (existingModal) existingModal.remove();
        
        const title = options.title || 'Onay';
        const confirmText = options.confirmText || 'Tamam';
        const cancelText = options.cancelText || 'İptal';
        const isDangerous = options.dangerous || false;
        
        // Create modal with unique button IDs using timestamp
        const timestamp = Date.now();
        const okBtnId = `confirmOkBtn_${timestamp}`;
        const cancelBtnId = `confirmCancelBtn_${timestamp}`;
        
        const modal = document.createElement('div');
        modal.id = 'confirmModal';
        modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4';
        modal.style.zIndex = '99999';
        
        modal.innerHTML = `
            <div class="bg-white rounded-xl p-6 max-w-md w-full shadow-2xl animate-scale-in">
                <h3 class="text-xl font-bold text-slate-900 mb-4">${title}</h3>
                <p class="text-slate-700 mb-6 whitespace-pre-line">${message}</p>
                <div class="flex gap-3">
                    <button id="${cancelBtnId}" 
                            class="flex-1 bg-slate-200 hover:bg-slate-300 text-slate-700 py-3 rounded-lg font-semibold transition-all">
                        ${cancelText}
                    </button>
                    <button id="${okBtnId}" 
                            class="flex-1 ${isDangerous ? 'bg-gradient-to-r from-red-600 to-red-500 hover:from-red-700 hover:to-red-600' : 'bg-gradient-to-r from-teal-700 to-teal-600 hover:from-teal-800 hover:to-teal-700'} text-white py-3 rounded-lg font-semibold transition-all">
                        ${confirmText}
                    </button>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Wait for next tick to ensure DOM is ready
        setTimeout(() => {
            const okBtn = document.getElementById(okBtnId);
            const cancelBtn = document.getElementById(cancelBtnId);
            
            if (!okBtn || !cancelBtn) {
                console.error('Confirm buttons not found in DOM');
                modal.remove();
                resolve(false);
                return;
            }
            
            const cleanup = () => {
                if (modal.parentNode) {
                    modal.remove();
                }
                document.removeEventListener('keydown', escapeHandler);
            };
            
            // OK button handler
            const okHandler = (e) => {
                e.preventDefault();
                e.stopPropagation();
                cleanup();
                resolve(true);
            };
            
            // Cancel button handler
            const cancelHandler = (e) => {
                e.preventDefault();
                e.stopPropagation();
                cleanup();
                resolve(false);
            };
            
            okBtn.addEventListener('click', okHandler, { once: true });
            cancelBtn.addEventListener('click', cancelHandler, { once: true });
            
            // Handle click outside
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    cleanup();
                    resolve(false);
                }
            });
            
            // Handle Escape key
            const escapeHandler = (e) => {
                if (e.key === 'Escape') {
                    cleanup();
                    resolve(false);
                }
            };
            document.addEventListener('keydown', escapeHandler);
        }, 0);
    });
}

// Add CSS animations
if (!document.getElementById('toast-styles')) {
    const style = document.createElement('style');
    style.id = 'toast-styles';
    style.textContent = `
        @keyframes slide-in {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        @keyframes slide-out {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(400px);
                opacity: 0;
            }
        }
        @keyframes scale-in {
            from {
                transform: scale(0.9);
                opacity: 0;
            }
            to {
                transform: scale(1);
                opacity: 1;
            }
        }
        .animate-slide-in {
            animation: slide-in 0.3s ease-out;
        }
        .animate-scale-in {
            animation: scale-in 0.2s ease-out;
        }
    `;
    document.head.appendChild(style);
}

// Override browser alert() with our toast
window.alert = function(message) {
    showToast(message, 'info', 4000);
};

// Override browser confirm() with our modal
const originalConfirm = window.confirm;
window.confirm = function(message) {
    console.warn('Using synchronous confirm() - consider using showConfirm() instead');
    return originalConfirm(message);
};
