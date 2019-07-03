
# Project NorthStar-Cloud

A microservices for providing NorthStar cloud operations.

NorthStar cloud is a set of gRPC-based distributed microservices (written in Python) that provide APIs and alerting for mobile end services. 
Northstar cloud services determine high risk wildfire conditions, determine active wildfire location, alert nearby users to be ready for evacuation or to evacuate, and provide safe coordinates for wildfire evacuation using IBM's analytics, weather, cloud and visual recognition services. 
The basic architecture of the NorthStar cloud is inspired by the Uber and Lyft model, which includes analytics to get the routes. 
This project is extensible and allows room to accommodate novel communication systems such as Project OWL (Call for Code 2018 winner), and data input from Project Lali (Call for Code 2018) via live fire sensors      


## Getting Started

## NorthStar Models

![Screenshot](examples/NorthStarModel.png)


### Prerequisites
Tools: Python, gRPC framework, MongoDB, Docker and Kubernetes.

First install required Python packages.

On Linux: `sudo apt install python python-dev python-pip sudo pip install -U tox`

On Mac: `brew install python`

Please refer below links for development tools to install (Mac OS),

Mongo:
https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/

Docker:
https://docs.docker.com/docker-for-mac/install/

Kubernetes:
https://matthewpalmer.net/kubernetes-app-developer/articles/guide-install-kubernetes-mac.html

### Installing
Now, navigate to the root of this repo (northstar-cloud)

``` shell
cd northstar-cloud/
pip install -r requirements.txt
python setup.py install or pip install .

Installing collected packages: northstar-cloud
  Found existing installation: northstar-cloud 0.0.1.dev12
    Uninstalling northstar-cloud-0.0.1.dev12:
      Successfully uninstalled northstar-cloud-0.0.1.dev12
  Running setup.py install for northstar-cloud ... done
Successfully installed northstar-cloud-0.0.1.dev12

```

To test everything is OK, run tox (automation testing library).

``` shell
tox -epy36
```

--------------------

### Running services

•	Run the server in one terminal root of this repo (northstar-cloud) ,
``` shell
~/git-repo-play/northstar-cloud$python northstar_cloud/cli/northstar_cloud_user_services_start.py 
2019-06-28 20:50:24,218 - __main__ - INFO - northstar-cloud: Service stating...
2019-06-28 20:50:24,221 - __main__ - INFO - northstar-cloud: is runnnig at localhost:50051
```

--------------------


•	 Run the northstar cloud user machine learning service. This enables alerts for high risk wildfire conditions. 

This service uses the hourly weather data and runs it against the trained Machine Learning model to infer if the current weather conditions show a high risk for wildfire occurrence at the location. For more information on the Machine Learning model and data, please see https://github.ibm.com/Rahul-Dalal/northstar.
TODO: A sample call to the ML model with sample data.


``` shell
~/git-repo-play/northstar-cloud$python northstar_cloud/cli/northstar_cloud_user_ml_start.py 
2019-06-28 21:04:13,636 - northstar_cloud.services.northstar_user_ml_analytics_service - INFO - weather_ml_analytics_job: checking weather fire patterns.
2019-06-28 21:04:13,653 - northstar_cloud.services.northstar_user_ml_analytics_service - INFO - _predict_fire: calling IBM ML analytics service.
2019-06-28 21:04:13,654 - northstar_cloud.services.ibm_cloud_services.ibm_weather_services - INFO - IBMWeatherServices: get_hourly_forecast for location lat: 37.32, lang: -122.03

```

If the current weather conditions show a high probability of wildfire, the following logs are seen, and an alert sent to users within a 10 mile radius to be aware of high risk conditions, 
prepare for a possible evacuation, and not accidentally start a wildfire.

