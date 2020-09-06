from django.db import models

class Preview(models.Model):
    """
        Preview represents a preview image from camera
    """
    class Meta:
        ordering = ["id"]
        unique_together =(("id","name"))

    # just testing
    preview_cam = models.ForeignKey(models.Cam,unique=True)
    pic_url = models.CharField(max_length=500)

    pass