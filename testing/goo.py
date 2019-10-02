
###
 # Copyright 2017, Google, Inc.
 # Licensed under the Apache License, Version 2.0 (the `License`);
 # you may not use this file except in compliance with the License.
 # You may obtain a copy of the License at
 # 
 #    http://www.apache.org/licenses/LICENSE-2.0
 # 
 # Unless required by applicable law or agreed to in writing, software
 # distributed under the License is distributed on an `AS IS` BASIS,
 # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 # See the License for the specific language governing permissions and
 # limitations under the License.
### 

#!/usr/bin/python

import datetime
import time
import jwt
import paho.mqtt.client as mqtt
# from googleapiclient import mqtt
import random
# from jwt.contrib.algorithms.pycrypto import RSAAlgorithm

import socket
import errno  
import ssl


# Define some project-based variables to be used below. This should be the only
# block of variables that you need to edit in order to run this script

ssl_private_key_filepath = '[PATH_TO_PRIVATE KEY]'
ssl_algorithm = 'RS256' # Either RS256 or ES256
root_cert_filepath = '[PATH_TO_PUBLIC_KEY]'
project_id = '[PROJECT_ID]'
gcp_location = '[PROJECT_REGION]'
registry_id = '[REGISTRY_NAME]'
device_id = '[DEVICE_NAME]'
ca_cert = '[PATH_TO_GOOGLE_CERTIFICATE_KEY]'

# end of user-variables

cur_time = datetime.datetime.utcnow()

def create_jwt():
  token = {
      'iat': cur_time,
      'exp': cur_time + datetime.timedelta(minutes=60),
      'aud': project_id
  }

  with open(ssl_private_key_filepath, 'r') as f:
    private_key = f.read()

#   return jwt.encode(token, private_key, RSAAlgorithm(RSAAlgorithm.SHA256))
  return jwt.encode(token, private_key, ssl_algorithm)

_CLIENT_ID = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(project_id, gcp_location, registry_id, device_id)
_MQTT_TOPIC = '/devices/{}/state'.format(device_id)

client = mqtt.Client(client_id=_CLIENT_ID)
# authorization is handled purely with JWT, no user/pass, so username can be whatever
client.username_pw_set(
    username='unused',
    password=create_jwt())

def error_str(rc):
    return '{}: {}'.format(rc, mqtt.error_string(rc))

def on_connect(unusued_client, unused_userdata, unused_flags, rc):
    print('on_connect', error_str(rc))

def on_publish(unused_client, unused_userdata, unused_mid):
    print('on_publish')

client.on_connect = on_connect
client.on_publish = on_publish

client.tls_set(ca_certs=ca_cert, tls_version=ssl.PROTOCOL_TLSv1_2)
client.tls_insecure_set(True)

# client.connect('mqtt.googleapis.com', 8883)
client.connect('mqtt.googleapis.com', 443)
client.loop_start()

# // Subscribe to the /devices/{device-id}/config topic to receive config updates. 
client.subscribe('/devices/' + device_id + '/config', qos=0)
# client.loop_forever()

# # Could set this granularity to whatever we want based on device, monitoring needs, etc
temperature = 0
humidity = 0
pressure = 0

for i in range(1, 11):
  cur_temp = random.randint(0,10)
  cur_pressure = random.randint(0,10)
  cur_humidity = random.randint(0,10)

  temperature = cur_temp
  pressure = cur_pressure
  humidity = cur_humidity

  payload = '{{ "ts": {}, "temperature": {}, "pressure": {}, "humidity": {} }}'.format(int(time.time()), temperature, pressure, humidity)

  # Uncomment following line when ready to publish
  client.publish(_MQTT_TOPIC, payload, qos=1)

  print("{}\n".format(payload))

  time.sleep(1)

client.loop_stop()