``` bash
~/git-repo-play/northstar-cloud$python northstar_cloud/cli/northstar_cloud_user_ml_start.py
/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/sklearn/externals/six.py:31: DeprecationWarning: The module is deprecated in version 0.21 and will be removed in version 0.23 since we've dropped support for Python 2.7. Please rely on the official version of six (https://pypi.org/project/six/).
  "(https://pypi.org/project/six/).", DeprecationWarning)
2019-07-02 19:10:58,685 - northstar_cloud.services.northstar_user_ml_analytics_service - INFO - weather_ml_analytics_job: checking weather fire patterns.
2019-07-02 19:10:58,878 - northstar_cloud.services.northstar_user_ml_analytics_service - INFO - _predict_fire: calling IBM ML analytics service.
2019-07-02 19:10:58,882 - northstar_cloud.services.ibm_cloud_services.ibm_weather_services - INFO - IBMWeatherServices: get_hourly_forecast for location lat: 37.32, lang: -122.03
2019-07-02 19:10:58,882 - northstar_cloud.services.ibm_cloud_services.ibm_watson_ml_services - INFO - IBMWatsonMLAnalytics:predict_fire: IBM ML analytics request for user (6b1f8ddf-7863-4078-87c7-1d78851f1103, help.me)
**_2019-07-02 19:10:58,883 - northstar_cloud.services.northstar_user_ml_analytics_service - INFO - weather_ml_analytics_job: -- PREDICTED HIGH PROBABILITY OF WILDFIRE -- (latitude 37.32, longitude -122.03) ->_** 
2019-07-02 19:10:58,883 - northstar_cloud.services.northstar_user_ml_analytics_service - INFO - weather_ml_analytics_job: Using current weather data: {'time': 1518991200, 'summary': 'Clear', 'icon': 'clear-day', 'precipIntensity': 0, 'precipProbability': 0, 'temperature': 59.2, 'apparentTemperature': 59.2, 'dewPoint': -0.78, 'humidity': 0.09, 'pressure': 998.1, 'windSpeed': 10.74, 'windGust': 32.81, 'windBearing': 257, 'cloudCover': 0, 'uvIndex': 3, 'visibility': 9.997, 'latitude': '37.40208', 'longitude': '-118.50235', 'Date': '02/18/18', 'hour': 14, 'dayofyear': 49, 'monthofyear': 2}
2019-07-02 19:10:58,883 - northstar_cloud.services.northstar_user_ml_analytics_service - INFO - weather_ml_analytics_job: Searching for users within 10 miles for notification.
2019-07-02 19:10:58,886 - northstar_cloud.services.northstar_user_ml_analytics_service - INFO - _get_users_from_fire_range: User (help.me, 6b1f8ddf-7863-4078-87c7-1d78851f1103, 37.32, -122.03) is 0.0 miles away from fire at (37.32, -122.03)
2019-07-02 19:10:58,886 - northstar_cloud.services.northstar_user_ml_analytics_service - INFO - _get_users_from_fire_range: User (user2, cf23163e-108c-4e11-8765-e63c6fea5773, 37.39, -122.08) is 5.557874861808834 miles away from fire at (37.32, -122.03)
_**2019-07-02 19:10:58,887 - northstar_cloud.services.northstar_user_ml_analytics_service - INFO - weather_ml_analytics_job: ALERT USERS [('6b1f8ddf-7863-4078-87c7-1d78851f1103', 'help.me')] ABOUT HIGH PROBABILITY OF WILDFIRE NEAR (latitude 37.32, longitude -122.03)**_

```


------------------------------

•	Run the northstar cloud image visual recognition service. This enables crowdsourced wildfire reporting.

This service processes uploaded images of a reported wildfire, and uses IBM Visual Recognition Service to confirm the wildfire occurrence. The IBM Visual Recognition Service has been trained using images of wildfires and also smoky conditions, and images of fires which are not wildfires (as a negative class).
``` shell
~/git-repo-play/northstar-cloud$python northstar_cloud/cli/northstar_cloud_image_services_start.py 
2019-06-28 21:02:33,133 - northstar_cloud.services.northstar_image_scanning_service - INFO - scan_recently_uploaded_images: Scanning images for detecting fire... 

```

•	This service also sends alerts for active nearby wildfires: 

If a wildfire is detected using a user-uploaded image, the following logs will be seen, and an alert sent to users within a 10 mile radius that a wildfire is near them and to prepare for evacuation if needed.

```bash
2019-07-02 19:14:59,782 - northstar_cloud.services.northstar_image_scanning_service - INFO - scan_recently_uploaded_images: No images found to scan..
2019-07-02 19:15:09,784 - northstar_cloud.services.northstar_image_scanning_service - INFO - scan_recently_uploaded_images: Scanning images for detecting fire... 
**_2019-07-02 19:15:09,788 - northstar_cloud.services.northstar_image_scanning_service - INFO - scan_recently_uploaded_images: - DETECTED FIRE USING IMAGE UPLOADED BY USER ---- @(latitude 37.32, longitude -122.03)_** 
2019-07-02 19:15:09,788 - northstar_cloud.services.northstar_image_scanning_service - INFO - weather_ml_analytics_job: Searching for users within 10 miles for notification.

```

•	This service sends customized alerts for evacuation to a safe location depending on current wind conditions: 

