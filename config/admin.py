from django.contrib import admin
from config.models import SideBar, Link
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin
# Register your models here.


@admin.register(SideBar, site=custom_site)
class SideBarAdmin(BaseOwnerAdmin):
    list_display = (
        'title',
        'display_type',
        'status',
        'created_time',
        'owner',
    )

    fields = (
        'title',
        'display_type',
        'content',
    )
    search_fields = ('title',)


@admin.register(Link, site=custom_site)
class LinkAdmin(BaseOwnerAdmin):
    list_display = (
        'title',
        'href',
        'status',
        'weight',
        'owner',
        'created_time',
    )
    fields = (
        'title',
        'href',
        'weight',
        'status',
    )

