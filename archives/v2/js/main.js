/* =========================================================================
   v2 — asadchattha.com
   The original ran on jQuery 2.1.3 plus skrollr 0.6.30. This is the same
   behaviour with neither: plain DOM, one rAF-throttled scroll handler, and an
   IntersectionObserver so only on-screen backgrounds are ever transformed.
   ========================================================================= */
(function () {
  'use strict';

  var DESKTOP = 768;
  var TRAVEL = 150;   // +/- 150px, so 300px of travel, same as the original

  var reduceMotion = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var dotNav = document.getElementById('dot-nav');
  var dotLinks = Array.prototype.slice.call(document.querySelectorAll('#dot-nav a'));
  var sections = Array.prototype.slice.call(document.querySelectorAll('.section'));
  var about = document.getElementById('about-section');
  var hamburger = document.getElementById('toggle');
  var overlay = document.getElementById('overlay');

  /* ------------------------------------------------------------- smooth scroll */
  function smoothScroll(hash) {
    var target = document.querySelector(hash);
    if (!target) { return; }
    var top = target.getBoundingClientRect().top + window.pageYOffset + 50;
    window.scrollTo({
      top: top,
      behavior: reduceMotion ? 'auto' : 'smooth'
    });
  }

  function wireScroll(selector, after) {
    Array.prototype.forEach.call(document.querySelectorAll(selector), function (el) {
      el.addEventListener('click', function (ev) {
        if (!el.hash) { return; }
        ev.preventDefault();
        smoothScroll(el.hash);
        if (after) { after(); }
      });
    });
  }

  /* --------------------------------------------------------------- dot nav */
  function updateNavigation() {
    var half = window.innerHeight / 2;
    var scrolled = window.pageYOffset;

    sections.forEach(function (section) {
      var link = document.querySelector('#dot-nav a[href="#' + section.id + '"]');
      if (!link) { return; }
      var offsetTop = section.getBoundingClientRect().top + scrolled;
      var inView = (offsetTop - half < scrolled) &&
                   (offsetTop + section.offsetHeight - half > scrolled);
      link.classList.toggle('is-selected', inView);
    });
  }

  /* The dots appear once you are three quarters of the way to About, which is
     what `about.offsetTop - about.offsetTop / 4` works out to. */
  function handleNavs() {
    if (!dotNav || !about) { return; }
    var isDesktop = window.innerWidth > DESKTOP;
    var topOfAbout = about.offsetTop - (about.offsetTop / 4);
    var isBelowIntro = window.pageYOffset > topOfAbout;
    var menuOpen = overlay && overlay.classList.contains('open');

    if (isDesktop && isBelowIntro) {
      dotNav.classList.add('active');
    } else if (isDesktop && menuOpen) {
      toggleMenu();
    } else {
      dotNav.classList.remove('active');
    }
  }

  /* ---------------------------------------------------------- mobile menu */
  function toggleMenu() {
    if (!hamburger || !overlay) { return; }
    var open = overlay.classList.toggle('open');
    hamburger.classList.toggle('active');
    document.body.classList.toggle('noScroll');
    hamburger.setAttribute('aria-expanded', open ? 'true' : 'false');
  }

  if (hamburger) { hamburger.addEventListener('click', toggleMenu); }

  document.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape' && overlay && overlay.classList.contains('open')) {
      toggleMenu();
    }
  });

  /* ------------------------------------------------------------- parallax */
  /* skrollr's replacement. The plate is exactly the size of its section, the
     same as the original, so the photo sits at its natural `cover` scale and
     is never enlarged to fill an oversized box. Moving the plate itself would
     therefore expose an edge, so the travel is applied to background-position
     instead, inside the slack that `cover` already leaves: fitted to the
     section width, a 3:2 plate stands taller than the section, and that
     overflow is the room the photo has to move in.
     Only plates the observer says are on screen get written to. */
  var plates = Array.prototype.slice.call(document.querySelectorAll('[data-parallax]'));
  var visible = [];

  /* the plates are four different shapes (3:2 landscape, 2:3 portrait, 26:15),
     so the aspect ratio is read off the file rather than assumed */
  function ratioFor(plate) {
    if (plate._ratio !== undefined) return plate._ratio;
    plate._ratio = null;
    var url = getComputedStyle(plate).backgroundImage.match(/url\(["']?(.*?)["']?\)/);
    if (!url) return null;
    var probe = new Image();
    probe.onload = function () {
      if (probe.naturalWidth) plate._ratio = probe.naturalHeight / probe.naturalWidth;
    };
    probe.src = url[1];
    return null;
  }

  function slackFor(plate, section) {
    /* half the vertical overflow of the covered image, capped at TRAVEL */
    var ratio = ratioFor(plate);
    if (!ratio) return 0;
    var drawn = section.offsetWidth * ratio;
    var slack = (drawn - section.offsetHeight) / 2;
    if (!(slack > 0)) return 0;
    return Math.min(slack, TRAVEL);
  }

  function renderParallax() {
    var vh = window.innerHeight;
    visible.forEach(function (plate) {
      var section = plate.parentElement;
      var rect = section.getBoundingClientRect();
      var span = vh + rect.height;
      var progress = (vh - rect.top) / span;
      progress = progress < 0 ? 0 : (progress > 1 ? 1 : progress);
      var travel = slackFor(plate, section);
      if (!travel) { plate.style.backgroundPosition = ''; return; }
      var y = travel - (travel * 2 * progress);
      plate.style.backgroundPosition = 'center calc(50% + ' + y.toFixed(2) + 'px)';
    });
  }

  if (!reduceMotion && plates.length && 'IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        var i = visible.indexOf(entry.target);
        if (entry.isIntersecting && i === -1) {
          visible.push(entry.target);
        } else if (!entry.isIntersecting && i !== -1) {
          visible.splice(i, 1);
        }
      });
      renderParallax();
    }, { rootMargin: '200px 0px' });

    plates.forEach(function (plate) { observer.observe(plate); });
  }

  /* -------------------------------------------------- one throttled handler */
  var ticking = false;

  function onScroll() {
    if (ticking) { return; }
    ticking = true;
    window.requestAnimationFrame(function () {
      updateNavigation();
      handleNavs();
      renderParallax();
      ticking = false;
    });
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);

  /* --------------------------------------------------------- contact form */
  var inputs = Array.prototype.slice.call(document.querySelectorAll('.contact-input'));

  function focusInput() {
    this.parentElement.classList.add('is-active', 'is-completed');
  }

  /* The original removed is-completed unconditionally on blur, so the floating
     label dropped back down on top of whatever the visitor had just typed.
     It is only removed when the field is actually empty. */
  function blurInput() {
    this.parentElement.classList.remove('is-active');
    if (!this.value.trim()) {
      this.parentElement.classList.remove('is-completed');
    }
  }

  inputs.forEach(function (input) {
    input.addEventListener('focus', focusInput);
    input.addEventListener('blur', blurInput);
    // a browser-restored or autofilled value should keep the label lifted
    if (input.value.trim()) { input.parentElement.classList.add('is-completed'); }
  });

  var textarea = document.getElementById('message');
  var LIMIT = 300;

  if (textarea) {
    textarea.addEventListener('input', function () {
      textarea.style.height = '';
      textarea.style.height = Math.min(textarea.scrollHeight, LIMIT) + 'px';
    });
  }

  /* Netlify Forms. The original did a native POST to Formspree and gave the
     visitor nothing: no pending state, no confirmation, and the page navigated
     away. This posts the form url-encoded back to the site root, which is what
     Netlify's AJAX path expects, and reports in place. The hidden form-name
     field in the markup is what the submission is matched on, so it has to be
     part of the body — building the body from the form itself keeps it there. */
  var form = document.getElementById('contactform');
  var status = document.getElementById('form-status');

  function encodeForm(f) {
    var data = new FormData(f);
    var pairs = [];
    data.forEach(function (value, key) {
      pairs.push(encodeURIComponent(key) + '=' + encodeURIComponent(value));
    });
    return pairs.join('&');
  }

  if (form && status && window.fetch) {
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var button = form.querySelector('.message-btn');

      status.className = 'form-status';
      status.textContent = 'Sending...';
      if (button) { button.disabled = true; }

      fetch(form.getAttribute('action') || '/', {
        method: 'POST',
        body: encodeForm(form),
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      }).then(function (res) {
        if (!res.ok) { throw new Error(res.status); }
        status.className = 'form-status is-success';
        status.textContent = 'Thanks. Your message is on its way, I will reply from m.asad.chatthaa@gmail.com.';
        form.reset();
        inputs.forEach(function (input) {
          input.parentElement.classList.remove('is-active', 'is-completed');
        });
        if (textarea) { textarea.style.height = ''; }
      }).catch(function () {
        /* Never make someone retype what they already wrote. If the POST fails,
           the fallback hands them a mail draft already carrying their subject
           and message, so the only thing left to do is press send. */
        var val = function (id) {
          var el = form.querySelector('#' + id);
          return el ? el.value : '';
        };
        var subject = val('subject') || 'Hello from asadchattha.com';
        var body = val('message');
        if (val('name')) { body += '\n\n' + val('name'); }

        /* The address is spelled out, not hidden behind link text: someone on a
           machine with no mail client configured needs to be able to copy it. */
        status.className = 'form-status is-error';
        status.innerHTML = 'That did not send. Email me at ' +
          '<a href="mailto:m.asad.chatthaa@gmail.com?subject=' + encodeURIComponent(subject) +
          '&amp;body=' + encodeURIComponent(body) + '">m.asad.chatthaa@gmail.com</a>' +
          ' and your message comes with it.';
      }).then(function () {
        if (button) { button.disabled = false; }
      });
    });
  }

  /* --------------------------------------------------------------- wiring */
  wireScroll('.scroll-down');
  wireScroll('#dot-nav a');
  wireScroll('#overlay a', function () {
    if (overlay.classList.contains('open')) { toggleMenu(); }
  });

  updateNavigation();
  handleNavs();
  renderParallax();
}());
