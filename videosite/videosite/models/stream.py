from django.db import models

class Stream(models.Model):
    """
        Stream represents a video stream
    """
    class Meta:
        ordering = ["id"]
        unique_together =(("id","name"))

    # just testing
    stream_cam = models.ForeignKey(models.Cam,unique=True)
    stream_url = models.CharField(max_length=500)
    started_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.cam.name


    

