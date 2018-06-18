import os

from django.conf import settings as cp
from django import forms
from django.core.exceptions import ValidationError

from . import models


class FileUploadForm(forms.Form):
    r"""
    Form for uploading files
    """
    # Keep name to 'file' for Dropzone
    file = forms.FileField(required=True)

    class Meta:
        model = models.UploadFile

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']

        # Check if the file is a valid image
        try:
            img = forms.ImageField()
            img.to_python(uploaded_file)

        # Check if the file is a valid PDF
        except forms.ValidationError:
            extension = os.path.splitext(uploaded_file.name)[1][1:].lower()
            if extension not in cp.ALLOWED_EXTENSION_LIST:
                raise forms.ValidationError('Only images and PDF files allowed')

        return uploaded_file
