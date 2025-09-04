from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.
class Bid(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    icon = models.ImageField(upload_to='bid_icon/')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Deal(models.Model):
    DEAL_STATUS_CHOICES = {
        'new': 'новая',
        'in progress': 'в процессе',
        'completed': 'выполнена',
        'cancelled': 'отменена'
    }

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='deals'
    )
    bid = models.ForeignKey(
        Bid,
        on_delete=models.SET_NULL,
        related_name='deals',
        null=True
    )
    date_of_deal = models.DateField()
    address = models.TextField()
    status = models.CharField(choices=DEAL_STATUS_CHOICES)
    phone_number = models.CharField(max_length=13)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)