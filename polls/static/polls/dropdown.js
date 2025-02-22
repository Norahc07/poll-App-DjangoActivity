document.addEventListener('DOMContentLoaded', function() {
    // Create portal container if it doesn't exist
    let portal = document.querySelector('.dropdown-portal');
    if (!portal) {
        portal = document.createElement('div');
        portal.className = 'dropdown-portal';
        document.body.appendChild(portal);
    }

    const dropbtns = document.querySelectorAll('.dropbtn');
    
    dropbtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const dropdownContent = this.nextElementSibling;
            const isCurrentlyShown = dropdownContent.classList.contains('show');
            
            // Close all dropdowns first
            document.querySelectorAll('.dropdown-content').forEach(content => {
                content.classList.remove('show');
                // Move content back to original position if it's not the current one
                if (content !== dropdownContent && content.parentElement === portal) {
                    const originalDropdown = document.querySelector(`button[data-dropdown-id="${content.dataset.dropdownId}"]`)
                        .parentElement;
                    originalDropdown.appendChild(content);
                }
            });
            
            // Toggle current dropdown
            if (!isCurrentlyShown) {
                const rect = this.getBoundingClientRect();
                // Add unique identifier if not exists
                if (!dropdownContent.dataset.dropdownId) {
                    dropdownContent.dataset.dropdownId = Math.random().toString(36).substr(2, 9);
                    this.dataset.dropdownId = dropdownContent.dataset.dropdownId;
                }
                dropdownContent.style.top = `${rect.bottom + window.scrollY}px`;
                dropdownContent.style.left = `${rect.right}px`;
                portal.appendChild(dropdownContent);
                dropdownContent.classList.add('show');
            }
        });
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.matches('.dropbtn') && !e.target.matches('.fa-ellipsis-v')) {
            document.querySelectorAll('.dropdown-content').forEach(content => {
                content.classList.remove('show');
                // Move content back to original position
                if (content.parentElement === portal) {
                    const originalDropdown = document.querySelector(`button[data-dropdown-id="${content.dataset.dropdownId}"]`)
                        .parentElement;
                    originalDropdown.appendChild(content);
                }
            });
        }
    });
}); 