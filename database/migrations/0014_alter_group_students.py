# Generated by Django 4.0.5 on 2022-10-08 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0013_alter_course_name_alter_group_students_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='students',
            field=models.ManyToManyField(related_name='groups', to='database.student'),
        ),
    ]
