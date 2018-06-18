from . import models

class ReleaseFilter():

    def __init__(self):
        dim_release_last = models.HelperPdasFootwearVansReleaseCurrent.objects.all().last().dim_release
        self.dim_release_id = dim_release_last.id
        self.dim_release_comment = dim_release_last.comment
        self.dim_buying_program_id = dim_release_last.dim_buying_program_id
        self.dim_release_dim_date_id = dim_release_last.dim_date_id

        self.filter_dict = dict()
        self.filter_dict['dim_release_id__exact'] = dim_release_last.id
