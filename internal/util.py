"""Helper static functions"""

from googleapiclient import discovery
from google.oauth2 import service_account
import config
import base64

def get_client(service_account_json, service_name):
    """Returns an authorized API client by discovering the IoT API and creating
    a service object using the service account credentials JSON."""
    api_scopes = ['https://www.googleapis.com/auth/cloud-platform']
    api_version = 'v1'
    discovery_api = 'https://cloudiot.googleapis.com/$discovery/rest'
    
    credentials = service_account.Credentials.from_service_account_file(
            service_account_json)
    scoped_credentials = credentials.with_scopes(api_scopes)

    discovery_url = '{}?version={}'.format(
            discovery_api, api_version)

    return discovery.build(
            service_name,
            api_version,
            discoveryServiceUrl=discovery_url,
            credentials=scoped_credentials)


def decode64(data):
        """Google Cloud Iot returns state data as base64 encoded strings.
        Use this Function to decode them."""
        return base64.b64decode(data)

def validate_region(region):
        """Checks if the region string sent from user is valid i.e. 'us' or 'eu'."""
        if region == config.cloud_region_eu:
                return True
        elif region == config.cloud_region_us:
                return True
        else:
                return False

def get_region_from_user(user):
        """Inputs google datastore object and extracts the user region.
        Converts region strings to region ids e.g. 'us' and converts to 'us-central1'."""
        if user[0].region == config.cloud_region_eu:
                return config.cloud_regions[config.cloud_region_eu]
        elif user[0].region == config.cloud_region_us:
                return config.cloud_regions[config.cloud_region_us]
        else:
                return None

def get_region_id(region_name):
        return config.cloud_regions[region_name]