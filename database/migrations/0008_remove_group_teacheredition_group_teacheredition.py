# Generated by Django 4.0.5 on 2022-10-06 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0007_alter_group_students'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='teacherEdition',
        ),
        migrations.AddField(
            model_name='group',
            name='teacherEdition',
            field=models.ManyToManyField(to='database.teacheredition'),
        ),
    ]