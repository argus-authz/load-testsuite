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
from utils import *

log = grinder.logger
props = grinder.getProperties()

TESTID = 200

def do_test(endpoint, ca_dirname, client_cert, client_key, client_passwd, proxy_path, resource_id, action_id):
    method_info = "do_test"
    log.debug("START %s" % method_info)
    pep_client = create_client(endpoint, ca_dirname, client_cert, client_key, client_passwd)
    certs = get_user_cert(proxy_path, client_passwd)
    request = create_request(certs, resource_id, action_id)
    response = pep_client.authorize(request)
    log.debug("END %s" % method_info)
    return response

def test_permit(self):
    id_range = self.range_permit.split(",")
    resource_id = get_resource_id(self, id_range)
    endpoint = get_endpoint(self, grinder.threadNumber)
    method_info = "test_permit - resourceid=[%s]" % resource_id
    log.debug("START %s" % method_info)
    response = do_test(endpoint, self.ca_dirname, self.client_cert, self.client_key, self.client_passwd, self.proxy_path, resource_id, self.action_id)
    result = response.getResults().get(0)
    decision = result.getDecision()
    check_result(decision, Result.DECISION_PERMIT)
    log.debug("END %s" % method_info)

def test_deny(self):
    id_range = self.range_deny.split(",")
    resource_id = get_resource_id(self, id_range)
    endpoint = get_endpoint(self, grinder.threadNumber)
    method_info = "test_deny - resourceid=[%s]" % resource_id
    log.debug("START %s" % method_info)
    response = do_test(endpoint, self.ca_dirname, self.client_cert, self.client_key, self.client_passwd, self.proxy_path, resource_id, self.action_id)
    result = response.getResults().get(0)
    decision = result.getDecision()
    check_result(decision, Result.DECISION_DENY)
    log.debug("END %s" % method_info)

def test_not_applicable(self):
    id_range = self.range_not_appl.split(",")
    resource_id = get_resource_id(self, id_range)
    endpoint = get_endpoint(self, grinder.threadNumber)
    method_info = "test_not_applicable - resourceid=[%s]" % resource_id
    log.debug("START %s" % method_info)
    response = do_test(endpoint, self.ca_dirname, self.client_cert, self.client_key, self.client_passwd, self.proxy_path, resource_id, self.action_id)
    result = response.getResults().get(0)
    decision = result.getDecision()
    check_result(decision, Result.DECISION_NOT_APPLICABLE)
    log.debug("END %s" % method_info)

def authorize_test(self):
    test_permit(self)
    test_deny(self)
    test_not_applicable(self)

class TestRunner:
    def __init__(self):
        method_info = "init"
        log.debug("START %s" % method_info)
        load_props(self)
        log.debug("END %s" % method_info)
        
    def __call__(self):
        method_info = "call"
        log.debug("START %s" % method_info)
        
        try:
            test = Test(TESTID, "Argus PEPD test")
            test.record(authorize_test)
            
            authorize_test(self)
            
        except Exception, e:
            log.error("Error executing PEPD test: %s" % traceback.format_exc())
            
        log.debug("END %s" % method_info)