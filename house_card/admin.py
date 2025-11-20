from django.contrib import admin
from .resources import HouseCardImportResource
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin

from .models import (
    District,
    GosAdministration,
    Settlement,
    Street,
    Address,

    Executor,
    CounterCause,
    CounterType,
    Counter,

    Tariff,
    TariffBand,

    Plot,
    Route, 

    HouseCard,
)



@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', )

@admin.register(GosAdministration)
class GosAdministrationAdmin(admin.ModelAdmin):
    list_display = ('id', )

@admin.register(Settlement)
class SettlementAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display = ['name', 'settlement', 'created_at']
    list_filter = ['settlement']
    search_fields = ['name']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['street', 'house', 'liter', 'apartment', 'apartment_liter']
    list_filter = ['street']
    search_fields = ['street__name', 'house']




@admin.register(Executor)
class ExecutorAdmin(admin.ModelAdmin):
    list_display = ('id', )
    search_fields = ['name']

@admin.register(CounterCause)
class CounterCauseAdmin(admin.ModelAdmin):
    list_display = ('id', )

@admin.register(CounterType)
class CounterTypeAdmin(admin.ModelAdmin):
    list_display = ('id', )
    search_fields = ['model']

@admin.register(Counter)
class CounterAdmin(admin.ModelAdmin):
    list_display = ('id', )
    search_fields = ['serial_number', 'counter_type__model', 'executor__name']





@admin.register(Plot)
class PlotAdmin(admin.ModelAdmin):
    list_display = ('id', )
    search_fields = ['code', 'name']

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('id', )
    search_fields = ['route_number', 'plot__name', 'plot__code']




class TariffBandInline(admin.TabularInline):
    model = TariffBand
    extra = 1
@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    inlines = [TariffBandInline]
    list_display = ('id', )
    search_fields = ['name']





@admin.register(HouseCard)
class HouseCardAdmin(ImportExportModelAdmin):
    autocomplete_fields = ['user', 'address', 'plot', 'route', 'counter', 'tariff']
    resource_class = HouseCardImportResource
    list_display = [
        'id',
        'house_card', 
        'old_house_card', 
        'user', 
        'get_user_name',
        'address',
    ]

    list_select_related = ['user', 'address']  # Оптимизация запросов
    
    def get_user_name(self, obj):
        return obj.user.name if obj.user else '-'
    
    get_user_name.short_description = 'Имя пользователя'
    get_user_name.admin_order_field = 'user__name'

    list_filter = ['tp_number', 'contract_date']
    search_fields = [
        'house_card', 
        'old_house_card', 
        'user__email',
        'user__name',
        'address__street__name'
    ]
    readonly_fields = ['registered_at', 'updated_at']
    
    # fieldsets = (
    #     ('Основная информация', {
    #         'fields': (
    #             'house_card', 
    #             'old_house_card',
    #             'user', 
    #             'address',
    #         )
    #     }),
    #     ('Договорные данные', {
    #         'fields': (
    #             'contract_number',
    #             'contract_date', 
    #             'tp_number',
    #         )
    #     }),
    #     ('Технические данные', {
    #         'fields': (
    #             'household_needs',
    #             'fact_summer', 
    #             'fact_winter',
    #             'max_summer', 
    #             'max_winter',
    #         )
    #     }),
    #     ('Финансовые данные', {
    #         'fields': (
    #             'overpayment_underpayment',
    #             'penalty',
    #         )
    #     }),
    #     ('Системные данные', {
    #         'fields': (
    #             'registered_at',
    #             'updated_at',
    #         ),
    #         'classes': ('collapse',)
    #     }),
    # )