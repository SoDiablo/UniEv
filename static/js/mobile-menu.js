// Mobile Menu Functionality

function initMobileMenu() {
    // Create mobile menu HTML
    const mobileMenuHTML = `
        <!-- Mobile Menu Overlay -->
        <div class="mobile-menu-overlay" id="mobileMenuOverlay" onclick="closeMobileMenu()"></div>
        
        <!-- Mobile Menu -->
        <div class="mobile-menu" id="mobileMenu">
            <div class="p-6">
                <div class="flex justify-between items-center mb-6">
                    <img src="/static/images/Logo.png" alt="UniEv" class="h-8" onerror="this.style.display='none'" />
                    <button onclick="closeMobileMenu()" class="text-slate-500 hover:text-slate-700">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>
                <nav id="mobileNavLinks" class="flex flex-col space-y-4">
                    <!-- Links will be populated by setupMobileNavigation() -->
                </nav>
            </div>
        </div>
    `;
    
    // Insert mobile menu after body
    document.body.insertAdjacentHTML('beforeend', mobileMenuHTML);
    
    // Create and add mobile menu button to header
    const headerContainer = document.querySelector('header .flex.justify-between, header .flex.items-center.justify-between');
    if (headerContainer) {
        // Check if button already exists
        if (!headerContainer.querySelector('.mobile-menu-btn')) {
            const menuBtn = document.createElement('button');
            menuBtn.className = 'mobile-menu-btn md:hidden text-slate-700 hover:text-teal-600 transition-colors';
            menuBtn.onclick = toggleMobileMenu;
            menuBtn.innerHTML = `
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                </svg>
            `;
            headerContainer.appendChild(menuBtn);
        }
    }
}

function toggleMobileMenu() {
    const menu = document.getElementById('mobileMenu');
    const overlay = document.getElementById('mobileMenuOverlay');
    
    if (menu && overlay) {
        menu.classList.toggle('active');
        overlay.classList.toggle('active');
        
        // Prevent body scroll when menu is open
        if (menu.classList.contains('active')) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    }
}

function closeMobileMenu() {
    const menu = document.getElementById('mobileMenu');
    const overlay = document.getElementById('mobileMenuOverlay');
    
    if (menu && overlay) {
        menu.classList.remove('active');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    }
}

function setupMobileNavigation() {
    const userStr = localStorage.getItem('user');
    const user = userStr ? JSON.parse(userStr) : null;
    const mobileNav = document.getElementById('mobileNavLinks');
    
    if (!mobileNav) return;
    
    const linkClass = 'block py-3 px-4 text-slate-700 hover:bg-teal-50 hover:text-teal-700 rounded-lg transition-colors font-medium';
    const activeLinkClass = 'block py-3 px-4 bg-teal-600 text-white rounded-lg font-medium';
    
    // Get current page
    const currentPath = window.location.pathname;
    
    if (!user) {
        mobileNav.innerHTML = `
            <a class="${currentPath === '/' ? activeLinkClass : linkClass}" href="/">Ana Sayfa</a>
            <a class="${currentPath === '/listings' ? activeLinkClass : linkClass}" href="/listings">İlanlar</a>
            <a class="${currentPath === '/help' ? activeLinkClass : linkClass}" href="/help">Yardım</a>
            <a class="${currentPath === '/login' ? activeLinkClass : linkClass}" href="/login">Giriş</a>
            <a class="${currentPath === '/register' ? activeLinkClass : linkClass}" href="/register">Kayıt Ol</a>
        `;
        return;
    }
    
    if (user.role === 'LANDLORD') {
        mobileNav.innerHTML = `
            <a class="${currentPath === '/' ? activeLinkClass : linkClass}" href="/">Ana Sayfa</a>
            <a class="${currentPath === '/listings' ? activeLinkClass : linkClass}" href="/listings">İlanlar</a>
            <a class="${currentPath === '/create-listing' ? activeLinkClass : linkClass}" href="/create-listing">İlan Oluştur</a>
            <a class="${currentPath === '/messages' ? activeLinkClass : linkClass}" href="/messages">Mesajlar</a>
            <a class="${currentPath === '/profile' ? activeLinkClass : linkClass}" href="/profile">Profil</a>
            <a class="${currentPath === '/help' ? activeLinkClass : linkClass}" href="/help">Yardım</a>
            <a class="${linkClass}" href="#" onclick="logout(); return false;">Çıkış</a>
        `;
    } else if (user.role === 'ADMIN') {
        mobileNav.innerHTML = `
            <a class="${currentPath === '/' ? activeLinkClass : linkClass}" href="/">Ana Sayfa</a>
            <a class="${currentPath === '/listings' ? activeLinkClass : linkClass}" href="/listings">İlanlar</a>
            <a class="${currentPath === '/admin' ? activeLinkClass : linkClass}" href="/admin">Admin Panel</a>
            <a class="${currentPath === '/messages' ? activeLinkClass : linkClass}" href="/messages">Mesajlar</a>
            <a class="${currentPath === '/profile' ? activeLinkClass : linkClass}" href="/profile">Profil</a>
            <a class="${currentPath === '/help' ? activeLinkClass : linkClass}" href="/help">Yardım</a>
            <a class="${linkClass}" href="#" onclick="logout(); return false;">Çıkış</a>
        `;
    } else {
        // STUDENT
        mobileNav.innerHTML = `
            <a class="${currentPath === '/' ? activeLinkClass : linkClass}" href="/">Ana Sayfa</a>
            <a class="${currentPath === '/listings' ? activeLinkClass : linkClass}" href="/listings">İlanlar</a>
            <a class="${currentPath === '/match' ? activeLinkClass : linkClass}" href="/match">Eşleşme</a>
            <a class="${currentPath === '/messages' ? activeLinkClass : linkClass}" href="/messages">Mesajlar</a>
            <a class="${currentPath === '/profile' ? activeLinkClass : linkClass}" href="/profile">Profil</a>
            <a class="${currentPath === '/help' ? activeLinkClass : linkClass}" href="/help">Yardım</a>
            <a class="${linkClass}" href="#" onclick="logout(); return false;">Çıkış</a>
        `;
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initMobileMenu();
    setupMobileNavigation();
});
