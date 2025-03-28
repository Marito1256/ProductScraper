// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get references to important elements
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');
    const loadingOverlay = document.getElementById('loading-overlay');
    
    // Add event listener for form submission
    if (searchForm) {
        searchForm.addEventListener('submit', function(event) {
            // Only run animation if input is not empty
            if (searchInput.value.trim() !== '') {
                // Prevent default form submission
                event.preventDefault();
                
                // Call the connectHERE function to handle transition
                connectHERE(searchInput.value);
            }
        });
    }
    
    // Focus search input when page loads (if it exists)
    if (searchInput) {
        searchInput.focus();
    }
    
    // Add staggered animation to result cards if we're on the results page
    const resultCards = document.querySelectorAll('.result-card');
    if (resultCards.length > 0) {
        animateResults();
    }
});

/**
 * Handles the transition animation and navigates to search results
 * @param {string} query - The search query
 */
function connectHERE(query) {
    // Show loading overlay
    const loadingOverlay = document.getElementById('loading-overlay');
    loadingOverlay.classList.add('show');
    
    // Create dynamic particles for the transition effect
    createTransitionParticles();
    
    // If we're on the search page, animate the search wrapper
    const searchWrapper = document.querySelector('.search-wrapper');
    if (searchWrapper) {
        // Apply a more dramatic transform animation
        searchWrapper.style.transform = 'scale(0.8) translateY(-30px)';
        searchWrapper.style.opacity = '0';
        
        // Add pulse effect to the search input before transition
        const searchInput = document.querySelector('.search-input');
        if (searchInput) {
            searchInput.style.boxShadow = '0 0 20px var(--accent-glow)';
            setTimeout(() => {
                searchInput.style.boxShadow = 'none';
            }, 300);
        }
    }
    
    // Increase transition time for a more noticeable effect
    setTimeout(function() {
        // fetch('/api/search', {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify({ query: query })
        // })
        // .then(res => res.json())
        // .then(data => {
        //     console.log('Results:', data); // Array of dictionaries
        //     // Handle the data however you need
        //     // For example: renderResults(data)
        // })
        // .catch(err => {
        //     console.error('Error:', err);
        // });
        const form = document.createElement('form');
        form.method='POST';
        form.action = '/api/search';

        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'q';
        input.value=query;
        form.appendChild(input);
        document.body.appendChild(form);
        form.submit();
    }, 1200);
}

/**
 * Creates particles for the transition effect
 */
function createTransitionParticles() {
    const overlay = document.getElementById('loading-overlay');
    
    // Clear any existing particles
    const existingParticles = overlay.querySelectorAll('.transition-particle');
    existingParticles.forEach(particle => particle.remove());
    
    // Create 30 particles for a more dramatic effect
    for (let i = 0; i < 30; i++) {
        const particle = document.createElement('div');
        particle.className = 'transition-particle';
        
        // Random position near the search input for a "burst" effect
        const searchInput = document.querySelector('.search-input');
        let posX, posY;
        
        if (searchInput && i < 15) {
            // Get search input position for first set of particles
            const rect = searchInput.getBoundingClientRect();
            posX = rect.left + rect.width / 2 + (Math.random() * 100 - 50);
            posY = rect.top + rect.height / 2 + (Math.random() * 100 - 50);
        } else {
            // Random position for remaining particles
            posX = Math.random() * window.innerWidth;
            posY = Math.random() * window.innerHeight;
        }
        
        // Random size between 5px and 20px
        const size = 5 + Math.random() * 15;
        
        // Random animation duration between 0.5s and 2s
        const animDuration = 0.5 + Math.random() * 1.5;
        
        // Random movement direction
        const randomX = (Math.random() * 200 - 100) + 'px';
        const randomY = (Math.random() * 200 - 100) + 'px';
        
        // Apply styles
        particle.style.width = size + 'px';
        particle.style.height = size + 'px';
        particle.style.left = posX + 'px';
        particle.style.top = posY + 'px';
        particle.style.animationDuration = animDuration + 's';
        
        // Set custom properties for random movement in the CSS animation
        particle.style.setProperty('--random-x', randomX);
        particle.style.setProperty('--random-y', randomY);
        
        // Random delay for a staggered effect
        particle.style.animationDelay = (Math.random() * 0.3) + 's';
        
        // Add a subtle rotation
        particle.style.transform = `rotate(${Math.random() * 360}deg)`;
        
        // Add to overlay
        overlay.appendChild(particle);
        
        // Auto-remove particles after animation completes
        setTimeout(() => {
            if (particle.parentNode === overlay) {
                overlay.removeChild(particle);
            }
        }, animDuration * 1000 + 500);
    }
}

/**
 * Adds staggered animation to search result cards
 */
function animateResults() {
    const resultCards = document.querySelectorAll('.result-card');
    
    resultCards.forEach((card, index) => {
        // Apply staggered animation delay
        card.style.animationDelay = `${0.1 + (index * 0.1)}s`;
    });
}

/**
 * Filter results based on price range
 * This could be expanded for future functionality
 */
function filterByPrice(minPrice, maxPrice) {
    // This is a placeholder for potential filtering functionality
    console.log(`Filtering results between $${minPrice} and $${maxPrice}`);
    
    // This would require an AJAX call to re-fetch filtered results
    // or client-side filtering of existing results
}

/**
 * Sort results by different criteria
 * This could be expanded for future functionality
 */
function sortResults(criteria) {
    // This is a placeholder for potential sorting functionality
    console.log(`Sorting results by ${criteria}`);
    
    // Implementation would depend on whether sorting happens server or client side
}
