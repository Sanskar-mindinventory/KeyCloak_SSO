from src.api.v1.UserAuthentication.utils.keycloak_utils import KeyCloakUtils

class UserServices:
    @staticmethod
    def login():
        response = KeyCloakUtils().get_login_link()
        return response

    @staticmethod    
    def get_tokens_from_code(code):
        response = KeyCloakUtils().get_token(code=code)
        return response
    
    @staticmethod
    def logout_user_keycloak(refresh_token):
        response = KeyCloakUtils().logout_user(refresh_token=refresh_token)
        return response


    
def verify_tokens(access_token):
    response = KeyCloakUtils().validate_token(token=access_token)
    return response