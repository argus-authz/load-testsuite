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

TESTID = 201

def parallel_test(self):
    id_range = self.range_permit.split(",")
    resource_id = "%s%03d" % (self.resource_id, int(id_range[0]))
    endpoint = get_endpoint(self, grinder.threadNumber)
    method_info = "parallel_test - resourceid=[%s] actionid=[%s] endpoint=[%s]" % (resource_id, self.action_id, endpoint)
    log.debug("START %s" % method_info)
    pep_client = create_client(endpoint, self.ca_dirname, self.client_cert, self.client_key, self.client_passwd)
    certs = get_user_cert(self.proxy_path, self.client_passwd)
    request = create_request(certs, resource_id, self.action_id)
    self.request_barrier.await()
    response = pep_client.authorize(request)
    result = response.getResults().get(0)
    decision = result.getDecision()
    check_result(decision, Result.DECISION_PERMIT)
    log.debug("END %s" % method_info)

class TestRunner:
    def __init__(self):
        method_info = "init"
        log.debug("START %s" % method_info)
        load_props(self)
        self.request_barrier = grinder.barrier("Request")
        log.debug("END %s" % method_info)
        
    def __call__(self):
        method_info = "call"
        log.debug("START %s" % method_info)
        
        try:
            test = Test(TESTID, "Argus PEPD parallel test")
            test.record(parallel_test)
            
            parallel_test(self)
            
        except Exception, e:
            log.error("Error executing PEPD test: %s" % traceback.format_exc())
            
        log.debug("END %s" % method_info)