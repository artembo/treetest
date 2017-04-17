from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from tree.models import Referat

admin.site.register(Referat, MPTTModelAdmin)