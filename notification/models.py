from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ExpoPushToken(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='expo_tokens'
    )
    token = models.CharField(max_length=255, unique=True)
    device_type = models.CharField(max_length=20, choices=(('ios', 'iOS'), ('android', 'Android')))
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.device_type}"