# gcloud-iot-appengine
A project to easily deploy a google clout Iot application on google app engine.

## Introduction
Google Iot Core makes use of several Google Cloud Integrations. This project aims to provide a simplified system to create registries and devices of Core Iot using Google App Engine.

## Functionality
The application, once deployed can perform the following functions. Returns in text/plain format.

* Create new registry:
```
curl -X POST -d "registry=[REGISTRY_NAME]&region=['us' or 'eu']" [URL]/accounts
```

* Check if registry exists:
```
curl -X GET [URL]/accounts?registry=[REGISTRY_NAME]
```

* Create new device:
```
curl -X PUT -F data=@[PATH_TO_PUBLIC_KEY] -F registry=[REGISTRY_NAME] -F device=[DEVICE_NAME] [URL]/accounts
```

* Fetch telemetry data for device:
```
curl -X GET "[URL]/data?registry=[REGISTRY_NAME]&states=[NUMBER_OF_STAES]&device=[DEVICE_NAME]"
```

## Getting Started

### Prerequisits
The following actions must be taken after cloaning the repository.

* Intsall Python 2.7
* Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/quickstarts) package
* Install project dependencies:
```
pip install -t lib -r requirements.txt
```
