# Generated by Django 4.2.1 on 2023-06-02 17:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("web", "0007_alter_cardrive_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="cardrive",
            name="odometer_km",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]