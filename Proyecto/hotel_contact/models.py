from django.db import models


class ContactMessage(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'Nuevo'
        READ = 'read', 'Leído'
        ANSWERED = 'answered', 'Respondido'

    name = models.CharField(max_length=140)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    subject = models.CharField(max_length=160)
    message = models.TextField()
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'mensaje de contacto'
        verbose_name_plural = 'mensajes de contacto'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.name} - {self.subject}'

# Create your models here.
