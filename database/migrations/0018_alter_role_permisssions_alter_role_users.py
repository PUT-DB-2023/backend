# Generated by Django 4.0.5 on 2022-10-10 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0017_alter_server_edition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='permisssions',
            field=models.ManyToManyField(blank=True, null=True, related_name='roles', to='database.permission'),
        ),
        migrations.AlterField(
            model_name='role',
            name='users',
            field=models.ManyToManyField(blank=True, null=True, related_name='roles', to='database.user'),
        ),
    ]
