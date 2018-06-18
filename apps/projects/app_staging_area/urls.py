from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^measurement_point_table/(?P<pk>[\w]+)$', views.MeasurementPointTable.as_view(), name='measurement_point_table'),
    # url(r'^tuple_table/(?P<pk>\d+)$', views.TupleTable.as_view(), name='tuple_table'),
]
