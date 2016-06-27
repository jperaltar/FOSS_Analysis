from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
import requests
import forms
import re
import simplejson as json
import helpers.analyzer as analyzer
from helpers.githubAPI import GithubProject as GithubProject
import helpers.format as format
from multiprocessing import Process, Manager
from git import Repo
import os.path
import models
from django.db.models import Count, Sum
from datetime import datetime
from django.utils import timezone

#Helper functions
def formatFiles(dbFiles):
    files = {}
    for file in dbFiles:
        files[file.path] = {
            'language': file.language,
            'authors': {},
            'copyrights': [],
            'licenses': []
        }

        #Add authors
        blames = models.Blame.objects.filter(file__pk=file.pk)
        for blame in blames:
            files[file.path]['authors'][blame.author.login] = {
                'lines': blame.lines,
                'email': blame.author.email
            }
            if not blame.author.email:
                files[file.path]['authors'][blame.author.login]['email'] = blame.author.login


        #Add copyrights
        dbCopyrights = []
        copyrights = file.copyrights.values('name')
        if len(copyrights) is not 0:
            for copyright in copyrights:
                dbCopyrights.append(copyright['name'])
            files[file.path]['copyrights'].append(dbCopyrights)

        #Add licenses
        licenses = file.licenses.values('name')
        for license in licenses:
            if license['name']:
                files[file.path]['licenses'].append({'short_name': license['name']})

    return files

def store_contributors(contributors, dbProject, owner):
    for contributor in contributors:
        models.Contributor.objects.update_or_create(login = contributor['login'],
                                                email = contributor['email'],
                                                defaults = {
                                                    'name': contributor['name'],
                                                    'type': contributor['type']
                                                })
        dbContrib = models.Contributor.objects.get(login = contributor['login'])
        if contributor['login'] == owner:
            dbProject.owner = dbContrib
            dbProject.save()
        else:
            dbProject.contributors.add(dbContrib)


def store_project_contents(scans, dbProject, new_json):
    for path, scan in scans.items():
        new_json['files'][path] = scan
        models.File.objects.update_or_create(path = path,
                                        defaults = {'language': scan['language'],
                                                    'project': dbProject})
        dbFile = models.File.objects.get(path = path)
        for copyright in scan['copyrights']:
            models.Copyright.objects.update_or_create(name = copyright[0])
            dbCopyright = models.Copyright.objects.get(name = copyright[0])
            dbFile.copyrights.add(dbCopyright)
        for license in scan['licenses']:
            models.License.objects.update_or_create(name = license['short_name'],
                                                owner = license['owner'])
            dbLicense = models.License.objects.get(name = license['short_name'])
            dbFile.licenses.add(dbLicense)
        for author in scan['authors']:
            try:
                dbAuthor = models.Contributor.objects.get(email = scan['authors'][author]['email'])
            except models.Contributor.DoesNotExist:
                try:
                    dbAuthor = models.Contributor.objects.get(login = author)
                except models.Contributor.DoesNotExist:
                    try:
                        dbAuthor = models.Contributor.objects.get(name = author)
                    except models.Contributor.DoesNotExist:
                        continue

            models.Blame.objects.update_or_create(file = dbFile,
                                            author = dbAuthor,
                                            defaults = {'lines': scan['authors'][author]['lines']})

# VIEWS


@ensure_csrf_cookie
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


def all(request):
    if request.method == 'POST':
        #Performs a count for each distinct copyright
        copyrights_count = models.File.objects.values('copyrights__name').annotate(count=Count('path', distinct=True))
        copyrights_count = format.count_to_d3_json(copyrights_count, 'copyrights__name', 'count')

        #Performs a count for each distinct license
        licenses_count = models.File.objects.values('licenses__name').annotate(count=Count('path', distinct=True))
        licenses_count = format.count_to_d3_json(licenses_count, 'licenses__name', 'count')

        #Performs a count for each distinct language
        languages_count = models.File.objects.values('language').annotate(count=Count('path', distinct=True))
        languages_count = format.count_to_d3_json(languages_count, 'language', 'count')

        #Performs a count for each contributors lines
        contributions_count = models.Blame.objects.values('author__login').annotate(count=Sum('lines', distinct=True))
        contributions_count = format.count_to_d3_json(contributions_count, 'author__login', 'count')

        new_json = {
            "contributors": contributions_count,
            "languages": languages_count,
            "copyrights": copyrights_count,
            "licenses": licenses_count
        }

        return HttpResponse(json.dumps(new_json))


