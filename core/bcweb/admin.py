from django.contrib import admin
from .models import Certificate, User, Company

admin.site.register(Certificate)
admin.site.register(User)
admin.site.register(Company)