# Generated by Django 4.0.5 on 2022-10-08 22:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0012_alter_dbaccount_editionserver_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='students',
            field=models.ManyToManyField(blank=True, null=True, related_name='groups', to='database.student'),
        ),
        migrations.AlterField(
            model_name='group',
            name='teacherEdition',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.teacheredition'),
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
