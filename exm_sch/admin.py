# from django.contrib import admin
# from .models import Department

# admin.site.register(Department)

from django.contrib import admin
from .models import Department

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('dept_id', 'dept_name', 'status')
    list_filter = ('dept_name', 'status')
    search_fields = ('dept_name',)
    list_per_page = 20

admin.site.register(Department, DepartmentAdmin)
