from django.contrib import admin
from activation import models
from django.utils.translation import ugettext_lazy as _


class UserAdmin(admin.ModelAdmin):
    model = models.User
    admin_list_display = ["id", "gloxon_id", "email",  "first_name", "last_name", "website"]
    dev_list_display = ["gloxon_id", "access_key", "access_secret", "rave_public_key"]
    list_display_links = ["gloxon_id"]
    search_fields = ["email", "first_name", "last_name", "gloxon_id"]
    dev_fields = ["gloxon_id", "first_name", "last_name", "access_key", "access_secret", "website", "mobile", "rave_public_key",  "rave_secret_key"]
    readonly_fields = ["gloxon_id", "access_key", "access_secret", 'first_name', "last_name"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.id)

    def get_list_display(self, request):
        if request.user.is_superuser:
            return self.admin_list_display
        else:
            return self.dev_list_display

    def get_search_fields(self, request):
        if request.user.is_superuser:
            return self.search_fields
        else:
            return []

    def get_fields(self, request, obj=None):
        fields = super(UserAdmin, self).get_fields(request, obj)
        if request.user.is_superuser:
            return fields
        else:
            return self.dev_fields


class LicenseInline(admin.TabularInline):
    model = models.License
    list_display = ["type", "duration", "price", "currency", "created_on"]
    max_num = 2


class DescriptionInline(admin.TabularInline):
    model = models.Description
    list_display = ['title', 'content', 'index']
    ordering = ['index', 'title']
    extra = 1


class SoftwareAdmin(admin.ModelAdmin):
    inlines = [LicenseInline, DescriptionInline]
    model = models.Software
    list_display = ["id", "name", "version", "is_active", "author", "short_description", "created_on"]
    list_display_links = ['id', 'name']
    exclude = ['author']

    def get_exclude(self, request, obj=None):
        if request.user.is_superuser:
            return []
        else:
            return self.exclude

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)


class OrderAdmin(admin.ModelAdmin):
    model = models.Order
    list_display = ["id", "reference", "software", "license", "email", "amount", "currency", "license_key", "is_paid", "is_used", "is_verified", "created_on"]
    search_fields = ["reference", "software__name", "email"]
    list_display_links = ["id", "reference"]
    list_filter = ["is_used", "is_paid", "is_verified", "created_on"]

    exclude = ['payment_response']

    def get_exclude(self, request, obj=None):
        if request.user.is_superuser:
            return []
        else:
            return self.exclude

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(software__author=request.user)


admin.site.site_header = _('Activations Dashboard')
admin.site.site_title = _('Activations Dashboard')
admin.site.index_title = _('License Administration')
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Software, SoftwareAdmin)
admin.site.register(models.Order, OrderAdmin)

