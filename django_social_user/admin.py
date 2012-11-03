from django.contrib import admin

from django_social_user.models import SocialIdentity

class SocialIdentityAdmin(admin.ModelAdmin):
    list_display = ['username', 'network', 'uid']
    search_fields = ('username', 'first_name', 'last_name')
    ordering = ['username']
    readonly_fields = ['_data']

admin.site.register(SocialIdentity, SocialIdentityAdmin)
