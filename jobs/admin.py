from django.contrib import admin
from .models import Employer, Job, Location


admin.site.register(Employer)
admin.site.register(Job)
admin.site.register(Location)