import wiotp.sdk.device
import time
import requests
import json
import numpy as np

# TODO: get from config/Geospatial service credentials on IBM Cloud
GEOSPATIAL_HOST='svc-cf.us-south.geospatial-analytics.cloud.ibm.com'
GEOSPATIAL_PORT= '443'
GEOSPATIAL_USER_ID='cf8a4fed-fc53-4b44-b975-7f6064493f80'
GEOSPATIAL_PASSWORD='835e4f76-9cd0-4ac0-a03a-f7da41621fac'
GEOSPATIAL_START_PATH='/jax-rs/geo/start/service_instances/be1bd479-e4ad-4c2c-b051-83cdadbe5f18/service_bindings/eec07b0a-7bd0-45f2-ab4c-23d0033a0bbf'
GEOSPATIAL_ADD_REGION_PATH='/jax-rs/geo/addRegion/service_instances/be1bd479-e4ad-4c2c-b051-83cdadbe5f18/service_bindings/eec07b0a-7bd0-45f2-ab4c-23d0033a0bbf'
GEOSPATIAL_REMOVE_REGION_PATH='/jax-rs/geo/removeRegion/service_instances/be1bd479-e4ad-4c2c-b051-83cdadbe5f18/service_bindings/eec07b0a-7bd0-45f2-ab4c-23d0033a0bbf'
GEOSPATIAL_STATUS_PATH='/jax-rs/geo/status/service_instances/be1bd479-e4ad-4c2c-b051-83cdadbe5f18/service_bindings/eec07b0a-7bd0-45f2-ab4c-23d0033a0bbf'
GEOSPATIAL_REGION_RADIUS = '16093' # 10 miles in meters

# TODO: get IoT service on IBM Cloud
IOT_ORGID="2rydnu"
IOT_APIKEY="a-2rydnu-3skwm5olpg"
IOT_AUTHTOKEN="IZLLmyrdA68uX9l54T"


def startGeospatial():
  headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
  # MQTT topic to notify once device enters or leaves a region
  notifyTopic=  "iot-2/type/api/id/geospatial/cmd/geoAlert/fmt/json"
  # MQTT topic to listen on for device location event
  inputTopic= "iot-2/type/+/id/+/evt/location/fmt/json"

  # MQTT client ID for notification
  notifyClientId = "a:"+IOT_ORGID+":geoNotify" + str(np.random.randint(0,999))
  # MQTT client ID for inputs
  inputClientId = "a:"+IOT_ORGID+":geoInput" + str(np.random.randint(0,999))

  startData = {
    'mqtt_uri': IOT_ORGID+".messaging.internetofthings.ibmcloud.com:8883",
    'mqtt_uid': IOT_APIKEY,
    'mqtt_pw':  IOT_AUTHTOKEN,
    'mqtt_input_topics': inputTopic,   # MQTT topic to listen on for device location event
    'mqtt_notify_topic': notifyTopic,  # MQTT topic to notify once device enters or leaves a region
    'device_id_attr_name':"ID",        # attribute in device event data that shows device ID
    'latitude_attr_name':'lat',        # attribute in device event data that shows device coordinate's latitude
    'longitude_attr_name':'lon',       # attribute in device event data that shows device coordinate's longitude
    'mqtt_client_id_input' : inputClientId,  # MQTT client ID for inputs
    'mqtt_client_id_notify' : notifyClientId # MQTT client ID for notification
  }

  request = "https://{}:{}{}".format(GEOSPATIAL_HOST,GEOSPATIAL_PORT,GEOSPATIAL_START_PATH)
  print(request)

  # curl -X PUT --tlsv1.2 -k --user "${userid}:${password}" -H "Accept: application/json" -H "Content-Type: application/json" --data "${start_params}" "${start_url}"
  print(json.dumps(startData))
  response = requests.put(request, data=json.dumps(startData), auth=(GEOSPATIAL_USER_ID, GEOSPATIAL_PASSWORD), headers=headers, verify=False)
  print(response)
  if response.status_code == 200:
    data = response.json()
    print(json.dumps(data))
  else:
    print('startGeospatial FAILED '+ str(response.status_code) + json.dumps(response.json()) )

def addGeospatialRegion(latitude, longitude, name ):

  headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

  addRegionData = {
    'regions': [ {
      'center_latitude': str(latitude),
      'center_longitude': str(longitude),
      'distance_to_vertices':   GEOSPATIAL_REGION_RADIUS,
      'name': name,
      'number_of_sides': '30', # emulate a circle
      'region_type': 'regular',
      'notifyOnEntry' : "true",  # generate notification on mqtt notification topic that device entered region
      'notifyOnExit' : "true" # generate notification on mqtt notification topic that device exited region
    }]
  }
  # add_region_url='https://${geo_host}:${geo_port}${add_region_path}'
  request = "https://{}:{}{}".format(GEOSPATIAL_HOST,GEOSPATIAL_PORT,GEOSPATIAL_ADD_REGION_PATH)
  print(request)

  # curl -X PUT --tlsv1.2 -k --user '${GEOSPATIAL_USER_ID}:${GEOSPATIAL_PASSWORD}' -H 'Accept: application/json' -H 'Content-Type: application/json' --data '${add_params}' '${GEOSPATIAL_ADD_REGION_URL}'
  response = requests.put(request, data=json.dumps(addRegionData), auth=(GEOSPATIAL_USER_ID, GEOSPATIAL_PASSWORD), headers=headers, verify=False)
  print(response)
  if response.status_code == 200:
    data = response.json()
    print(json.dumps(data))
  else:
    print('addRegion FAILED '+ str(response.status_code) + json.dumps(response.json()) )
  return

def getGeospatialStatus():
  headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
  #status_url="https://${geo_host}:${geo_port}${status_path}"
  #curl -X GET --tlsv1.2 -k --user "${userid}:${password}" -H "Accept: application/json" "${status_url}"
  request = "https://{}:{}{}".format(GEOSPATIAL_HOST,GEOSPATIAL_PORT,GEOSPATIAL_STATUS_PATH)
  print(request)
  response = requests.get(request, auth=(GEOSPATIAL_USER_ID, GEOSPATIAL_PASSWORD), headers=headers, verify=False)
  print(response)
  if response.status_code == 200:
    data = response.json()
    status_code = data['status_code']
    print(json.dumps(data))
  else:
    print('status FAILED '+ str(response.status_code) + json.dumps(response.json()) )
  return status_code

print("Starting Geospatial service")

startGeospatial()
print("Checking status for Geospatial")

while True:
  status_code = getGeospatialStatus()
  print(status_code)
  if(status_code == 2): # 2: The Geospatial Analytics service has started and is processing device location messages.
    break
  time.sleep(2) # wait

print("Adding region to Geospatial")

addGeospatialRegion(36.12,-115.224, 'fireZone1')
print("Checking status for Geospatial")
while True:
  status_code = getGeospatialStatus()
  print(status_code)
  if(status_code == 2): # 2: The Geospatial Analytics service has started and is processing device location messages. https://cloud.ibm.com/apidocs/geospatial-analytics?code=node#introduction
    break
  time.sleep(2) # wait


time.sleep(1000) # wait