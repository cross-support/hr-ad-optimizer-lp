document.addEventListener('DOMContentLoaded', () => {
  // Hamburger menu toggle
  const hamburger = document.getElementById('hamburger');
  const nav = document.getElementById('nav');

  if (hamburger && nav) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('header__hamburger--active');
      nav.classList.toggle('header__nav--active');
      const isExpanded = hamburger.classList.contains('header__hamburger--active');
      hamburger.setAttribute('aria-expanded', isExpanded);
    });
  }

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const href = anchor.getAttribute('href');
      if (href === '#') return;
      e.preventDefault();
      const target = document.querySelector(href);
      if (target) {
        const headerHeight = document.querySelector('.header')?.offsetHeight || 0;
        const top = target.getBoundingClientRect().top + window.pageYOffset - headerHeight;
        window.scrollTo({ top, behavior: 'smooth' });
      }
      // Close mobile menu
      if (nav) nav.classList.remove('header__nav--active');
      if (hamburger) {
        hamburger.classList.remove('header__hamburger--active');
        hamburger.setAttribute('aria-expanded', 'false');
      }
    });
  });

  // Scroll animation with Intersection Observer
  const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-in');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  // Exclude hero sections from animation
  const heroSelectors = ['.p1-hero', '.p2-concept', '.p3-hero', '.p4-hero'];

  document.querySelectorAll('.section-padding').forEach(section => {
    const isHeroSection = heroSelectors.some(selector => section.classList.contains(selector.slice(1)));
    if (!isHeroSection) {
      section.classList.add('animate-ready');
      observer.observe(section);
    }
  });

  // Add staggered animation to grid children
  document.querySelectorAll('.grid').forEach(grid => {
    const parentSection = grid.closest('.section-padding');
    const isHeroSection = heroSelectors.some(selector => parentSection?.classList.contains(selector.slice(1)));
    if (parentSection && !isHeroSection) {
      parentSection.classList.add('animate-ready');
      observer.observe(parentSection);
    }
  });
});
