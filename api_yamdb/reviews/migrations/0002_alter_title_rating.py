# Generated by Django 3.2 on 2024-08-01 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='rating',
            field=models.IntegerField(null=True, verbose_name='Рейтинг произведения'),
        ),
    ]