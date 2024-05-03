import time

import pytest
import unittest
import json
import os
import requests

# from pytest_schema import schema

from jsonschema import validate
from .param import Param as param
from .user import User
from .utils import db_connect
from .utils.reporting import reporting
from .utils import status, headers, users
from .token import Token
from .utils import cred_reference

from .schemas.pc_connectivity_schema import successful_schema, create_post_mouse_schema, create_post_pen_schema, \
    get_accessory, get_list_accessory, create_post_ownership, get_devcache_secapi, test_get_devcache_fapi, \
    create_order_with_invalid_username, create_order_successful_schema, create_post_keyboard_schema, \
    create_post_neg_keyboard_schema, create_post_neg_connectiontype_keyboard_schema, \
    create_post_mouse_invalid_type_schema, create_post_mouse_invalid_connectiontype_schema, get_neg_accessory, \
    test_get_list_neg_accessory, test_get_list_invalidsort_accessory, create_post_neg_ownership, \
    create_post_neg_serial_ownership, create_post_neg_pen_schema, create_post_association_schema, \
    create_post_neg_association_schema, create_post_neg_associationtype_schema, \
    create_api_dynamo_schema, get_device_successful_schema, \
    test_get_devcache_internal_device_schema, get_api_device_provision_schema

from .apis.pcconnectivity_mgt_svc import PC_Connectivity