Users within 10 miles of the path of the wildfire (determined through the wind direction) will be alerted to evacuate immediately, with safe coordinates to evacuate to. The safe coordinates are away from the fire and the direction of the wind. (The mobile app will show a navigation route to the safe coordinates.) 


```bash
2019-07-02 19:15:09,788 - northstar_cloud.services.northstar_image_scanning_service - INFO - weather_ml_analytics_job: Searching for users within 10 miles for notification.
2019-07-02 19:15:09,794 - northstar_cloud.services.northstar_image_scanning_service - INFO - _get_users_from_fire_range: User (help.me, 6b1f8ddf-7863-4078-87c7-1d78851f1103, 37.32, -122.03) is 0.0 miles away from fire at (37.32, -122.03)
2019-07-02 19:15:09,795 - northstar_cloud.services.northstar_image_scanning_service - INFO - _get_users_from_fire_range: User (user2, cf23163e-108c-4e11-8765-e63c6fea5773, 37.39, -122.08) is 5.557874861808834 miles away from fire at (37.32, -122.03)
**_2019-07-02 19:15:09,795 - northstar_cloud.services.northstar_image_scanning_service - INFO - scan_recently_uploaded_images: ALERT USERS [('6b1f8ddf-7863-4078-87c7-1d78851f1103', 'help.me')] THAT THEY ARE NEAR WILDFIRE. GET READY FOR POSSIBLE EVACUATION. WILL ALERT WHEN EVACUATION NEEDED._**
```


•	The service sends customized alerts for users with medical needs: 

If the mobile app user has indicated that they need medical attention, the safe coordinates will be that of a hospital.

```bash
~/git-repo-play/northstar-cloud$python northstar_cloud/cli/northstar_cloud_image_services_start.py 
2019-07-02 19:14:29,711 - northstar_cloud.services.northstar_image_scanning_service - INFO - scan_recently_uploaded_images: Scanning images for detecting fire... 
2019-07-02 19:14:29,770 - northstar_cloud.services.northstar_image_scanning_service - INFO - scan_recently_uploaded_images: No images found to scan..
2019-07-02 19:14:39,772 - northstar_cloud.services.northstar_image_scanning_service - INFO - scan_recently_uploaded_images: Scanning images for detecting fire... 
2019-07-02 19:14:39,773 - northstar_cloud.services.northstar_image_scanning_service - INFO - scan_recently_uploaded_images: No images found to scan..
2019-07-02 19:14:49,775 - northstar_cloud.services.northstar_image_scanning_service - INFO - scan_recently_uploaded_images: Scanning images for detecting fire... 
2019-07-02 19:14:49,777 - northstar_cloud.services.northstar_image_scanning_service - INFO - scan_recently_uploaded_images: No images found to scan..
2019-07-02 19:14:59,781 - northstar_cloud.services.northstar_image_scanning_service - INFO - scan_recently_uploaded_images: Scanning images for detecting fire... 
2019-07-02 19:14:59,782 - northstar_cloud.services.northstar_image_scanning_service - INFO - scan_recently_uploaded_images: No images found to scan..
2019-07-02 19:15:09,784 - northstar_cloud.services.northstar_image_scanning_service - INFO - scan_recently_uploaded_images: Scanning images for detecting fire... 
2019-07-02 19:15:09,788 - northstar_cloud.services.northstar_image_scanning_service - INFO - scan_recently_uploaded_images: - DETECTED FIRE USING IMAGE UPLOADED BY USER ---- @(latitude 37.32, longitude -122.03)
2019-07-02 19:15:09,788 - northstar_cloud.services.northstar_image_scanning_service - INFO - weather_ml_analytics_job: Searching for users within 10 miles for notification.
2019-07-02 19:15:09,794 - northstar_cloud.services.northstar_image_scanning_service - INFO - _get_users_from_fire_range: User (help.me, 6b1f8ddf-7863-4078-87c7-1d78851f1103, 37.32, -122.03) is 0.0 miles away from fire at (37.32, -122.03)
2019-07-02 19:15:09,795 - northstar_cloud.services.northstar_image_scanning_service - INFO - _get_users_from_fire_range: User (user2, cf23163e-108c-4e11-8765-e63c6fea5773, 37.39, -122.08) is 5.557874861808834 miles away from fire at (37.32, -122.03)
2019-07-02 19:15:09,795 - northstar_cloud.services.northstar_image_scanning_service - INFO - scan_recently_uploaded_images: ALERT USERS [('6b1f8ddf-7863-4078-87c7-1d78851f1103', 'help.me')] THAT THEY ARE NEAR WILDFIRE. GET READY FOR POSSIBLE EVACUATION. WILL ALERT WHEN EVACUATION NEEDED.
2019-07-02 19:15:09,796 - northstar_cloud.services.ibm_cloud_services.ibm_weather_services - INFO - IBMWeatherServices: get_current_forecast for location lat: 37.32, lang: -122.03
2019-07-02 19:15:10,046 - northstar_cloud.services.ibm_cloud_services.ibm_weather_services - INFO - IBMWeatherServices: get_current_forecast for location lat: 37.32, lang: -122.03
_**_2019-07-02 19:15:10,131 - northstar_cloud.services.northstar_image_scanning_service - INFO - scan_recently_uploaded_images: ALERT USERS WITH MEDICAL NEED (6b1f8ddf-7863-4078-87c7-1d78851f1103 , help.me) TO EVACUATE IMMEDIATELY TO HOSPITAL [].WILDFIRE IS APPROACHING_**_
2019-07-02 19:15:20,138 - northstar_cloud.services.northstar_image_scanning_service - INFO - scan_recently_uploaded_images: Scanning images for detecting fire... 
2019-07-02 19:15:20,140 - northstar_cloud.services.northstar_image_scanning_service - INFO - scan_recently_uploaded_images: No images found to scan..

```


