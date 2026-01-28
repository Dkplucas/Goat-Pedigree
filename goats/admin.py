from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Goat

# Unregister default Group and User models (optional)
admin.site.unregister(Group)
admin.site.unregister(User)

# Register your models with custom options
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff')

@admin.register(Goat)
class GoatAdmin(admin.ModelAdmin):
    list_display = ("name", "breed", "species", "gender", "birth_date", "registration")
    search_fields = ("name", "breed", "registration")
    list_filter = ("breed", "species", "gender")
    list_per_page = 20

