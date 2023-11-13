from django.contrib import admin
from .models import Registered_Vehicles,Entry_Exit



class EntryExit(admin.ModelAdmin):
    list_display = ("vehicle_number","date_created")
    search_fields = ("vehicle_number",)
    ordering=("date_created",)

admin.site.register(Entry_Exit,EntryExit)

class RegVeh(admin.ModelAdmin):
    list_display = ("vehicle_number","first","uid","email","date_created")
    search_fields = ("uid","vehicle_number")
    ordering=("date_created",)

admin.site.register(Registered_Vehicles,RegVeh)
# Register your models here.
