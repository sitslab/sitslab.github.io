(() => {
  document.querySelectorAll('[data-carousel]').forEach((carousel) => {
    const slides = Array.from(carousel.querySelectorAll('.group-photo'));
    const controls = carousel.querySelector('[data-carousel-controls]');
    const previous = carousel.querySelector('[data-carousel-prev]');
    const next = carousel.querySelector('[data-carousel-next]');
    const pause = carousel.querySelector('[data-carousel-pause]');
    const counter = carousel.querySelector('[data-carousel-counter]');
    const dots = Array.from(carousel.querySelectorAll('[data-carousel-dot]'));
    if (slides.length < 2 || !controls || !previous || !next || !pause || !counter || dots.length !== slides.length) return;

    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    let index = 0;
    let paused = reducedMotion.matches;
    let hovered = false;
    let focused = false;
    let timer;

    const stop = () => {
      window.clearTimeout(timer);
      timer = undefined;
    };
    const updatePause = () => {
      pause.textContent = paused ? pause.dataset.playLabel : pause.dataset.pauseLabel;
      pause.setAttribute('aria-label', pause.textContent);
    };
    const show = (requestedIndex) => {
      index = (requestedIndex + slides.length) % slides.length;
      slides.forEach((slide, i) => { slide.hidden = i !== index; });
      dots.forEach((dot, i) => { dot.setAttribute('aria-current', i === index ? 'true' : 'false'); });
      counter.textContent = `${index + 1} / ${slides.length}`;
    };
    const schedule = () => {
      stop();
      if (paused || hovered || focused || document.hidden) return;
      timer = window.setTimeout(() => {
        show(index + 1);
        schedule();
      }, 5000);
    };
    const select = (requestedIndex) => {
      show(requestedIndex);
      schedule();
    };

    previous.addEventListener('click', () => select(index - 1));
    next.addEventListener('click', () => select(index + 1));
    dots.forEach((dot, i) => dot.addEventListener('click', () => select(i)));
    pause.addEventListener('click', () => {
      paused = !paused;
      updatePause();
      schedule();
    });
    carousel.addEventListener('mouseenter', () => { hovered = true; stop(); });
    carousel.addEventListener('mouseleave', () => { hovered = false; schedule(); });
    carousel.addEventListener('focusin', () => { focused = true; stop(); });
    carousel.addEventListener('focusout', (event) => {
      if (!carousel.contains(event.relatedTarget)) { focused = false; schedule(); }
    });
    carousel.addEventListener('keydown', (event) => {
      if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
        event.preventDefault();
        select(index + (event.key === 'ArrowRight' ? 1 : -1));
      }
    });
    document.addEventListener('visibilitychange', schedule);
    reducedMotion.addEventListener('change', () => {
      paused = reducedMotion.matches;
      updatePause();
      schedule();
    });

    show(0);
    updatePause();
    controls.hidden = false;
    carousel.classList.add('is-ready');
    schedule();
  });
})();
