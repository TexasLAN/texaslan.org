# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-06 22:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20170222_1402'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveSemester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'semester',
            },
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='active_semesters',
            field=models.ManyToManyField(blank=True, to='users.ActiveSemester'),
        ),
    ]
