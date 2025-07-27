from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # <-- important
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from accounts.models import User, Address, UserActivityLog, SellerAccount

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ('id', 'username', 'email', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'gender', 'date_of_birth', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'street', 'city', 'state', 'postal_code', 'country')
    search_fields = ('user__username', 'street', 'city', 'state', 'postal_code')
    
@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'timestamp')
    search_fields = ('user__username', 'activity_type')
    list_filter = ('activity_type', 'timestamp')
    ordering = ('-timestamp',)

@admin.register(SellerAccount)
class SellerAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'store_name', 'is_active', 'created_at')
    search_fields = ('user__username', 'store_name')
    list_filter = ('created_at', 'updated_at', 'is_active')