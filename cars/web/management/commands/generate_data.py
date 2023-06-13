import random
import string
from datetime import datetime
from django.contrib.gis.geos import Point
from django.core.management import BaseCommand
from django.utils.timezone import make_aware

from web.models import CarTypes, Drive, CarDrive

#
# def generate_random_date(min_date: datetime, max_date: datetime):
#     date_range = (max_date - min_date).total_seconds()
#     random_seconds = random.randint(0, int(date_range))
#     random_date = min_date + timedelta(seconds=random_seconds)
#
#     return random_date
#
#
# def generate_trip_dates(trip_distance_km, car_manufacture_date):
#     travel_time_hours = timedelta(hours=(trip_distance_km / 50))
#
#     earliest_date = car_manufacture_date
#     latest_date = datetime.now() - travel_time_hours
#
#     start_date = generate_random_date(earliest_date, latest_date)
#     end_date = start_date + travel_time_hours
#
#     return start_date, end_date


def generate_random_point():
    min_lon, min_lat = 12.765721, 51.10789
    max_lon, max_lat = 17.765611, 45.758834

    lon = random.uniform(min_lon, max_lon)
    lat = random.uniform(min_lat, max_lat)

    return lon, lat


class Command(BaseCommand):
    help = "Generate random cars and their drives"

    def add_arguments(self, parser):
        parser.add_argument(
            "--num_cars",
            dest="num_cars",
            help="Number of cars to generate",
            required=True,
            type=int,
        )
        parser.add_argument(
            "--num_drives",
            dest="num_drives",
            help="Number of drives each car should make",
            required=True,
            type=int,
        )
        parser.add_argument(
            "--min_distance_km",
            dest="min_distance_km",
            help="Minimum distance of car trip",
            required=True,
            type=int,
        )
        parser.add_argument(
            "--max_distance_km",
            dest="max_distance_km",
            help="Maximum distance of car trip",
            required=True,
            type=int,
        )
        # parser.add_argument(
        #     "--mean_drive_distance",
        #     dest="mean_drive_distance",
        #     help="Mean value of each drive distance",
        #     required=True,
        #     type=int,
        # )

    def handle(self, *args, **options):
        num_cars = options["num_cars"]
        num_drives = options["num_drives"]
        min_distance_km = options["min_distance_km"]
        max_distance_km = options["max_distance_km"]

        default_car = CarTypes.objects.get(name="Kodiaq 2.0 TDI automat")

        for _ in range(num_cars):
            car_years_old = round(random.normalvariate(5, 3))
            current_year = datetime.now().year

            care_made_date = datetime(current_year - car_years_old, 1, 1)

            def rand_string(length: int):
                return "".join(random.choices(string.ascii_uppercase, k=length))

            license_plate = f"{rand_string(3)}-{rand_string(4)}"

            car_drive, _ = CarDrive.objects.get_or_create(
                license_plate=license_plate,
                type=default_car,
                year_made=make_aware(care_made_date),
            )

            for _ in range(num_drives):
                # trip_distance_km = random.normalvariate(mean_drive_distance, mean_drive_distance/3)
                # odometer_end_km += trip_distance_km

                # time_start, time_stop = generate_trip_dates(trip_distance_km, care_made_date)

                # generate_random_point()

                points_distance_km = 0

                while (
                    points_distance_km < min_distance_km
                    or points_distance_km > max_distance_km
                ):
                    # TODO
                    point_start = Point(*generate_random_point())
                    point_stop = Point(*generate_random_point())

                    points_distance_km = point_start.distance(point_stop) * 100

                print(points_distance_km)
                Drive.objects.create(
                    car=car_drive,
                    location_start=point_start,
                    location_stop=point_stop,
                )

                # print(drive)
