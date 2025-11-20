from django.contrib import admin


from .models import Check
# Register your models here.
@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'get_username_name', 'house_card', 'paid')
    autocomplete_fields = ['username', 'house_card', 'tariff']
# Register your models here.

    list_select_related = ['username', 'house_card']  # Оптимизация запросов
    
    def get_username_name(self, obj):
        return obj.username.name if obj.username else '-'
    
    get_username_name.short_description = 'Имя пользователя'
    get_username_name.admin_order_field = 'username__name'

    search_fields = [
        'house_card__house_card', 
        'house_card__old_house_card', 
        'username__email',
        'username__name',
        'house_card__address__street__name'
    ]

from .models import PaymentTransaction
# Register your models here.
@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', )