# Generated by Django 3.2.4 on 2021-08-02 23:28

import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EnvColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', colorfield.fields.ColorField(default='#FF0000', max_length=18, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FloorType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FloorTexture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30)),
                ('image_file', models.ImageField(upload_to='floors/')),
                ('floortype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rugviz.floortype')),
            ],
        ),
    ]
