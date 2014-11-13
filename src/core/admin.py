from django.contrib import admin
from django.core.cache import cache

from simple_history.admin import SimpleHistoryAdmin

from core import models


class CustomerAdmin(SimpleHistoryAdmin):
    list_display = ('msisdn', 'created_by', 'date_inserted')
    search_fields = ('msisdn', )
    readonly_fields = ['created_by']
    actions = ['delete_selected']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        cache.delete('blacklist')
        obj.save()

admin.site.disable_action('delete_selected')
admin.site.register(models.Customer, CustomerAdmin)
