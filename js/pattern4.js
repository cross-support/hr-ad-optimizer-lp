/**
 * Pattern4 専用 JavaScript
 * ヒーロー背景パーティクル、カウンターアニメーション、パララックス、スクロールアニメーションを提供
 */

// ========================================
// 1. ParticleSystem クラス
// ========================================
class ParticleSystem {
  constructor(canvasId, options = {}) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    this.particles = [];
    this.count = options.count || 60;
    this.maxSize = options.maxSize || 2;
    this.speed = options.speed || 0.3;
    this.running = true;
    this.init();
  }

  init() {
    this.resize();
    window.addEventListener('resize', () => this.resize());
    for (let i = 0; i < this.count; i++) {
      this.particles.push(this.createParticle());
    }
    this.animate();
  }

  resize() {
    this.canvas.width = this.canvas.parentElement.offsetWidth;
    this.canvas.height = this.canvas.parentElement.offsetHeight;
  }

  createParticle() {
    return {
      x: Math.random() * this.canvas.width,
      y: Math.random() * this.canvas.height,
      size: Math.random() * this.maxSize + 0.5,
      speedX: (Math.random() - 0.5) * this.speed,
      speedY: (Math.random() - 0.5) * this.speed,
      opacity: Math.random() * 0.5 + 0.1
    };
  }

  animate() {
    if (!this.running) return;
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.particles.forEach(p => {
      p.x += p.speedX;
      p.y += p.speedY;
      if (p.x < 0) p.x = this.canvas.width;
      if (p.x > this.canvas.width) p.x = 0;
      if (p.y < 0) p.y = this.canvas.height;
      if (p.y > this.canvas.height) p.y = 0;
      this.ctx.beginPath();
      this.ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      this.ctx.fillStyle = `rgba(255, 255, 255, ${p.opacity})`;
      this.ctx.fill();
    });
    requestAnimationFrame(() => this.animate());
  }

  destroy() {
    this.running = false;
  }
}

// ========================================
// 2. Animated Counter
// ========================================
function initCounters() {
  const counters = document.querySelectorAll('[data-counter]');
  if (!counters.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = parseInt(el.dataset.counter, 10);
        const suffix = el.dataset.suffix || '';
        animateCounter(el, target, 2000, suffix);
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(el => observer.observe(el));
}

function animateCounter(element, target, duration, suffix) {
  const startTime = performance.now();
  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3); // ease-out-cubic
    const current = Math.floor(eased * target);
    element.textContent = current.toLocaleString() + suffix;
    if (progress < 1) requestAnimationFrame(update);
  }
  requestAnimationFrame(update);
}

// ========================================
// 3. Parallax Effect
// ========================================
function initParallax() {
  const elements = document.querySelectorAll('[data-parallax]');
  if (!elements.length) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  window.addEventListener('scroll', () => {
    requestAnimationFrame(() => {
      elements.forEach(el => {
        const speed = parseFloat(el.dataset.parallax) || 0.1;
        const rect = el.getBoundingClientRect();
        const scrolled = window.innerHeight - rect.top;
        if (scrolled > 0 && rect.top < window.innerHeight) {
          el.style.transform = `translateY(${scrolled * speed}px)`;
        }
      });
    });
  }, { passive: true });
}

// ========================================
// 4. Enhanced Scroll Animations
// ========================================
function initP4Animations() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('p4-animate-in');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -80px 0px' });

  document.querySelectorAll('[data-p4-animate], [data-p4-stagger]').forEach(el => {
    observer.observe(el);
  });
}

// ========================================
// 5. DOMContentLoaded 初期化
// ========================================
document.addEventListener('DOMContentLoaded', () => {
  const isMobile = window.innerWidth < 768;

  // Particles (reduce on mobile)
  new ParticleSystem('particles', {
    count: isMobile ? 25 : 60,
    maxSize: isMobile ? 1.5 : 2,
    speed: 0.2
  });

  // Counters
  initCounters();

  // Parallax (skip on mobile)
  if (!isMobile) {
    initParallax();
  }

  // Scroll animations
  initP4Animations();
});
