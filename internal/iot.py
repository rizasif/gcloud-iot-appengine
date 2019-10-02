from util import get_client, get_region_id
import config, io
from googleapiclient.errors import HttpError

class IOT:
    """Class to interact with the google cloud iot core"""

    def __init__(self):
        pass

    def get_client_by_region(self, region):
        """Creates a google authentication client provided the region of the serice account"""
        if region == config.cloud_regions[config.cloud_region_eu]:
            return get_client(config.service_file_eu, config.service_name_eu)
        else:
            return get_client(config.service_file_us, config.service_name_us)

    def get_project_id_by_region(self, region):
        if region == config.cloud_regions[config.cloud_region_eu]:
            return config.project_id_eu
        else:
            return config.project_id_us

    def create_registry(self, region, topic="default"):
        """Creates registry in the google cloud iot core
        --Inputs--
        region: The server region of cloud iot core.
        topic: The name of the topic for telemetry, also the name of the registry"""
        client = self.get_client_by_region(region)
        project_id = self.get_project_id_by_region(region)
        registry_parent = 'projects/{}/locations/{}'.format(
                project_id,
                region)
        body = {
            'eventNotificationConfigs': [{
                'pubsubTopicName': "projects/{}/topics/{}".format(project_id,topic)
            }],
            'id': topic
        }
        request = client.projects().locations().registries().create(
            parent=registry_parent, body=body)

        try:
            response = request.execute()
            return True, response
        except HttpError as error:
            return False, error

    def create_device(self, device_id, registry, certificate, region):
        """Creates device in the google cloud iot core
        --Inputs--
        device_id: Name of the device to be registered
        registry: Name of the registry
        certificate: The public RSA -x509 key of the device
        region: The server region of cloud iot core."""
        client = self.get_client_by_region(region)
        project_id = self.get_project_id_by_region(region)
        registry_name = 'projects/{}/locations/{}/registries/{}'.format(
        project_id, region, registry)

        # Note: You can have multiple credentials associated with a device.
        device_template = {
            'id': device_id,
            'credentials': [{
                'publicKey': {
                    'format': 'RSA_X509_PEM',
                    'key': certificate
                }
            }]
        }

        devices = client.projects().locations().registries().devices()
        try:
            return True, devices.create(parent=registry_name, body=device_template).execute()
        except HttpError as error:
            return False, error

    def get_data(self, device_id, registry, states, region):
        """Fetches telemetry data of a paticular device in Iot Core
        --Inputs--
        device_id: Name of the device to be registered
        registry: Name of the registry
        states: Number of telemetry data to be fetched
        region: The server region of cloud iot core."""
        client = self.get_client_by_region(region)
        project_id = self.get_project_id_by_region(region)
        registry_name = 'projects/{}/locations/{}/registries/{}'.format(
                project_id, region, registry)

        device_name = '{}/devices/{}'.format(registry_name, device_id)
        devices = client.projects().locations().registries().devices()

        try:
            return True, devices.states().list(name=device_name, numStates=states).execute()
        except HttpError as error:
            return False, error