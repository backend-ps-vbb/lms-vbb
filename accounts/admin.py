from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email','is_superuser', 'regno', 'branch', 'section','semester','yearofadm')
    list_filter = ('email', 'is_superuser', 'branch','section',)

    fieldsets = (
        (None, {
            'fields': ('username', 'email','is_superuser', 'regno', 'branch', 'section','semester','yearofadm', 'password')
        }),
    )
admin.site.register(CustomUser, CustomUserAdmin)
