# Generated by Django 4.1.5 on 2023-02-28 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0007_employee_dtr_total_working_hours'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee_dtr',
            name='date_in',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
