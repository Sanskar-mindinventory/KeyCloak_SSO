from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.routes.routes import router as auth_routes

app = FastAPI(description='APP 2 for KeyCloak Single Sign-On POC', title='APP-2 KeyCloak SSO', version='1.0.0')

app.include_router(auth_routes)

@app.get("/")
async def index():
    return "KEYCLOAK SSO SERVICE POC."


@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"message": f"Oops! Something went wrong..."},
    )