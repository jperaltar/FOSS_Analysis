from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Contributor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, null=True)
    login = models.CharField(max_length=128, null=True, unique=True)
    email = models.EmailField(max_length=128, null=True, unique=True)
    type = models.CharField(max_length=128, null=True)

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, null=True)
    owner = models.ForeignKey('Contributor', null=True, blank=True, related_name='owner')
    contributors = models.ManyToManyField('Contributor', null=True, blank=True, related_name='contributors')

class File(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey('Project', null=True, blank='True')
    path = models.CharField(max_length=256)
    copyright = models.CharField(max_length=128)
    license = models.CharField(max_length=128)

class Blame(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.ForeignKey('File', related_name='file')
    author = models.ForeignKey('Contributor', related_name='author')
    lines = models.IntegerField()
