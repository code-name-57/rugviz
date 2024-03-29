# from enum import unique
# from django.db import models
# from django.contrib import admin
# from django.db.models import constraints
# from django.db.models.base import Model
# from django.db.models.deletion import CASCADE
# from django.db.models.fields import CharField

# from django.utils.safestring import mark_safe

# class Design(models.Model):
#     # Appear as 6208B
#     name = models.CharField(max_length=30)
#     description = models.CharField(max_length=200)
#     collection = models.ForeignKey(Collection, on_delete=models.CASCADE, null=True)

#     available_colors = models.ManyToManyField(Color)

#     def __str__(self):
#         return self.name



# class Carpet(models.Model):
#     design = models.ForeignKey(Design, on_delete=models.CASCADE, null = True)
#     color = models.ForeignKey(Color, on_delete=CASCADE, null = True)
#     size = models.ForeignKey(Size, on_delete=models.CASCADE, null = True)
#     image_file = models.FileField(upload_to='carpets/', null=True)
#     inventory = models.IntegerField(default=0)

#     def __str__(self):
#         return (f"({str(self.design.collection)}) "
#                 f"{self.design} "
#                 f"{self.color} -"
#                 f"({self.size})")

#     def in_stock(self):
#         return self.inventory > 0

#     def image_tag(self):
#         if self.image_file:
#             return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.image_file.url)
#         else:
#             return 'No Image Found'
#     image_tag.short_description = 'Image'

#     class Meta:
#         constraints = [models.UniqueConstraint(fields=['design','color','size'], name="unique_ein")]

# from django.db.models.signals import m2m_changed, post_save
# from .models import *

# def available_size_changed(sender, instance, action, model, pk_set, **kwargs):
#     if action == "post_add":
#         for pk in pk_set:
#             for des in instance.design_set.all():
#                 for col in des.available_colors.all():
#                     Carpet.objects.get_or_create(
#                         design = des,
#                         color = col,
#                         size = model.objects.get(pk=pk)
#                     )
#             print(str(model.objects.get(pk=pk)))
#         print("sizes added for  collection : ", instance.name)
#     elif action == "post_remove":
#         for pk in pk_set:
#             print(str(model.objects.get(pk=pk)))
#         print("sizes removed from collection  : ", instance.name)
#     pass

# def available_color_changed(sender, instance, action, model, pk_set, **kwargs):
#     if action == "post_add":
#         for pk in pk_set:
#             for sz in instance.collection.available_sizes.all():
#                 Carpet.objects.get_or_create(
#                     design=instance,
#                     size=sz,
#                     color = model.objects.get(pk=pk)
#                 )
#         print("colors added for design : ", instance.name)
#     elif action == "post_remove":
#         for pk in pk_set:
#             print(str(model.objects.get(pk=pk)))
#         print("colors removed from design  : ", instance.name)
#     pass

# def design_created(sender, instance, created, **kwargs):
#     instance.design.available_colors.add(instance.color)
#     instance.design.collection.available_sizes.add(instance.size)
#     pass

# # m2m_changed.connect(available_color_changed, sender = Design.available_colors.through)
# # m2m_changed.connect(available_size_changed, sender = Collection.available_sizes.through)
# # post_save.connect(design_created, sender = Carpet)

