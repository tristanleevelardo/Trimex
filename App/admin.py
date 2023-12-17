# faculty/admin.py
from django.contrib import admin
from .models import Faculty,Student,thirdYear,unit,Mail

admin.site.register(Faculty)
admin.site.register(Student)
admin.site.register(thirdYear)
admin.site.register(unit)
admin.site.register(Mail)

