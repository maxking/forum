from django.db import models
import datetime
# Create your models here.

class post(models.Model):
    '''Defines the basic info about a forum post'''
    date = models.DateTimeField(editable=False)
    posted_by = models.CharField(max_length = 25, blank = False)
    title = models.CharField(max_length = 150, blank = False)
    message = models.TextField()

    def __unicode__(self):
        return "%s %s" %(self.posted_by, self.title)
