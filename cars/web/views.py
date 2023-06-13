# Create your views here.
from collections import defaultdict
from datetime import datetime, timezone

from django.contrib.gis.db.models.functions import Distance
from django.db.models import F, Sum, QuerySet, Count, Prefetch
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    TemplateView,
)

from web.forms import CarDriveForm, AnalysisForm
from web.models import Drive, CarDrive, Analysis, CarTypes, EngineTypes

qs_cars_with_details = (
    CarDrive.objects.annotate(
        distance_total=Sum(
            Distance(F("drives__location_start"), F("drives__location_stop"))
        )
    )
    .annotate(distance_avg=F("distance_total") / 1000 / Count("drives"))
    .annotate(
        original_emissions_total_t=(
            (F("distance_total") / 1000) * F("type__emissions_fuel_per_km")
        )
        / 1000000
    )
    .annotate(
        proposed_emissions_total_t=(
            (F("distance_total") / 1000) * F("proposed_type__emissions_fuel_per_km")
        )
        / 1000000
    )
)


class DriveDetail(DetailView):
    queryset = Drive.objects.all()
    template_name = "base.html"


class DataFileDetail(TemplateView):
    # queryset = DataFile.objects.all()
    template_name = "data_file_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["original_number_of_cars"] = CarDrive.objects.count()
        context["proposed_number_of_cars"] = CarDrive.objects.filter(
            proposed_type__isnull=False
        ).count()

        def sum_column(qs: QuerySet, column_name: str):
            return round(sum(qs.values_list(column_name, flat=True)))

        context["original_emissions_total"] = sum_column(
            qs_cars_with_details, "original_emissions_total_t"
        )
        context["proposed_emissions_total"] = sum_column(
            qs_cars_with_details.filter(proposed_type__isnull=False),
            "proposed_emissions_total_t",
        )

        context["percentage_decrease_emissions"] = round(
            (
                (
                    context["original_emissions_total"]
                    - context["proposed_emissions_total"]
                )
                / context["original_emissions_total"]
            )
            * 100
        )

        context["total_sum_refresh"] = CarDrive.objects.filter(
            proposed_type__isnull=False
        ).aggregate(Sum("proposed_type__cost_new"))["proposed_type__cost_new__sum"]

        context["original_distances_sum"] = round(
            sum(
                [
                    v.km
                    for v in qs_cars_with_details.values_list(
                        "distance_total", flat=True
                    )
                ]
            )
        )
        context["proposed_distances_sum"] = round(
            sum(
                [
                    v.km
                    for v in qs_cars_with_details.filter(
                        proposed_type__isnull=False
                    ).values_list("distance_total", flat=True)
                ]
            )
        )

        original_car_type_counter = defaultdict(int)
        proposed_car_type_counter = defaultdict(int)

        for car in qs_cars_with_details.filter().all():
            original_car_type_counter[car.type.name] += 1

        for car in qs_cars_with_details.filter(proposed_type__isnull=False).all():
            proposed_car_type_counter[car.proposed_type.name] += 1

        context["original_car_type_keys"] = list(original_car_type_counter.keys())
        context["original_car_type_values"] = list(original_car_type_counter.values())

        context["proposed_car_type_keys"] = list(proposed_car_type_counter.keys())
        context["proposed_car_type_values"] = list(proposed_car_type_counter.values())

        # for d in qs_cars_with_distance.all():
        #     print(d)
        #     print(d.emissions_total)

        # for car in qs_cars_with_distance.all():
        #     current_cars_emissions.append(car.distance.km * car.type.emissions_fuel_per_km)

        # proposed_cars_emissions = []
        # current_cars_emissions = []
        # current_cars_distance = []
        # proposed_cars_distance = []
        # car_type_counter = defaultdict(int)
        # car_proposed_type_counter = defaultdict(int)
        #
        # fleet_refresh_cost = 0

        # for car in qs_cars_with_distance.filter(proposed_type__isnull=False).all():
        #     proposed_cars_emissions.append(car.distance.km * car.proposed_type.emissions_fuel_per_km)
        #     car_proposed_type_counter[car.proposed_type.name] += 1
        #     fleet_refresh_cost += car.proposed_type.cost_new
        #
        # for car in qs_cars_with_distance.all():
        #     current_cars_emissions.append(car.distance.km * car.type.emissions_fuel_per_km)
        #     car_type_counter[car.type.name] += 1
        #     current_cars_distance.append(car.distance.km)
        #     proposed_cars_distance.append(car.distance.km)
        #
        # initial_emissions = sum(current_cars_emissions)
        # proposed_emissions = sum(proposed_cars_emissions)
        #
        # percentage_decrease_emissions = round(((initial_emissions - proposed_emissions) / initial_emissions) * 100)
        #
        # context["all_current_cars_emissions"] = sum(current_cars_emissions)
        # context["all_current_cars_max_distance"] = max(current_cars_distance)
        # context["all_current_cars_avg_distance"] = round(sum(current_cars_distance) / len(current_cars_distance))
        # context["all_current_cars_sum_distance"] = sum(current_cars_distance)
        #
        # context["all_current_cars_types_keys"] = list(car_type_counter.keys())
        # context["all_current_cars_types_values"] = list(car_type_counter.values())
        #
        # context["all_proposed_cars_sum_distance"] = sum(proposed_cars_distance)
        # # context["all_proposed_cars_avg_distance"] = round(sum(proposed_cars_distance) / len(proposed_cars_distance))
        # # context["all_proposed_cars_max_distance"] = max(proposed_cars_distance)
        # context["all_proposed_cars_emissions"] = sum(proposed_cars_emissions)
        # context["all_proposed_cars_types_keys"] = list(car_proposed_type_counter.keys())
        # context["all_proposed_cars_types_values"] = list(car_proposed_type_counter.values())
        # context["all_proposed_cars_num"] = sum(list(car_proposed_type_counter.values()))
        #
        # context["percentage_decrease_emissions"] = percentage_decrease_emissions
        #
        # context["cost_refresh_fleet"] = fleet_refresh_cost

        return context


