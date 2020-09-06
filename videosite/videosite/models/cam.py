from django.db import models

class Cam(models.Model):
    """
        Stream represents a video stream
    """
    class Meta:
        ordering = ["id"]
        unique_together =(("id","name"))

        name = models.CharField(max_length=100)
        position=models.CharField(max_length=200)
        url = models.CharField(max_length=500)

    pass