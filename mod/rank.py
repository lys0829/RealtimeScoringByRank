import requests
import logging
import json

from mod import config

logger = logging.getLogger(__name__)

class RankingWebServer(object):
    
    def __init__(self, url, user, passwd):
        self.url = url
        self.user = user
        self.passwd = passwd
    
    def get_raw(self, path):
        return (requests.get(self.url+path, auth=(self.user, self.passwd), headers={'content-type': 'application/json'})).text
    
    def get(self, path):
        return json.loads(self.get_raw(path))

    def put(self, path, body):
        requests.put(self.url+path, body, auth=(self.user, self.passwd), headers={'content-type': 'application/json'})
    
    def delete(self, path):
        requests.delete(self.url+path, auth=(self.user, self.passwd), headers={'content-type': 'application/json'})
    