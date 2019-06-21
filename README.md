# northstar-cloud

A microservice for providing NorthStar cloud operations.

### Design
Requirements


### Developer Setup
Tools: Python, gRPC framework, REST framework, MySQL, Docker and Kubernetes.

First install some basic Python things.

if linux,
sudo apt install python python-dev python-pip
sudo pip install -U tox


Now, Go to the root of this repo (northstar-cloud)

To install northstar-cloud,
``` shell
cd northstar-cloud/
pip install -r requirements.txt
python setup.py install
```

To test everything OK, run tox (automation testing library).

``` shell
tox -epy36
```

add user into northstar-cloud from cli,
``` shell
python northstar_cloud/clients/northstart_service.py examples/sample-user.json

2019-06-20 15:39:31,373 - __main__ - INFO - northstar-service-client: Request :user {
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
    latitude: 37.121
    longitude: -121.5655
  }
  health_info {
    need_medical_support: true
  }
}

2019-06-20 15:39:31,697 - __main__ - INFO - northstar-service-client: Response :success: true
```

Run server in one terminal,
``` shell
python northstar_cloud/cli/northstar_cloud_start.py 

2019-06-20 15:39:20,074 - __main__ - INFO - northstar-cloud: service stating...
2019-06-20 15:39:20,076 - __main__ - INFO - northstar-cloud: is runnnig at ... localhost:50051
```

Run client in other terminal,
``` shell
python northstar_cloud/clients/northstart_service.py examples/sample-user.json

2019-06-20 15:39:31,373 - __main__ - INFO - northstar-service-client: Request :user {
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
    latitude: 37.121
    longitude: -121.5655
  }
  health_info {
    need_medical_support: true
  }
}

2019-06-20 15:39:31,697 - __main__ - INFO - northstar-service-client: Response :success: true
```


### Building and Running northstar-cloud in Docker

Build docker image.

Run commands from ROOT directory (smart-detective-api)
``` shell
docker build -t northstar-cloud . 
```

Run northstar-cloud's docker container and test APIs 

``` shell
docker images
REPOSITORY                                        TAG                 IMAGE ID            CREATED             SIZE
northstar-cloud                                latest              642ac58bed81        8 hours ago         1.21GB

docker run -d -it --name northstar-cloud northstar-cloud:latest

docker ps
CONTAINER ID        IMAGE                        COMMAND             CREATED             STATUS              PORTS               NAMES
fc9dbd868e87        northstar-cloud:latest   "python3"           4 seconds ago       Up 3 seconds                            northstar-cloud

docker exec -it fc9dbd868e87 bash

CLI:
root@fc9dbd868e87:/usr/src/app# python northstar_cloud/cli/detective_api_cli.py examples/example1.json 
2019-04-30 03:51:34,771 - northstar_cloud.services.detective_api_service - INFO - init_aggregate_witness_events: Initializing input witness events [['fight', 'gunshot', 'fleeing'], ['gunshot', 'falling', 'fleeing']]
2019-04-30 03:51:34,771 - northstar_cloud.services.detective_api_service - INFO - calculate_witness_merge: Calculating witness event merge for: [['fight', 'gunshot', 'fleeing'], ['gunshot', 'falling', 'fleeing']]

detective-api: OUTPUT
detective-api: Witness events given input : [['fight', 'gunshot', 'fleeing'], ['gunshot', 'falling', 'fleeing']] 
detective-api: Witness events prediction      : WITNESS_DECISION_MERGE_ALL_POSSIBLE 
detective-api: Witness events predicted list  : [['fight', 'gunshot', 'falling', 'fleeing']]


gRPC:
root@fc9dbd868e87:/usr/src/app# python northstar_cloud/api/detective_api_rpc_client.py examples/example1.json 
2019-04-30 03:54:09,888 - __main__ - INFO - detective-api-client: Request :witness_events {
  name: "fight"
  name: "gunshot"
  name: "fleeing"
}
witness_events {
  name: "gunshot"
  name: "falling"
  name: "fleeing"
}

2019-04-30 03:54:09,893 - __main__ - INFO - detective-api-client: Response :decision: WITNESS_DECISION_MERGE_ALL_POSSIBLE
witness_events {
  name: "fight"
  name: "gunshot"
  name: "falling"
  name: "fleeing"
}

detective-api: OUTPUT
detective-api: Witness events given input : [['fight', 'gunshot', 'fleeing'], ['gunshot', 'falling', 'fleeing']] 
detective-api: Witness events prediction      : WITNESS_DECISION_MERGE_ALL_POSSIBLE 
detective-api: Witness events predicted list  : [['fight', 'gunshot', 'falling', 'fleeing']]
```


### Building and running northstar-cloud for kubernetes.

Local development is done using [minikube]
First, install kubernetes and minikube and then start minikube cluster.

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
~/northstar-cloud/minikube$ls -lrt
total 24
78 Apr 29 15:41 detective-api-config.json
204 Apr 29 22:30 detective-api-config.yaml
1102 Apr 29 22:30 detective-api-deployement.yaml
```

Deploy service on k8s cluster,
```
$ cd minikube/
$ kubectl create -f detective-api-deployement.yaml
```

```bash
$ kubectl get services
NAME                  TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)     AGE
kubernetes            ClusterIP   10.0.0.1     <none>        443/TCP     18d
smart-detective-api   ClusterIP   None         <none>        50051/TCP   9s
```


```bash
$ kubectl get pod
NAME                                   READY     STATUS    RESTARTS   AGE
northstar-cloud-3517672685-n8gdp   1/1       Running   0          43s
```


```bash
kubectl logs smart-detective-api-3517672685-n8gdp
2019-04-30 03:58:35,152 - northstar_cloud.api.detective_api_rpc - INFO - detective-api: service stating...
2019-04-30 03:58:35,156 - northstar_cloud.api.detective_api_rpc - INFO - detective-api: is runnnig at ... localhost:50051
```


```shell
kubectl exec -it smart-detective-api-3517672685-n8gdp bash
root@smart-detective-api-3517672685-n8gdp:/usr/src/app# python northstar_cloud/api/detective_api_rpc_client.py examples/example1.json 
2019-04-30 04:01:48,965 - __main__ - INFO - detective-api-client: Request :witness_events {
  name: "fight"
  name: "gunshot"
  name: "fleeing"
}
witness_events {
  name: "gunshot"
  name: "falling"
  name: "fleeing"
}

2019-04-30 04:01:48,968 - __main__ - INFO - detective-api-client: Response :decision: WITNESS_DECISION_MERGE_ALL_POSSIBLE
witness_events {
  name: "fight"
  name: "gunshot"
  name: "falling"
  name: "fleeing"
}

detective-api: OUTPUT
detective-api: Witness events given input : [['fight', 'gunshot', 'fleeing'], ['gunshot', 'falling', 'fleeing']] 
detective-api: Witness events prediction      : WITNESS_DECISION_MERGE_ALL_POSSIBLE 
detective-api: Witness events predicted list  : [['fight', 'gunshot', 'falling', 'fleeing']]
```

if further questions, please reach me at: hitesh.wadekar@ibm.com
