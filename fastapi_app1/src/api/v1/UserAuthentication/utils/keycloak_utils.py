from fastapi import HTTPException
from keycloak.keycloak_openid import KeycloakOpenID
from keycloak import KeycloakAdmin, KeycloakOpenIDConnection
from config.config import KeyCloakSettings



class KeyCloakUtils:
    """
    This is initial class of keycloak which contain connection of keycloak server connection
    and all other function of keycloak library.
    """
    def __init__(self) -> None:
        self.keycloak_credentials = KeyCloakSettings()
        self.keycloak_openid = KeycloakOpenID(server_url=self.keycloak_credentials.KEYCLOAK_SERVER_URL, realm_name=self.keycloak_credentials.REALM_NAME, client_id=self.keycloak_credentials.CLIENT_ID, client_secret_key=self.keycloak_credentials.SECRET_KEY, verify=True)
        self.keycloak_openid_connection = KeycloakOpenIDConnection(server_url=self.keycloak_credentials.KEYCLOAK_SERVER_URL, user_realm_name=self.keycloak_credentials.REALM_NAME,realm_name=self.keycloak_credentials.REALM_NAME, client_id=self.keycloak_credentials.CLIENT_ID, client_secret_key=self.keycloak_credentials.SECRET_KEY, verify=True)
        self.keycloak_admin = KeycloakAdmin(connection=self.keycloak_openid_connection)

    def create_user(self, kwargs: dict):
        user_kwargs = {
                "username": kwargs.get('user_name'),
                "email": kwargs.get('email'),
                "firstName": kwargs.get("first_name"),
                "lastName": kwargs.get('last_name'),
                "enabled": True,
                "emailVerified": True,
                "credentials":[{
                    "value": kwargs.get("password"),
                    "type": "password"
                }],
                "attributes":{"phone_number":kwargs.get("phone_number"),"address": kwargs.get('address', 'N/A')}
            }
        new_user_id = self.keycloak_admin.create_user(user_kwargs)
        return new_user_id

    def update_user(self, user_id, kwargs):
        data = {'attributes':{}}
        if kwargs.get('first_name'):
              data['firstName'] = kwargs.get('first_name')
        if kwargs.get('last_name'):
            data['lastName'] = kwargs.get('last_name')
        if kwargs.get('phone_number'):
            data['attributes']['phone_number'] = kwargs.get('phone_number')
        keycloak_update = self.keycloak_admin.update_user(user_id=user_id, payload=data)
        return keycloak_update
    
    def logout_user(self, refresh_token):
        response = self.keycloak_openid.logout(refresh_token)
        return response

    def get_auth_token(self, username: str, password: str):
        token = self.keycloak_openid.token(username, password)
        return token

    def validate_token(self, token: str):
        token_info = self.keycloak_openid.introspect(token)
        is_active = token_info["active"]
        if is_active:
            return token_info
        raise HTTPException(status_code=401, detail='User is not authenticated')

    def decode_auth_token(self, token: str):
        if not self.validate_token(token=token):
            return False
        res = self.keycloak_openid.userinfo(token)
        return res

    def get_auth_token_by_refresh_token(self, refresh_token: str):
        token = self.keycloak_openid.refresh_token(refresh_token)
        return token
    
    def logout_user_session(self, user_id):
        response = self.keycloak_admin.user_logout(user_id=user_id)
        return response
    
    def get_login_link(self):
        authorization_url = self.keycloak_openid.auth_url(redirect_uri=self.keycloak_credentials.REDIRECT_URL)
        return authorization_url
    
    def get_token(self, code):
        tokens = self.keycloak_openid.token(code=code, grant_type=["authorization_code"], redirect_uri=self.keycloak_credentials.REDIRECT_URL)
        return tokens