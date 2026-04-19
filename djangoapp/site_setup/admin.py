from re import S

from django.contrib import admin
from django.http import HttpRequest

from site_setup.models import MenuLink, SiteSetup

# Register your models here.


@admin.register(MenuLink)
class MenuLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'url_or_path', 'new_tab')
    list_display_links = ('id', 'text', 'url_or_path')
    search_fields = ('id', 'text', 'url_or_path')

@admin.register(SiteSetup)
class SiteSetupAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')

    def has_add_permission(self, request: HttpRequest) -> bool:
        return not SiteSetup.objects.exists()   
