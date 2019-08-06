from flask import Flask
from ubiquiti.unifi import UNIFI_API as UNIFI
from sys import argv

app = Flask(__name__)

@app.route('/')

def hello_world():

    while True:

        with UNIFI(username="admin", password="Smhau$31.%", site="default", baseurl="https://unifi.smarthaus.com.mx:8443", verify=False) as unifi:

            for user in unifi.list_clients():
                return user

