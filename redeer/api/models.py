from django.db import models


class ApiKey(models.Model):
    md5 = models.CharField(max_length=40,
        help_text="echo -n 'email:password' | openssl md5")
