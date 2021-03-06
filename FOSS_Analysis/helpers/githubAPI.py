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
reqToken = ''
headers = {
    'User-Agent': 'FOSS_Analysis'
}

class GithubProject(object):
    def __init__(self, url):
        super(GithubProject, self).__init__()
        self.user = re.split(r'http[s]?://github.com/', url)[1].split('/')[0]
        self.repo = re.split(r'http[s]?://github.com/', url)[1].split('/')[1]

    def getUpdateTime(self):
        url = apiUrl + 'repos/' + self.user + '/' + self.repo
        response = json.loads(requests.get(url,
            headers=headers, auth=(reqUser, reqToken)).content)
        return response['updated_at']

    def getOwner(self):
        url = apiUrl + 'users/' + self.user
        return json.loads(requests.get(url,
            headers=headers, auth=(reqUser, reqToken)).content)

    def getContributors(self):
        contributors = []
        url = apiUrl + 'repos/' + self.user + '/' + self.repo + '/contributors'
        response = json.loads(requests.get(url,
            headers=headers, auth=(reqUser, reqToken)).content)

        for item in response:
            contributors.append(json.loads(requests.get(item['url'],
                headers=headers, auth=(reqUser, reqToken)).content))

        return contributors
