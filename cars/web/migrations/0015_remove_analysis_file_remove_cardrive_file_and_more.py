# Generated by Django 4.2.1 on 2023-06-08 10:16

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("web", "0014_alter_analysis_max_range_margin_km_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="analysis",
            name="file",
        ),
        migrations.RemoveField(
            model_name="cardrive",
            name="file",
        ),
        migrations.RemoveField(
            model_name="drive",
            name="file",
        ),
        migrations.DeleteModel(
            name="DataFile",
        ),
    ]
