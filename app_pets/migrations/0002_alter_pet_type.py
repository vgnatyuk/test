# Generated by Django 4.0.3 on 2022-03-17 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_pets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='type',
            field=models.CharField(choices=[('Cat', 'cat'), ('Dog', 'dog')], max_length=3),
        ),
    ]
