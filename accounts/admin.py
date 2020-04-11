from django.contrib import admin
from django.utils.html import escape, mark_safe
from .models import Profile


# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["profile_name", "email_confirmed",
                    "phone_number", "city", "user_email", "profile_pic", "active"]
    search_fields = ('user__username', 'phone_number',)
    list_filter = ['phone_number', 'user__email']
    list_editable = ['active','email_confirmed']
    list_per_page = 20

    def profile_name(self, obj):
        return obj.user.username

    def user_email(self, obj):
        return obj.user.email


admin.site.register(Profile, ProfileAdmin)
