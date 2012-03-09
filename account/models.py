from django.db import models
from django.contrib.auth.models import User
import wiki.account.choices as choices


# Create your models here.
class person(models.Model):
    '''Defines the basic infoo about the user'''
    user_id=models.ForeignKey(User)
    sex=models.CharField(max_length=1, choices=choices.sex_choice, blank=False)
    phno=models.CharField(max_length=10, verbose_name='phone-number')
    pin=models.CharField(max_length=10)
    website=models.URLField(verify_exists=True, null=True , blank=True)
#    image=models.FileField( upload_to ='documents/%Y/%m/%d' )
    def __unicode__(self):
        return "%s %s" %(self.first_name, self.last_name)
