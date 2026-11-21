document.addEventListener('DOMContentLoaded', () => {
    const carousel = document.querySelector('.hero-carousel');
    if (!carousel) return;

    const slides = [...carousel.querySelectorAll('.hero-slide')];
    const stories = [...carousel.querySelectorAll('.hero-story[data-story]')];
    const dots = [...carousel.querySelectorAll('.carousel-dot')];
    let activeIndex = 0;
    let timer;

    const showSlide = (nextIndex) => {
        if (!slides.length) return;
        activeIndex = (nextIndex + slides.length) % slides.length;
        slides.forEach((slide, index) => {
            const active = index === activeIndex;
            slide.classList.toggle('is-active', active);
            slide.setAttribute('aria-hidden', String(!active));
        });
        stories.forEach((story, index) => {
            const active = index === activeIndex;
            story.classList.toggle('is-active', active);
            story.setAttribute('aria-hidden', String(!active));
        });
        dots.forEach((dot, index) => {
            const active = index === activeIndex;
            dot.classList.toggle('is-active', active);
            dot.setAttribute('aria-current', String(active));
        });
    };

    const stop = () => window.clearInterval(timer);
    const start = () => {
        stop();
        if (slides.length > 1) timer = window.setInterval(() => showSlide(activeIndex + 1), 5000);
    };

    carousel.querySelector('.js-carousel-prev')?.addEventListener('click', () => { showSlide(activeIndex - 1); start(); });
    carousel.querySelector('.js-carousel-next')?.addEventListener('click', () => { showSlide(activeIndex + 1); start(); });
    dots.forEach((dot) => dot.addEventListener('click', () => { showSlide(Number(dot.dataset.carouselTarget)); start(); }));
    start();
});
