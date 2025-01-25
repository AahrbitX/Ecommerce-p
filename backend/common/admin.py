from django.contrib import admin
from django.apps import apps
from django.contrib.auth.admin import UserAdmin
from common.models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'role', 'is_active')
    list_filter = ('role', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'role', 'is_active',)}),
        ('Permissions', {'fields': ('is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
     
    search_fields = ('email',)
    ordering = ('email',)

    def has_change_permission(self, request, obj=None):
        return request.user.has_perm('common.change_customuser')   

    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm('common.delete_customuser')   

    def has_add_permission(self, request):
        return request.user.has_perm('common.add_customuser')   


admin.site.register(CustomUser, CustomUserAdmin)
app = apps.get_app_config('common')  
for model in app.get_models():
    if model != CustomUser:
     admin.site.register(model)

