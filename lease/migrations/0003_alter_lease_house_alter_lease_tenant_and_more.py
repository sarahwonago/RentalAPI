# Generated by Django 5.1.2 on 2024-11-13 10:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0009_remove_house_is_paid'),
        ('lease', '0002_lease_house_alter_lease_tenant'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='lease',
            name='house',
            field=models.ForeignKey(limit_choices_to={'is_occupied': False}, on_delete=django.db.models.deletion.CASCADE, related_name='leases', to='building.house'),
        ),
        migrations.AlterField(
            model_name='lease',
            name='tenant',
            field=models.ForeignKey(limit_choices_to={'role': 'tenant'}, on_delete=django.db.models.deletion.CASCADE, related_name='leases', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='lease',
            unique_together={('tenant', 'house')},
        ),
    ]