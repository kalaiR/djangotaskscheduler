from django.db import models


class Demo(models.Model):
    email   = models.CharField("Email address", max_length=50)
    note    = models.CharField("Note", max_length=200)

    def __unicode__(self):
        return 'Demo: ', self.id
