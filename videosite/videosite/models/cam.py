from django.db import models

class Cam(models.Model):
    """
        Cam represents a video camera
    """
    class Meta:
        ordering = ["id","name"]
        unique_together =(("id","name"))

    name = models.CharField(max_length=100)
    host = models.CharField(max_length=50)
    position=models.CharField(max_length=200)
    img_url = models.CharField(max_length=200,default=" ")
    stream_url = models.CharField(max_length=200,default=" ")

    pass