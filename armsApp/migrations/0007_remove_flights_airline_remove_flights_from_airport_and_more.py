# Generated by Django 4.2.7 on 2023-12-04 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('armsApp', '0006_reservation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flights',
            name='airline',
        ),
        migrations.RemoveField(
            model_name='flights',
            name='from_airport',
        ),
        migrations.RemoveField(
            model_name='flights',
            name='to_airport',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='flight',
        ),
        migrations.DeleteModel(
            name='Airlines',
        ),
        migrations.DeleteModel(
            name='Airport',
        ),
        migrations.DeleteModel(
            name='Flights',
        ),
        migrations.DeleteModel(
            name='Reservation',
        ),
    ]
