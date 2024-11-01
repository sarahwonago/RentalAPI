# Generated by Django 5.1.2 on 2024-10-30 13:46

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0004_alter_building_name_alter_building_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='The house name/number', max_length=255)),
                ('rent_due_date', models.DateField()),
                ('rent_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_occupied', models.BooleanField(default=False)),
                ('building', models.ForeignKey(help_text='The Building of the House', on_delete=django.db.models.deletion.CASCADE, related_name='houses', to='building.building')),
            ],
            options={
                'unique_together': {('name', 'building')},
            },
        ),
    ]
