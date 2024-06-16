// Smooth scroll function
const smoothScroll = (targetId) => {
    const targetElement = document.getElementById(targetId);

    if (targetElement) {
        window.scrollTo({
        top: targetElement.offsetTop,
        behavior: 'smooth' // Smooth scrolling behavior
        });
    }
    };

    // Add event listeners to each anchor link
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();

        const targetId = this.getAttribute('href').substring(1); // Remove the "#" from href
        smoothScroll(targetId);
    });
    });