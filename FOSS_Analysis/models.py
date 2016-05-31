from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Contributor(models.Model):
    name = models.CharField(max_length=128, null=True)
    login = models.CharField(max_length=128, null=True)
    email = models.EmailField(max_length=128, null=True)
    type = models.CharField(max_length=128, null=True)

    class Meta:
        unique_together = ("login", "email")

class Project(models.Model):
    name = models.CharField(max_length=128, null=True)
    owner = models.ForeignKey('Contributor', null=True, blank=True, related_name='owner')
    contributors = models.ManyToManyField('Contributor', related_name='contributors')

class File(models.Model):
    project = models.ForeignKey('Project', null=True, blank='True')
    path = models.CharField(max_length=254, unique=True)
    language = models.CharField(max_length=128, null=True)
    copyrights = models.ManyToManyField('Copyright', related_name='copyrights')
    licenses = models.ManyToManyField('License', related_name='licenses')

class Copyright(models.Model):
    name = models.CharField(max_length=250, unique=True)

class License(models.Model):
    name = models.CharField(max_length=250, null=True)
    owner = models.CharField(max_length=250, null=True)

    class Meta:
        unique_together = ("name", "owner")

class Blame(models.Model):
    file = models.ForeignKey('File', related_name='file')
    author = models.ForeignKey('Contributor', related_name='author')
    lines = models.IntegerField()

    class Meta:
        unique_together = ("file", "author")
