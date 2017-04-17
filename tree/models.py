from __future__ import unicode_literals
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

 
class Referat(MPTTModel):
    name = models.CharField(max_length=200)
    text = models.CharField(max_length=10000)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    def __unicode__(self):
    	return self.name
