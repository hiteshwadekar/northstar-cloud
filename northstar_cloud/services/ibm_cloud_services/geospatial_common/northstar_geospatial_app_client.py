import time
import json
import wiotp.sdk.device

# TODO: get from IoT service on IBM Cloud
IOT_ORGID="2rydnu"
IOT_APIKEY="a-2rydnu-3skwm5olpg"
IOT_AUTHTOKEN="IZLLmyrdA68uX9l54T"
NORTHSTAR_IOT_DEVICE_TYPE="northstar"
NORTHSTAR_IOT_DEVICE="northstar1"

myConfig = {
    "identity": {
        "appId": "northstarGeospatialAppClient"
    },
    "auth": {
        "key": IOT_APIKEY,
        "token": IOT_AUTHTOKEN
    },
    "options": {
        "domain": "internetofthings.ibmcloud.com",
        "logLevel": "debug",
        "http": {
            "verify": False
        },
        "mqtt": {
            "instanceId": "northstarGeospatialAppClientMQTT",
            "port": 8883,
            "transport": "tcp",
            "cleanStart": True,
            "sessionExpiry": 3600,
            "keepAlive": 60,
        }
    }
}


def deviceEventCallback(event):
    str = "%s event '%s' received from device [%s]: %s"
    print(str % (event.format, event.eventId, event.device, json.dumps(event.data)))

def commandCallback(cmd):
    print("Command received: %s" % cmd.data)


appClient = wiotp.sdk.application.ApplicationClient(config=myConfig)
appClient.connect()
appClient.deviceEventCallback = deviceEventCallback
appClient.commandCallback = commandCallback

# Subscribing to all events from all devices
appClient.subscribeToDeviceEvents()

#Each event message sent by the Geospatial Analytics service will look like:
#{ "deviceInfo": { "id": "64", "location": { "latitude": 36.1356304, "longitude": -115.1502579 },
# "originalMessage": "{\"ID\":64,\"lon\":-115.1502579,\"lat\":36.1356304,\"heading\":\"271.478\"}" },
# "eventType": "Exit", "regionId": "Tracking Path", "time": "13:19:21" }

commandData = {
  "deviceInfo":
  { "id": "64",
    "location": { "latitude": 36.1356304, "longitude": -115.1502579 },
    "originalMessage": "{\"ID\":64,\"lon\":-115.1502579,\"lat\":36.1356304,\"heading\":\"271.478\"}"
  },
  "eventType": "Entry",
  "regionId": "fireZone1",
  "time": "13:19:21"
}

# Publish test command to device
#appClient.publishCommand(NORTHSTAR_IOT_DEVICE_TYPE, NORTHSTAR_IOT_DEVICE, "geoAlert", "json", commandData)

time.sleep(2) # wait
# Publish test command emulating Geospatial service, to "iot-2/type/api/id/geospatial/cmd/geoAlert/fmt/json"
appClient.publishCommand("api", "geospatial", "geoAlert", "json", commandData)