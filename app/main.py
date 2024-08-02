from fastapi import FastAPI
from app.api.main import api_router
from app.configuration.config import AuthSettings
from app.configuration.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from app.exceptions.custom_exception import (CustomBadGatewayException, EmailAlreadyUsedException, EmptyInputException, InactiveUserException, InvalidCredentialsException,
                                             InvalidTokenException, PhoneAlreadyUsedException, SameUsernamePasswordException, UserAlreadyExistsException, UserNotFoundException, UserNotValidException)
from app.exceptions.exception_handler import (handle_custom_bad_gateway, handle_email_already_used, handle_empty_input, handle_inactive_user, handle_invalid_credentials,
                                              handle_invalid_token, handle_phone_already_used, handle_same_username_password, handle_user_already_exists, handle_user_not_found, handle_user_not_valid)
import logfire

settings = AuthSettings()

app = FastAPI(title="Bon coin User Authentication Microservice")




def create_db_and_tables():
    Base.metadata.create_all(bind=engine)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix=settings.API_V1_STR)

# Configure logfire
logfire.configure(send_to_logfire='if-token-present')
logfire.info('Auth Microservice Started')


# Register exception handlers
app.add_exception_handler(InvalidCredentialsException,
                          handle_invalid_credentials)
app.add_exception_handler(UserNotFoundException, handle_user_not_found)
app.add_exception_handler(UserAlreadyExistsException,
                          handle_user_already_exists)
app.add_exception_handler(UserNotValidException, handle_user_not_valid)
app.add_exception_handler(EmptyInputException, handle_empty_input)
app.add_exception_handler(InvalidTokenException, handle_invalid_token)
app.add_exception_handler(CustomBadGatewayException, handle_custom_bad_gateway)
app.add_exception_handler(SameUsernamePasswordException,
                          handle_same_username_password)
app.add_exception_handler(InactiveUserException, handle_inactive_user)
app.add_exception_handler(EmailAlreadyUsedException, handle_email_already_used)
app.add_exception_handler(PhoneAlreadyUsedException, handle_phone_already_used)


if __name__ == "__main__":
    create_db_and_tables()