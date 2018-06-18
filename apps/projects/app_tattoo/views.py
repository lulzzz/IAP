import os
from datetime import date

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.conf import settings as cp
from django.urls import reverse_lazy
from django.http import JsonResponse

from blocks import views
from core import utils
from core import mixins_view

from . import models
from . import forms


# RPCs
from workflows.extractions.standards.pdf.image_extractor import extract_images_from_pdf
from workflows.extractions.standards.zip.image_extractor import extract_images_from_zip
from workflows.extractions.standards.zip.zip_utils import zip_files

# Analytics
from analytics.core import image_utils


class FileUploadView(views.FormUpload):
    r"""
    View that shows the box for dragging image and PDF files for upload
    """
    pass


class ImageUploadFunction(views.SimpleUpload):
    r"""
    View that processes the upload
    """

    def upload_file(self, file_obj):
        new_file = models.UploadFile(file=file_obj)
        new_file.user = self.request.user
        new_file.extension = os.path.splitext(new_file.file.name)[1][1:].lower()
        new_file.size = new_file.file.size
        new_file.save()
        return new_file

    def process_image(self, upload_file, image_path, image_type):
        new_file = models.ConvertImage(
            upload_file=upload_file,
            image=image_path,
            image_type=image_type,
            size=0,
            extension=os.path.splitext(image_path)[1][1:].lower(),
        )
        new_file.save()
        return new_file

    def post(self, request, **kwargs):
        self.request = request
        form = forms.FileUploadForm(request.POST, request.FILES)

        if form.is_valid():
            file_obj = request.FILES['file']
            new_file = self.upload_file(file_obj)
            base_file = new_file

            # Check if extraction is needed
            if new_file.extension not in cp.ALLOWED_IMAGE_EXTENSION_LIST:

                # Check if PDF extraction is needed
                if new_file.extension == 'pdf':
                    abs_path = os.path.join(cp.MEDIA_ROOT, new_file.file.name)

                    # Extract first image from PDF
                    file_property = {
                        'name': os.path.splitext(os.path.basename(new_file.file.name))[0],
                        'rel_path': new_file.file.name,
                        'abs_path': abs_path,
                        'extension': '.' + new_file.extension,
                    }
                    output_folder = os.path.dirname(abs_path)

                    extracted_image_obj = extract_images_from_pdf(
                        file_property,
                        output_folder,
                        # page_limit=1,
                        # image_on_page_limit=1
                    )

                    extracted_image_list = list()
                    for extracted_image in extracted_image_obj:
                        extracted_image_list.append(os.path.basename(extracted_image.get('source_master_component_reference')))

                elif new_file.extension in('zip', 'docx', 'pptx'):
                    abs_path = os.path.join(cp.MEDIA_ROOT, new_file.file.name)
                    output_folder = os.path.dirname(abs_path)

                    extracted_image_list = extract_images_from_zip(
                        abs_path,
                        output_folder,
                        # page_limit=1,
                        # image_on_page_limit=1
                    )

                # Check if image(s) were extracted correctly
                if len(extracted_image_list) > 0:
                    for extracted_file_name in extracted_image_list:
                        file_obj = models.upload_to_dump(new_file, extracted_file_name)
                        new_file = self.upload_file(file_obj)
                else:
                    return JsonResponse(False, safe=False)

            # Get path information
            folder_path_output_rel = 'uploads/user{}/magic'.format(str(request.user.id))
            folder_path_output = os.path.join(cp.MEDIA_ROOT, folder_path_output_rel)

            # Create folder if not exist
            if not os.path.exists(folder_path_output):
                os.makedirs(folder_path_output)

            # Convert image into 80x80 thumbnail
            thumb = image_utils.thumbnail_pil(
                new_file.file.path[:len(new_file.file.path)-4] + ' - processed.jpg',
                folder_path_output,
                folder_path_output_rel,
                width=80,
                height=80,
                suffix='thumbnail',
                extension='jpg',
            )
            processed_image = self.process_image(
                base_file,
                thumb,
                'thumbnail_80x80',
            )

            # Convert image into recommended size
            file_list = list()
            thumb = image_utils.thumbnail_pil(
                new_file.file.path,
                folder_path_output,
                folder_path_output_rel,
                width=cp.OUTPUT_IMAGE_WIDTH,
                height=cp.OUTPUT_IMAGE_HEIGHT,
                suffix=cp.OUTPUT_IMAGE_SUFFIX,
                extension=cp.OUTPUT_IMAGE_EXTENSION,
            )
            processed_image = self.process_image(
                base_file,
                thumb,
                'tattoo',
            )

            # Create large append image
            image_path_input_list = list()
            queryset = models.ConvertImage.objects.filter(
                upload_file__user=self.request.user,
                image_type='tattoo',
            ).order_by('id')
            for query in queryset:
                image_path_input_list.append(os.path.join(cp.MEDIA_ROOT, query.upload_file.file.path))
                file_list.append(os.path.join(cp.MEDIA_ROOT, query.image))

            summary_image = image_utils.append_pil(
                image_path_input_list,
                folder_path_output,
                'summary_tattoo',
                'jpg',
                direction='vertical',
            )
            file_list.append(summary_image)

            # Add to zip folder
            zip_files(file_list, os.path.join(folder_path_output, 'output_without_tattoo.zip'), mode='w')

            return JsonResponse(True, safe=False)

        else:
            return JsonResponse(form.errors, safe=False)


