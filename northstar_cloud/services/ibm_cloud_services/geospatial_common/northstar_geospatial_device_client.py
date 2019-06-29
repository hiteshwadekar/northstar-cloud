import wiotp.sdk.device
import time
import json

# TODO: get from IoT service on IBM Cloud
IOT_ORGID="2rydnu"
IOT_APIKEY="a-2rydnu-3skwm5olpg"
IOT_AUTHTOKEN="IZLLmyrdA68uX9l54T"
NORTHSTAR_IOT_DEVICE_TYPE="northstar"
NORTHSTAR_IOT_DEVICE="northstar1"

NORTHSTAR_IOT_DEVICEAUTHTOKEN="mynorthstart0ken"

myConfig = {
  "identity": {
    "orgId": IOT_ORGID,
    "typeId": NORTHSTAR_IOT_DEVICE_TYPE,
    "deviceId": NORTHSTAR_IOT_DEVICE
  },
  "auth": {
    "token": NORTHSTAR_IOT_DEVICEAUTHTOKEN
  }
}
def deviceCommandCallback(cmd):
    print("Command received: %s" % cmd.data)

def deviceEventCallback(event):
    str = "%s event '%s' received from device [%s]: %s"
    print(str % (event.format, event.eventId, event.device, json.dumps(event.data)))

client = wiotp.sdk.device.DeviceClient(config=myConfig)
client.connect()
client.commandCallback = deviceCommandCallback
client.deviceEventCallback = deviceEventCallback


locationData={'ID':NORTHSTAR_IOT_DEVICE, 'lat':  "40", 'lon':"-120"}
client.publishEvent(eventId="location", msgFormat="json", data=locationData, qos=0, onPublish=None)

time.sleep(2)
locationData={'ID':NORTHSTAR_IOT_DEVICE, 'lat':  "36.12", 'lon':"-115.224"}
client.publishEvent(eventId="location", msgFormat="json", data=locationData, qos=0, onPublish=None)

time.sleep(2)
locationData={'ID':NORTHSTAR_IOT_DEVICE, 'lat':  "45", 'lon':"100"}
client.publishEvent(eventId="location", msgFormat="json", data=locationData, qos=0, onPublish=None)

time.sleep(1000) # wait