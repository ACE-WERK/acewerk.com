
(function(){
  "use strict";
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (!toggle || !nav) return;
  var links = nav.querySelectorAll('a');
  var first = links[0];
  var last = links[links.length - 1];
  var logo = document.querySelector('.nav-logo');

  function isOpen(){ return toggle.classList.contains('open'); }
  function openMenu(){
    toggle.classList.add('open');
    nav.classList.add('open');
    toggle.setAttribute('aria-expanded', 'true');
    toggle.setAttribute('aria-label', 'Close menu');
    document.body.classList.add('nav-open');
    if (logo) logo.setAttribute('tabindex', '-1');
    if (first) first.focus();
  }
  function closeMenu(){
    toggle.classList.remove('open');
    nav.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open menu');
    document.body.classList.remove('nav-open');
    if (logo) logo.removeAttribute('tabindex');
    toggle.focus();
  }

  toggle.addEventListener('click', function(){ isOpen() ? closeMenu() : openMenu(); });

  document.addEventListener('keydown', function(e){
    if (!isOpen()) return;
    if (e.key === 'Escape') { e.preventDefault(); closeMenu(); return; }
    if (e.key === 'Tab') {
      if (e.shiftKey && (document.activeElement === toggle || document.activeElement === first)) {
        e.preventDefault(); if (last) last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault(); toggle.focus();
      }
    }
  });

  document.addEventListener('click', function(e){
    if (!isOpen()) return;
    if (nav.contains(e.target) || toggle.contains(e.target)) return;
    closeMenu();
  });

  nav.addEventListener('click', function(e){
    if (e.target.closest && e.target.closest('a')) closeMenu();
  });
})();
