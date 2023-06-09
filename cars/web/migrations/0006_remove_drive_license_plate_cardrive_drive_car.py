# Generated by Django 4.2.1 on 2023-06-02 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("web", "0005_drive_location_start_drive_location_stop"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="drive",
            name="license_plate",
        ),
        migrations.CreateModel(
            name="CarDrive",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("license_plate", models.CharField()),
                (
                    "file",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cars",
                        to="web.datafile",
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="web.cartypes"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="drive",
            name="car",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="drives",
                to="web.cardrive",
            ),
            preserve_default=False,
        ),
    ]
