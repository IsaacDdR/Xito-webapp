import urllib3
from requests import Session
import json
import re
import certifi
from typing import Pattern, Dict, Union
from requests_toolbelt.adapters import host_header_ssl
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 

class LoggedInException(Exception):

    def __init__(self, *args, **kwargs):
        super(LoggedInException, self).__init__(*args, **kwargs)

class UNIFI_API(object):

    def __init__(self, username: str="admin", password: str="Smhau$31.%", site: str="default", baseurl: str="https://unifi.smarthaus.com.mx:8443", verify: str="/home/capcrunch/Documents/Unifi"):

        self._login_data = {}
        self._current_satus_code = None
        self._login_data['username'] = username
        self._login_data['password'] = password
        self._site = site
        self._verify = verify
        self._baseurl = baseurl
        self._session = Session()

    def __enter__(self):

       self.login()
       return self

    def __exit__(self, *args):

        self.logout()

    def login(self):

        self._session.mount(self._baseurl, host_header_ssl.HostHeaderSSLAdapter())

        self._current_status_code = self._session.post("{}/api/login".format(self._baseurl), data=json.dumps(self._login_data), headers={"Host": "UniFi"}, verify=self._verify).status_code
        if self._current_status_code == 400:
            raise LoggedInException("Failed to log in to api with provided credentials")

    def logout(self):

        self._session.mount(self._baseurl, host_header_ssl.HostHeaderSSLAdapter())
        self._session.get("{}/logout".format(self._baseurl), headers={"Host": "UniFi"})
        self._session.close()

    def list_clients(self) -> list:

        r = self._session.get("{}/api/s/{}/stat/sta".format(self._baseurl, self._site, verify=self._verify), data="json={}")
        self._current_status_code = r.status_code

        if self._current_status_code == 401:
            raise LoggedInException("Invalid login, or login has expired")

        data = r.json()['data']

        return data

