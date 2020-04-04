from django.contrib import admin
from activation import models


class UserAdmin(admin.ModelAdmin):
    model = models.User
    list_display = ["id", "email", "first_name", "last_name", "mobile", "website"]
    list_display_links = ["id", "email"]
    search_fields = ["email", "first_name", "last_name"]


class SoftwareAdmin(admin.ModelAdmin):
    model = models.Software
    list_display = ["id", "name", "version", "is_active", "author", "short_description", "created_on"]


class OrderAdmin(admin.ModelAdmin):
    model = models.Order
    list_display = ["id", "reference", "software", "license", "email", "amount", "currency", "license_key", "is_paid", "is_used", "is_verified", "created_on"]
    search_fields = ["reference", "software__name", "email"]
    list_display_links = ["id", "reference"]
    list_filter = ["is_used", "is_paid", "is_verified", "created_on"]


class LicenseAdmin(admin.ModelAdmin):
    model = models.License
    list_display = ["id", "software", "type", "duration", "price", "currency", "created_on"]


admin.site.site_header = 'Activations Dashboard'
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Software, SoftwareAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.License, LicenseAdmin)
admin.site.register(models.Description)