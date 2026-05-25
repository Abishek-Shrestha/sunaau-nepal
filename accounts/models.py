from django.db import models
from django.contrib.auth.models import AbstractUser


class Municipality(models.Model):
    name = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.district}"

    class Meta:
        verbose_name_plural = "Municipalities"


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('citizen', 'Citizen'),
        ('officer', 'Municipality Officer'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='citizen')
    phone = models.CharField(max_length=15, blank=True)
    municipality = models.ForeignKey(
        Municipality,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='officers'
    )
    ward_number = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    def is_officer(self):
        return self.role == 'officer'

    def is_citizen(self):
        return self.role == 'citizen'

