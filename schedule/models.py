from django.db import models


class Appointment(models.Model):
    category = models.CharField(max_length=50, choices=(
        ('eletro', 'eletro'),
        ('musculação', 'musculação'),
    ))
    date = models.DateTimeField()
    client_name = models.CharField(max_length=255)
    client_phone = models.CharField(max_length=255)
    description = models.TextField()
    feedback = models.BooleanField(default=False, blank=False, null=False)

    def __str__(self) -> str:
        return f'{self.category} - {self.date} - {self.client_name}'
