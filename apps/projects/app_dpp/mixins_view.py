from . import models

class ReleaseFilter():

    def __init__(self):
        dim_release_last = models.DimRelease.objects.all().last()
        self.dim_release_comment = dim_release_last.comment

        self.filter_dict = dict()
        self.filter_dict['dim_release_id'] = dim_release_last.id
