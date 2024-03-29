from enum import unique
from django.db import models
from django.contrib import admin
from django.db.models import constraints
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField

import pathlib
from django.utils.safestring import mark_safe

from catalog.models import Carpet
# Rugviz speecific models
from colorfield.fields import ColorField

class EnvColor(models.Model):
    color = ColorField(default='#FF0000', unique=True)

class FloorType(models.Model):
    name = models.CharField(max_length=30, unique=True)

class FloorTexture(models.Model):
    floortype = models.ForeignKey(FloorType, on_delete=models.CASCADE)
    name = CharField(max_length=30, blank = True)
    image_file = models.ImageField(upload_to='floors/')

    def image_tag(self):
        if self.image_file:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.image_file.url)
        else:
            return 'No Image Found'
    image_tag.short_description = 'Image'

def carpet_picture_path(instance, filename):
    return 'rugviz/Carpet3d/{0}/{1}_{2}{3}'.format(instance.carpet.designColor.design.collection.name, instance.carpet.designColor.design.name, instance.carpet.designColor.color, pathlib.Path(filename).suffix)

class CarpetPicture(models.Model):
    carpet = models.ForeignKey(Carpet, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=carpet_picture_path, blank=True, null=True)
