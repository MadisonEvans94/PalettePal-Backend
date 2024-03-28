

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField


class Palette(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    imageUrl = models.URLField(null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='palettes')

    def __str__(self):
        return self.name


class ClusterData(models.Model):
    palette = models.ForeignKey(
        Palette, on_delete=models.CASCADE, related_name='cluster_data')
    cluster_index = models.IntegerField()
    # Use TextField and serialize to JSON manually if not using PostgreSQL
    colors = JSONField()
    ratios = JSONField()

    def __str__(self):
        return f"Cluster {self.cluster_index} of Palette {self.palette.name}"

# Additional functions or model methods can be added as needed
