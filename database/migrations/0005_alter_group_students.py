# Generated by Django 4.0.5 on 2022-11-22 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0004_alter_group_students'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='groups', to='database.student'),
        ),
    ]
