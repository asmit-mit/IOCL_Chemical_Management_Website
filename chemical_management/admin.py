from django.contrib import admin

from .models import ChemicalMaster, DailyConsumptions

# Register your models here.
admin.site.register(ChemicalMaster)
admin.site.register(DailyConsumptions)
