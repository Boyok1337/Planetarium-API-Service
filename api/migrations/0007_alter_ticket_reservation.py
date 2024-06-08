# Generated by Django 5.0.6 on 2024-06-07 17:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_ticket_options_ticket_unique_ticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='reservation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tickets', to='api.reservation'),
        ),
    ]