class HPOnePCConnectivity(unittest.TestCase):
    user = User(users.USER_ID, None)
    PC_Connectivity = PC_Connectivity(user)
    token = Token()
    tenant_id = param.tenant_id
    accessory_id = param.accessory_id
    type = param.type
    tenant_id1 = param.tenant_id1
    accessory_id1 = param.accessory_id1
    device_id = param.device_id
    device_id1 = param.device_id1
    s_no = param.s_no
    s_no1 = param.s_no1

    stack = os.environ['HPONE_ENVIRONMENT']
    priorities = {}
    priority = os.environ['ADO_PRIORITY']
    mongo_auth = requests.auth.HTTPBasicAuth('vttUser', 'vtt@pass123')
    proxies = {
        'http': 'http://web-proxy.corp.hp.com:8080',
        'https': 'http://web-proxy.corp.hp.com:8080'
    }
    if stack == "dev":
        url = 'https://virtual-test-tools-dev.tropos-rnd.com/vtt-tools/api/testcases'
    elif stack == "pie":
        url = 'https://virtual-test-tools-pie.tropos-rnd.com/vtt-tools/api/testcases'
    elif stack == "stage":
        url = 'https://virtual-test-tools-stg.tropos-rnd.com/vtt-tools/api/testcases'

    test_cases = requests.get(url, auth=mongo_auth, proxies=proxies).json()
    for e in test_cases:
        if e['priority'] is None:
            priorities[e['uuid']] = True
        else:
            if e['priority'] != "Unassigned":
                if priority == "High" and e['priority'] == "High":
                    if e['enabled']:
                        priorities[e['uuid']] = False
                    else:
                        priorities[e['uuid']] = True
                elif priority == "Low" and e['priority'] != "High":
                    if e['enabled']:
                        priorities[e['uuid']] = False
                    else:
                        priorities[e['uuid']] = True
                else:
                    priorities[e['uuid']] = True
            else:
                priorities[e['uuid']] = True

    @pytest.fixture(autouse=True)
    def init(self):
        pass

    def setUp(self):
        os.environ['http_proxy'] = param.proxy_url
        os.environ['HTTP_PROXY'] = param.proxy_url
        os.environ['https_proxy'] = param.proxy_url
        os.environ['HTTPS_PROXY'] = param.proxy_url


    def teardown_class(self):
        param.result["directory"] = "pc_connectivity"
        # Open the test case file to get Jira epic data.
        with open('test_cases.txt', 'r') as file:
            for case in param.result['test_list']:
                for line in file:
                    split_line = line.split('|')
                    if split_line[0] == case['test_name']:
                        case['eqtr'] = split_line[1].rstrip('\n')
                        break
        with open('test_cases.txt', 'r') as file:
            for case in param.result['failed_api']:
                for line in file:
                    split_line = line.split('|')
                    if split_line[0] == case['test_name']:
                        case['eqtr'] = split_line[1].rstrip('\n')
                        break
        # Create result file for reporting.
        with open('result.json', 'w', encoding='utf-8') as f:
            json.dump(param.result, f)

    # @pytest.mark.key('EQTR-000')
    # @pytest.mark.timeout(120)
    # @reporting
    # def test_apigee_token_status_code(self):
    #     # EQTR-000 - send only the required parameters, expect a 200 status code
    #     token, res = self.token.get_APIGEE_token()
    #     self.assertEqual(status.HTTP_200_OK, res.status_code)
    #     validate(res.json(), schema=successful_schema)

    # @pytest.mark.key("EQTR-000")
    # @pytest.mark.timeout(120)
    # @reporting
    # def test_provision_api_snr_status_code(self):
    #     # EQTR-000 - send only the required parameters, expect a 202 status code
    #     token, res = self.token.get_APIGEE_token()
    #     rand = self.PC_Connectivity.random_alphanumeric_string(15)
    #     payload = self.PC_Connectivity.payload_create_snr(rand)
    #     response = self.PC_Connectivity.create_api_snr(token=token,payload=json.dumps(payload))
    #     self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code)


    # @pytest.mark.key("EQTR-000")
    # @pytest.mark.timeout(120)
    # @reporting
    # def test_create_device_dynamo(self):
    #     # EQTR-000 - send only the required parameters, expect a 200 status code
    #     token, res = self.token.get_APIGEE_token()
    #     rand = self.PC_Connectivity.random_alphanumeric_string(15)
    #     payload = self.PC_Connectivity.payload_create_dynamo(rand)
    #     response = self.PC_Connectivity.create_api_dynamo(token=token, payload=json.dumps(payload))
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     validate(response.json(), schema=create_api_dynamo_schema)

    # @pytest.mark.key("EQTR-000")
    # @pytest.mark.timeout(120)
    # @reporting
    # def test_create_device_neg_dynamo(self):
    #     # EQTR-000 - send only the required parameters, expect a 500 status code
    #     token, res = self.token.get_APIGEE_token()
    #     rand = self.PC_Connectivity.random_alphanumeric_string(15)
    #     payload = self.PC_Connectivity.payload_create_neg_dynamo(rand)
    #     response = self.PC_Connectivity.create_api_dynamo(token=token, payload=json.dumps(payload))
    #     self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
    


    # @pytest.mark.key("EQTR-000")
    # @pytest.mark.timeout(120)
    # @reporting
    # def test_get_device_provision(self):
    #     # EQTR-000 - send only the required parameters, expect a 200 status code
    #     token, res = self.token.get_APIGEE_token()
    #     payload = self.PC_Connectivity.payload_get_device()
    #     response = self.PC_Connectivity.get_device_provision(token=token, payload=json.dumps(payload))
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     validate(response.json(), schema=get_api_device_provision_schema)


    
    @pytest.mark.skipif(priorities["5d548ee3-b488-4cbb-8820-dc5ad3bb7c8d"], reason="required")
    @pytest.mark.key('ECOTEST-2728')
    @pytest.mark.timeout(120)
    @reporting
    def test_client_credential_pie(self):
        # ECOTEST-2728 - send only the required parameters, expect a 200 status code
        token, res = self.token.get_ems_token()
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        validate(res.json(), schema=create_order_successful_schema)

    @pytest.mark.skipif(priorities["ca591a7a-7c09-4aad-be08-fcefc12e620b"], reason="required")
    @pytest.mark.key('ECOTEST-2728')
    @pytest.mark.timeout(120)
    @reporting
    def test_client_credential_with_invalid_username(self):
        # ECOTEST-2728 - send only the required parameters, expect a 401 status code
        res = self.token.get_neg_pie_token()
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, res.status_code)
        validate(res.json(), schema=create_order_with_invalid_username)

    # @pytest.mark.key("ECOTEST-2728")
    # @pytest.mark.timeout(120)
    # @reporting
    # def test_post_keyboard_accessory(self):
    #     # ECOTEST-2728 - send only the required parameters, expect a 201 status code
    #     rand = self.PC_Connectivity.random_alphanumeric_string(15)
    #     payload = self.PC_Connectivity.payload_post_keyboard_accessory(rand)
    #     response = self.PC_Connectivity.create_post_accessory(payload=json.dumps(payload))
    #     self.assertEqual(status.HTTP_201_CREATED, response.status_code)
    #     validate(response.json(), schema=create_post_keyboard_schema)

    # @pytest.mark.key("ECOTEST-2728")
    # @pytest.mark.timeout(120)
    # @reporting
    # def test_post_keyboard_neg_invalid_type_accessory(self):
    #     # ECOTEST-2728 - send only the required parameters, expect a 400 status code
    #     payload = self.PC_Connectivity.payload_post_neg_keyboard_accessory()
    #     response = self.PC_Connectivity.create_post_neg_accessory(payload=json.dumps(payload),
    #                                                               username=cred_reference.serviceClient_universal_username,
    #                                                               password=cred_reference.serviceClient_universal_password)
    #     self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
    #     validate(response.json(), schema=create_post_neg_keyboard_schema)

    # @pytest.mark.key("ECOTEST-2728")
    # @pytest.mark.timeout(120)
    # @reporting
    # def test_post_keyboard_neg_invalid_connectiontype_accessory(self):
    #     # ECOTEST-2728 - send only the required parameters, expect a 201 status code
    #     payload = self.PC_Connectivity.payload_post_neg_keyboard_connectiontype_accessory()
    #     response = self.PC_Connectivity.create_post_neg_accessory(payload=json.dumps(payload),
    #                                                               username=cred_reference.serviceClient_universal_username,
    #                                                               password=cred_reference.serviceClient_universal_password)
    #     self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
    #     validate(response.json(), schema=create_post_neg_connectiontype_keyboard_schema)

    # @pytest.mark.key("ECOTEST-2728")
    # @pytest.mark.timeout(120)
    # @reporting
    # def test_post_mouse_accessory(self):
    #     # ECOTEST-2728 - send only the required parameters, expect a 201 status code
    #     rand = self.PC_Connectivity.random_alphanumeric_string(15)
    #     payload = self.PC_Connectivity.payload_post_mouse_accessory(rand)
    #     response = self.PC_Connectivity.create_post_accessory(payload=json.dumps(payload))
    #     self.assertEqual(status.HTTP_201_CREATED, response.status_code)
    #     validate(response.json(), schema=create_post_mouse_schema)

    # @pytest.mark.key("ECOTEST-2728")
    # @pytest.mark.timeout(120)
    # @reporting
    # def test_mouse_post_neg_mouse_invalid_type_accessory(self):
    #     # ECOTEST-2728 - send only the required parameters, expect a 400 status code
    #     payload = self.PC_Connectivity.payload_post_mouse_neg_invalid_type_accessory()
    #     response = self.PC_Connectivity.create_post_accessory(payload=json.dumps(payload),
    #                                                           username=cred_reference.serviceClient_universal_username,
    #                                                           password=cred_reference.serviceClient_universal_password)
    #     self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
    #     validate(response.json(), schema=create_post_mouse_invalid_type_schema)

    # @pytest.mark.key("ECOTEST-2728")
    # @pytest.mark.timeout(120)
    # @reporting
    # def test_mouse_post_neg_mouse_invalid_connectiontype_accessory(self):
    #     # ECOTEST-2728 - send only the required parameters, expect a 400 status code
    #     payload = self.PC_Connectivity.payload_post_mouse_neg_invalid_connectiontype_accessory()
    #     response = self.PC_Connectivity.create_post_accessory(payload=json.dumps(payload),
    #                                                           username=cred_reference.serviceClient_universal_username,
    #                                                           password=cred_reference.serviceClient_universal_password)
    #     self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
    #     validate(response.json(), schema=create_post_mouse_invalid_connectiontype_schema)

    # @pytest.mark.key("ECOTEST-2728")
    # @pytest.mark.timeout(120)
    # @reporting
    # def test_post_pen_accessory(self):
    #     # ECOTEST-2728 - send only the required parameters, expect a 201 status code
    #     rand = self.PC_Connectivity.random_alphanumeric_string(15)
    #     payload = self.PC_Connectivity.payload_post_pen_accessory(rand)
    #     response = self.PC_Connectivity.create_post_accessory(payload=json.dumps(payload))
    #     self.assertEqual(status.HTTP_201_CREATED, response.status_code)
    #     validate(response.json(), schema=create_post_pen_schema)

    # @pytest.mark.key("ECOTEST-2728")
    # @pytest.mark.timeout(120)
    # @reporting
    # def test_post_pen_neg_invalid_connectiontype_accessory(self):
    #     # ECOTEST-2728 - send only the required parameters, expect a 400 status code
    #     payload = self.PC_Connectivity.payload_post_pen_neg_accessory()
    #     response = self.PC_Connectivity.create_post_accessory(payload=json.dumps(payload))
    #     self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
    #     validate(response.json(), schema=create_post_neg_pen_schema)

    # @pytest.mark.key("ECOTEST-2728")
    # @pytest.mark.timeout(120)
    # @reporting
    # def test_get_accessory(self):
    #     # ECOTEST-2728 - send only the required parameters, expect a 200 status code
    #     response = self.PC_Connectivity.test_get_accessory(accessory_id=self.accessory_id,
    #                                                        username=cred_reference.serviceClient_universal_username,
    #                                                        password=cred_reference.serviceClient_universal_password)
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     validate(response.json(), schema=get_accessory)

    # @pytest.mark.key("ECOTEST-2728")
    # @pytest.mark.timeout(120)
    # @reporting
    # def test_get_neg_accessory(self):
    #     # ECOTEST-2728 - send only the required parameters, expect a 400 status code
    #     response = self.PC_Connectivity.test_get_neg_accessory(accessory_id1=self.accessory_id1,
    #                                                            username=cred_reference.serviceClient_universal_username,
    #                                                            password=cred_reference.serviceClient_universal_password)
    #     self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
    #     validate(response.json(), schema=get_neg_accessory)

    # @pytest.mark.key("ECOTEST-2728")
    # @pytest.mark.timeout(120)
    # @reporting
    # def test_get_list_accessory(self):
    #     # ECOTEST-2728 - send only the required parameters, expect a 200 status code
    #     param = self.PC_Connectivity.param_get_pen_accessory()
    #     response = self.PC_Connectivity.test_get_list_accessory(param=param,
    #                                                             username=cred_reference.serviceClient_universal_username,
    #                                                             password=cred_reference.serviceClient_universal_password)
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     validate(response.json(), schema=get_list_accessory)

    # @pytest.mark.key("ECOTEST-2728")
    # @pytest.mark.timeout(120)
    # @reporting
    # def test_get_list_neg_accessory(self):
    #     # ECOTEST-2728 - send only the required parameters, expect a 404 status code
    #     param = self.PC_Connectivity.param_get_neg_list_pen_accessory()
    #     response = self.PC_Connectivity.test_get_list_accessory(param=param,
    #                                                             username=cred_reference.serviceClient_universal_username,
    #                                                             password=cred_reference.serviceClient_universal_password)
    #     self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
    #     validate(response.json(), schema=test_get_list_neg_accessory)

    # @pytest.mark.key("ECOTEST-2728")
    # @pytest.mark.timeout(120)
    # @reporting
    # def test_get_list_neg_invalidsort_accessory(self):
    #     # ECOTEST-2728 - send only the required parameters, expect a 400 status code
    #     param = self.PC_Connectivity.test_get_list_neg_invalidsort_accessory()
    #     response = self.PC_Connectivity.test_get_list_accessory(param=param,
    #                                                             username=cred_reference.serviceClient_universal_username,
    #                                                             password=cred_reference.serviceClient_universal_password)
    #     self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
    #     validate(response.json(), schema=test_get_list_invalidsort_accessory)

    # @pytest.mark.key("ECOTEST-2728")
    # @pytest.mark.timeout(120)
    # @reporting
    # def test_post_ownerships(self):
    #     # ECOTEST-2728 - send only the required parameters, expect a 201 status code
    #     payload = self.PC_Connectivity.payload_post_ownerships()
    #     response = self.PC_Connectivity.create_post_ownership(payload=json.dumps(payload))
    #     self.assertEqual(status.HTTP_201_CREATED, response.status_code)
    #     validate(response.json(), schema=create_post_ownership)

    # @pytest.mark.key("ECOTEST-2728")
    # @pytest.mark.timeout(120)
    # @reporting
    # def test_post_neg_invalidtenant_ownerships(self):
    #     # ECOTEST-2728 - send only the required parameters, expect a 400 status code
    #     payload = self.PC_Connectivity.payload_post_neg_invalidtenant_ownerships()
    #     response = self.PC_Connectivity.create_post_ownership(payload=json.dumps(payload))
    #     self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
    #     validate(response.json(), schema=create_post_neg_serial_ownership)

    # @pytest.mark.key("ECOTEST-2728")
    # @pytest.mark.timeout(120)
    # @reporting
    # def test_post_neg_invalidserial_ownerships(self):
    #     # ECOTEST-2728 - send only the required parameters, expect a 404 status code
    #     payload = self.PC_Connectivity.payload_post_neg_invalidserial_ownerships()
    #     response = self.PC_Connectivity.create_post_ownership(payload=json.dumps(payload))
    #     self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
    #     validate(response.json(), schema=create_post_neg_ownership)

    # @pytest.mark.key("ECOTEST-3140")
    # @pytest.mark.timeout(120)
    # @reporting
    # def test_get_devcache_secapi(self):
    #     # ECOTEST-2728 - send only the required parameters, expect a 200 status code
    #     response = self.PC_Connectivity.test_get_devcache_secapi(accessory_id=self.accessory_id,
    #                                                              username=cred_reference.serviceClient_universal_username,
    #                                                              password=cred_reference.serviceClient_universal_password)
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     validate(response.json(), schema=get_devcache_secapi)

    @pytest.mark.skipif(priorities["cdd302d6-3e26-434b-9278-049eda9a1cc7"], reason="required")
    @pytest.mark.key("ECOTEST-3140")
    @pytest.mark.timeout(120)
    @reporting
    def test_get_devcache_neg_secapi(self):
        # ECOTEST-2728 - send only the required parameters, expect a 404 status code
        response = self.PC_Connectivity.test_get_devcache_neg_secapi(accessory_id1=self.accessory_id1,
                                                                     username=cred_reference.serviceClient_universal_username,
                                                                     password=cred_reference.serviceClient_universal_password)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    # @pytest.mark.key("ECOTEST-2728")
    # @pytest.mark.timeout(120)
    # @reporting
    # def test_get_devcache_fapi(self):
    #     # ECOTEST-2728 - send only the required parameters, expect a 200 status code
    #     param = self.PC_Connectivity.param_get_devcache_fapi()
    #     response = self.PC_Connectivity.test_get_devcache_fapi(param=param)
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     # print(response.content)
    #     # validate(response.json(), schema=test_get_devcache_fapi)
    #
    # @pytest.mark.key("ECOTEST-2728")
    # @pytest.mark.timeout(120)
    # @reporting
    # def test_get_devcache_neg_fapi(self):
    #     # ECOTEST-2728 - send only the required parameters, expect a 200 status code
    #     param = self.PC_Connectivity.param_get_devcache_neg_fapi()
    #     response = self.PC_Connectivity.test_get_devcache_fapi(param=param)
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)

    @pytest.mark.skipif(priorities["02e88c40-a08f-4dd6-8f9a-37b37088d1b3"], reason="required")
    @pytest.mark.key("ECOTEST-00")
    @pytest.mark.timeout(120)
    @reporting
    def test_post_create_association(self):
        # ECOTEST-3140 - send only the required parameters, expect a 201 status code
        payload = self.PC_Connectivity.payload_post_create_association()
        response = self.PC_Connectivity.create_association(payload=json.dumps(payload),
                                                           username=cred_reference.serviceClient_universal_username,
                                                           password=cred_reference.serviceClient_universal_password)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        validate(response.json(), schema=create_post_association_schema)

    @pytest.mark.skipif(priorities["0c07b160-cb88-4607-af56-71c2e05edea9"], reason="required")
    @pytest.mark.key("ECOTEST-00")
    @pytest.mark.timeout(120)
    @reporting
    def test_post_create_neg_invaliduser_association(self):
        # ECOTEST-3140 - send only the required parameters, expect a 400 status code
        payload = self.PC_Connectivity.payload_post_create_neg_invaliduser_association()
        response = self.PC_Connectivity.create_association(payload=json.dumps(payload),
                                                           username=cred_reference.serviceClient_universal_username,
                                                           password=cred_reference.serviceClient_universal_password)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        validate(response.json(), schema=create_post_neg_association_schema)

    # @pytest.mark.skipif(priorities["4fda6df5-dff2-4516-b1a9-ed0bb2cdca72"], reason="required")
    # @pytest.mark.key("ECOTEST-00")
    # @pytest.mark.timeout(120)
    # @reporting
    # def test_post_create_neg_invalidtype_association(self):
    #     # ECOTEST-3140 - send only the required parameters, expect a 400 status code
    #     payload = self.PC_Connectivity.payload_post_create_neg_invalidtype_association()
    #     response = self.PC_Connectivity.create_association(payload=json.dumps(payload),
    #                                                        username=cred_reference.serviceClient_universal_username,
    #                                                        password=cred_reference.serviceClient_universal_password)
    #     self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
    #     validate(response.json(), schema=create_post_neg_associationtype_schema)

    # @pytest.mark.key("ECOTEST-00")
    # @pytest.mark.timeout(120)
    # @reporting
    # def test_get_devcache_internal_device_deviceid(self):
    #     # ECOTEST-3140 - send only the required parameters, expect a 200 status code
    #     response = self.PC_Connectivity.test_get_devcache_internal_device(device_id=self.device_id,
    #                                                                       username=cred_reference.serviceClient_universal_username,
    #                                                                       password=cred_reference.serviceClient_universal_password)
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     validate(response.json(), schema=test_get_devcache_internal_device_schema)

    @pytest.mark.skipif(priorities["53727e4e-fac5-42d5-9d9b-39a5eff50bc5"], reason="required")
    @pytest.mark.key("ECOTEST-00")
    @pytest.mark.timeout(120)
    @reporting
    def test_get_devcache_neg_internal_device_deviceid(self):
        # ECOTEST-3140 - send only the required parameters, expect a 200 status code
        response = self.PC_Connectivity.test_get_devcache_neg_internal_device(device_id1=self.device_id1,
                                                                              username=cred_reference.serviceClient_universal_username,
                                                                              password=cred_reference.serviceClient_universal_password)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    # @pytest.mark.key("ECOTEST-00")
    # @pytest.mark.timeout(120)
    # @reporting
    # def test_get_devcache_internal_device_sno(self):
    #     # ECOTEST-3140 - send only the required parameters, expect a 200 status code
    #     response = self.PC_Connectivity.test_get_devcache_internal_device_sno(s_no=self.s_no,
    #                                                                           username=cred_reference.serviceClient_universal_username,
    #                                                                           password=cred_reference.serviceClient_universal_password)
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     #print(response.content)
    #     validate(response.json(), schema=test_get_devcache_internal_device_schema)

    @pytest.mark.skipif(priorities["b5afebfb-cbf6-4aa8-ab59-fb60d1610718"], reason="required")
    @pytest.mark.key("ECOTEST-00")
    @pytest.mark.timeout(120)
    @reporting
    def test_get_devcache_neg_internal_device_sno(self):
        # ECOTEST-3140 - send only the required parameters, expect a 200 status code
        response = self.PC_Connectivity.test_get_devcache_neg_internal_device_sno(s_no1=self.s_no1,
                                                                                  username=cred_reference.serviceClient_universal_username,
                                                                                  password=cred_reference.serviceClient_universal_password)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    # @pytest.mark.key("ECOTEST-3449")
    # @pytest.mark.timeout(200)
    # @reporting
    # def test_running_1eclient_diagnostic_commands_in_device_1019(self):
    #     """ECOTEST-3449 - Run Successful Diagnostics command execution of remote Agent Query on 1E client Device"""
    #     token, res = self.token.get_OneUID_token()
    #     print(f"Generated token: {token}")
    #     correlation_id = f"8c51192d-b00e-eb11-a813-tests-{self.PC_Connectivity.random_alphanumeric_string(7)}"
    #     print(f"Asset details correlation_id: {correlation_id}")
    #
    #     # Fetching diagnostic commends from device
    #     post_assets_details_payload = self.PC_Connectivity.payload_post_assets_details(correlation_id=correlation_id)
    #     post_assets_details_response = self.PC_Connectivity.test_post_assets_details(
    #         token=token,
    #         payload=json.dumps(post_assets_details_payload))
    #     self.assertEqual(status.HTTP_202_ACCEPTED, post_assets_details_response.status_code)
    #
    #     # DB Connection to find diagnostic commands from DB Response of Asset details
    #     db_response = db_connect.execute_query(correlation_id=correlation_id)
    #     commands_list, fetching_commands_status = db_connect.filtering_diagnostic_commands(commands_data=db_response)
    #     self.assertEqual(True, fetching_commands_status)
    #
    #     # Run diagnostic commands execution in device
    #     print("commands_list: ", commands_list)
    #     print("Count of fetching commands list from Device: ", len(commands_list))
    #     start = time.time()
    #     instructions_response = self.PC_Connectivity.running_diagnostic_commands_01(token=token)
    #     self.assertEqual(status.HTTP_202_ACCEPTED, instructions_response)
    #     end = time.time()
    #     print("Time consuming to Run Diagnostic commands in Seconds: ", divmod(end - start, 60)[0])

    # @pytest.mark.key("ECOTEST-3449")
    # @pytest.mark.timeout(200)
    # @reporting
    # def test_running_1eclient_diagnostic_commands_in_device_1020(self):
    #     """ECOTEST-3449 - Run Successful Diagnostics command execution of remote Agent Query on 1E client Device"""
    #     token, res = self.token.get_OneUID_token()
    #     print(f"Generated token: {token}")
    #     correlation_id = f"8c51192d-b00e-eb11-a813-tests-{self.PC_Connectivity.random_alphanumeric_string(7)}"
    #     print(f"Asset details correlation_id: {correlation_id}")
    #
    #     # Fetching diagnostic commends from device
    #     post_assets_details_payload = self.PC_Connectivity.payload_post_assets_details(correlation_id=correlation_id)
    #     post_assets_details_response = self.PC_Connectivity.test_post_assets_details(
    #         token=token,
    #         payload=json.dumps(post_assets_details_payload))
    #     self.assertEqual(status.HTTP_202_ACCEPTED, post_assets_details_response.status_code)
    #
    #     # DB Connection to find diagnostic commands from DB Response of Asset details
    #     db_response = db_connect.execute_query(correlation_id=correlation_id)
    #     commands_list, fetching_commands_status = db_connect.filtering_diagnostic_commands(commands_data=db_response)
    #     self.assertEqual(True, fetching_commands_status)
    #
    #     # Run diagnostic commands execution in device
    #     print("commands_list: ", commands_list)
    #     print("Count of fetching commands list from Device: ", len(commands_list))
    #     start = time.time()
    #     instructions_response = self.PC_Connectivity.running_diagnostic_commands_02(
    #         token=token
    #     )
    #     self.assertEqual(status.HTTP_202_ACCEPTED, instructions_response)
    #     end = time.time()
    #     print("Time consuming to Run Diagnostic commands in Seconds: ", divmod(end - start, 60)[0])

    # @pytest.mark.key("ECOTEST-3449")
    # @pytest.mark.timeout(200)
    # @reporting
    # def test_running_1eclient_diagnostic_commands_in_device_1024(self):
    #     """ECOTEST-3449 - Run Successful Diagnostics command execution of remote Agent Query on 1E client Device"""
    #     token, res = self.token.get_OneUID_token()
    #     print(f"Generated token: {token}")
    #     correlation_id = f"8c51192d-b00e-eb11-a813-tests-{self.PC_Connectivity.random_alphanumeric_string(7)}"
    #     print(f"Asset details correlation_id: {correlation_id}")
    #
    #     # Fetching diagnostic commends from device
    #     post_assets_details_payload = self.PC_Connectivity.payload_post_assets_details(correlation_id=correlation_id)
    #     post_assets_details_response = self.PC_Connectivity.test_post_assets_details(
    #         token=token,
    #         payload=json.dumps(post_assets_details_payload))
    #     self.assertEqual(status.HTTP_202_ACCEPTED, post_assets_details_response.status_code)
    #
    #     # DB Connection to find diagnostic commands from DB Response of Asset details
    #     db_response = db_connect.execute_query(correlation_id=correlation_id)
    #     commands_list, fetching_commands_status = db_connect.filtering_diagnostic_commands(commands_data=db_response)
    #     self.assertEqual(True, fetching_commands_status)
    #
    #     # Run diagnostic commands execution in device
    #     print("commands_list: ", commands_list)
    #     print("Count of fetching commands list from Device: ", len(commands_list))
    #     start = time.time()
    #     instructions_response = self.PC_Connectivity.running_diagnostic_commands_03(
    #         token=token
    #     )
    #     self.assertEqual(status.HTTP_202_ACCEPTED, instructions_response)
    #     end = time.time()
    #     print("Time consuming to Run Diagnostic commands in Seconds: ", divmod(end - start, 60)[0])

    # @pytest.mark.key("ECOTEST-3449")
    # @pytest.mark.timeout(200)
    # @reporting
    # def test_running_1eclient_diagnostic_commands_in_device_1025(self):
    #     """ECOTEST-3449 - Run Successful Diagnostics command execution of remote Agent Query on 1E client Device"""
    #     token, res = self.token.get_OneUID_token()
    #     print(f"Generated token: {token}")
    #     correlation_id = f"8c51192d-b00e-eb11-a813-tests-{self.PC_Connectivity.random_alphanumeric_string(7)}"
    #     print(f"Asset details correlation_id: {correlation_id}")
    #
    #     # Fetching diagnostic commends from device
    #     post_assets_details_payload = self.PC_Connectivity.payload_post_assets_details(correlation_id=correlation_id)
    #     post_assets_details_response = self.PC_Connectivity.test_post_assets_details(
    #         token=token,
    #         payload=json.dumps(post_assets_details_payload))
    #     self.assertEqual(status.HTTP_202_ACCEPTED, post_assets_details_response.status_code)
    #
    #     # DB Connection to find diagnostic commands from DB Response of Asset details
    #     db_response = db_connect.execute_query(correlation_id=correlation_id)
    #     commands_list, fetching_commands_status = db_connect.filtering_diagnostic_commands(commands_data=db_response)
    #     self.assertEqual(True, fetching_commands_status)
    #
    #     # Run diagnostic commands execution in device
    #     print("commands_list: ", commands_list)
    #     print("Count of fetching commands list from Device: ", len(commands_list))
    #     start = time.time()
    #     instructions_response = self.PC_Connectivity.running_diagnostic_commands_04(
    #         token=token
    #     )
    #     self.assertEqual(status.HTTP_202_ACCEPTED, instructions_response)
    #     end = time.time()
    #     print("Time consuming to Run Diagnostic commands in Seconds: ", divmod(end - start, 60)[0])

    # @pytest.mark.key("ECOTEST-3449")
    # @pytest.mark.timeout(200)
    # @reporting
    # def test_running_1eclient_diagnostic_commands_in_device_1026(self):
    #     """ECOTEST-3449 - Run Successful Diagnostics command execution of remote Agent Query on 1E client Device"""
    #     token, res = self.token.get_OneUID_token()
    #     print(f"Generated token: {token}")
    #     correlation_id = f"8c51192d-b00e-eb11-a813-tests-{self.PC_Connectivity.random_alphanumeric_string(7)}"
    #     print(f"Asset details correlation_id: {correlation_id}")
    #
    #     # Fetching diagnostic commends from device
    #     post_assets_details_payload = self.PC_Connectivity.payload_post_assets_details(correlation_id=correlation_id)
    #     post_assets_details_response = self.PC_Connectivity.test_post_assets_details(
    #         token=token,
    #         payload=json.dumps(post_assets_details_payload))
    #     self.assertEqual(status.HTTP_202_ACCEPTED, post_assets_details_response.status_code)
    #
    #     # DB Connection to find diagnostic commands from DB Response of Asset details
    #     db_response = db_connect.execute_query(correlation_id=correlation_id)
    #     commands_list, fetching_commands_status = db_connect.filtering_diagnostic_commands(commands_data=db_response)
    #     self.assertEqual(True, fetching_commands_status)
    #
    #     # Run diagnostic commands execution in device
    #     print("commands_list: ", commands_list)
    #     print("Count of fetching commands list from Device: ", len(commands_list))
    #     start = time.time()
    #     instructions_response = self.PC_Connectivity.running_diagnostic_commands_05(
    #         token=token
    #     )
    #     self.assertEqual(status.HTTP_202_ACCEPTED, instructions_response)
    #     end = time.time()
    #     print("Time consuming to Run Diagnostic commands in Seconds: ", divmod(end - start, 60)[0])

    # @pytest.mark.key("ECOTEST-3449")
    # @pytest.mark.timeout(200)
    # @reporting
    # def test_running_1eclient_diagnostic_commands_in_device_1027(self):
    #     """ECOTEST-3449 - Run Successful Diagnostics command execution of remote Agent Query on 1E client Device"""
    #     token, res = self.token.get_OneUID_token()
    #     print(f"Generated token: {token}")
    #     correlation_id = f"8c51192d-b00e-eb11-a813-tests-{self.PC_Connectivity.random_alphanumeric_string(7)}"
    #     print(f"Asset details correlation_id: {correlation_id}")
    #
    #     # Fetching diagnostic commends from device
    #     post_assets_details_payload = self.PC_Connectivity.payload_post_assets_details(correlation_id=correlation_id)
    #     post_assets_details_response = self.PC_Connectivity.test_post_assets_details(
    #         token=token,
    #         payload=json.dumps(post_assets_details_payload))
    #     self.assertEqual(status.HTTP_202_ACCEPTED, post_assets_details_response.status_code)
    #
    #     # DB Connection to find diagnostic commands from DB Response of Asset details
    #     db_response = db_connect.execute_query(correlation_id=correlation_id)
    #     commands_list, fetching_commands_status = db_connect.filtering_diagnostic_commands(commands_data=db_response)
    #     self.assertEqual(True, fetching_commands_status)
    #
    #     # Run diagnostic commands execution in device
    #     print("commands_list: ", commands_list)
    #     print("Count of fetching commands list from Device: ", len(commands_list))
    #     start = time.time()
    #     instructions_response = self.PC_Connectivity.running_diagnostic_commands_06(
    #         token=token
    #     )
    #     self.assertEqual(status.HTTP_202_ACCEPTED, instructions_response)
    #     end = time.time()
    #     print("Time consuming to Run Diagnostic commands in Seconds: ", divmod(end - start, 60)[0])

    # @pytest.mark.key("ECOTEST-3449")
    # @pytest.mark.timeout(200)
    # @reporting
    # def test_running_1eclient_diagnostic_commands_in_device_1028(self):
    #     """ECOTEST-3449 - Run Successful Diagnostics command execution of remote Agent Query on 1E client Device"""
    #     token, res = self.token.get_OneUID_token()
    #     print(f"Generated token: {token}")
    #     correlation_id = f"8c51192d-b00e-eb11-a813-tests-{self.PC_Connectivity.random_alphanumeric_string(7)}"
    #     print(f"Asset details correlation_id: {correlation_id}")
    #
    #     # Fetching diagnostic commends from device
    #     post_assets_details_payload = self.PC_Connectivity.payload_post_assets_details(correlation_id=correlation_id)
    #     post_assets_details_response = self.PC_Connectivity.test_post_assets_details(
    #         token=token,
    #         payload=json.dumps(post_assets_details_payload))
    #     self.assertEqual(status.HTTP_202_ACCEPTED, post_assets_details_response.status_code)
    #
    #     # DB Connection to find diagnostic commands from DB Response of Asset details
    #     db_response = db_connect.execute_query(correlation_id=correlation_id)
    #     commands_list, fetching_commands_status = db_connect.filtering_diagnostic_commands(commands_data=db_response)
    #     self.assertEqual(True, fetching_commands_status)
    #
    #     # Run diagnostic commands execution in device
    #     print("commands_list: ", commands_list)
    #     print("Count of fetching commands list from Device: ", len(commands_list))
    #     start = time.time()
    #     instructions_response = self.PC_Connectivity.running_diagnostic_commands_07(
    #         token=token
    #     )
    #     self.assertEqual(status.HTTP_202_ACCEPTED, instructions_response)
    #     end = time.time()
    #     print("Time consuming to Run Diagnostic commands in Seconds: ", divmod(end - start, 60)[0])


    # @pytest.mark.key("ECOTEST-3449")
    # @pytest.mark.timeout(200)
    # @reporting
    # def test_running_1eclient_diagnostic_commands_in_device_1029(self):
    #     """ECOTEST-3449 - Run Successful Diagnostics command execution of remote Agent Query on 1E client Device"""
    #     token, res = self.token.get_OneUID_token()
    #     print(f"Generated token: {token}")
    #     correlation_id = f"8c51192d-b00e-eb11-a813-tests-{self.PC_Connectivity.random_alphanumeric_string(7)}"
    #     print(f"Asset details correlation_id: {correlation_id}")
    #
    #     # Fetching diagnostic commends from device
    #     post_assets_details_payload = self.PC_Connectivity.payload_post_assets_details(correlation_id=correlation_id)
    #     post_assets_details_response = self.PC_Connectivity.test_post_assets_details(
    #         token=token,
    #         payload=json.dumps(post_assets_details_payload))
    #     self.assertEqual(status.HTTP_202_ACCEPTED, post_assets_details_response.status_code)
    #
    #     # DB Connection to find diagnostic commands from DB Response of Asset details
    #     db_response = db_connect.execute_query(correlation_id=correlation_id)
    #     commands_list, fetching_commands_status = db_connect.filtering_diagnostic_commands(commands_data=db_response)
    #     self.assertEqual(True, fetching_commands_status)
    #
    #     # Run diagnostic commands execution in device
    #     print("commands_list: ", commands_list)
    #     print("Count of fetching commands list from Device: ", len(commands_list))
    #     start = time.time()
    #     instructions_response = self.PC_Connectivity.running_diagnostic_commands_08(
    #         token=token
    #     )
    #     self.assertEqual(status.HTTP_202_ACCEPTED, instructions_response)
    #     end = time.time()
    #     print("Time consuming to Run Diagnostic commands in Seconds: ", divmod(end - start, 60)[0])

    # @pytest.mark.key("ECOTEST-3449")
    # @pytest.mark.timeout(200)
    # @reporting
    # def test_running_1eclient_diagnostic_commands_in_device_1030(self):
    #     """ECOTEST-3449 - Run Successful Diagnostics command execution of remote Agent Query on 1E client Device"""
    #     token, res = self.token.get_OneUID_token()
    #     print(f"Generated token: {token}")
    #     correlation_id = f"8c51192d-b00e-eb11-a813-tests-{self.PC_Connectivity.random_alphanumeric_string(7)}"
    #     print(f"Asset details correlation_id: {correlation_id}")
    #
    #     # Fetching diagnostic commends from device
    #     post_assets_details_payload = self.PC_Connectivity.payload_post_assets_details(correlation_id=correlation_id)
    #     post_assets_details_response = self.PC_Connectivity.test_post_assets_details(
    #         token=token,
    #         payload=json.dumps(post_assets_details_payload))
    #     self.assertEqual(status.HTTP_202_ACCEPTED, post_assets_details_response.status_code)
    #
    #     # DB Connection to find diagnostic commands from DB Response of Asset details
    #     db_response = db_connect.execute_query(correlation_id=correlation_id)
    #     commands_list, fetching_commands_status = db_connect.filtering_diagnostic_commands(commands_data=db_response)
    #     self.assertEqual(True, fetching_commands_status)
    #
    #     # Run diagnostic commands execution in device
    #     print("commands_list: ", commands_list)
    #     print("Count of fetching commands list from Device: ", len(commands_list))
    #     start = time.time()
    #     instructions_response = self.PC_Connectivity.running_diagnostic_commands_09(
    #         token=token
    #     )
    #     self.assertEqual(status.HTTP_202_ACCEPTED, instructions_response)
    #     end = time.time()
    #     print("Time consuming to Run Diagnostic commands in Seconds: ", divmod(end - start, 60)[0])

    # @pytest.mark.key("ECOTEST-3428")
    # @pytest.mark.timeout(200)
    # @reporting
    # def test_negative_running_1eclient_diagnostic_commands_in_device(self):
    #     """ECOTEST-3428 - Run UnSuccessful Diagnostics command execution of remote Agent Query on 1E client Device"""
    #     token, res = self.token.get_OneUID_token()
    #     print(f"Generated token: {token}")
    #     correlation_id = f"8c51192d-b00e-eb11-a813-cesar-{self.PC_Connectivity.random_alphanumeric_string(7)}"
    #     print(f"Asset details correlation_id: {correlation_id}")
    #
    #     # Fetching diagnostic commends from device
    #     post_assets_details_payload = self.PC_Connectivity.payload_post_assets_details(correlation_id=correlation_id)
    #     post_assets_details_response = self.PC_Connectivity.test_post_assets_details(
    #         token=token,
    #         payload=json.dumps(post_assets_details_payload))
    #     self.assertEqual(status.HTTP_202_ACCEPTED, post_assets_details_response.status_code)
    #
    #     # DB Connection to find diagnostic commands from DB Response of Asset details
    #     db_response = db_connect.execute_query(correlation_id=correlation_id)
    #     commands_list, fetching_commands_status = db_connect.filtering_diagnostic_commands(commands_data=db_response)
    #     self.assertEqual(True, fetching_commands_status)
    #
    #     # Run diagnostic commands execution in device
    #     print("commands_list: ", commands_list)
    #     print("Count of fetching commands list from Device: ", len(commands_list))
    #     start = time.time()
    #     instructions_response = self.PC_Connectivity.running_diagnostic_commands_negative(
    #         token=token
    #     )
    #     self.assertEqual(status.HTTP_202_ACCEPTED, instructions_response)
    #     end = time.time()
    #     print("Time consuming to Run Diagnostic commands in Seconds: ", divmod(end - start, 60)[0])
