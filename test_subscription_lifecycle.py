import pytest
import unittest
import json
import os
import requests
from jsonschema import validate
from pytest_schema import schema
from .param import Param as param
from .user import User
from .apis.subscription_svc import SubscriptionSvc
from .utils.reporting import reporting
from .schemas.subscription_schema import get_subscription_pie_successful_schema , get_subscription_stg_successful_schema
from .utils import status, users, base_urls
from .apis.warranty import Warranty
from .schemas.warranty_schema import create_warranty_successful_schema, delete_warranty_400_schema, \
    delete_warranty_401_unauthorized_schema, delete_warranty_401_expired_token_schema
from .utils import cred_reference


class HPOneSubscriptionLifecycle(unittest.TestCase):
    subscription_svc = SubscriptionSvc(
        user=User(users.USER_ID)
    )

    blld_id = param.bl_id
    subscription_id = param.subscription_id
    wrong_bl_id = param.wrong_bl_id
    wrong_subscription_id = param.wrong_subscription_id

    """Below Warranty payload details are hardcoded(generated using simulator), in future test scripts these will be fetched
    from dependent APIs"""
    if base_urls.environment == "pie":
        warranty = Warranty(
            user=User(users.USER_ID_OB),
            model_number="349U4A",
            serial_number="UMZVR3Y6OM",
            addressId="6396b2115d89d8274a5d4507"
        )
    if base_urls.environment == "stage":
        warranty = Warranty(
            user=User(users.USER_ID_OB),
            model_number="257G3A",
            serial_number="W09NU9C6I0",
            addressId="63eca423e10b652bce19b871"
        )
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
        param.result["directory"] = 'subscription_lifecycle'
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

    @pytest.mark.skipif(priorities["9577ce0b-5fdb-4bfc-8416-260a41f1bfe5"], reason="required")
    @pytest.mark.key("ECOTEST-1336")
    @pytest.mark.timeout(120)
    @reporting
    def test_get_subscription_response_status_code(self):
        # ECOTEST-1336" - send only the required parameters, expect a 200 status code
        response = self.subscription_svc.request_get_subscription_status(blld_id=self.blld_id,
                                                                         subscription_id=self.subscription_id,
                                                                         username=cred_reference.subscription_serviceClient_username,
                                                                         password=cred_reference.subscription_serviceClient_password)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    @pytest.mark.skipif(priorities["bd388e51-9b32-4125-a64c-d6964b428396"], reason="required")
    @pytest.mark.key("ECOTEST-1336")
    @pytest.mark.timeout(120)
    @reporting
    def test_get_subscription_response_schema(self):
        # ECOTEST-1336" - send only the required payload, expect the correct schema
        response = self.subscription_svc.request_get_subscription_status(blld_id=self.blld_id,
                                                                         subscription_id=self.subscription_id,
                                                                         username=cred_reference.subscription_serviceClient_username,
                                                                         password=cred_reference.subscription_serviceClient_password)
        content = json.loads(response.content)
        if base_urls.environment == "pie":
            validate(content, get_subscription_pie_successful_schema)
        elif base_urls.environment == "stage":
            validate(content, get_subscription_stg_successful_schema)

    @pytest.mark.skipif(priorities["df0f9899-f6c8-47c6-9c17-6c36120a260d"], reason="required")
    @pytest.mark.key("ECOTEST-1336")
    @pytest.mark.timeout(120)
    @reporting
    def test_get_subscription_wrong_bl_id(self):
        # ECOTEST-1336" - send false required parameters, expect a 404 status code
        response = self.subscription_svc.request_get_subscription_status(blld_id=self.wrong_bl_id,
                                                                         subscription_id=self.wrong_subscription_id,
                                                                         username=cred_reference.subscription_serviceClient_username,
                                                                         password=cred_reference.subscription_serviceClient_password)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    @pytest.mark.skipif(priorities["5d05a118-16b4-488f-a3e5-d5c80f55ae80"], reason="required")
    @pytest.mark.key("ECOTEST-1336")
    @pytest.mark.timeout(120)
    @reporting
    def test_get_subscriptions_latency(self):
        # ECOTEST-1336 - sending a request to GET subscriptions, expect the response time below or equal 1 second
        response = self.subscription_svc.request_get_subscription_status(blld_id=self.blld_id,
                                                                         subscription_id=self.subscription_id,
                                                                         username=cred_reference.subscription_serviceClient_username,
                                                                         password=cred_reference.subscription_serviceClient_password)
        response_time = response.elapsed.microseconds / 1000  # convert to milliseconds
        assert response_time <= 1000, "The response time is bigger than 1 second."

    @pytest.mark.skipif(priorities["8fa23728-9f35-49ed-9ef3-55730959ab73"], reason="required")
    @pytest.mark.key("ECOTEST-1336")
    @pytest.mark.timeout(120)
    @reporting
    def test_get_subscription_no_auth_status_code(self):
        # ECOTEST-1336" - send only the required parameters, expect a 200 status code
        response = self.subscription_svc.request_get_subscription_status(blld_id=self.blld_id,
                                                                         subscription_id=self.subscription_id,
                                                                         token='',
                                                                         username=cred_reference.subscription_serviceClient_username,
                                                                         password=cred_reference.subscription_serviceClient_password)
        if base_urls.environment == "pie":
            self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        elif base_urls.environment == "stage":
            self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    @pytest.mark.skipif(priorities["e583c482-afd3-4ccf-b20a-61853f71c388"], reason="required")
    @pytest.mark.key("ECOTEST-1342")
    @pytest.mark.timeout(120)
    @reporting
    def test_create_warranty_payload_status_code(self):
        # Passing correct payload to create warranty and check response status code
        payload = self.warranty.payload_create_warranty()
        response = self.warranty.request_create_warranty(payload=json.dumps(payload))
        self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code)

    @pytest.mark.skipif(priorities["cb76f87a-cee1-4402-8a78-9dc674929272"], reason="required")
    @pytest.mark.key("ECOTEST-1342")
    @pytest.mark.timeout(120)
    @reporting
    def test_delete_warranty_payload_status_code(self):
        # Passing correct payload to delete warranty and check response status code
        payload = self.warranty.payload_delete_warranty()
        response = self.warranty.request_delete_warranty(payload=json.dumps(payload))
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    @pytest.mark.skipif(priorities["ca058442-af97-4b46-9378-575654717441"], reason="required")
    @pytest.mark.key("ECOTEST-1342")
    @pytest.mark.timeout(120)
    @reporting
    def test_create_warranty_payload_schema(self):
        # Passing correct payload to create warranty and check response schema
        payload = self.warranty.payload_create_warranty()
        response = self.warranty.request_create_warranty(payload=json.dumps(payload))
        content = json.loads(response.content)
        validate(content, create_warranty_successful_schema)

    @pytest.mark.skipif(priorities["26aa5d8a-ef52-4d26-8ff4-985a0d348ba7"], reason="required")
    @pytest.mark.key("ECOTEST-1342")
    @pytest.mark.timeout(120)
    @reporting
    def test_delete_warranty_negative_payload_schema(self):
        # Passing payload with invalid TenantResourceID
        payload = self.warranty.negative_payload_delete_warranty()
        response = self.warranty.request_delete_warranty(payload=json.dumps(payload))
        content = json.loads(response.content)
        validate(content, delete_warranty_400_schema)

    @pytest.mark.skipif(priorities["08272d55-89d4-4366-9326-da603952d730"], reason="required")
    @pytest.mark.key("ECOTEST-1342")
    @pytest.mark.timeout(120)
    @reporting
    def test_delete_warranty_payload_no_auth_schema(self):
        # Passing invalid payload with No Auth
        payload = self.warranty.payload_delete_warranty()
        response = self.warranty.request_delete_warranty(payload=json.dumps(payload), token="")
        content = json.loads(response.content)
        validate(content, delete_warranty_401_unauthorized_schema)

    @pytest.mark.skipif(priorities["c848f042-5142-4e25-83a7-4f155654857e"], reason="required")
    @pytest.mark.key("ECOTEST-1342")
    @pytest.mark.timeout(120)
    @reporting
    def test_delete_warranty_payload_expired_token_schema(self):
        # Passing invalid payload with Expired token
        payload = self.warranty.payload_delete_warranty()
        response = self.warranty.request_delete_warranty(payload=json.dumps(payload), token=Warranty.expired_token)
        content = json.loads(response.content)
        validate(content, delete_warranty_401_unauthorized_schema)

    @pytest.mark.skipif(priorities["5da728dc-1670-448a-8074-ea0565a41bec"], reason="required")
    @pytest.mark.key("ECOTEST-1342")
    @pytest.mark.timeout(120)
    @reporting
    def test_delete_warranty_internalserver_error_status_code(self):
        # Passing correct payload to delete warranty and check response status code for internal server error
        payload = self.warranty.payload_delete_warranty()
        response = self.warranty.delete_warranty_internalserver_error(payload=json.dumps(payload))
        if base_urls.environment == "pie":
            self.assertEqual(status.HTTP_500_INTERNAL_SERVER_ERROR, response.status_code)
        elif base_urls.environment == "stage":
            self.assertEqual(status.HTTP_500_INTERNAL_SERVER_ERROR, response.status_code)


    @pytest.mark.skipif(priorities["c61fb913-1b33-4583-b4f4-9f86002e1231"], reason="required")
    @pytest.mark.key("OBSRV-288")
    @pytest.mark.timeout(120)
    @reporting
    def test_country_code_status_code_with_ca(self):
        # Passing correct payload to register country for warranty and check response status code
        payload = self.warranty.payload_address(state='CA')
        response = self.warranty.request_country_register(payload=json.dumps(payload))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    @pytest.mark.skipif(priorities["dc58f813-5977-4261-ad7a-4c2d65bfba23"], reason="required")
    @pytest.mark.key("OBSRV-288")
    @pytest.mark.timeout(120)
    @reporting
    def test_country_code_status_code_with_us(self):
        # Passing correct payload to register country for warranty and check response status code
        payload = self.warranty.payload_address(state='US')
        response = self.warranty.request_country_register(payload=json.dumps(payload))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    @pytest.mark.skipif(priorities["32f648dc-33af-46b6-a6bc-a60769756528"], reason="required")
    @pytest.mark.key("OBSRV-288")
    @pytest.mark.timeout(120)
    @reporting
    def test_country_code_status_code_with_gr(self):
        # Passing correct payload to register country for warranty and check response status code
        # Passing correct payload to register country for warranty and check response status code
        payload = self.warranty.payload_address(state='GR')
        response = self.warranty.request_country_register(payload=json.dumps(payload))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    @pytest.mark.skipif(priorities["ca6542c2-7b91-4b57-90e8-ca0edda46462"], reason="required")
    @pytest.mark.key("OBSRV-288")
    @pytest.mark.timeout(120)
    @reporting
    def test_country_code_status_code_with_it(self):
        # Passing correct payload to register country for warranty and check response status code
        # Passing correct payload to register country for warranty and check response status code
        payload = self.warranty.payload_address(state='IT')
        response = self.warranty.request_country_register(payload=json.dumps(payload))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    @pytest.mark.skipif(priorities["019fee10-eca6-4db8-b883-95f07a4a2423"], reason="required")
    @pytest.mark.key("OBSRV-288")
    @pytest.mark.timeout(120)
    @reporting
    def test_country_code_status_code_with_at(self):
        # Passing correct payload to register country for warranty and check response status code
        payload = self.warranty.payload_address(state='AT')
        response = self.warranty.request_country_register(payload=json.dumps(payload))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
