# Generated by Django 4.2.1 on 2023-10-18 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myclient', '0008_remove_pojistenci_smlouva_smlouva_pojistenec'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pojistenci',
            name='bydliste',
        ),
        migrations.AddField(
            model_name='bydliste',
            name='pojistenec',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='myclient.pojistenci'),
        ),
    ]
