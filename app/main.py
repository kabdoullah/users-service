from typing import Optional
from fastapi import FastAPI, Depends, Header, status, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.configuration.config import AuthSettings, ServerSettings
from app.exceptions.custom_exception import (CustomBadGatewayException, EmailAlreadyUsedException, EmptyInputException, InactiveUserException, InvalidCredentialsException, InvalidPasswordException, InvalidTokenException, PhoneAlreadyUsedException, SameUsernamePasswordException, UserAlreadyExistsException, UserNotFoundException, UserNotValidException)
from app.exceptions.exception_handler import (handle_custom_bad_gateway, handle_email_already_used, handle_empty_input, handle_inactive_user, handle_invalid_credentials, handle_invalid_password, handle_invalid_token, handle_phone_already_used, handle_same_username_password, handle_user_already_exists, handle_user_not_found, handle_user_not_valid)
import logfire


app = FastAPI(title="Bon coin User Authentication Microservice")


origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logfire
logfire.configure(service_name='auth-microservice',)
logfire.info('Auth Microservice Started')


# Logfire metrics counter
request_counter = logfire.metric_counter(
    'request',
    unit='1',
    description='Number of requests received by auth microservice'
)

@app.middleware("http")
async def logfire_middleware(request: Request, call_next):
    request_counter.add(1)
    with logfire.span('{method} {path}', path=request.url.path, method=request.method):
        logfire.info("Request to access " + request.url.path)
        try:
            response = await call_next(request)
            logfire.info("Successfully accessed {path}", path=request.url.path)
        except Exception as e:
            logfire.error("Request to {request} failed: {e}", request=request.url, ex=e)
            response = JSONResponse(content={"success": False}, status_code=500)
        return response
    

# Dependency Injection for configuration
def build_config():
    return AuthSettings()

def fetch_config():
    return ServerSettings()

@app.get('/index', status_code=status.HTTP_200_OK)
def index_auth(
    config: AuthSettings = Depends(build_config),
    fconfig: ServerSettings = Depends(fetch_config)
):
    return {
        'project_name': config.APPLICATION,
        'webmaster': config.WEBMASTER,
        'created': config.CREATED,
        'development_server': fconfig.PRODUCTION_SERVER,
        'dev_port': fconfig.PROD_PORT
    }
    
@app.get("/headers/verify", status_code=status.HTTP_200_OK)
def verify_headers(
    host: Optional[str] = Header(None),
    accept: Optional[str] = Header(None),
    user_agent: Optional[str] = Header(None),
    accept_language: Optional[str] = Header(None),
    accept_encoding: Optional[str] = Header(None)
):
    return {
        "host": host,
        "accept": accept,
        "user_agent": user_agent,
        "accept_language": accept_language,
        "accept_encoding": accept_encoding
    }

# Register exception handlers
app.add_exception_handler(InvalidCredentialsException, handle_invalid_credentials)
app.add_exception_handler(UserNotFoundException, handle_user_not_found)
app.add_exception_handler(UserAlreadyExistsException, handle_user_already_exists)
app.add_exception_handler(InvalidPasswordException, handle_invalid_password)
app.add_exception_handler(UserNotValidException, handle_user_not_valid)
app.add_exception_handler(EmptyInputException, handle_empty_input)
app.add_exception_handler(InvalidTokenException, handle_invalid_token)
app.add_exception_handler(CustomBadGatewayException, handle_custom_bad_gateway)
app.add_exception_handler(SameUsernamePasswordException, handle_same_username_password)
app.add_exception_handler(InactiveUserException, handle_inactive_user)
app.add_exception_handler(EmailAlreadyUsedException, handle_email_already_used)
app.add_exception_handler(PhoneAlreadyUsedException, handle_phone_already_used)