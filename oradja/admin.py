from django.contrib import admin

from oradja.models import ApiModProperty, UmvDocument, ApiModule, ApiUser


# Register your models here.

@admin.register(ApiUser)
class ApiUserAdmin(admin.ModelAdmin):
    list_per_page = 20


@admin.register(ApiModule)
class ApiModuleAdmin(admin.ModelAdmin):
    list_per_page = 20


@admin.register(ApiModProperty)
class ApiModPropertyAdmin(admin.ModelAdmin):
    list_per_page = 20


@admin.register(UmvDocument)
class UmvDocumentAdmin(admin.ModelAdmin):
    list_per_page = 5 #small limit as there is blob in column, to speed up loading
