import requests
import json
from .param import Param as param
from .utils import base_urls, cred_reference, status, users


class Token:
    token = None
    ems_token = None
    # OneUID_token = None
    stratus_auth_token = None

    def __init__(self) -> None:
        self.bearer_token = None
        self.clients_token = {}
        self.auth_code_token = None
        self.delegation_token = None
        self.delegation_token_resp = None
        self.delegation_subject_token = None
        self.authz_service_token = None
        self.APIGEE_token = None
        self.OneUID_token = None
    def get_token(self, username, password):
        if Token.token is None:
            try:
                url = f"{base_urls.AUTHZ_GETPRODUCTS}/token"
                headers = {'content_type': 'application/x-www-form-urlencoded'}
                params = {'grant_type': 'client_credentials'}
                # auth = (param.username, param.password)
                auth = (username, password)
                r = requests.post(url, headers=headers, params=params, auth=auth, timeout=15)
                assert r.status_code == status.HTTP_200_OK
                resp = json.loads(r.content)
                token = resp['access_token']
                Token.token = token
            except Exception:
                print("get_token failed")
                Token.ems_token = None
                r = None
                raise
        return Token.token

    def get_authz_service_token(self):
        if self.authz_service_token is None:
            try:
                url = f"{base_urls.AUTHZ_GETPRODUCTS}/token"
                # headers = {'content_type': 'application/x-www-form-urlencoded','Authorization': 'Basic cXA0clllZWJOR1ZCeFF1U0x0U1FiT1RVSVljWlFSUHo6bHZwSDhXcHE1QWFYdFpyWnJrREdtZzN4Slk1SHppaGg='}
                params = {'grant_type': 'client_credentials'}
                # auth = (param.username, param.password)
                auth = (cred_reference.eCommerce_AuthZ_username, cred_reference.eCommerce_AuthZ_password)
                authz_service_token_res = requests.post(url, data=params, params=params, auth=auth, timeout=15)
                # assert authz_service_token_res.status_code == status.HTTP_200_OK
                respcont = json.loads(authz_service_token_res.content)
                if authz_service_token_res.status_code == status.HTTP_200_OK:
                    token = respcont['access_token']
                    self.authz_service_token = token
            except Exception:
                print("get_authz_service_token failed")
                Token.ems_token = None
                r = None
                raise
        return self.authz_service_token

    def get_bearer_token(self):
        if self.bearer_token is None:
            try:
                url = f"{base_urls.AUTHZ_GETPRODUCTS}/token?grant_type=client_credentials"
                headers = {'Authorization': f'Basic {cred_reference.bearer_authorization}',
                           'Content-Type': f'Basic {cred_reference.bearer_cont_type}'
                           }
                # 'Authorization': 'Basic NUlWZzMwMmZ3V2twNWxucVBpaGZITTRZM3RFbU5VZWY6UkJkQkZVWmVjSENiUlZtVVNGNHFtRTFzZ0JnY0M1czM='}
                params = {'grant_type': 'client_credentials'}
                # auth = (param.username, param.password)
                auth = (
                    cred_reference.eCommerce_serviceClient_username, cred_reference.eCommerce_serviceClient_password)
                r = requests.post(url, headers=headers, params=params, auth=auth, timeout=15)
                assert r.status_code == status.HTTP_200_OK
                resp = json.loads(r.content)
                token = resp['access_token']
                self.bearer_token = token
            except Exception:
                print("get_bearer_token failed.")
                Token.ems_token = None
                r = None
                raise
        return self.bearer_token

    def get_no_auth_bearer_token(self):

        url = f"{base_urls.AUTHZ_GETPRODUCTS}/token"
        headers = {
            'Authorization': f'Basic {cred_reference.bearer_authorization}'}
        params = {'grant_type': 'client_credentials'}
        auth = (cred_reference.serviceClient_universal_username, cred_reference.invalid_password)
        r = requests.post(url, headers=headers, params=params, auth=auth, timeout=15)
        return r.status_code, r.reason

    def get_delegationsubject_token(self):
        if self.delegation_subject_token is None:
            try:
                url = f"{base_urls.AUTHZ_GETPRODUCTS_DELEGATION}/token"
                headers = {
                    'Authorization': f'Basic {cred_reference.delegation_authorization}'}
                # 'Authorization': 'Basic cXA0clllZWJOR1ZCeFF1U0x0U1FiT1RVSVljWlFSUHo6bHZwSDhXcHE1QWFYdFpyWnJrREdtZzN4Slk1SHppaGg='}
                params = {'grant_type': 'client_credentials'}
                r = requests.post(url, headers=headers, params=params, timeout=15)
                assert r.status_code == status.HTTP_200_OK
                resp = json.loads(r.content)
                token = resp['access_token']
                self.delegation_subject_token = token
            except Exception:
                print("get_delegationsubject_token failed.")
                Token.ems_token = None
                r = None
                raise
        return self.delegation_subject_token

    def get_delegation_token(self):
        if self.delegation_token is None:
            try:
                url = f"{base_urls.AUTHZ_GETPRODUCTS_DELEGATION}/token"
                headers = {'content_type': 'application/x-www-form-urlencoded',
                           'Authorization': f'Basic {cred_reference.delegation_authorization}'}
                # 'Authorization': 'Basic cXA0clllZWJOR1ZCeFF1U0x0U1FiT1RVSVljWlFSUHo6bHZwSDhXcHE1QWFYdFpyWnJrREdtZzN4Slk1SHppaGg='}
                params = {'grant_type': 'urn:ietf:params:oauth:grant-type:token-exchange'}
                data = {
                    'subject_token': self.get_delegationsubject_token(),
                    'subject_token_type': 'urn:ietf:params:oauth:token-type:access_token',
                    # 'requested_user': '631f760326026d031dfeb254',  # old value
                    'requested_user': cred_reference.delegation_requested_user,
                    # 'requested_user': '63d95b440789d30034280bec',
                    'requested_user_type': 'hp:authz:params:oauth:user-id-type:stratusid',
                    # 'tenant_id': '56d76967-fa08-4176-b6f4-db7b5204cf98'  # old value
                    'tenant_id': cred_reference.delegation_tenant_id,
                    # 'tenant_id': 'a2872a52-9651-47fa-a6f3-160b892f1a4a'

                }
                self.delegation_token_resp = requests.post(url, headers=headers, data=data, params=params, timeout=15)
                assert self.delegation_token_resp.status_code == status.HTTP_200_OK
                respcont = json.loads(self.delegation_token_resp.content)
                token = respcont['access_token']
                self.delegation_token = token
            except Exception:
                print("get_delegation_token failed")
                Token.ems_token = None
                r = None
                raise
        return self.delegation_token, self.delegation_token_resp

    def get_client_token(self, requested_user_idpid='umnsbgkcknbtyjw1f4aspth6kq8ec9z9'):
        if requested_user_idpid not in self.clients_token.keys():
            try:
                url = f"{base_urls.AUTHZ_SVC}/token"
                headers = {'content_type': 'application/x-www-form-urlencoded'}
                # auth = (param.username, param.password)
                auth = (
                    cred_reference.serviceClient_universal_username, cred_reference.serviceClient_universal_password)
                data = {
                    'grant_type': 'urn:ietf:params:oauth:grant-type:token-exchange',
                    'subject_token': self.get_token(),
                    'subject_token_type': 'urn:ietf:params:oauth:token-type:access_token',
                    'requested_user': requested_user_idpid,
                    'requested_user_type': 'hp:authz:params:oauth:user-id-type:hpid'
                }
                r = requests.post(url, headers=headers, data=data, auth=auth, timeout=15)
                assert r.status_code == status.HTTP_200_OK
                resp = json.loads(r.content)
                token = resp['access_token']
                self.clients_token[requested_user_idpid] = token

            except Exception as e:
                print("get_client_token failed")
                Token.ems_token = None
                r = None
                raise

        return self.clients_token[requested_user_idpid]

    def get_auth_code(self):
        from selenium import webdriver
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from webdriver_manager.chrome import ChromeDriverManager
        from webdriver_manager.utils import ChromeType
        from selenium.webdriver.common.by import By

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument('--incognito')
        driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install(), options=options)
        authorization_flow_url = f'{base_urls.AUTHZ_WPP}/authorize?response_type=code&client_id={param.username}&redirect_uri=http://localhost:8080/test&scope=openid+email+profile&prompt=consent&state=0c4c4889-90d6-4752-9042-aea853a7c63b'
        driver.get(authorization_flow_url)
        WebDriverWait(driver, 5000).until(EC.visibility_of_element_located((By.ID, 'username')))
        driver.find_element_by_id('username').send_keys(users.USERNAME)
        driver.find_element_by_class_name('next-btn').click()
        WebDriverWait(driver, 1000).until(EC.element_to_be_clickable((By.ID, 'sign-in')))
        driver.find_element_by_id('password').send_keys(users.PASSWORD)
        driver.find_element_by_id('sign-in').click()
        WebDriverWait(driver, 1000).until(EC.url_contains('localhost'))
        auth_code_url = driver.current_url
        driver.close()
        auth_code = auth_code_url.split('?code=')[1].split('&state')[0]
        return auth_code

    def get_token_auth_code(self):
        if self.auth_code_token is None:
            auth_code = self.get_auth_code()
            url = f'{base_urls.AUTHZ_WPP}/token?grant_type=authorization_code&code={auth_code}&redirect_uri=http://localhost:8080/test'
            auth = (param.username, param.password)

            response = requests.post(
                url,
                auth=auth,
                timeout=15
            )

            token = response.json()['access_token']
            self.auth_code_token = token
        return self.auth_code_token

    def get_token_expired(self):
        return "eyJraWQiOiJhdXRoei1waWUtMTY0ODAzNzM2MiIsInR5cCI6IkpXVCIsImFsZyI6IlJTMjU2In0.eyJmcV90ZW5hbnRfaWQiOiI1YzFjMjU0N2JmOTY1ZGVlMDA0NjVhM2IvYzFhNDY5ODctY2JkMy00NWRiLWI5NGEtYTY1NDQxMTZmYzJkIiwibmJmIjoxNjczOTI0OTA1LCJncm91cF9wb2xpY3kiOiJSZWFkTWFnZW50b1BheW1lbnREZXRhaWxzLFJlYWRBZGRyZXNzLE1hbmFnZUZ1bGZpbGxtZW50cyxSZWFkTWFnZW50b1Byb2R1Y3RzLE1hbmFnZVBheW1lbnRNZXRob2RzLFJlYWRNYWdlbnRvT3JkZXJzIiwicG9saWN5X2lkIjoiUzZXUVdTajA0ZDR5bmhTUnlBdmhrUmRJN3hKOGR1YlYiLCJzY29wZSI6Im9wZW5pZCBvZmZsaW5lX2FjY2VzcyIsImlzcyI6Imh0dHBzOi8vcGllLmF1dGh6LndwcC5hcGkuaHAuY29tLyIsImFjY2Vzc19wb2xpY2llcyI6eyI1YzFjMjU0N2JmOTY1ZGVlMDA0NjVhM2IvYzFhNDY5ODctY2JkMy00NWRiLWI5NGEtYTY1NDQxMTZmYzJkLyoqIjoiODBjOGViNjAzMmI4MTcxOGVjMmQ2NGY2YWRmOGFiOTAyNWU2YWRhOCIsIjVjMWMyNTQ3YmY5NjVkZWUwMDQ2NWEzYi9jMWE0Njk4Ny1jYmQzLTQ1ZGItYjk0YS1hNjU0NDExNmZjMmQiOiI4MGM4ZWI2MDMyYjgxNzE4ZWMyZDY0ZjZhZGY4YWI5MDI1ZTZhZGE4In0sImV4cCI6MTY3MzkyODUwNSwiaWF0IjoxNjczOTI0OTA1LCJqdGkiOiIxZGM4YjkyYS1mNTc2LTRiM2UtYTc2NS03OGY0ZTg3MTE5OTNfQVQiLCJjbGllbnRfaWQiOiJTNldRV1NqMDRkNHluaFNSeUF2aGtSZEk3eEo4ZHViViJ9.yuQq48KmuWmXZ_EdVG5uRXfudwsMfvNQMzFqTIp-WQNQCyTubnJlhwmfTO9ljaZfaxHZFWKlQFl5DhhsYoD7jGM1ODFIcAhVBK2TPq5J3BbBYzEaxRivDF6toiISp69TXo9USpmrvUjWmAbFbEA1A_ORcawa1lFFfPq7wFWlEN80viDh7SwhTd52bBiDLxo2JsW3stP_YJ0STKk1aTe32xu64kgLjm_Ex9hzPEj5FYsnp-9ts7oT7nyXz569mKJy2akwwGCWf-eL7ZFIPaHjYOQxoW0lFmR1eidjkjWxYTBg0Uc05U4gZz-NQQHrSb9fBLf7B34nkUaVyIG5ioE3EA"

    def get_token_ems(self):
        if Token.token is None:
            try:
                url = f"{base_urls.AUTHZ_WPP}/token"
                headers = {'content_type': 'application/x-www-form-urlencoded'}
                params = {'grant_type': 'client_credentials'}
                # auth = (param.username, param.password)
                auth = (
                    cred_reference.subscription_serviceClient_username,
                    cred_reference.subscription_serviceClient_password)
                r = requests.post(url, headers=headers, params=params, auth=auth, timeout=15)
                assert r.status_code == status.HTTP_200_OK
                resp = json.loads(r.content)
                token = resp['access_token']
                Token.token = token
            except Exception:
                print("get_token_ems failed")
                Token.ems_token = None
                r = None
                raise
        return Token.token

    def get_APIGEE_token(self):
        if self.APIGEE_token is None:
            try:
                url = f"{base_urls.PCConnect_Prvsn_APIGEE}/token"
                headers = {
                    'Authorization': 'Basic TkhZblVVS09mVVJEQ1dHaWp3dW4ySmg1RkNTaTJHcGU6RlZDdjNuM2N0dndXa3dycG5mdFFxd3R4ekk5NFo4dXA=',
                    'content_type': 'application/x-www-form-urlencoded'}
                params = {'grant_type': 'client_credentials'}
                data = {
                    'grant_type': 'client_credentials',
                    'redirect_uri': 'http://localhost:8087/redirect',
                    'scope': 'Read'
                }
                r = requests.post(url, headers=headers, params=params, data=data, timeout=15)
                assert r.status_code == status.HTTP_200_OK
                resp = json.loads(r.content)
                token = resp['access_token']
                Token.APIGEE_token = token
            except Exception:
                print("get_APIGEE_token failed")
                Token.ems_token = None
                r = None
                raise
        return Token.APIGEE_token, r

    def get_ems_token(self):
        if Token.ems_token is None:
            try:
                url = f"{base_urls.AUTHZ_WPP}/token"
                headers = {'content_type': 'application/x-www-form-urlencoded'}
                params = {'grant_type': 'client_credentials'}
                # auth = (param.username, param.password)
                auth = (
                    cred_reference.serviceClient_universal_username, cred_reference.serviceClient_universal_password)
                r = requests.post(url, headers=headers, params=params, auth=auth, timeout=15)
                assert r.status_code == status.HTTP_200_OK
                resp = json.loads(r.content)
                token = resp['access_token']
                Token.ems_token = token
            except Exception:
                print("get_ems_token failed")
                Token.ems_token = None
                r = None
                raise
        return Token.ems_token, r

    def get_neg_pie_token(self):

        url = f"{base_urls.AUTHZ_WPP}/token"
        headers = {'content_type': 'application/x-www-form-urlencoded'}
        params = {'grant_type': 'client_credentials'}
        # auth = (param.invalid_username, param.password)
        auth = (cred_reference.serviceClient_universal_username, cred_reference.invalid_password)
        res = requests.post(url, headers=headers, params=params, auth=auth, timeout=15)
        return res

    def get_3po_token(self):

        url = f"{base_urls.AUTHZ_WPP}/token"
        params = {'grant_type': 'client_credentials'}
        auth = (cred_reference.Ecommerce_3po_AuthZ_username, cred_reference.Ecommerce_3po_AuthZ_password)
        res = requests.post(url, params=params, auth=auth, timeout=15)
        r = json.loads(res.content)
        token = r["access_token"]
        return token

    def get_OneUID_token(self):
        response = None
        if self.OneUID_token is None:
            try:
                url = f"{base_urls.PC_CONNECT_POST_OneUID}/token.oauth2"
                headers = {
                    'Authorization': 'Basic TWV0aG9uZTpHTE1pZHoxMlplMHJkZmx2b2Z0MHZaZnk4R0xYMnJ3blVsTzJDbzBuWElqcUF0VWZjeTVBbnVsb3RGNjJjWk41',
                }
                params = {'grant_type': 'client_credentials'}
                response = requests.post(url, headers=headers, params=params, timeout=15)
                assert response.status_code == status.HTTP_200_OK
                resp = json.loads(response.content)
                token = resp['access_token']
                self.OneUID_token = token
            except Exception:
                print("get_OneUID_token failed")
                Token.ems_token = None
                r = None
                raise

        return self.OneUID_token, response

    def get_stratus_API_service_token(self):
        if self.stratus_auth_token is None:
            try:
                url = f"{base_urls.STRATUS_AUTH_TOKEN}/token?grant_type=client_credentials"
                # headers = {'content_type': 'application/x-www-form-urlencoded','Authorization': 'Basic cXA0clllZWJOR1ZCeFF1U0x0U1FiT1RVSVljWlFSUHo6bHZwSDhXcHE1QWFYdFpyWnJrREdtZzN4Slk1SHppaGg='}
                params = {'grant_type': 'client_credentials'}
                auth = (cred_reference.Bizops_Auth_username, cred_reference.Bizops_Auth_password)
                stratus_auth_token_res = requests.post(url, data=params, params=params, auth=auth, timeout=15)
                assert stratus_auth_token_res.status_code == status.HTTP_200_OK
                respcont = json.loads(stratus_auth_token_res.content)
                token = respcont['access_token']
                self.stratus_auth_token = token

            except Exception:
                print("get_stratus_API_service_token failed")
                Token.ems_token = None
                r = None
                raise
        return self.stratus_auth_token

    def get_communications_client_token(self):

        url = f"{base_urls.AUTHZ_WPP}/token"
        params = {'grant_type': 'client_credentials'}
        auth = (cred_reference.Communications_client_username, cred_reference.Communications_client_password)
        res = requests.post(url, params=params, auth=auth, timeout=15)
        r = json.loads(res.content)
        token = r["access_token"]
        return token

