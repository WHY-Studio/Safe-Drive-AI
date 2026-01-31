from django.conf import settings
from django.db import models


class AccessCode(models.Model):
    code = models.CharField(max_length=64, unique=True)
    is_used = models.BooleanField(default=False)
    used_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='access_codes',
    )
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = 'used' if self.is_used else 'available'
        return f'{self.code} ({status})'
