/**
 * Pattern5 専用 JavaScript
 * カウンターアニメーション、スクロールアニメーションを提供
 * （パーティクル・パララックスなし - クリーンデザイン向け）
 */

// ========================================
// 1. Animated Counter
// ========================================
function initP5Counters() {
  const counters = document.querySelectorAll('[data-counter]');
  if (!counters.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = parseInt(el.dataset.counter, 10);
        const suffix = el.dataset.suffix || '';
        animateP5Counter(el, target, 2000, suffix);
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(el => observer.observe(el));
}

function animateP5Counter(element, target, duration, suffix) {
  const startTime = performance.now();
  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = Math.floor(eased * target);
    element.textContent = current.toLocaleString() + suffix;
    if (progress < 1) requestAnimationFrame(update);
  }
  requestAnimationFrame(update);
}

// ========================================
// 2. Scroll Animations
// ========================================
function initP5Animations() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('p5-animate-in');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -80px 0px' });

  document.querySelectorAll('[data-p5-animate], [data-p5-stagger]').forEach(el => {
    observer.observe(el);
  });
}

// ========================================
// 3. DOMContentLoaded 初期化
// ========================================
document.addEventListener('DOMContentLoaded', () => {
  initP5Counters();
  initP5Animations();
});
