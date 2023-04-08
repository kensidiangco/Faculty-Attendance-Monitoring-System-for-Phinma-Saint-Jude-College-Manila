# Generated by Django 4.1.5 on 2023-04-05 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0021_alter_schedule_weekday_delete_weekday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='employee_status',
            field=models.CharField(choices=[('DEAN', 'DEAN'), ('PROFESSOR', 'PROFESSOR'), ('PROGRAM HEAD', 'PROGRAM HEAD')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='position',
            field=models.CharField(choices=[('CONTRACTUAL', 'CONTRACTUAL'), ('PART TIME', 'PART TIME'), ('REGULAR', 'REGULAR')], max_length=20, null=True),
        ),
        migrations.DeleteModel(
            name='Employee_Position',
        ),
    ]