--------------------

## Insert sample data

To insert sample data through client, run in other terminal root of this repo (northstar-cloud). 

``` shell
~/git-repo-play/northstar-cloud$python northstar_cloud/clients/northstart_user_services_client.py -h
usage: northstart_user_services_client.py [-h]
                                          [-create_user_json CREATE_USER_JSON]
                                          [-get_user_json GET_USER_JSON]
                                          [-upload_image_json UPLOAD_IMAGE_JSON]
                                          [-get_image_json GET_IMAGE_JSON]
                                          [-get_weather_json GET_WEATHER_JSON]

NorthStar cloud tools.

optional arguments:
  -h, --help            show this help message and exit
  -create_user_json CREATE_USER_JSON
                        Path to user information json format file.
  -get_user_json GET_USER_JSON
                        Path to get user information json format file.
  -upload_image_json UPLOAD_IMAGE_JSON
                        Path to user information json format file.
  -get_image_json GET_IMAGE_JSON
                        Path to user information json format file.
  -get_weather_json GET_WEATHER_JSON
                        Path to user information json format file.
```

--------------------

•	Insert Users:  

This sample data represents the user of the mobile app. In addition to personal data such as name and contact information, the data provided to the backend also includes the user's location and whether or not he needs medical attention in case of a mandatory evacuation.

```
~/git-repo-play/northstar-cloud$python northstar_cloud/clients/northstart_user_services_client.py -create_user_json examples/create-user1.json 
2019-06-28 20:52:45,631 - __main__ - INFO - northstar-service-client: Request :user {
  user_name: "help.me"
  first_name: "acb"
  last_name: "xyz"
  phone_number: "4089779890"
  home_address: "IBM Silicon valley"
  email_address: "abc@xyz.com"
  office_address: "IBM Silicon valley"
  app_id: "app_id_1"
  app_type: "iPhone"
  current_location {
    latitude: 37.3229978
    longitude: -122.0321823
  }
  health_info {
    need_medical_support: true
  }
}

2019-06-28 20:52:45,934 - __main__ - INFO - northstar-service-client: Response :success: true

NorthStar-Cloud: OUTPUT
NorthStar-Cloud: AddUser %s success: true
```

```
~/git-repo-play/northstar-cloud$python northstar_cloud/clients/northstart_user_services_client.py -create_user_json examples/create-user2.json 
2019-06-28 20:53:45,592 - __main__ - INFO - northstar-service-client: Request :user {
  user_name: "user2"
  first_name: "first2"
  last_name: "lastname2"
  phone_number: "9999999890"
  home_address: "IBM Silicon valley"
  email_address: "abc1@xyz.com"
  office_address: "IBM Silicon valley"
  app_id: "app_id_2"
  app_type: "iPhone"
  current_location {
    latitude: 37.3860517
    longitude: -122.0838511
  }
  health_info {
    need_medical_support: true
  }
}

2019-06-28 20:53:45,599 - __main__ - INFO - northstar-service-client: Response :success: true


NorthStar-Cloud: OUTPUT
NorthStar-Cloud: AddUser %s success: true
```

--------------------

