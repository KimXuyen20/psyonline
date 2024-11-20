from django.contrib import admin

from .models import Blog

# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    list_display = ('blog_name', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('blog_name',)}



admin.site.register(Blog,BlogAdmin)