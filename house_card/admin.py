from django.contrib import admin

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
    list_display = ('id', )

@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display = ('id', )

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', )




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






@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('id', )





@admin.register(HouseCard)
class HouseCardAdmin(admin.ModelAdmin):
    list_display = ('id', )