•	Upload Image: 
This call is used by the mobile app to upload the image of a wildfire, to report the wildfire occurrence. This functionality enables crowdsourced wildfire reporting. The northstar cloud image visual recognition service will use this image to determine if a wildfire has started at or spread to the reported location.

```
~/git-repo-play/northstar-cloud$python northstar_cloud/clients/northstart_user_services_client.py -upload_image_json examples/upload-image.json 
2019-06-28 20:54:47,186 - __main__ - INFO - northstar-service-client: Request :image_name: "fire_burned.jpg"
image_format: JPEG
image: "{bytecode}"
user {
  user_name: "help.me"
}

2019-06-28 20:54:47,312 - __main__ - INFO - northstar-service-client: Response :success: true


NorthStar-Cloud: OUTPUT
NorthStar-Cloud: UploadFile resp -> %s success: true
```

--------------------

•	Get current weather: 
We get the current weather for the wildfire location using IBM Weather Company Data. This data is used to determine the wind direction during an active wildfire to determine its spreading behavior. This information is used to alert users within a 10 mile radius of the wildfire in the path of the wind directiob to evacuate.


```
~/git-repo-play/northstar-cloud$python northstar_cloud/clients/northstart_user_services_client.py -get_weather_json examples/weather-info.json 
2019-06-28 20:56:07,968 - northstar_cloud.services.ibm_cloud_services.ibm_weather_services - INFO - IBMWeatherServices: get_current_forecast for location lat: 37.3229978, lang: -122.0321823

NorthStar-Cloud: OUTPUT
NorthStar-Cloud: IBM Weather channel : 
{
    "class": "fod_short_range_hourly",
    "clds": 5,
    "day_ind": "N",
    "dewpt": 8,
    "dow": "Friday",
    "expire_time_gmt": 1561780962,
    "fcst_valid": 1561780800,
    "fcst_valid_local": "2019-06-28T21:00:00-0700",
    "feels_like": 18,
    "golf_category": "",
    "golf_index": null,
    "gust": 37,
    "hi": 18,
    "icon_code": 31,
    "icon_extd": 3100,
    "mslp": 1017.19,
    "num": 1,
    "phrase_12char": "Clear",
    "phrase_22char": "Clear",
    "phrase_32char": "Clear",
    "pop": 0,
    "precip_type": "rain",
    "qpf": 0.0,
    "rh": 51,
    "severity": 1,
    "snow_qpf": 0.0,
    "subphrase_pt1": "Clear",
    "subphrase_pt2": "",
    "subphrase_pt3": "",
    "temp": 18,
    "uv_desc": "Low",
    "uv_index": 0,
    "uv_index_raw": 0,
    "uv_warning": 0,
    "vis": 16.0,
    "wc": 18,
    "wdir": 327,
    "wdir_cardinal": "NNW",
    "wspd": 15,
    "wxman": "wx1500"
}



```


## Running the tests

End to end tests are yet to be fully implemented, however, to run the sample use the commands below:

Unit tests to run root of this repo (northstar-cloud),
``` shell
tox -epy36
```

Functional tests to run root of this repo (northstar-cloud),
``` shell
tox -efunctional
```


### And coding style tests

We are using Python PEP8 coding style while writting code, we run to check style to confirm it is acceptable, 
from root of this repo (northstar-cloud)
``` shell
tox -epep8
```

## Deployment
We have enabled kubernetes deployement, for production, using below yaml files, we can deploy and scale it on 
IBM Cloud kubernetes service

### Building and running northstar-cloud for kubernetes.

Local development is done using [minikube]
First, install kubernetes and minikube (refer Prerequisites section) and then start minikube cluster.

```
$ minikube start
Starting local Kubernetes v1.6.4 cluster...
Starting VM...
Moving files into cluster...
Setting up certs...
Starting cluster components...
Connecting to cluster...
Setting up kubeconfig...
Kubectl is now configured to use the cluster.
```

```
$ cd northstar-cloud
```

```
$ eval $(minikube docker-env)
```

```
$ docker build -t northstar-cloud .
```

gRPC server port configuration at, 

```bash
~/git-repo-play/northstar-cloud/minikube$ls -lrt
total 40
-rw-r--r--  1 887 Jun 26 20:29 northstar-image-scanning-service-deployement.yaml
-rw-r--r--  1 442 Jun 26 20:49 northstart-mongodb.yaml
-rw-r--r--  1 1262 Jun 27 23:42 northstar-api-service-deployement.yaml
-rw-r--r--  1 883 Jun 27 23:49 northstar-weather-service-deployement.yaml
-rw-r--r--  1 1010 Jun 28 20:00 northstar-service-config.yaml
```

