from django.contrib import admin
from django.core.cache import cache

from core import models


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'msisdn', 'created_by', 'date_inserted')
    search_fields = ('msisdn', )
    readonly_fields = ['created_by']
    actions = ['delete_selected']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        cache.delete(str(obj.msisdn))
        obj.save()
        cache.set(str(obj.msisdn), obj, None)

    def delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()
            cache.delete(obj.msisdn)
            models.CustomerHistory.objects.create(
                msisdn=obj.msisdn,
                created_by=obj.created_by,
                date_inserted=obj.date_inserted,
                action=models.CustomerHistory.ACTION_DELETE,
                history_changed_by=request.user
            )


class CustomerHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'msisdn', 'created_by', 'date_inserted', 'history_changed_by')
    search_fields = ('msisdn', )
    readonly_fields = ['created_by']


admin.site.disable_action('delete_selected')
admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.CustomerHistory, CustomerHistoryAdmin)