class ImageDisplay(views.SimpleBlockView):
    r"""
    View that displays the uploaded image
    """

    paginate_by = 8
    order_by = 'id'
    order_type = '-' # - for desc
    model = models.ConvertImage
    template_name = 'blocks/thumbnail_gallery.html'

    def get_context_dict(self, request):

        # Query images
        query = self.model.objects.filter(
            upload_file__user=self.request.user,
            image_type='thumbnail_80x80',
        ).order_by(self.order_type + self.order_by)[:self.paginate_by]

        # If user has uploaded an image before
        if query.exists():
            # Prepare context object
            image_context_dict = dict()
            image_context_dict['zip_file'] = os.path.join(cp.IMAGE_URL, r'''uploads\user1\magic\output_without_tattoo.zip''')
            image_context_dict['generate_url'] = reverse_lazy('generate_image_list')

            image_list = list()
            for idx, image in enumerate(query):
                image_list.append({
                    'id': image.id,
                    'label': os.path.basename(str(image.image)),
                    'text': image.created,
                    'reference': image.image,
                })

            image_context_dict['image_list'] = image_list
            return image_context_dict

        # If user has never uploaded an image
        else:
            return {
                'message': {
                    'text': 'No image uploaded',
                    'type': 'info',
                    'position_left': True,
                }
            }



class ComparisonDisplay(views.SimpleBlockView):
    r"""
    View that displays the uploaded image
    """

    paginate_by = 8
    order_by = 'id'
    order_type = '-' # - for desc
    model = models.ConvertImage
    template_name = 'blocks/thumbnail_gallery.html'

    def get_context_dict(self, request):

        # Query images
        query = self.model.objects.filter(
            upload_file__user=self.request.user,
            image_type='thumbnail_80x80',
        ).order_by(self.order_type + self.order_by)[:self.paginate_by]

        # If user has uploaded an image before
        if query.exists():

            # Image path list
            image_path_list = [
                os.path.join(r'uploads/display', 'Woman Red.jpg'),
                os.path.join(r'uploads/display', 'Woman Red - processed.jpg'),
                os.path.join(r'uploads/display', 'Aquaman.jpg'),
                os.path.join(r'uploads/display', 'Aquaman - processed.jpg'),
                os.path.join(r'uploads/display', 'Beckham.jpg'),
                os.path.join(r'uploads/display', 'Beckham - processed.jpg'),
                os.path.join(r'uploads/display', 'Boateng.jpg'),
                os.path.join(r'uploads/display', 'Boateng - processed.jpg'),
                os.path.join(r'uploads/display', 'Ibrahimovich.jpg'),
                os.path.join(r'uploads/display', 'Ibrahimovich - processed.jpg'),
                os.path.join(r'uploads/display', 'Jeep Model.jpg'),
                os.path.join(r'uploads/display', 'Jeep Model - processed.jpg'),
                os.path.join(r'uploads/display', 'Malin Akerman.jpg'),
                os.path.join(r'uploads/display', 'Malin Akerman - processed.jpg'),
                os.path.join(r'uploads/display', 'Messi.jpg'),
                os.path.join(r'uploads/display', 'Messi - processed.jpg'),
            ]

            # Prepare context object
            image_list = list()
            for idx, image_path in enumerate(image_path_list):
                image_list.append({
                    'id': 0,
                    'label': os.path.basename(str(image_path)),
                    'text': 'Person',
                    'reference': image_path,
                })

            image_context_dict = dict()
            image_context_dict['image_list'] = image_list
            return image_context_dict

        # If user has never uploaded an image
        else:
            return {
                'message': {
                    'text': 'No image uploaded',
                    'type': 'info',
                    'position_left': True,
                }
            }



class GenerateImageList(views.SimpleUpdate):
    r"""
    View that generate the tattoo specific images and zip download
    """
    order_by = 'id'
    order_type = '-' # - for desc
    model = models.ConvertImage

    def business_logic(self, request=None):

        # Query images
        query = self.model.objects.filter(
            upload_file__user=self.request.user,
            image_type='tattoo',
        ).order_by(self.order_type + self.order_by)

        # If user has uploaded an image before
        if query.exists():

            # Append
            image_path_input_list = list()
            for idx, image in enumerate(query):
                image_path_input_list.append(os.path.join(cp.MEDIA_ROOT, image))

            image_utils.append_pil(
                image_path_input_list,
                folder_path_output,
                image,
                extension_output,
                direction='vertical',
            )

            return True

        else:
            return False
