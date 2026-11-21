document.addEventListener('DOMContentLoaded', () => {
    const estimate = document.querySelector('[data-reservation-estimate]');
    if (estimate) {
        const form = document.querySelector('.hotel-form');
        const checkIn = form.querySelector('#id_check_in_date');
        const checkOut = form.querySelector('#id_check_out_date');
        const guests = form.querySelector('#id_guests');
        const serviceData = JSON.parse(document.getElementById('reservation-service-pricing').textContent);
        const roomTotal = estimate.querySelector('[data-estimate-room]');
        const servicesTotal = estimate.querySelector('[data-estimate-services]');
        const estimatedTotal = estimate.querySelector('[data-estimate-total]');
        const message = estimate.querySelector('[data-estimate-message]');
        const roomRate = Number(estimate.dataset.roomRate);
        const currency = new Intl.NumberFormat('es-CO', {
            style: 'currency', currency: 'COP', maximumFractionDigits: 0,
        });

        const updateEstimate = () => {
            const start = Date.parse(checkIn.value);
            const end = Date.parse(checkOut.value);
            const guestCount = Number(guests.value);
            const nights = Math.round((end - start) / 86400000);
            if (!Number.isFinite(start) || !Number.isFinite(end) || nights < 1 || guestCount < 1) {
                roomTotal.textContent = '—';
                servicesTotal.textContent = '—';
                estimatedTotal.textContent = '—';
                message.textContent = 'Elija fechas válidas para calcular un valor aproximado.';
                return;
            }

            const roomAmount = roomRate * nights;
            let servicesAmount = 0;
            form.querySelectorAll('input[name="services"]:checked').forEach((input) => {
                const service = serviceData[input.value];
                if (!service) return;
                const quantity = service.unit === 'night' ? nights : service.unit === 'person' ? guestCount : 1;
                servicesAmount += Number(service.price) * quantity;
            });
            roomTotal.textContent = currency.format(roomAmount);
            servicesTotal.textContent = currency.format(servicesAmount);
            estimatedTotal.textContent = currency.format(roomAmount + servicesAmount);
            message.textContent = `Estimado para ${nights} noche${nights === 1 ? '' : 's'}. El hotel confirmará la disponibilidad.`;
        };

        form.addEventListener('input', updateEstimate);
        form.addEventListener('change', updateEstimate);
        updateEstimate();
    }

    const dialog = document.getElementById('reservation-confirmation');
    if (!dialog) return;
    dialog.showModal();
    dialog.querySelectorAll('.js-confirmation-close').forEach((button) => {
        button.addEventListener('click', () => dialog.close());
    });
});
