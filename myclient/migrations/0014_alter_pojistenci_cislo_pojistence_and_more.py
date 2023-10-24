# Generated by Django 4.2.1 on 2023-10-21 07:59

from django.db import migrations, models
import myclient.models


class Migration(migrations.Migration):

    dependencies = [
        ('myclient', '0013_alter_pojistenci_cislo_pojistence_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pojistenci',
            name='cislo_pojistence',
            field=models.IntegerField(error_messages={'unique': 'Pojištěnec s tímto číslem již existuje.'}, unique=True, validators=[myclient.models.validate_cislo_pojistence]),
        ),
        migrations.AlterField(
            model_name='smlouva',
            name='cislo_smlouvy',
            field=models.CharField(error_messages={'unique': 'Smlouva s tímto číslem již existuje.'}, max_length=9, unique=True),
        ),
    ]