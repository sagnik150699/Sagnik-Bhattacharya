/**
 * Sagnik Bhattacharya — Enhanced Animations
 * Requires GSAP + ScrollTrigger loaded before this script
 */
(function(){
  'use strict';

  // ── NAV ──
  const navbar = document.getElementById('navbar');
  const hamburger = document.getElementById('hamburger');
  const navLinks = document.getElementById('navLinks');

  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 20);
  });
  hamburger.addEventListener('click', () => navLinks.classList.toggle('active'));
  navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => navLinks.classList.remove('active'));
  });

  // ── SCROLL PROGRESS BAR ──
  const progressBar = document.createElement('div');
  progressBar.className = 'scroll-progress';
  document.body.prepend(progressBar);

  window.addEventListener('scroll', () => {
    const scrolled = window.scrollY;
    const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
    const pct = maxScroll > 0 ? (scrolled / maxScroll) * 100 : 0;
    progressBar.style.width = pct + '%';
  }, { passive: true });

  // ── CURSOR GLOW (desktop only) ──
  if (window.matchMedia('(min-width:901px) and (pointer:fine)').matches) {
    const glow = document.createElement('div');
    glow.className = 'cursor-glow';
    document.body.appendChild(glow);
    let mouseX = -500, mouseY = -500, glowX = -500, glowY = -500;

    document.addEventListener('mousemove', e => {
      mouseX = e.clientX; mouseY = e.clientY;
      glow.classList.add('active');
    });
    document.addEventListener('mouseleave', () => glow.classList.remove('active'));

    (function loop() {
      glowX += (mouseX - glowX) * 0.08;
      glowY += (mouseY - glowY) * 0.08;
      glow.style.left = glowX + 'px';
      glow.style.top = glowY + 'px';
      requestAnimationFrame(loop);
    })();
  }

  // ── CHECK IF GSAP LOADED ──
  const hasGSAP = typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined';

  if (hasGSAP) {
    gsap.registerPlugin(ScrollTrigger);
    document.body.classList.add('gsap-ready');
    initGSAPAnimations();
  } else {
    // Fallback: use the simple IntersectionObserver
    initFallbackAnimations();
  }

  // ── GSAP ANIMATIONS ──
  function initGSAPAnimations() {

    // Hero elements (only on homepage)
    const heroBadge = document.querySelector('.hero-badge');
    const heroH1 = document.querySelector('.hero h1');
    const heroSub = document.querySelector('.hero-sub');
    const heroActions = document.querySelector('.hero-actions');
    const heroVisual = document.querySelector('.hero-visual');

    if (heroBadge) {
      const heroTL = gsap.timeline({ defaults: { ease: 'power3.out' } });

      heroTL
        .fromTo(heroBadge,
          { opacity: 0, y: 30, scale: 0.9 },
          { opacity: 1, y: 0, scale: 1, duration: 0.7 })
        .fromTo(heroH1,
          { opacity: 0, y: 40 },
          { opacity: 1, y: 0, duration: 0.8 }, '-=0.4')
        .fromTo(heroSub,
          { opacity: 0, y: 30 },
          { opacity: 1, y: 0, duration: 0.7 }, '-=0.5')
        .fromTo(heroActions,
          { opacity: 0, y: 20 },
          { opacity: 1, y: 0, duration: 0.6 }, '-=0.4')
        .fromTo(heroVisual,
          { opacity: 0, y: 40, scale: 0.95, rotateY: 8 },
          { opacity: 1, y: 0, scale: 1, rotateY: 0, duration: 1 }, '-=0.6');
    }

    // Page hero (inner pages)
    const pageHero = document.querySelector('.page-hero');
    if (pageHero && !heroBadge) {
      const pgTL = gsap.timeline({ defaults: { ease: 'power3.out' } });
      const pgLabel = pageHero.querySelector('.section-label');
      const pgH1 = pageHero.querySelector('h1');
      const pgP = pageHero.querySelector('p');

      pgTL
        .fromTo(pgLabel,
          { opacity: 0, x: -20 },
          { opacity: 1, x: 0, duration: 0.6 })
        .fromTo(pgH1,
          { opacity: 0, y: 30 },
          { opacity: 1, y: 0, duration: 0.7 }, '-=0.3')
        .fromTo(pgP,
          { opacity: 0, y: 20 },
          { opacity: 1, y: 0, duration: 0.6 }, '-=0.4');
    }

    // Section reveals with stagger
    document.querySelectorAll('.reveal').forEach(el => {
      gsap.fromTo(el,
        { opacity: 0, y: 40 },
        {
          opacity: 1, y: 0,
          duration: 0.8,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: el,
            start: 'top 85%',
            once: true
          }
        }
      );
    });

    // Stagger grid children (cards come in one-by-one)
    document.querySelectorAll('.courses-grid, .services-grid, .projects-grid').forEach(grid => {
      const children = grid.children;
      if (children.length > 0) {
        gsap.fromTo(children,
          { opacity: 0, y: 50, scale: 0.97 },
          {
            opacity: 1, y: 0, scale: 1,
            duration: 0.7,
            stagger: 0.15,
            ease: 'power3.out',
            scrollTrigger: {
              trigger: grid,
              start: 'top 80%',
              once: true
            }
          }
        );
      }
    });

    // Section labels: slide in from left
    document.querySelectorAll('.section-label').forEach(label => {
      gsap.fromTo(label,
        { opacity: 0, x: -30 },
        {
          opacity: 1, x: 0,
          duration: 0.6,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: label,
            start: 'top 88%',
            once: true
          }
        }
      );
      // Animate the ::before pseudo-element via the label's width trigger
      gsap.fromTo(label,
        { '--label-line-width': '0px' },
        {
          '--label-line-width': '24px',
          duration: 0.5,
          delay: 0.3,
          scrollTrigger: {
            trigger: label,
            start: 'top 88%',
            once: true
          }
        }
      );
    });

    // CTA banners: scale up from slightly small
    document.querySelectorAll('.cta-inner').forEach(cta => {
      gsap.fromTo(cta,
        { opacity: 0, y: 30, scale: 0.97 },
        {
          opacity: 1, y: 0, scale: 1,
          duration: 0.8,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: cta,
            start: 'top 82%',
            once: true
          }
        }
      );
    });

    // Social cards stagger (contact page)
    const socialCards = document.querySelectorAll('.social-card');
    if (socialCards.length) {
      gsap.fromTo(socialCards,
        { opacity: 0, x: 30 },
        {
          opacity: 1, x: 0,
          duration: 0.6,
          stagger: 0.1,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: socialCards[0],
            start: 'top 80%',
            once: true
          }
        }
      );
    }

    // About tags stagger
    const aboutTags = document.querySelectorAll('.about-tag');
    if (aboutTags.length) {
      gsap.fromTo(aboutTags,
        { opacity: 0, y: 15, scale: 0.85 },
        {
          opacity: 1, y: 0, scale: 1,
          duration: 0.4,
          stagger: 0.06,
          ease: 'back.out(2)',
          scrollTrigger: {
            trigger: aboutTags[0].parentElement,
            start: 'top 85%',
            once: true
          }
        }
      );
    }

    // Topic tags stagger (courses page)
    document.querySelectorAll('.topics').forEach(topicGroup => {
      const topics = topicGroup.querySelectorAll('.topic');
      if (topics.length) {
        gsap.fromTo(topics,
          { opacity: 0, y: 10, scale: 0.85 },
          {
            opacity: 1, y: 0, scale: 1,
            duration: 0.35,
            stagger: 0.04,
            ease: 'back.out(2)',
            scrollTrigger: {
              trigger: topicGroup,
              start: 'top 85%',
              once: true
            }
          }
        );
      }
    });

    // Parallax effect on hero background orbs
    document.querySelectorAll('.parallax-orb').forEach(orb => {
      const speed = parseFloat(orb.dataset.speed) || 0.3;
      gsap.to(orb, {
        y: () => window.innerHeight * speed * -0.5,
        ease: 'none',
        scrollTrigger: {
          trigger: orb.closest('section') || orb.closest('header') || orb.closest('.hero') || document.body,
          start: 'top top',
          end: 'bottom top',
          scrub: 1
        }
      });
    });
  }

  // ── FALLBACK ANIMATIONS (no GSAP) ──
  function initFallbackAnimations() {
    const reveals = document.querySelectorAll('.reveal');
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry, i) => {
        if (entry.isIntersecting) {
          setTimeout(() => entry.target.classList.add('visible'), i * 80);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    reveals.forEach(el => observer.observe(el));
  }

  // ── COUNTER ANIMATION ──
  document.querySelectorAll('[data-count]').forEach(el => {
    const target = el.dataset.count;
    const suffix = el.dataset.suffix || '';
    const isNum = !isNaN(parseFloat(target));
    if (!isNum) { el.textContent = target; return; }

    const targetNum = parseFloat(target);
    const duration = 2000;
    let started = false;

    const startCount = () => {
      if (started) return;
      started = true;
      const start = performance.now();

      function step(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        // Ease out cubic
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = Math.round(eased * targetNum);

        if (target.includes('K')) {
          el.textContent = (current >= 1000 ? Math.round(current / 1000) + 'K' : current) + suffix;
        } else {
          el.textContent = current.toLocaleString() + suffix;
        }

        if (progress < 1) requestAnimationFrame(step);
        else el.textContent = target + suffix;
      }
      requestAnimationFrame(step);
    };

    // Trigger on scroll into view
    const obs = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) { startCount(); obs.unobserve(el); }
    }, { threshold: 0.5 });
    obs.observe(el);
  });

  // ── MAGNETIC BUTTON EFFECT (desktop) ──
  if (window.matchMedia('(pointer:fine)').matches) {
    document.querySelectorAll('.btn-primary, .btn-outline, .nav-cta').forEach(btn => {
      btn.addEventListener('mousemove', e => {
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        btn.style.transform = `translate(${x * 0.15}px, ${y * 0.15}px) scale(1.02)`;
      });
      btn.addEventListener('mouseleave', () => {
        btn.style.transform = '';
      });
    });
  }

  // ── TILT EFFECT ON CARDS (desktop) ──
  if (window.matchMedia('(pointer:fine)').matches) {
    document.querySelectorAll('.course-card, .project-card, .hero-card').forEach(card => {
      card.style.transformStyle = 'preserve-3d';
      card.style.perspective = '800px';

      card.addEventListener('mousemove', e => {
        const rect = card.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;
        card.style.transform = `perspective(800px) rotateY(${x * 6}deg) rotateX(${-y * 6}deg) translateY(-4px) scale(1.01)`;
      });
      card.addEventListener('mouseleave', () => {
        card.style.transform = '';
        card.style.transition = 'transform .5s cubic-bezier(0.16,1,0.3,1)';
        setTimeout(() => { card.style.transition = ''; }, 500);
      });
    });
  }

  // ── SMOOTH SECTION SEPARATOR PARALLAX ──
  document.querySelectorAll('.stat-divider').forEach(div => {
    if (!hasGSAP) return;
    gsap.fromTo(div,
      { scaleX: 0 },
      {
        scaleX: 1,
        duration: 1,
        ease: 'power3.out',
        scrollTrigger: {
          trigger: div,
          start: 'top 85%',
          once: true
        }
      }
    );
  });

})();