def user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = data['user']

        #Performs a count for each distinct language by user
        languages_count = models.Blame.objects.filter(author__login=user).values('file__language').annotate(count=Count('file', distinct=True))
        languages_count = format.count_to_d3_json(languages_count, 'file__language', 'count')

        #Performs a search of every project that has the user as contributor
        ownedProjects = models.Project.objects.filter(owner__login=user).values('name')
        collaborations = models.Project.objects.filter(contributors__login=user).values('name')
        ownedProjects = format.list_to_json_array(ownedProjects, 'name')
        collaborations = format.list_to_json_array(collaborations, 'name')

        #Performs a count for each distinct license by user
        licenses_count = models.Blame.objects.filter(author__login=user).values('file__licenses__name').annotate(count=Count('file', distinct=True))
        licenses_count = format.count_to_d3_json(licenses_count, 'file__licenses__name', 'count')

        #Performs a count for each distinct copyright by user
        copyrights_count = models.Blame.objects.filter(author__login=user).values('file__copyrights__name').annotate(count=Count('file', distinct=True))
        copyrights_count = format.count_to_d3_json(copyrights_count, 'file__copyrights__name', 'count')

        new_json = {
            "languages": languages_count,
            "projects": {
                "owned": ownedProjects,
                "collaborations": collaborations
            },
            "licenses": licenses_count,
            "copyrights": copyrights_count
        }

        return HttpResponse(json.dumps(new_json))


def legal(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        copyright = data['copyright']
        license = data['license']

        dbFiles = models.File.objects.filter(licenses__name__contains=license, copyrights__name__contains=copyright)
        files = formatFiles(dbFiles)

        new_json = {
            'files': files
        }

        return HttpResponse(json.dumps(new_json))


def analyze(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        url = data['url']
        project = GithubProject(url)

        new_json = {
            'created': False,
            'owner': project.user,
            'url': url,
            'num_files': 0,
            'files': {}
        }

        #Compare last update time
        dbProject, created = models.Project.objects.get_or_create(name=project.repo)
        lastUpdate = project.getUpdateTime()
        lastUpdate = datetime.strptime(lastUpdate, '%Y-%m-%dT%H:%M:%SZ')
        lastUpdate = timezone.make_aware(lastUpdate, timezone.get_default_timezone())

        # print dbProject.name
        # print lastUpdate
        # print dbProject.created_at
        # if lastUpdate > dbProject.created_at and not created:
        #     dbProject = models.Project.objects.filter(name=project.repo).update(created_at=datetime.now())
        #     created = True

        #Store project
        print created
        if created:
            new_json['created'] = True

            #Store contributors
            contributors = project.getContributors()
            store_contributors(contributors, dbProject, project.user)

            #Clone project
            localDir = '/tmp/FOSS_Analysis'
            repoDir = localDir + '/' + project.user + '/' + project.repo
            if not os.path.exists(repoDir):
                Repo.clone_from(url, repoDir)

            #Analyze project
            repo = Repo(repoDir)
            scans = analyzer.scanFolder(repo, repoDir)
            new_json['num_files'] = len(scans)

            #Store project contents
            store_project_contents(scans, dbProject, new_json)

        else:
            dbFiles = models.File.objects.filter(project=dbProject)
            new_json['num_files'] = len(dbFiles)
            files = formatFiles(dbFiles)

            new_json['files'] = files

        return HttpResponse(json.dumps(new_json))
