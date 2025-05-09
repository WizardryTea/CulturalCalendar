# Generated by Django 4.2.20 on 2025-05-03 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affiche', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='performance',
        ),
        migrations.AlterField(
            model_name='performance',
            name='genre',
            field=models.CharField(choices=[('performance', 'Спектакль'), ('tragicomedy', 'Трагикомедия'), ('drama', 'Драма'), ('comedy', 'Комедия'), ('baby', 'Для детей'), ('musical', 'Мюзикл'), ('show', 'Шоу')], default='default', max_length=20),
        ),
        migrations.DeleteModel(
            name='ActorRole',
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]
