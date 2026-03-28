from django.contrib import admin


from .models import Bid, Deal
# Register your models here.
@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('id', )
# Register your models here.

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('id', )





from django.contrib import admin

from django.contrib.auth.models import Group

from rest_framework.authtoken.models import Token, TokenProxy

from django_celery_beat.models import (
    PeriodicTask,
    IntervalSchedule,
    CrontabSchedule,
    SolarSchedule,
    ClockedSchedule,
)

from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken,
)

def safe_unregister(model):
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass



safe_unregister(Group)

safe_unregister(Token)
safe_unregister(TokenProxy)



safe_unregister(PeriodicTask)
safe_unregister(IntervalSchedule)
safe_unregister(CrontabSchedule)
safe_unregister(SolarSchedule)
safe_unregister(ClockedSchedule)



safe_unregister(OutstandingToken)
safe_unregister(BlacklistedToken)
