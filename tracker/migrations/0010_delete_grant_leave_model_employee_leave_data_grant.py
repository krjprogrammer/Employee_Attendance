# Generated by Django 5.0.1 on 2025-01-08 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0009_alter_grant_leave_model_emp_id_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='grant_leave_model',
        ),
        migrations.AddField(
            model_name='employee_leave_data',
            name='grant',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
