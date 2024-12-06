# Generated by Django 5.0.2 on 2024-11-28 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landapp', '0002_purchaserequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='land',
            name='price',
            field=models.DecimalField(decimal_places=2, help_text='Price in KSH', max_digits=10),
        ),
    ]
