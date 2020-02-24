
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import logging
import grpc
from casbin import casbin_pb2, casbin_pb2_grpc
import os
from omniscient.settings import BASE_DIR, CASBIN_SERVER_IP
file_path = os.path.join(BASE_DIR, "casbin/model.conf")

class Client:
    ADDRESS = f'{CASBIN_SERVER_IP}:50051'

    def NewClient(self, address=""):
    	print("NewClient called")
    	channel = grpc.insecure_channel(address or self.ADDRESS)
    	stub = casbin_pb2_grpc.CasbinStub(channel)
    	adapter = stub.NewAdapter(casbin_pb2.NewAdapterRequest())
    	with open(file_path, 'r') as file:
    		data = file.read()
    	enforcer = stub.NewEnforcer(casbin_pb2.NewEnforcerRequest(modelText=data, adapterHandle= adapter.handler))
    	return [stub, enforcer]

    def AddPolicy(subject, domain, obj, action):
        stub.AddPolicy(casbin_pb2.PolicyRequest(enforcerHandler= enforcer.handler, params=[subject, domain, obj, action]))

    def AddGroupingPolicy(subject, group, domain):
        stub.AddGroupingPolicy(casbin_pb2.PolicyRequest(enforcerHandler=enforcer.handler, params=[subject, group, domain]))

    def CheckPermissions(subject, domain, obj, action):
        allowed = stub.Enforce(casbin_pb2.EnforceRequest(enforcerHandler=enforcer.handler, params=[subject, domain, obj, action]))
        return allowed.res


c = Client().NewClient()
stub = c[0]
enforcer = c[1]