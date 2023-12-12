
# from django.contrib.gis.db import models
from django.db  import models

# class Shapes0(models.Model):
#     name = models.CharField('name',max_length=30)
#     subname = models.CharField('subname', max_length=30)
#     # classmane=models.PositiveSmallIntegerField('classname')
#     geom=models.PolygonField(srid=3857)


class Shapes0(models.Model):
    level=models.IntegerField('level')
    id = models.TextField('id', primary_key=True)
    name = models.TextField('name')    
    classes=models.TextField('classes')
    geom=models.TextField('geom')
