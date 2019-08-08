from sanic import Sanic
from sanic.response import json
from ubiquiti.unifi import UNIFI_API as UNIFI


app = Sanic()


@app.route('/')

async def test(request):


        with UNIFI(username ="admin", password="Smhau$31.%", site="default", baseurl="https://unifi.smarthaus.com.mx:8443", verify=False) as unifi:
            while True:
                return json(unifi.list_clients())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
