from django.db import models
from house_card.models import HouseCard
from user.models import User

# Create your models here.
class Check(models.Model):
    personal_account = models.ForeignKey(
        HouseCard,
        on_delete=models.CASCADE,
        related_name='checks'
    )
    current_check = models.PositiveIntegerField()
    username = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='checks'
    )

    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)