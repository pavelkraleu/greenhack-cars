# Register your models here.

from django.contrib import admin
from django.contrib.gis.db.models import PointField
from django.contrib.gis.forms import OSMWidget

from web.models import CarTypes, Drive, CarDrive


# @admin.register(DataFile)
# class DataFileAdmin(admin.ModelAdmin):
#     pass


@admin.register(CarTypes)
class CarTypesAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "engine_type",
        "max_range_km",
        "emissions_fuel_per_km",
        "cost_new",
    ]


@admin.register(CarDrive)
class CarDriveAdmin(admin.ModelAdmin):
    pass


@admin.register(Drive)
class DriveAdmin(admin.ModelAdmin):
    formfield_overrides = {
        PointField: {
            "widget": OSMWidget(attrs={"map_type": "roadmap"}),
        }
    }
