from django.contrib import admin

from .import models


class OfficeAdmin(admin.ModelAdmin):
    list_display = ('named', 'location', 'picture')
    search_fields = ['named']
    list_filter = ['location']

admin.site.register(models.OfficesModel, OfficeAdmin)

# Register your models here.


class Member(admin.ModelAdmin):
    list_display = ('l_name', 'f_name', 'position', 'user_id')
    search_fields = ['l_name']
    list_filter = ['position']

admin.site.register(models.MembersModel, Member)