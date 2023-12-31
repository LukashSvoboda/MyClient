# Generated by Django 4.2.1 on 2023-10-17 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bydliste',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ulice', models.CharField(max_length=100)),
                ('cislo_popisne', models.CharField(blank=True, max_length=10, null=True)),
                ('mesto', models.CharField(max_length=100)),
                ('psc', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Pojistenci',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jmeno', models.CharField(max_length=100)),
                ('prijmeni', models.CharField(max_length=100)),
                ('cislo_pojistence', models.IntegerField()),
                ('datum_narozeni', models.DateField()),
                ('telefon', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
