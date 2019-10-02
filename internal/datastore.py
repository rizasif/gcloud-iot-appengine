import config
from google.appengine.ext import ndb

class Registry(ndb.Model):
    """Google datastore class to define user object.
    value: name of the registry
    region: The server region it belongs to i.e. 'us' or 'eu'."""
    value = ndb.StringProperty(indexed=True)
    region = ndb.StringProperty(indexed=False)

class Datastore:
    """Class to interact with google datastore
    Putpose of datastore is to save registries of the user"""

    def add_registry(self, registry, region):
        """Creates a registry provided the name and region as strings."""
        exists = self.check_registry_exists(registry)
        if not exists:
            reg = Registry(value=registry, region=region)
            reg.put()
            return True
        else:
            return False

    def get_registry(self, registry):
        """Gets the registry object from google datastore 
        provided the registry name as a string"""
        return Registry.query(Registry.value == registry).fetch()

    def check_registry_exists(self, registry):
        """Checks a registry value exists in the datastore"""
        check = Registry.query(Registry.value == registry).fetch()
        if len(check) > 0:
            return True
        return False



    