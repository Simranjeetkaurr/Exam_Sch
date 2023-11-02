from django.contrib import admin

# Register your models here.
from .models import Department,Session

admin.site.register(Department)
admin.site.register(Session)