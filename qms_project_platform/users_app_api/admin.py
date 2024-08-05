from django.contrib import admin
from .models import UserSessionModel, MyAPIKeyModel

@admin.register(UserSessionModel)
class UserSessionModelAdmin(admin.ModelAdmin):  
    list_display = ('id', 'user', 'token', 'created_at', 'expires_at')
    search_fields = ('id', 'user__username', 'token')

@admin.register(MyAPIKeyModel)
class MyAPIKeyModelAdmin(admin.ModelAdmin):  
    list_display = ('key', 'description', 'is_active', 'created_at')
    search_fields = ('key', 'description')
