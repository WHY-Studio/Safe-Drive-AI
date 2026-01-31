from django.contrib import admin

from accounts.models import AccessCode


@admin.register(AccessCode)
class AccessCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_used', 'used_by', 'used_at', 'created_at')
    search_fields = ('code',)
    list_filter = ('is_used',)
