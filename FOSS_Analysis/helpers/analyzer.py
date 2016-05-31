#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
License and copyright parser, using the scancode toolkit
"""

import sys
import os
import re
import subprocess
import json
from scancode.src.scancode import api as scancode
from scancode.src.licensedcode import detect as licenseDetect
from scancode.src.licensedcode import models as licenseModels
from pygments.lexers import guess_lexer, guess_lexer_for_filename
import magic
from git import Repo
from multiprocessing import Process, Manager, Pool
import time
import multiprocessing
from functools import partial

_INDEX = None
_LICENSES_BY_KEY = None

def loadIndexes():
    global _INDEX
    global _LICENSES_BY_KEY

    if _INDEX == None:
        _INDEX = licenseDetect.get_index()

    if _LICENSES_BY_KEY == None:
        _LICENSES_BY_KEY = licenseModels.get_licenses_by_key()

def readFile(location):
    content = ''
    with open(location, 'r') as openedFile:
        for line in openedFile:
            content += line

    return content

def getBlame(repo, file):
    authors = {}
    blame = repo.git.blame('--line-porcelain', file)
    prog = re.compile(r'author .*\nauthor-mail.*', re.MULTILINE)
    lines = prog.findall(blame)
    for line in lines:
        author = str(line.split('author ')[1].split('\n')[0])
        if authors.has_key(author):
            authors[author]['lines'] = authors[author]['lines'] + 1
        else:
            email = str(line.split('author-mail <')[1].split('>')[0])
            authors[author] = {}
            authors[author]['email'] = email
            authors[author]['lines'] = 1

    return authors

def scan(repo, scans, location):
    global _INDEX
    global _LICENSES_BY_KEY

    fileName = location.split('/')[-1]

    try:
        authors = getBlame(repo, location)
        content = readFile(location)
    except:
        authors = {}
        print "Non utf-8 file, " + fileName + "."
        return 0

    startTime = time.time()
    try:
        language = guess_lexer_for_filename(fileName, content).name
    except:
        language = ''

    copyrights = scancode.get_copyrights(content)
    print "Copyrights -- " + fileName

    licenses = scancode.get_licenses(content, _INDEX, _LICENSES_BY_KEY)
    print "Licenses -- " + fileName

    print "Done -- " + fileName + " time: " + str(time.time() - startTime)

    scans[location] = {
        'language': language,
        'copyrights': copyrights,
        'licenses': licenses,
        'authors': authors
    }

    return 1

def getFiles(folder, files):
    for file in os.listdir(folder):
        if file != ".git":
            localPath = folder + '/' + file
            if os.path.isfile(localPath):
                #type = magic.from_file(localPath, mime=True)
                #if "text" in type:
                files.append(localPath)
            elif os.path.isdir(localPath):
                getFiles(localPath, files)

def scanFolder(repo, location):
    jobs = []
    manager = Manager()
    scans = manager.dict()
    pool = Pool(2)

    startTime = time.time()
    files = []
    getFiles(location, files)
    func = partial(scan, repo, scans)
    list = pool.map(func, files)
    pool.close()
    pool.join()

    print time.time() - startTime
    return scans
