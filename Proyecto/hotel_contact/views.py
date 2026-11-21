from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ContactMessageForm


def contact(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gracias. Su mensaje fue recibido y será atendido por el hotel.')
            return redirect('hotel_contact:contact')
        messages.error(request, 'Revise los campos marcados para poder enviar su mensaje.')
    else:
        form = ContactMessageForm()

    return render(request, 'hotel_contact/contact.html', {'form': form})
