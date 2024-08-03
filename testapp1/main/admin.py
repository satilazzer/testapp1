from django.contrib import admin
from .models import Menu, MenuItem


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    fields = ['title', 'url', 'named_url', 'is_active']
    readonly_fields = ['url', 'named_url']


class MenuAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'menu', 'parent', 'url', 'named_url', 'is_active']
    list_filter = ['menu', 'parent', 'is_active']
    search_fields = ['title']


admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
