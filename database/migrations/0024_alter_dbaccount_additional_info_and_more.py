# Generated by Django 4.0.5 on 2022-10-20 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0023_major_course_major'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dbaccount',
            name='additional_info',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='major',
            name='description',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='permission',
            name='description',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='role',
            name='description',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
