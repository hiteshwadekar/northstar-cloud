# smart-detective-api

A microservice for providing detective decision over witness's input.

### Design

Requirements
As the detective, we have to put together a timeline of events, in the order they occurred. The longer the resulting timeline is, the better. 
If all witnesses present a single sequence of events or if at least parts of them can be combined to create a longer timeline then the probability of a successful conviction goes up. 
Therefore, it’s important to merge their timelines to the maximum degree possible. However, the ordering of events must be absolutely correct or else the judge will throw the case out.  
In case there are events in those timelines that cannot be strictly ordered, it is better to present multiple separate timelines. 
Therefore, for each case, merge as many of the timelines as possible.  More specifically: 

if all witnesses remember events in a fully consistent manner then present a single merged timeline, 
if some of the events they remember can be combined or if some of them can be extended without fully merging them then present multiple timelines with events merged across them to the degree possible 
if none of the events can be combined or extended then present the original unmodified timelines

Considering above requirement, the ordering of events must be correct. Since each witnesses saw events in different timeline but in ordered. We used Graph data structure to build ordered wintesses events. Each event would be a vertex in graph, an edge between two events if both one comes before in timeline. Topological sort has been used for linear ordering of vertices such that for every directed edge uv, vertex u comes before v in the ordering.

Basic Algorithm.
1. Build adjcancy list of Graph of all witness events.
2. Check if cycle present, if Yes: No merege possible.
3. Sort graph using topplogical sorting.
4. Find multiple path from souce and destination from topological sorting.
5. if multiple path coveres all events then merge possible.
6. else partial merge
7. if no path then no merge. 


### Developer Setup
Tools: Python, gRPC framework, Docker and Kubernetes.

First install some basic Python things.

if linux,
sudo apt install python python-dev python-pip
sudo pip install -U tox


Now, Go to the root of this repo (smart-detective-api)

To install detective-api,
``` shell
cd smart-detective-api/
pip install -r requirements.txt
python setup.py install
```

To test everything OK, run tox (automation testing library).

``` shell
tox -epy36
```

detective-api for witness event decision from cli,
``` shell
python detective_api/cli/detective_api_cli.py examples/example1.json

detective-api: OUTPUT
detective-api: Witness events given input     : [['fight', 'gunshot', 'fleeing'], ['gunshot', 'falling', 'fleeing']] 
detective-api: Witness events prediction      : WITNESS_DECISION_MERGE_ALL_POSSIBLE 
detective-api: Witness events predicted list  : [['fight', 'gunshot', 'falling', 'fleeing']] 

```

detective-api for witness event decision from gRPC API,

Run server in one terminal,
``` shell
python detective_api/api/detective_api_rpc.py

2019-04-29 20:44:36,151 - __main__ - INFO - detective-api: service stating...
2019-04-29 20:44:36,154 - __main__ - INFO - detective-api: is runnnig at ... localhost:50051
```

Run client in other terminal,
``` shell
python detective_api/api/detective_api_rpc_client.py examples/example1.json 

2019-04-29 20:45:39,309 - __main__ - INFO - detective-api-client: Request :witness_events {
  name: "fight"
  name: "gunshot"
  name: "fleeing"
}
witness_events {
  name: "gunshot"
  name: "falling"
  name: "fleeing"
}

2019-04-29 20:45:39,316 - __main__ - INFO - detective-api-client: Response :decision: WITNESS_DECISION_MERGE_ALL_POSSIBLE
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


### Building and Running smart-detective-api in Docker

Build docker image.

Run commands from ROOT directory (smart-detective-api)
``` shell
docker build -t smart-detective-api . 
```

Run smart-detective-api's docker container and test APIs 

``` shell
docker images
REPOSITORY                                        TAG                 IMAGE ID            CREATED             SIZE
smart-detective-api                               latest              642ac58bed81        8 hours ago         1.21GB

docker run -d -it --name detective-api smart-detective-api:latest

docker ps
CONTAINER ID        IMAGE                        COMMAND             CREATED             STATUS              PORTS               NAMES
fc9dbd868e87        smart-detective-api:latest   "python3"           4 seconds ago       Up 3 seconds                            detective-api

docker exec -it fc9dbd868e87 bash

CLI:
root@fc9dbd868e87:/usr/src/app# python detective_api/cli/detective_api_cli.py examples/example1.json 
2019-04-30 03:51:34,771 - detective_api.services.detective_api_service - INFO - init_aggregate_witness_events: Initializing input witness events [['fight', 'gunshot', 'fleeing'], ['gunshot', 'falling', 'fleeing']]
2019-04-30 03:51:34,771 - detective_api.services.detective_api_service - INFO - calculate_witness_merge: Calculating witness event merge for: [['fight', 'gunshot', 'fleeing'], ['gunshot', 'falling', 'fleeing']]

detective-api: OUTPUT
detective-api: Witness events given input : [['fight', 'gunshot', 'fleeing'], ['gunshot', 'falling', 'fleeing']] 
detective-api: Witness events prediction      : WITNESS_DECISION_MERGE_ALL_POSSIBLE 
detective-api: Witness events predicted list  : [['fight', 'gunshot', 'falling', 'fleeing']]


gRPC:
root@fc9dbd868e87:/usr/src/app# python detective_api/api/detective_api_rpc_client.py examples/example1.json 
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


### Building and running smart-detective-api for kubernetes.

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
$ cd smart-detective-api
```

```
$ eval $(minikube docker-env)
```

```
$ docker build -t smart-detective-api .
```

gRPC server port configuration at, 

```bash
~/smart-detective-api/minikube$ls -lrt
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
smart-detective-api-3517672685-n8gdp   1/1       Running   0          43s
```


```bash
kubectl logs smart-detective-api-3517672685-n8gdp
2019-04-30 03:58:35,152 - detective_api.api.detective_api_rpc - INFO - detective-api: service stating...
2019-04-30 03:58:35,156 - detective_api.api.detective_api_rpc - INFO - detective-api: is runnnig at ... localhost:50051
```


```shell
kubectl exec -it smart-detective-api-3517672685-n8gdp bash
root@smart-detective-api-3517672685-n8gdp:/usr/src/app# python detective_api/api/detective_api_rpc_client.py examples/example1.json 
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

if further questions, please reach me at: hitesh.wadekar@gmail.com
