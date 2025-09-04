from django.contrib import admin


from .models import PushNotificationLog, ExpoPushToken
# Register your models here.
@admin.register(ExpoPushToken)
class ExpoPushTokenAdmin(admin.ModelAdmin):
    list_display = ('id', )

@admin.register(PushNotificationLog)
class PushNotificationLogAdmin(admin.ModelAdmin):
    list_display = ('id', )