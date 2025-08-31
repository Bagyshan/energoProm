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
