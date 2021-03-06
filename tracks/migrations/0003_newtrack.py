# Generated by Django 2.1.1 on 2018-09-14 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0002_now'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewTrack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='tracks')),
                ('name', models.CharField(blank=True, max_length=256)),
                ('start_time', models.DateTimeField(blank=True)),
                ('end_time', models.DateTimeField(blank=True)),
                ('distance', models.FloatField(blank=True)),
                ('geojson', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('-start_time',),
            },
        ),
    ]
