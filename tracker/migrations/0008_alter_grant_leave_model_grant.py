# Generated by Django 5.0.1 on 2025-01-08 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0007_grant_leave_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grant_leave_model',
            name='grant',
            field=models.BooleanField(default=False),
        ),
    ]
