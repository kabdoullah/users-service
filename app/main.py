from fastapi import FastAPI
from app.api.main import api_router
from app.configuration.config import AuthSettings
from app.configuration.database import create_db_and_tables
from fastapi.middleware.cors import CORSMiddleware
import logfire
from contextlib import asynccontextmanager

from app.exceptions.exception_handler import (
    handle_invalid_credentials, handle_user_not_found, handle_user_already_exists,
    handle_user_not_valid, handle_empty_input, handle_invalid_token,
    handle_same_username_password, handle_inactive_user, handle_email_already_used,
    handle_phone_already_used, handle_profile_not_found, handle_profile_already_exists,
    handle_invalid_profile_data, handle_right_not_found, handle_right_already_exists,
    handle_invalid_right_data, handle_category_not_found, handle_category_already_exists,
    handle_invalid_category_data, handle_subcategory_not_found, handle_subcategory_already_exists,
    handle_invalid_subcategory_data
)
from app.exceptions.custom_exception import (
    InvalidCredentialsException, UserNotFoundException, UserAlreadyExistsException,
    UserNotValidException, EmptyInputException, InvalidTokenException,
    SameUsernamePasswordException, InactiveUserException, EmailAlreadyUsedException,
    PhoneAlreadyUsedException, ProfileNotFoundException, ProfileAlreadyExistsException,
    InvalidProfileDataException, RightNotFoundException, RightAlreadyExistsException,
    InvalidRightDataException, CategoryNotFoundException, CategoryAlreadyExistsException,
    InvalidCategoryDataException, SubCategoryNotFoundException, SubCategoryAlreadyExistsException,
    InvalidSubCategoryDataException
)

settings = AuthSettings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan,
              title="Bon coin User Authentication Microservice")


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


# Enregistrement des exception handlers
app.add_exception_handler(InvalidCredentialsException,
                          handle_invalid_credentials)
app.add_exception_handler(UserNotFoundException, handle_user_not_found)
app.add_exception_handler(UserAlreadyExistsException,
                          handle_user_already_exists)
app.add_exception_handler(UserNotValidException, handle_user_not_valid)
app.add_exception_handler(EmptyInputException, handle_empty_input)
app.add_exception_handler(InvalidTokenException, handle_invalid_token)
app.add_exception_handler(SameUsernamePasswordException,
                          handle_same_username_password)
app.add_exception_handler(InactiveUserException, handle_inactive_user)
app.add_exception_handler(EmailAlreadyUsedException, handle_email_already_used)
app.add_exception_handler(PhoneAlreadyUsedException, handle_phone_already_used)
app.add_exception_handler(ProfileNotFoundException, handle_profile_not_found)
app.add_exception_handler(ProfileAlreadyExistsException,
                          handle_profile_already_exists)
app.add_exception_handler(InvalidProfileDataException,
                          handle_invalid_profile_data)
app.add_exception_handler(RightNotFoundException, handle_right_not_found)
app.add_exception_handler(RightAlreadyExistsException,
                          handle_right_already_exists)
app.add_exception_handler(InvalidRightDataException, handle_invalid_right_data)
app.add_exception_handler(CategoryNotFoundException, handle_category_not_found)
app.add_exception_handler(CategoryAlreadyExistsException,
                          handle_category_already_exists)
app.add_exception_handler(InvalidCategoryDataException,
                          handle_invalid_category_data)
app.add_exception_handler(SubCategoryNotFoundException,
                          handle_subcategory_not_found)
app.add_exception_handler(
    SubCategoryAlreadyExistsException, handle_subcategory_already_exists)
app.add_exception_handler(InvalidSubCategoryDataException,
                          handle_invalid_subcategory_data)
