document.addEventListener('DOMContentLoaded', () => {
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const revealItems = document.querySelectorAll('.reveal');
    const hotelSection = document.getElementById('hotel');
    const scrollToHotel = (behavior) => {
        if (!hotelSection) return;
        const header = document.querySelector('.site-header');
        const headerHeight = header?.getBoundingClientRect().height ?? 0;
        const breathingRoom = Number.parseFloat(getComputedStyle(hotelSection).scrollMarginTop) || 56;
        const top = window.scrollY + hotelSection.getBoundingClientRect().top - headerHeight - breathingRoom;
        window.scrollTo({ top: Math.max(0, top), behavior });
    };

    if (hotelSection && window.location.hash === '#hotel') {
        requestAnimationFrame(() => scrollToHotel('auto'));
    }

    document.querySelectorAll('a[href$="#hotel"]').forEach((link) => {
        link.addEventListener('click', (event) => {
            const targetUrl = new URL(link.href, window.location.href);
            if (!hotelSection || targetUrl.origin !== window.location.origin || targetUrl.pathname !== window.location.pathname) return;
            event.preventDefault();
            if (window.location.hash !== '#hotel') history.pushState(null, '', '#hotel');
            scrollToHotel(reducedMotion ? 'auto' : 'smooth');
        });
    });

    if (reducedMotion || !('IntersectionObserver' in window)) {
        revealItems.forEach((item) => item.classList.add('is-visible'));
    } else {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
            });
        }, { threshold: 0.14 });

        revealItems.forEach((item) => observer.observe(item));
    }
});
