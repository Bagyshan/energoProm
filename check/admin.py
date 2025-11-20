from django.contrib import admin


from .models import Check
# Register your models here.
@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ('id', )
    autocomplete_fields = ['username', 'house_card', 'tariff']
# Register your models here.


from .models import PaymentTransaction
# Register your models here.
@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', )