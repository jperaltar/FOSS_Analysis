#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Github API methods to retrieve the different types of
information it contains.
"""

import requests
import re
import json

apiUrl = 'https://api.github.com/'
reqUser = 'jperaltar'
reqToken = '1b65a5ab2d26f585f179ee3efa681efec7f5dd23'
headers = {
    'User-Agent': 'FOSS_Analysis'
}

class GithubProject(object):
    def __init__(self, url):
        super(GithubProject, self).__init__()
        self.user = re.split(r'http[s]?://github.com/', url)[1].split('/')[0]
        self.repo = re.split(r'http[s]?://github.com/', url)[1].split('/')[1]

    def getOwner(self):
        url = apiUrl + 'users/' + self.user
        return json.loads(requests.get(url,
            headers=headers, auth=(reqUser, reqToken)).content)

    def getContributors(self):
        url = apiUrl + 'repos/' + self.user + '/' + self.repo + '/contributors'
        return json.loads(requests.get(url,
            headers=headers, auth=(reqUser, reqToken)).content)
