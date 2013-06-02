from django.db import models


class ApiKey(models.Model):
    user = models.ForeignKey('auth.User')
    md5 = models.CharField(max_length=40,
        help_text="echo -n 'email:password' | openssl md5")

    def __unicode__(self):
        return unicode(self.user)
