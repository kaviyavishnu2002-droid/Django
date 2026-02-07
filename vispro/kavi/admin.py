from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from cbv.models import Detail, Age_Group
from .models import movies, category,Article

# Register your models here.

User = get_user_model()

@admin.register(User)
class AuserAdmin(UserAdmin):
    model = User

    list_display = ('username', 'email', 'age', 'phone_number', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'role')
    search_fields = ('username', 'email')
    ordering = ('username',)

    # fieldsets = UserAdmin.fieldsets
    # add_fieldsets = UserAdmin.add_fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': (
                'phone_number',
                'role',
                'age',
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {
            'fields': (
                'phone_number',
                'role',
            )
        }),
    )

class PostAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        return obj.author == request.user


admin.site.register(Detail)
admin.site.register(Age_Group)

@admin.register(movies)
class MoviesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "is_published", "created_at", "user")
    search_fields = ("name", "movie_charecter")
    list_filter = ("category",)

@admin.register(category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "id")
    search_fields = ("name",)

class MyAdminSite(admin.AdminSite):
    site_header = "My Custom Admin"

custom_admin = MyAdminSite(name='myadmin')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'body')
