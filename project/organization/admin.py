from django.contrib import admin

from .models import Department
from .models import Employee

admin.site.register(Employee)
admin.site.register(Department)
