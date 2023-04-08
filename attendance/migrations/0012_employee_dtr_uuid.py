# Generated by Django 4.1.5 on 2023-03-04 14:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0011_alter_employee_status_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee_dtr',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]