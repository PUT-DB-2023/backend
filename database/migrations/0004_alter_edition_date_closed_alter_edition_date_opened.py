# Generated by Django 4.0.5 on 2022-10-04 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_remove_edition_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edition',
            name='date_closed',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='edition',
            name='date_opened',
            field=models.DateField(blank=True, null=True),
        ),
    ]