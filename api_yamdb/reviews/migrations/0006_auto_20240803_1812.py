# Generated by Django 3.2 on 2024-08-03 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20240803_1728'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='genre',
        ),
        migrations.AddField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(related_name='titles', to='reviews.Genre'),
        ),
    ]
