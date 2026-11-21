from django import forms

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ('name', 'email', 'phone', 'subject', 'message')
        labels = {
            'name': 'Nombre',
            'email': 'Correo electrónico',
            'phone': 'Teléfono',
            'subject': 'Asunto',
            'message': 'Mensaje',
        }
        widgets = {
            'name': forms.TextInput(attrs={'autocomplete': 'name'}),
            'email': forms.EmailInput(attrs={'autocomplete': 'email'}),
            'phone': forms.TextInput(attrs={'autocomplete': 'tel'}),
            'subject': forms.TextInput(),
            'message': forms.Textarea(attrs={'rows': 6}),
        }