Deploy service on k8s cluster,
```
$ cd minikube/
$ kubectl create -f .
```

```bash
~/git-repo-play/northstar-cloud/minikube$ kubectl get pod
NAME                                         READY     STATUS    RESTARTS   AGE
mongo-3764497210-g355s                       1/1       Running   0          1h
northstar-image-scanning-972372552-vvmxl     1/1       Running   0          1h
northstar-user-service-2440208372-h49v2      1/1       Running   0          1h
northstar-weather-service-3724735887-5tgjn   1/1       Running   0          1h
```

```bash
~/git-repo-play/northstar-cloud/minikube$ kubectl logs -f northstar-user-service-2440208372-h49v2 
2019-06-29 02:46:20,211 - northstar_cloud.cli.northstar_cloud_user_services_start - INFO - northstar-cloud: Service stating...
2019-06-29 02:46:20,214 - northstar_cloud.cli.northstar_cloud_user_services_start - INFO - northstar-cloud: is runnnig at localhost:50051

```

```bash

~/git-repo-play/northstar-cloud/minikube$ kubectl logs -f northstar-user-service-2440208372-h49v2 
2019-06-29 02:46:20,211 - northstar_cloud.cli.northstar_cloud_user_services_start - INFO - northstar-cloud: Service stating...
2019-06-29 02:46:20,214 - northstar_cloud.cli.northstar_cloud_user_services_start - INFO - northstar-cloud: is runnnig at localhost:50051
^C
~/git-repo-play/northstar-cloud/minikube$ kubectl logs -f northstar-image-scanning-972372552-vvmxl
2019-06-29 02:46:20,308 - northstar_cloud.services.northstar_image_scanning_service - INFO - scan_recently_uploaded_images: Scanning images for detecting fire... 
2019-06-29 02:46:40,887 - northstar_cloud.services.northstar_image_scanning_service - INFO - scan_recently_uploaded_images: No images found to scan..
2019-06-29 02:46:50,888 - northstar_cloud.services.northstar_image_scanning_service - INFO - scan_recently_uploaded_images: Scanning images for detecting fire... 

```

```bash
~/git-repo-play/northstar-cloud/minikube$kubectl logs -f northstar-image-scanning-972372552-vvmxl
2019-06-29 02:46:20,308 - northstar_cloud.services.northstar_image_scanning_service - INFO - scan_recently_uploaded_images: Scanning images for detecting fire... 
2019-06-29 02:46:40,887 - northstar_cloud.services.northstar_image_scanning_service - INFO - scan_recently_uploaded_images: No images found to scan..
2019-06-29 02:46:50,888 - northstar_cloud.services.northstar_image_scanning_service - INFO - scan_recently_uploaded_images: Scanning images for detecting fire... 
2019-06-29 02:46:50,891 - northstar_cloud.services.northstar_image_scanning_service - INFO - scan_recently_uploaded_images: No images found to scan..
2019-06-29 02:47:00,901 - northstar_cloud.services.northstar_image_scanning_service - INFO - scan_recently_uploaded_images: Scanning images for detecting fire...
```


## Development Start

All the end user mobile client API defined in ``northstar.proto`` and using ``build_proto.sh`` 
proto file can be build for python.


``` bash
~/git-repo-play/northstar-cloud/northstar_cloud/api/proto$ls -lrt
total 224
-rwxr-xr-x  1 Hitesh.Wadekar@ibm.com  staff    235 Jun  9 18:16 build_proto.sh
-rw-r--r--  1 Hitesh.Wadekar@ibm.com  staff      0 Jun 10 16:24 __init__.py
-rw-r--r--  1 Hitesh.Wadekar@ibm.com  staff  31798 Jun 20 21:38 northstar_pb2.py
-rw-r--r--  1 Hitesh.Wadekar@ibm.com  staff   6127 Jun 20 21:38 northstar_pb2_grpc.py
-rw-r--r--  1 Hitesh.Wadekar@ibm.com  staff   2185 Jun 25 17:52 northstar.proto
-rw-r--r--  1 Hitesh.Wadekar@ibm.com  staff  17156 Jun 25 18:49 northstar.grpc.swift
-rw-r--r--  1 Hitesh.Wadekar@ibm.com  staff  41740 Jun 25 18:49 northstar.pb.swift
```