class CarDriveFileList(ListView):
    # model = CarDrive
    template_name = "data_file_cars_detail.html"

    # def get_queryset(self):
    #     return CarDrive.objects.annotate(
    #         distance=Distance('location_start', 'location_stop')
    #     ).all()

    def get_queryset(self):
        return qs_cars_with_details.order_by("-original_emissions_total_t")


class CarDriveEdit(UpdateView):
    model = CarDrive
    form_class = CarDriveForm
    template_name = "data_file_cars_update.html"

    def get_queryset(self):
        return CarDrive.objects.prefetch_related(
            Prefetch(
                "drives",
                queryset=Drive.objects.annotate(
                    distance=Distance(F("location_start"), F("location_stop"))
                ),
            )
        )


def get_proposed_car(current_car: CarDrive, analysis: Analysis) -> CarTypes:
    if current_car.distance_sum.km < analysis.replace_min_odometer_km:
        print(f"Car {current_car} too few kms")
        return current_car.type

    car_age = (datetime.now(timezone.utc) - current_car.year_made).days // 365
    if car_age <= analysis.replace_min_age_years:
        print(f"Car {current_car} too new")
        return current_car.type

    max_distance = 0
    for drive in current_car.drives.all():
        if max_distance < drive.distance.km:
            max_distance = drive.distance.km

    electro = (
        CarTypes.objects.filter(
            engine_type=EngineTypes.ELECTRIC, max_range_km__gt=max_distance
        )
        .order_by("max_range_km")
        .first()
    )
    if electro:
        return electro

    default_car = CarTypes.objects.get(name="Octavia 1.5 TSI manual")
    return default_car


class AnalysisCreate(CreateView):
    form_class = AnalysisForm
    template_name = "analysis_create.html"
    success_url = "/"

    def form_valid(self, form):
        self.object: Analysis = form.save()
        print(self.object)

        for car in (
            CarDrive.objects.annotate(
                distance_sum=Sum(
                    Distance(F("drives__location_start"), F("drives__location_stop"))
                )
            )
            .prefetch_related(
                Prefetch(
                    "drives",
                    queryset=Drive.objects.annotate(
                        distance=Distance(F("location_start"), F("location_stop"))
                    ),
                )
            )
            .all()
        ):
            print(car)
            car.proposed_type = get_proposed_car(car, self.object)
            car.save()
        return super().form_valid(form)
