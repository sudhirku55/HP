import json

import requests
from .utils import base_urls, headers, status
from .token import Token
from .apis.user_mgt_svc import UserMgtSvc


class User(Token):
    user_mgt_svc = UserMgtSvc()

    def __init__(self, user_id: str, email=None) -> None:
        Token.__init__(self)
        self.user_id = user_id
        self.idp_id = None
        self.tenant_id = None
        self.email = email
        self.username = None
        self.addresses = None
        self.devices = None

    def get_user_auth_header(self, token=None) -> dict:
        """mounts the authorization user/client token header"""
        if token is None:
            token = self.get_client_token(self.get_idp_id())
        if token != "":
            return {"Authorization": f"Bearer {token}"}
        return {}

    def get_service_auth_header(self, token=None, username=None, password=None) -> dict:
        """mounts the authorization service token header"""
        if token is None:
            token = self.get_token(username, password)
        if token != "":
            return {"Authorization": f"Bearer {token}"}
        return {}

    def get_customer_auth_header(self, token=None) -> dict:
        """mounts the authorization auth code token header"""
        if token is None:
            token = self.get_token_auth_code()
        if token != "":
            return {"Authorization": f"Bearer {token}"}
        return {}

    def create_user(self):
        payload = User.user_mgt_svc.payload_create_user()
        response = User.user_mgt_svc.request_create_user(payload=json.dumps(payload))
        assert response.status_code == status.HTTP_200_OK
        assert all(k in response.json().keys() for k in ('resourceId', 'idpId', 'email', 'userName'))
        self.user_id = response.json()['resourceId']
        self.idp_id = response.json()['idpId']
        self.email = response.json()['email']['value']
        self.username = response.json()['userName']

    def confirm_existence(self) -> bool:
        response = User.user_mgt_svc.request_get_user(user_id=self.user_id)
        if response.status_code == status.HTTP_200_OK:
            return True
        return False

    def get_idp_id(self) -> str:
        """retrieve the idp id of the user"""
        if self.idp_id is None:
            response = User.user_mgt_svc.request_get_user(user_id=self.user_id)
            assert response.status_code == status.HTTP_200_OK
            assert all(k in response.json().keys() for k in ('idpId', 'email', 'userName'))
            self.idp_id = response.json()['idpId']
            self.email = response.json()['email']['value']
            self.username = response.json()['userName']
        return self.idp_id

    def get_email(self) -> str:
        """retrieve the email of the user"""
        if self.email is None:
            response = User.user_mgt_svc.request_get_user(user_id=self.user_id)

            assert response.status_code == status.HTTP_200_OK
            assert all(k in response.json().keys() for k in ('idpId', 'email', 'userName'))
            self.idp_id = response.json()['idpId']
            self.email = response.json()['email']['value']
            self.username = response.json()['userName']
        return self.email

    def get_username(self) -> str:
        """retrieve the email of the user"""
        if self.username is None:

            response = User.user_mgt_svc.request_get_user(user_id=self.user_id)

            assert response.status_code == status.HTTP_200_OK
            assert all(k in response.json().keys() for k in ('idpId', 'email', 'userName'))
            self.idp_id = response.json()['idpId']
            self.email = response.json()['email']['value']
            self.username = response.json()['userName']
        return self.username

    def get_tenant_id(self) -> str:
        """retrieve the tenant id of the user"""
        if self.tenant_id is None:
            url = f"{base_urls.ACCOUNT_SVC}/accounts"
            response = requests.get(url, headers=self.get_user_auth_header())
            assert response.status_code == status.HTTP_200_OK
            assert 'resourceId' in response.json().keys()
            self.tenant_id = response.json()['resourceId']
        return self.tenant_id

    def get_addresses(self):
        """retrieve the addresses of the user tenant"""
        if self.addresses is None:
            url = f"{base_urls.ADDRESS_SVC}/addresses"
            response = requests.get(
                url,
                headers={**headers.JSON, **self.get_user_auth_header()},
                timeout=15
            )
            assert response.status_code == status.HTTP_200_OK
            assert 'totalCount' in response.json()
            if response.json()['totalCount'] == 0:
                self._add_address()
            else:
                self.addresses = response.json()['resourceList']
        return self.addresses

    def get_devices(self):
        """retrieve the devices of the user tenant"""
        if self.devices is None:
            url = f"{base_urls.DEVICE}/devices/v1"
            response = requests.get(
                url,
                headers={**headers.JSON, **self.get_user_auth_header()},
                timeout=15
            )
            assert response.status_code in [200, 404]
            if response.status_code == status.HTTP_200_OK:
                self.devices = response.json()['devices']
            else:
                self.devices = []
        return self.devices

    def _add_address(self):
        """add a new address to the user tenant"""
        url = f"{base_urls.ADDRESS_SVC}/addresses"
        data = {
            "tenantId": self.get_tenant_id(),
            "firstName": "John",
            "lastName": "Doe",
            "company": "",
            "address": "149 New Montgomery St",
            "address2": "",
            "city": "San Francisco",
            "state": "CA",
            "postalCode": "94105-3739",
            "countryCode": "US",
            "phoneNumber": "(415) 835-9888",
            "bisPrimary": True
        }
        response = requests.post(
            url,
            headers={**headers.JSON, **self.get_user_auth_header()},
            data=json.dumps(data),
            timeout=15
        )
        assert response.status_code == status.HTTP_200_OK
        if self.addresses is None:
            self.addresses = [response.json()]
        else:
            self.addresses.append(response.json())

    def get_service_auth_header_for_ems(self, token=None) -> dict:
        """mounts the authorization service token header"""
        if token is None:
            token = self.get_token_ems()
        if token != "":
            return {"Authorization": f"Bearer {token}"}
        return {}
