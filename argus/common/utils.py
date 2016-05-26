from net.grinder.script.Grinder import grinder
from net.grinder.script import Test
from org.glite.authz.pep.client import PEPClient, PEPClientException
from org.glite.authz.pep.client.config import PEPClientConfiguration, PEPClientConfigurationException
from org.glite.authz.pep.profile import CommonXACMLAuthorizationProfile
from org.glite.authz.common.security import PEMFileReader
from org.glite.authz.common.model import Request, Response, Result
import os
import traceback
from random import randint

log = grinder.logger
props = grinder.getProperties()

def not_null(label, value):
    test = (label is None) or (value is not None and value == "")
    if test:
        raise Exception("%s is empty" % label)

def check_result(value, expected):
    if value != expected:
        msg = "Result value mismatch. Obtained [%s] instead of [%s]" % (value, expected)
        raise Exception(msg)
    
def get_resource_id(self, id_range):
    rand = randint(int(id_range[0]), int(id_range[1]))
    resource_id = "%s%03d" % (self.resource_id, rand)
    return resource_id

def get_endpoint(self, thread_id):
    idx = thread_id % len(self.endpoint_list)
    endpoint = self.endpoint_list[idx]
    return endpoint

def create_client(endpoint, ca_dirname, client_cert, client_key, client_passwd):
    method_info = "create_client - endpoint=[%s] cert=[%s] key=[%s]" % (endpoint, client_cert, client_key)
    log.debug("START %s" % method_info)
    config = PEPClientConfiguration()
    config.addPEPDaemonEndpoint(endpoint)
    config.setTrustMaterial(ca_dirname)
    config.setKeyMaterial(client_cert, client_key, client_passwd)
    pep_client = PEPClient(config)
    log.debug("END %s" % method_info)
    return pep_client

def get_user_cert(proxy_path, proxy_passwd):
    method_info = "ger_user_cert - proxypath=[%s]" % proxy_path
    log.debug("START %s" % method_info)
    reader = PEMFileReader()
    certs = reader.readProxyCertificates(proxy_path, proxy_passwd)
    log.debug("END %s" % method_info)
    return certs

def create_request(user_certs, resource_id, action_id):
    method_info = "create_request - resourceid=[%s] actionid=[%s]" % (resource_id, action_id)
    log.debug("START %s" % method_info)
    profile = CommonXACMLAuthorizationProfile.getInstance()
    request = profile.createRequest(user_certs, resource_id, action_id)
    log.debug("END %s" % method_info)
    return request

def load_props(self):
    method_info = "load_props"
    log.debug("START %s" % method_info)
    self.ca_dirname = props["common.cadirname"]
    self.client_cert = props["common.clientcert"]
    self.client_key = props["common.clientkey"]
    self.client_passwd = props["common.clientpasswd"]
    self.endpoints = props["common.pepd.endpoints"]
    self.endpoint_list = self.endpoints.split()
    self.resource_id = props["common.pepd.resourceid"]
    self.range_permit = props["common.pepd.resourceid.range.permit"]
    self.range_deny = props["common.pepd.resourceid.range.deny"]
    self.range_not_appl = props["common.pepd.resourceid.range.notappl"]
    self.action_id = props["common.pepd.actionid"]
    uid = os.geteuid()
    self.proxy_path = os.getenv('X509_USER_PROXY', "/tmp/x509up_u%s" % uid)
    log.debug("END %s" % method_info)
