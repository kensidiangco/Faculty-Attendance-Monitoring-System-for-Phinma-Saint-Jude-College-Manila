# Generated by Django 4.1.5 on 2023-04-05 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0017_alter_employee_dtr_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='status',
            field=models.CharField(default='', max_length=20),
        ),
    ]
