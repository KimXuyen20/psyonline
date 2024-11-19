from django.contrib import admin

from doctor.models import Doctor

# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'doctor_name', 'is_approved', 'created_at')
    list_display_links = ('user', 'doctor_name')
    list_editable = ('is_approved',)

admin.site.register(Doctor, DoctorAdmin)