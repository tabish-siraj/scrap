# Generated by Django 4.2.1 on 2023-11-29 21:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_remove_user_phone_number_personaldetails_addres1_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="personaldetails",
            name="phone_number",
        ),
        migrations.AlterField(
            model_name="personaldetails",
            name="addres1",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="personaldetails",
            name="city",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="personaldetails",
            name="country",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="personaldetails",
            name="state",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="personaldetails",
            name="status",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="personaldetails",
            name="vehicle_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("TWO_WHEELER", "two wheeler"),
                    ("THREE_WHEELER", "three wheeler"),
                    ("FOUR_WHEELER", "four wheeler"),
                ],
                max_length=13,
                null=True,
            ),
        ),
    ]
