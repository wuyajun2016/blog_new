from django.db import models
from django.contrib.auth.models import User


# django的ORM
class OAuth_type(models.Model):
    type_name = models.CharField(max_length=12)
    title = models.CharField(max_length=12)
    img = models.ImageField(upload_to='uploadImages')

    def __str__(self):
        return self.type_name


class OAuth_ex(models.Model):
    user = models.ForeignKey(User)
    openid = models.CharField(max_length=64, default='')
    oauth_type = models.ForeignKey(OAuth_type,default=1)

    def __str__(self):
        return u'<%s>' % (self.user)



