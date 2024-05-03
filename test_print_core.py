import pytest
import unittest
import requests
import json
import os

from .utils.reporting import reporting

from .param import Param as param


class HPOnePrintCore(unittest.TestCase):

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
        param.result["directory"] = 'print_core'
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

    @pytest.mark.skipif(priorities["f39d054e-cd2e-4513-b522-f0167af19be2"], reason="required")
    @pytest.mark.key('ECOTEST-930')
    @pytest.mark.timeout(120)
    @reporting
    def test_print_core_dummy_low(self):
        assert True

    @pytest.mark.skipif(priorities["1fd0194a-e635-4fd8-8c1f-8eb63b349f15"], reason="required")
    @pytest.mark.key('ECOTEST-930')
    @pytest.mark.timeout(120)
    @reporting
    def test_print_core_dummy_high(self):
        assert True
