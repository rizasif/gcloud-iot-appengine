# gcloud-iot-appengine
A project to easily deploy a google clout Iot application on google app engine.

[See Tutorial here](https://blog.rizasif.com/iot-appengine)

## Introduction
Google Iot Core makes use of several Google Cloud Integrations. This project aims to provide a simplified system to create registries and devices of Core Iot using Google App Engine (GAE).

## Functionality
The application, once deployed can perform the following functions. Returns in text/plain format.

* Create new registry:
A registry indicates a group of devices. This project assumes that each user has only one kind of device and they all transmit the same data. Therefore, only one registry is created. [REGISTRY_NAME] can be any alphanumeric string.
```
curl -X POST -d "registry=[REGISTRY_NAME]&region=['us' or 'eu']" [URL]/accounts
```

* Check if registry exists:
```
curl -X GET [URL]/accounts?registry=[REGISTRY_NAME]
```

* Create new device:
Inorder to create a new device, you will need to upload an RSA -x509 key. It is recommended to generate the key on the Iot device through OpenSSL. [This](https://cloud.google.com/iot/docs/how-tos/credentials/keys) resource can be useful.
```
curl -X PUT -F data=@[PATH_TO_PUBLIC_KEY] -F registry=[REGISTRY_NAME] -F device=[DEVICE_NAME] [URL]/accounts
```

* Fetch telemetry data for device:
Only limited amount of data can be fetched from Cloud Iot i.e 0 < [NUMBER_OF_STATES] <= 10.
```
curl -X GET "[URL]/data?registry=[REGISTRY_NAME]&states=[NUMBER_OF_STATES]&device=[DEVICE_NAME]"
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

### Setup Google Cloud
Setup your google cloud project and enable all required components.

#### Create Cloud Project
Create a new project at [google cloud console](https://console.cloud.google.com/). Remeber the [project_id] for future use.

#### Enable APIs
Go to `APIs and Services` in the console and enable the following
* [Pub/Sub](https://cloud.google.com/pubsub/docs/)
* [Realtime API](https://developers.google.com/realtime/overview)
* [Cloud Iot](https://cloud.google.com/iot-core/)
* [GAE](https://cloud.google.com/appengine/)

### Create Service Account
In order to allow GAE to access the Core Iot we have to create a service account.
* Go to `IAM & Admin` in cloud console and go to 'Service Accounts'.
* Create a new service account and give `Editor` access to it. Remeber the [service_name] for future use.
* Download the JSON key file and store it at the root of this project (in the same folder as app.yaml)

### Configure Project
Now we are ready to provide the code all essential variables and addresses to be deployed. In `internal/config.py` fill in the following variables (assuming we are using a USA region server).
```
[PROJECT_NAME_US] = [project_id]
[US_SERVER_ID] = The region name of your project e.g. us-central1
[US_SERVICE_ACCOUNT_NAME] = [service_name]
[US_SERVICE_ACCOUNT_FILE] = Name of your service account JSON key you downloaded.

[PROJECT_NAME_EU] = (Optional) [project_id] for EU region if being used.
[EU_SERVER_NAME] = (Optional) The region name of your project, if you are using multiple regions e.g. europe-central1
[EU_SERVICE_ACCOUNT_NAME] = (Optional) [service_name]
[EU_SERVICE_ACCOUNT_FILE] = (Optional) Name of your service account JSON key you downloaded. If you are using multiple regions.
```

### Deploying
Now the application can be deployed. Use the Goolgle Cloud SDK to deploy. Remember to select the correct project. [This](https://cloud.google.com/appengine/docs/standard/python/getting-started/deploying-the-application) resource can be helpful.
```
gcloud app deploy
```

## Multi-Region
Due to data security in production applications, it is essential to keep data of each continent e.g. US and EU, in their respective regions. In order to acheive this, we have a common GAE application (since, GAE does not store sensitive data) but keep separate projects for both regions. For the second reagion you will need separate service accounts, thus providing different JSON keys. Remeber to refer them accordingly in the config.py file.

## Testing
The `testing/goo.py` can be used to simulate an IOT device on any linux PC and send rendom data to the system. Fill in the required variables and you are good to go!