# Generated by Django 2.1 on 2019-05-07 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0004_alarma'),
    ]

    operations = [
        migrations.AddField(
            model_name='alarma',
            name='descripcion',
            field=models.CharField(default='', max_length=100),
        ),
    ]
