/* =============================================================================
   asadchattha.com — v3

   Port of _scripts/main.js from the original v3. Same four jobs: the theme
   toggle, the back-to-top button, the waving hand, and the scroll reveal.

   Three dependencies are gone and nothing replaced them:
     - jQuery, which the original used only for a fade and a scroll animation.
       Both are one CSS class and one scrollTo call now.
     - ScrollReveal, loaded unversioned from unpkg. IntersectionObserver drives
       the `.waypoint` / `.in-view` pair that was already sitting unused in the
       original's own _base.scss, with the same easing and the same 20px offset.
     - The system clock. The original picked dark between 7pm and 7am and did not
       remember your choice, so it could overrule you on every reload.
   ========================================================================== */
(function () {
  'use strict';

  var body = document.body;

  /* ------------------------------------------------------------- theme ---- */
  /* The pre-paint script in index.html has already put `.night` on the body.
     This only has to sync the checkbox and persist what the user picks.

     The original listened on the LABEL and read input.checked BEFORE the click
     was applied, so its branches read inverted. Listening on the input's own
     `change` means the state is already flipped when this runs — checked IS
     night, no inversion. */
  var input = document.getElementById('switch');
  input.checked = body.classList.contains('night');

  input.addEventListener('change', function () {
    body.classList.toggle('night', input.checked);
    try {
      localStorage.setItem('theme', input.checked ? 'night' : 'day');
    } catch (e) {
      /* private mode — the toggle still works, it just will not be remembered */
    }
  });

  /* No prefers-color-scheme listener. The page opens light by design and only
     the switch changes that, so an OS theme change mid-visit must not flip a
     page the visitor is already reading. */

  /* --------------------------------------------------------- top button ---- */
  var intro = document.querySelector('.intro');
  var topButton = document.getElementById('top-button');

  var syncTopButton = function () {
    topButton.classList.toggle('is-visible', window.scrollY > intro.offsetHeight);
  };

  window.addEventListener('scroll', syncTopButton, { passive: true });
  window.addEventListener('resize', syncTopButton);
  syncTopButton();

  topButton.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  /* ---------------------------------------------------------- wave hand ---- */
  var hand = document.querySelector('.emoji.wave-hand');
  var waveTimer;

  function wave() {
    clearTimeout(waveTimer);
    hand.classList.add('wave');
    waveTimer = setTimeout(function () {
      hand.classList.remove('wave');
    }, 2000);
  }

  setTimeout(wave, 1000);
  hand.addEventListener('mouseover', function () {
    hand.classList.add('wave');
  });
  hand.addEventListener('mouseout', function () {
    hand.classList.remove('wave');
  });

  /* ------------------------------------------------------ scroll reveal ---- */
  var sections = document.querySelectorAll('.waypoint');

  var revealAll = function () {
    Array.prototype.forEach.call(sections, function (el) {
      el.classList.add('in-view');
    });
  };

  if (!('IntersectionObserver' in window)) {
    revealAll();
    return;
  }

  /* An IntersectionObserver only fires on a CHANGE, so a section that is jumped
     clean over — a deep link, a browser restoring last session's scroll position,
     End on the keyboard — never intersects and would stay invisible for good.
     Anything now above the fold has been passed and is shown unconditionally. */
  var revealPassed = function () {
    Array.prototype.forEach.call(sections, function (el) {
      if (!el.classList.contains('in-view') && el.getBoundingClientRect().top < 0) {
        el.classList.add('in-view');
      }
    });
  };
  window.addEventListener('scroll', revealPassed, { passive: true });
  revealPassed();

  Array.prototype.forEach.call(sections, function (el) {
    /* Per-section view factors, carried over from the original's sr.reveal
       calls: 0.3 for background and skills, 0.2 experience, 0.1 featured,
       0.05 other. A section taller than the viewport can never satisfy a high
       factor, so each one is clamped to what its own height can actually
       reach. Without this the tall sections simply never appear. */
    var wanted = parseFloat(el.dataset.viewFactor) || 0.3;
    var reachable = (window.innerHeight * 0.9) / el.offsetHeight;
    var threshold = Math.max(0.01, Math.min(wanted, reachable));

    var io = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: threshold });

    io.observe(el);
  });
})();
