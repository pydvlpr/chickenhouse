from django.db import models
from .cam import Cam

class Preview(models.Model):
    """
        Preview represents a preview image from camera
    """
    class Meta:
        ordering = ["id"]
        #unique_together =(("id","name"))

    # just testing
    preview_cam = models.ForeignKey(Cam,unique=True,on_delete=models.CASCADE)
    pic_url = models.CharField(max_length=500)

    pass