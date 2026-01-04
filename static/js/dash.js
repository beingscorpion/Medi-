

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle functionality
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.querySelector('.sidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');

    function toggleSidebar() {
        if (sidebar && sidebarOverlay) {
            const isActive = sidebar.classList.contains('active');
            sidebar.classList.toggle('active');
            sidebarOverlay.classList.toggle('active');
            // Prevent body scroll when sidebar is open
            if (!isActive) {
                document.body.classList.add('sidebar-open');
            } else {
                document.body.classList.remove('sidebar-open');
            }
        }
    }

    function closeSidebar() {
        if (sidebar && sidebarOverlay) {
            sidebar.classList.remove('active');
            sidebarOverlay.classList.remove('active');
            document.body.classList.remove('sidebar-open');
        }
    }

    if (menuToggle) {
        menuToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            toggleSidebar();
        });
    }

    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', closeSidebar);
    }

    // Handle window resize - close sidebar on mobile when resizing to desktop
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            if (window.innerWidth > 768) {
                closeSidebar();
            }
        }, 250);
    });

    // Sidebar view switching functionality
    document.querySelectorAll('.sidebar-menu a[data-view]').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const viewType = this.getAttribute('data-view');
            
            // Close sidebar on mobile when clicking a link
            if (window.innerWidth <= 768) {
                closeSidebar();
            }
            
            // Remove active class from all sidebar links
            document.querySelectorAll('.sidebar-menu a').forEach(a => a.classList.remove('sidebar-active'));
            this.classList.add('sidebar-active');
            
            // Hide all view sections
            document.querySelectorAll('.view-section').forEach(section => {
                section.classList.remove('active');
            });
            
            // Show selected view section
            const viewSection = document.querySelector(`[data-view-section="${viewType}"]`);
            if (viewSection) {
                viewSection.classList.add('active');
            }
        });
    });

    // Tab switching functionality (works for both MDcat and Past Paper)
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Get the parent view section
            const viewSection = this.closest('.view-section');
            if (!viewSection) return;
            
            // Remove active class from all tabs in this view section
            viewSection.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            // Hide all tab content in this view section
            viewSection.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            
            // Show selected tab content
            const tabName = this.getAttribute('data-tab');
            const content = viewSection.querySelector(`[data-content="${tabName}"]`);
            if (content) {
                content.classList.add('active');
            }
        });
    });

    // Chapter card click functionality (for MDcat)
    document.querySelectorAll('[data-view-section="mdcat"] .subject-card[data-chapter]').forEach(card => {
        card.addEventListener('click', function() {
            const chapter = this.getAttribute('data-chapter');
            
            // Remove selected class from all cards in the same tab
            const currentTab = this.closest('.tab-content');
            if (currentTab) {
                currentTab.querySelectorAll('.subject-card').forEach(c => c.classList.remove('selected'));
            }
            this.classList.add('selected');
            
            // Navigate to paper selection page for this chapter
            if (chapter) {
                window.location.href = `/chapter/${chapter}/`;
            }
        });
    });

    // Year card click functionality (for Past Paper)
    document.querySelectorAll('[data-view-section="past-paper"] .subject-card[data-year-slug]').forEach(card => {
        card.addEventListener('click', function() {
            const yearSlug = this.getAttribute('data-year-slug');
            
            // Remove selected class from all cards in the same tab
            const currentTab = this.closest('.tab-content');
            if (currentTab) {
                currentTab.querySelectorAll('.subject-card').forEach(c => c.classList.remove('selected'));
            }
            this.classList.add('selected');
            
            // Navigate to past paper MCQs for this year
            if (yearSlug) {
                window.location.href = `/past-paper/${yearSlug}/`;
            }
        });
    });

    // Logout button
    document.getElementById('logoutBtn')?.addEventListener('click', function() {
        this.textContent = 'Logging out...';
        this.disabled = true;
        const logoutUrl = this.getAttribute('data-logout-url');
        if (logoutUrl) {
            window.location.href = logoutUrl;
        }
    });
});