document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.js-room-trigger').forEach((trigger) => {
        trigger.addEventListener('click', () => {
            const dialog = document.getElementById(trigger.dataset.roomDialog);
            if (!dialog) return;
            trigger.classList.add('is-opening');
            window.setTimeout(() => {
                dialog.showModal();
                trigger.classList.remove('is-opening');
            }, window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 520);
        });
    });

    document.querySelectorAll('.room-dialog').forEach((dialog) => {
        dialog.querySelector('.js-dialog-close')?.addEventListener('click', () => dialog.close());
        dialog.addEventListener('click', (event) => {
            const bounds = dialog.getBoundingClientRect();
            const outside = event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom;
            if (outside) dialog.close();
        });
    });
});
