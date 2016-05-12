from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import RequestContext
import requests
import forms
import re
import json
import helpers.analyzer as analyzer
from helpers.githubAPI import GithubProject as GithubProject
from multiprocessing import Process, Manager
from git import Repo
import os.path
import models

# VIEWS
@csrf_exempt
def main(request):
    if request.method == 'GET':
        template = get_template("index.html")
        urlForm = forms.urlForm()

        context = {
            'main': True,
            'urlForm': urlForm
        }

        analyzer.loadIndexes()

        return HttpResponse(template.render(context, request))

def analyze(request):
    if request.method == 'POST':
        url = request.POST['url']
        project = GithubProject(url)

        #Store project
        models.Project.objects.update_or_create(name = project.repo)
        dbProject = models.Project.objects.get(name = project.repo)

        #Store contributors
        contributors = project.getContributors()
        for contributor in contributors:
            models.Contributor.objects.update_or_create(name = contributor['name'],
                                login = contributor['login'],
                                email = contributor['email'],
                                type = contributor['type'])
            dbContrib = models.Contributor.objects.get(name = contributor['name'])
            if contributor['login'] == project.user:
                dbProject.owner = dbContrib
                dbProject.save()
            else:
                dbProject.contributors.add(dbContrib)

        #Store project contents
        localDir = '/tmp/FOSS_Analysis'
        repoDir = localDir + '/' + project.user + '/' + project.repo
        if not os.path.exists(repoDir):
            Repo.clone_from(url, repoDir)

        scans = []
        repo = Repo(repoDir)
        scans = analyzer.scanFolder(repo, repoDir, scans)

        return HttpResponse(scans, content_type="application/json")
