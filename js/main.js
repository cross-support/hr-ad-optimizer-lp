// Main JavaScript File
// Initialize when DOM is fully loaded

document.addEventListener('DOMContentLoaded', function() {
  console.log('HR Ad-Optimizer LP loaded successfully');

  // Hamburger menu toggle (for mobile)
  const hamburger = document.getElementById('hamburger');
  const nav = document.getElementById('nav');

  if (hamburger && nav) {
    hamburger.addEventListener('click', function() {
      nav.classList.toggle('header__nav--active');
      hamburger.classList.toggle('header__hamburger--active');
    });
  }

  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href !== '#' && href.length > 1) {
        e.preventDefault();
        const targetId = href.substring(1);
        const targetElement = document.getElementById(targetId);

        if (targetElement) {
          const headerHeight = document.getElementById('header').offsetHeight;
          const targetPosition = targetElement.offsetTop - headerHeight;

          window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
          });

          // Close mobile menu if open
          if (nav && nav.classList.contains('header__nav--active')) {
            nav.classList.remove('header__nav--active');
            hamburger.classList.remove('header__hamburger--active');
          }
        }
      }
    });
  });
});
