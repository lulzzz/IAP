import os

from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

from core import mixins_model
from core import utils

def upload_to_dump(instance, filename):
    if utils.is_ascii(filename) is False:
        filename = 'image' + os.path.splitext(filename)[1].lower()

    return 'uploads/user{}/dump/{}'.format(str(instance.user.id), filename)
class UploadFile(models.Model):
    user = models.ForeignKey(User)
    file = models.FileField(upload_to=upload_to_dump)
    extension = models.CharField(max_length=10)
    size = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

class ConvertImage(models.Model):

    IMAGE_TYPE_CHOICES = [
        ('thumbnail_80x80', 'thumbnail 80x80'),
        ('thumbnail_80x200', 'thumbnail 80x200'),
    ]

    upload_file = models.ForeignKey(UploadFile, models.CASCADE)
    image = models.CharField(max_length=500)
    image_type = models.CharField(max_length=50, choices=IMAGE_TYPE_CHOICES)
    extension = models.CharField(max_length=10)
    size = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Magic Conversion'


class UserSettings(models.Model, mixins_model.ModelFormFieldNames):
    user = models.ForeignKey(User)

    DEFAULT_CHOICE = 1
    SAVING_CHOICES = (
        (DEFAULT_CHOICE, 'Default'),
    )
    saving_choice = models.IntegerField(default=DEFAULT_CHOICE)

    form_field_list = []

    class Meta:
        verbose_name = 'Settings'
