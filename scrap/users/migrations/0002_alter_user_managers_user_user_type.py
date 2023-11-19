# Generated by Django 4.2.1 on 2023-11-19 13:18

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[],
        ),
        migrations.AddField(
            model_name="user",
            name="user_type",
            field=models.CharField(
                choices=[
                    (users.models.UserType["CUSTOMER"], "customer"),
                    (users.models.UserType["EMPLOYEE"], "employee"),
                ],
                default="customer",
                max_length=10,
            ),
        ),
    ]