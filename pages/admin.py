from django.contrib import admin
from .models import FeedBack, Contact, Terms, Setting


# Register your models here.


class FeedBackAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name",
                    "phone_number", "email", "short_description"]
    search_fields = ("first_name", "last_name", "phone_number",
                     "email", "short_description",)
    list_per_page = 20


admin.site.register(FeedBack, FeedBackAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "ad_url",
                    "phone_number", "short_description"]
    search_fields = ("name", "email", "phone_number", "short_description")
    list_per_page = 20


admin.site.register(Contact, ContactAdmin)


class TermsAdmin(admin.ModelAdmin):
    list_display = ["name", "short_description"]
    search_fields = ("name", "short_description")
    list_per_page = 20


admin.site.register(Terms, TermsAdmin)


class SettingAdmin(admin.ModelAdmin):
    list_display = ["name", "location", "email", "phone_number"]
    search_fields = ("name", "location", "email", "phone_number")
    list_per_page = 20

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else True


admin.site.register(Setting, SettingAdmin)
