# Create your models here.
from django.contrib.gis.db.models import PointField
from django.db import models
from django.urls import reverse

Manufacturers = models.TextChoices("Manufacturers", "SKODA VW")
EngineTypes = models.TextChoices("EngineTypes", "GAS DIESEL ELECTRIC HYBRID")


class CarTypes(models.Model):
    name = models.CharField(max_length=128)
    manufacturer = models.CharField(choices=Manufacturers.choices)
    engine_type = models.CharField(choices=EngineTypes.choices)
    emissions_fuel_per_km = models.PositiveIntegerField(default=0)
    max_range_km = models.PositiveIntegerField(default=0)
    cost_new = models.PositiveIntegerField(default=0)

    @property
    def range(self):
        if self.engine_type == EngineTypes.ELECTRIC:
            return self.max_range_km

        return float("inf")

    def __str__(self):
        return f"{self.manufacturer} {self.name}"


# class DataFile(models.Model):
#     file_name = models.CharField()


class CarDrive(models.Model):
    license_plate = models.CharField()
    type = models.ForeignKey(
        CarTypes,
        on_delete=models.CASCADE,
        null=True,
    )
    proposed_type = models.ForeignKey(
        CarTypes,
        on_delete=models.CASCADE,
        null=True,
        default=None,
        related_name="proposed",
        blank=True,
    )
    # file = models.ForeignKey(DataFile, on_delete=models.CASCADE, related_name="cars")
    # odometer_km = models.IntegerField(default=0)
    year_made = models.DateTimeField()
    frozen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.license_plate} - {self.type}"

    def get_absolute_url(self):
        return reverse("cars_file_update", args=[str(self.id)])


class Drive(models.Model):
    # file = models.ForeignKey(DataFile, on_delete=models.CASCADE, related_name="drives")
    car = models.ForeignKey(CarDrive, on_delete=models.CASCADE, related_name="drives")

    # distance_km = models.PositiveIntegerField()
    # odometer_end_km = models.IntegerField()

    location_start = PointField()
    location_stop = PointField()

    # time_start = models.DateTimeField()
    # time_stop = models.DateTimeField()


class Analysis(models.Model):
    # file = models.ForeignKey(DataFile, on_delete=models.CASCADE, related_name="analysis")

    replace_min_age_years = models.PositiveIntegerField()
    replace_min_odometer_km = models.PositiveIntegerField()
    max_range_margin_km = models.PositiveIntegerField(default=0)