The server and background (thread services) are defined here,
```bash
~/git-repo-play/northstar-cloud/northstar_cloud/services$ls -lrt
total 56
-rw-r--r--  1 Hitesh.Wadekar@ibm.com  staff     0 Jun  3 16:20 __init__.py
drwxr-xr-x  3 Hitesh.Wadekar@ibm.com  staff    96 Jun 27 16:15 project_lali_services
drwxr-xr-x  3 Hitesh.Wadekar@ibm.com  staff    96 Jun 27 16:15 project_owl_services
-rw-r--r--  1 Hitesh.Wadekar@ibm.com  staff  8044 Jun 27 16:23 northstar_user_services.py
-rw-r--r--  1 Hitesh.Wadekar@ibm.com  staff  4948 Jun 28 17:19 northstar_user_ml_analytics_service.py
drwxr-xr-x  5 Hitesh.Wadekar@ibm.com  staff   160 Jun 28 18:48 ml_models
drwxr-xr-x  7 Hitesh.Wadekar@ibm.com  staff   224 Jun 28 19:06 ibm_cloud_services
-rw-r--r--  1 Hitesh.Wadekar@ibm.com  staff  9085 Jun 28 19:57 northstar_image_scanning_service.py

```

## Built With
TO BE ADDED


## Presentation
[Keynote Presentation](examples/CFC_Northstar.key)


## Contributing
TO BE ADDED

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning
TO BE ADDED 

## Authors
* **Daxit Agarwal** - Daxit.Agarwal@ibm.com 
* **Rahul Dalal** - rahul.dalal@ibm.com
* **Uzma Siddiqui** - usiddiqu@us.ibm.com
* **Anita Chung** - chunga@us.ibm.com
* **Hitesh Wadekar** - hitesh.wadekar@ibm.com

if further questions, please reach me at: hitesh.wadekar@ibm.com or team northstar

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.


## Northstar mobile app repository
https://github.com/agarwaldax/cfc_northstar

## Northstar Machine learning repository
https://github.ibm.com/Rahul-Dalal/northstar

## License

