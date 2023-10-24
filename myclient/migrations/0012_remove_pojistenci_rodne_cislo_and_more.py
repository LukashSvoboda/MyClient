# Generated by Django 4.2.1 on 2023-10-20 17:02

from django.db import migrations, models
import myclient.models


class Migration(migrations.Migration):

    dependencies = [
        ('myclient', '0011_pojistenci_rodne_cislo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pojistenci',
            name='rodne_cislo',
        ),
        migrations.AlterField(
            model_name='pojistenci',
            name='cislo_pojistence',
            field=models.IntegerField(validators=[myclient.models.validate_cislo_pojistence]),
        ),
        migrations.AlterField(
            model_name='pojistenci',
            name='email',
            field=models.EmailField(max_length=254, validators=[myclient.models.validate_email_format]),
        ),
        migrations.AlterField(
            model_name='pojistenci',
            name='jmeno',
            field=models.CharField(max_length=100, validators=[myclient.models.validate_name]),
        ),
        migrations.AlterField(
            model_name='pojistenci',
            name='prijmeni',
            field=models.CharField(max_length=100, validators=[myclient.models.validate_name]),
        ),
    ]
