# Generated by Django 3.1.5 on 2021-04-28 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Compare', '0005_auto_20210427_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='top',
            field=models.IntegerField(null=True),
        ),
    ]
