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

@admin.register(CounterCause)
class CounterCauseAdmin(admin.ModelAdmin):
    list_display = ('id', )

@admin.register(CounterType)
class CounterTypeAdmin(admin.ModelAdmin):
    list_display = ('id', )

@admin.register(Counter)
class CounterAdmin(admin.ModelAdmin):
    list_display = ('id', )





@admin.register(Plot)
class PlotAdmin(admin.ModelAdmin):
    list_display = ('id', )

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('id', )





class TariffBandInline(admin.TabularInline):
    model = TariffBand
    extra = 1
@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    inlines = [TariffBandInline]
    list_display = ('id', )





@admin.register(HouseCard)
class HouseCardAdmin(ImportExportModelAdmin):
    resource_class = HouseCardImportResource
    list_display = [
        'house_card', 
        'old_house_card', 
        'user', 
        'address', 
        'contract_number',
        'tp_number'
    ]
    list_filter = ['tp_number', 'contract_date']
    search_fields = [
        'house_card', 
        'old_house_card', 
        'user__name',
        'address__street__name'
    ]
    readonly_fields = ['registered_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': (
                'house_card', 
                'old_house_card',
                'user', 
                'address',
            )
        }),
        ('Договорные данные', {
            'fields': (
                'contract_number',
                'contract_date', 
                'tp_number',
            )
        }),
        ('Технические данные', {
            'fields': (
                'household_needs',
                'fact_summer', 
                'fact_winter',
                'max_summer', 
                'max_winter',
            )
        }),
        ('Финансовые данные', {
            'fields': (
                'overpayment_underpayment',
                'penalty',
            )
        }),
        ('Системные данные', {
            'fields': (
                'registered_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )