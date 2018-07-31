from django.contrib import admin
from .models import OAuth_type, OAuth_ex


class OAuthTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type_name', 'title', 'img']


class OAuthAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'openid', 'oauth_type']


admin.site.register(OAuth_type, OAuthTypeAdmin)
admin.site.register(OAuth_ex, OAuthAdmin)





