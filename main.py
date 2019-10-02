# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

from internal.datastore import Datastore
from internal.iot import IOT
from internal.util import decode64, get_region_from_user, validate_region, get_region_id

class Data(webapp2.RequestHandler):
    def get(self):
        """Fetches telemetry data for a paticular device.
        curl -X GET "[URL]/data?registry=[REGISTRY_NAME]&states=[NUMBER_OF_STATES]&device=[DEVICE_NAME]" """
        dev =  self.request.get('device')
        reg =  self.request.get('registry')
        states = self.request.get('states')

        self.response.headers['Content-Type'] = 'text/plain'
        if (not dev) or len(dev)==0:
            self.response.write('parameter dev not found')
        elif (not reg) or len(reg)==0:
            self.response.write('parameter reg not found')
        elif (not states) or states <= 0:
            self.response.write('invalid or no states found')
        else:
            # Get user account
            ds = Datastore()
            user = ds.get_registry(reg)
            if len(user) == 0:
                self.response.write("Registry does not exist")
            else:
                region = get_region_from_user(user)

                # Add Device on IOT Core
                iot = IOT()
                success, message = iot.get_data(dev, reg, states, region)
                if success:
                    try:
                        for msg in message['deviceStates']:
                            msg['binaryData'] = decode64(msg['binaryData'])
                        self.response.write(message)
                    except:
                        self.response.write([])
                else:
                    self.response.write(message)
        

class Accounts(webapp2.RequestHandler):
    def get(self):
        """Checks if a registry exists.
        curl -X GET [URL]/accounts?registry=[REGISTRY_NAME] """
        reg =  self.request.get('registry')
        if reg and len(reg) > 0:
            ds = Datastore()
            self.response.headers['Content-Type'] = 'text/plain'
            try:
                check = ds.check_registry_exists(reg)
                if check:
                    self.response.write("Registry Account Exists")
                else:
                    self.response.write("Registry Account Not Found")
            except Exception as error:
                self.response.write(error.message)
        else:
            self.response.write('parameter reg not found')

    def post(self):
        """Creates a new registry
        curl -X POST -d "registry=[REGISTRY_NAME]&region=['us' or 'eu']" [URL]/accounts """
        reg =  self.request.get('registry')
        region_name =  self.request.get('region')
        if reg and len(reg) > 0 and reg.isalnum() and validate_region(region_name):
            region = get_region_id(region_name)
            # Create Registry on IOT Core
            iot = IOT()
            success, message = iot.create_registry(region,reg)
            if success:
                # Add registry to Datastore
                ds = Datastore()
                status = ds.add_registry(reg, region_name)
                self.response.headers['Content-Type'] = 'text/plain'
                if status:
                    self.response.write('Registry Added')
                else:
                    self.response.write('Registry already exists')
            else:
                self.response.write(message)
        else:
            self.response.write('invalid parameters: ' + reg + " " + region_name )

    def put(self):
        """Creates a new device.
        curl -X PUT -F data=@[PATH_TO_PUBLIC_KEY] -F registry=[REGISTRY_NAME] -F device=[DEVICE_NAME] [URL]/accounts """
        dev =  self.request.get('device')
        reg =  self.request.get('registry')
        uploaded_file = self.request.POST.get('data')
        data = uploaded_file.file.read()

        self.response.headers['Content-Type'] = 'text/plain'
        if (not dev) and len(dev)==0:
            self.response.write('parameter device not found')
        elif (not reg) and len(reg)==0:
            self.response.write('parameter registry not found')
        elif (not data) and len(data)==0:
            self.response.write('invalid or no key file found')
        else:
            # Get user account
            ds = Datastore()
            user = ds.get_registry(reg)
            if len(user) == 0:
                self.response.write("Registry does not exist")
            else:
                region = get_region_from_user(user)

                # Add Device on IOT Core
                iot = IOT()
                success, message = iot.create_device(dev, reg, data, region)
                if success:
                    self.response.write('Device Added')
                else:
                    self.response.write(message)
        


app = webapp2.WSGIApplication([
    ('/accounts', Accounts),
    ('/data', Data)
], debug=True)
