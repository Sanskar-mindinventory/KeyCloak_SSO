from fastapi import Depends, APIRouter
from src.api.v1.UserAuthentication.services.services import verify_tokens
from src.api.v1.UserAuthentication.services.services import UserServices

app1 = APIRouter(prefix='/app1')

@app1.get('/tokens')
def get_token(state:str|None, session_state:str|None, code:str|None):
    tokens = UserServices.get_tokens_from_code(code=code)
    return tokens

@app1.get("/")
def read_root(token: dict = Depends(verify_tokens)):
    return {"message": "Welcome to App1!"}

@app1.get("/login")
def login():
    authorization_url = UserServices.login()
    return {"Authorization URL": authorization_url}

@app1.get("/logout")
def logout(refresh_token: str):
    return UserServices.logout_user_keycloak(refresh_token=refresh_token) 