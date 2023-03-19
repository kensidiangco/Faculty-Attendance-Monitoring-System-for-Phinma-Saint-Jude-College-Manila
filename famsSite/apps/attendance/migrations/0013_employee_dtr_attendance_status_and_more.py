# Generated by Django 4.1.5 on 2023-03-19 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0012_employee_dtr_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee_dtr',
            name='attendance_status',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='employee_dtr',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.employee'),
        ),
    ]
