from django.contrib import admin
from .models import User


# Register your models here.
# admin.site.register(User)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['username', 'first_name', 'last_name']
    list_display = ['__str__', 'first_name', 'last_name']
    list_filter = (
        ('username', admin.AllValuesFieldListFilter),
        ('created_at', admin.DateFieldListFilter),
    )
