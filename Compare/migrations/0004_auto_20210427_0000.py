# Generated by Django 3.1.5 on 2021-04-26 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Compare', '0003_image_range'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='range',
            field=models.TextField(null=True),
        ),
    ]
