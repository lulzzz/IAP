from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    # Image matching
    url(r'^file_upload_view$', views.FileUploadView.as_view(), name='file_upload_view'),
    url(r'^file_upload_function$', views.ImageUploadFunction.as_view(), name='file_upload_function'),
    url(r'^image_display$', views.ImageDisplay.as_view(), name='image_display'),
    url(r'^image_comparison$', views.ComparisonDisplay.as_view(), name='image_comparison'),
    url(r'^generate_image_list$', views.GenerateImageList.as_view(), name='generate_image_list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