This project is licensed under the Apache 2 License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Based on [Billie Thompson's README template](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2).



---------------


## Optional

The app also uses IBM Geospatial Analytics and Watson Internet of Things services to detect the app users entering or exiting active wildfire danger zones. 

- We created an instance of the Geospatial Analytics service on IBM Cloud.
- In IBM Cloud, we created a Cloud Foundry app of type `Internet of Things Platform Starter` which created the node-red app (https://northstar-nodered.mybluemix.net/red/#flow/) and the corresponding Internet of Things service instance.
- We used the MQTT server for the Watson IoT org, to  start the Geospatial Analytics service.


As a sample, from the directory `northstar-cloud/northstar_cloud/services/ibm_cloud_services/geospatial_common/` you can run 
`python northstar_geospatial.py`
This starts the Geospatial Analytics service instance with the following configurations:
```
$ python northstar_geospatial.py 
Starting Geospatial service
https://svc-cf.us-south.geospatial-analytics.cloud.ibm.com:443/jax-rs/geo/start/service_instances/be1bd479-e4ad-4c2c-b051-83cdadbe5f18/service_bindings/eec07b0a-7bd0-45f2-ab4c-23d0033a0bbf
{"mqtt_uri": "2rydnu.messaging.internetofthings.ibmcloud.com:8883", 
"mqtt_uid": "a-2rydnu-3skwm5olpg", 
"mqtt_pw": "...", 
"mqtt_input_topics": "iot-2/type/+/id/+/evt/location/fmt/json", 
"mqtt_notify_topic": "iot-2/type/api/id/geospatial/cmd/geoAlert/fmt/json",
"device_id_attr_name": "ID", 
"latitude_attr_name": "lat", 
"longitude_attr_name": "lon", 
"mqtt_client_id_input": "a:2rydnu:geoInput499", 
"mqtt_client_id_notify": "a:2rydnu:geoNotify226"}
<Response [200]>
{}
```
The configurations specify that the Geospatial Analytics service
- Uses the MQTT server and credentials of the Watson IoT org.
- Listens to incoming IoT device events on the input topic `iot-2/type/+/id/+/evt/location/fmt/json` via the Watson IoT platform. The device events publish the current location of the mobile app users at regular intervals to the topic `iot-2/type/northstar/id/_deviceid_/evt/location/fmt/json`. The latitude and longitude are specified using the fields `lat` and `lon` respectively in the MQTT JSON message.
- Publishes commands to the topic `iot-2/type/api/id/geospatial/cmd/geoAlert/fmt/json`. These commands are published if the devices are detected to enter or exit wildfire danger zones (added as circular 10-mile radius regions to the Geospatial service). The commands are of the format:
```
{ "deviceInfo": { "id": "64", "location": { "latitude": 36.1356304, "longitude": -115.1502579 }, "originalMessage": "{\"ID\":64,\"lon\":-115.1502579,\"lat\":36.1356304,\"heading\":\"271.478\"}" }, "eventType": "Entry", "regionId": "Wildfire Zone Morgan Hill", "time": "13:19:21" } 
```

The script also adds a sample wildfire danger zone by adding a circular region to the Geospatial service, which starts at the reported coordinates of the wildfire, and has a 10-mile radius. It also specifies to notify if a device exits or enters the region.
```
Adding region to Geospatial
https://svc-cf.us-south.geospatial-analytics.cloud.ibm.com:443/jax-rs/geo/addRegion/service_instances/be1bd479-e4ad-4c2c-b051-83cdadbe5f18/service_bindings/eec07b0a-7bd0-45f2-ab4c-23d0033a0bbf

<Response [200]>
{}
Checking status for Geospatial
https://svc-cf.us-south.geospatial-analytics.cloud.ibm.com:443/jax-rs/geo/status/service_instances/be1bd479-e4ad-4c2c-b051-83cdadbe5f18/service_bindings/eec07b0a-7bd0-45f2-ab4c-23d0033a0bbf
<Response [200]>
{"status_code": 2, "custom_regions": ..., "regular_regions": [...
{"numberOfSides": 30, 
"minimumDwellTime": 0, 
"distanceToVerticesInMeters": 16093, 
"notifyOnExit": true, 
"id": "fireZone1", 
"centerLat": 36.12, 
"notifyOnEntry": true, 
"remove": false, 
"timeout": 0, 
"centerLong": -115.224},
...]}

```


- In the Watson IoT instance, we created a device type named `northstar`, and a sample device named `northstar1` of device type `northstar`. Each device represents a Northstar mobile app user.


- We created a Watson IoT device client which simulates the IoT device client for the device `northstar1`. We use the `Python for IBM Watson IoT Platform` (https://github.com/ibm-watson-iot/iot-python) library for connecting to IBM Watson IoT using Python 3.x.

You can  run the following script:
`python northstar_geospatial_device_client.py`

The device client publishes its current coordinates to the MQTT topic `iot-2/type/northstar/id/northstar1/evt/location/fmt/json`.

- We created a Watson IoT app client which simulates the IoT app client
You can  run the following script:
`python northstar_geospatial_app_client.py`

The app client listens to device events:
```
json event 'location' received from device [northstar:northstar1]: {"ID": "northstar1", "lat": "40", "lon": "-120"}
json event 'location' received from device [northstar:northstar1]: {"ID": "northstar1", "lat": "36.12", "lon": "-115.224"}
json event 'location' received from device [northstar:northstar1]: {"ID": "northstar1", "lat": "45", "lon": "100"}
```

It also publishes commands to `iot-2/type/api/id/geospatial/cmd/geoAlert/fmt/json`.


---------------

You can open the Node-RED starter app at https://northstar-nodered.mybluemix.net/red/#flow/2b328ba4.5e07c4
and see the debug window for the device events and commands:

```
6/27/2019, 8:43:41 AMnode: device data
iot-2/type/northstar/id/northstar1/evt/location/fmt/json : msg : Object
object
topic: "iot-2/type/northstar/id/northstar1/evt/location/fmt/json"
payload: object
deviceId: "northstar1"
deviceType: "northstar"
eventType: "location"
format: "json"
_msgid: "b3790c5f.3711c"
6/27/2019, 8:43:45 AMnode: device command
iot-2/type/api/id/geospatial/cmd/geoAlert/fmt/json : msg.payload : Object
object
deviceInfo: object
eventType: "Entry"
regionId: "fireZone1"
time: "13:19:21"
```

---------------

Future work for Geospatial Analytics integration:
- Register the Northstar Cloud backend service as a Watson IoT App client which listens to incoming device commands on `iot-2/type/api/id/geospatial/cmd/geoAlert/fmt/json` sent by the Geospatial Analytics service.  In response to incoming device commands, the backend will detect if a mobile app user has entered an active wildfire danger zone, and send it an alert to leave the zone, and specify safe coordinates for the user to navigate to.

- Add functionality to register each mobile app user as a Watson IoT device of type `northstar`.

- Add functionality for each mobile app user to simulate a Watson IoT device client which publishes its location information at short regular intervales to the MQTT topic `iot-2/type/northstar/id/_deviceid_/evt/location/fmt/json`

