# Generated by Django 4.1.5 on 2023-04-16 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("attendance", "0026_alter_employee_employee_status_and_more"),
    ]

    operations = [
        migrations.DeleteModel(name="Employee_Status",),
    ]
