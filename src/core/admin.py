from django.contrib import admin

from core import models


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('msisdn', 'status', 'created_by', 'deleted_by', 'date_inserted', 
            'date_updated', )
    search_fields = ('msisdn', )
    readonly_fields = ['created_by', 'deleted_by', ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()

admin.site.disable_action('delete_selected')
admin.site.register(models.Customer, CustomerAdmin)
