# Generated by Django 4.1.5 on 2023-04-05 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0019_employee_dtr_schedule_alter_schedule_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='status',
            field=models.CharField(default='OUT', max_length=20),
        ),
    ]
