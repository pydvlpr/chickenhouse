from django.db import models
from .cam import Cam

class Stream(models.Model):
    """
        Stream represents a video stream
    """
    class Meta:
        ordering = ["id"]
        #unique_together =(("id","name"))

    # just testing
    stream_cam = models.ForeignKey(Cam,unique=True,on_delete=models.CASCADE)
    stream_url = models.CharField(max_length=500)
    started_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.cam.name


    

