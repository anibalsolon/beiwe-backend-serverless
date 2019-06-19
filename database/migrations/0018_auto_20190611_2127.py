# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-06-11 21:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0017_chunkregistry_file_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='PipelineRegistry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('data_type', models.CharField(db_index=True, max_length=32)),
                ('processed_data', django_extensions.db.fields.json.JSONField(blank=True, default=dict, null=True)),
                ('uploaded_at', models.DateTimeField(db_index=True)),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pipeline_registries', to='database.Participant')),
                ('study', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pipeline_registries', to='database.Study')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='chunkregistry',
            name='data_type',
            field=models.CharField(db_index=True, max_length=32),
        ),
    ]