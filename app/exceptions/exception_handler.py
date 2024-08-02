from fastapi import Request
from fastapi.responses import JSONResponse
from .custom_exception import (
    InvalidCredentialsException, UserNotFoundException, UserAlreadyExistsException,
    UserNotValidException, EmptyInputException,
    InvalidTokenException, SameUsernamePasswordException,
    InactiveUserException, EmailAlreadyUsedException, PhoneAlreadyUsedException,
    ProfileNotFoundException, ProfileAlreadyExistsException, InvalidProfileDataException,
    RightNotFoundException, RightAlreadyExistsException, InvalidRightDataException,
    CategoryNotFoundException, CategoryAlreadyExistsException, InvalidCategoryDataException,
    SubCategoryNotFoundException, SubCategoryAlreadyExistsException, InvalidSubCategoryDataException
)

# Handlers for User-related exceptions

async def handle_invalid_credentials(req: Request, ex: InvalidCredentialsException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail}, headers=ex.headers)


async def handle_user_not_found(req: Request, ex: UserNotFoundException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})


async def handle_user_already_exists(req: Request, ex: UserAlreadyExistsException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})


async def handle_user_not_valid(req: Request, ex: UserNotValidException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})


async def handle_empty_input(req: Request, ex: EmptyInputException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})


async def handle_invalid_token(req: Request, ex: InvalidTokenException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})


async def handle_same_username_password(req: Request, ex: SameUsernamePasswordException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})


async def handle_inactive_user(req: Request, ex: InactiveUserException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})


async def handle_email_already_used(req: Request, ex: EmailAlreadyUsedException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})


async def handle_phone_already_used(req: Request, ex: PhoneAlreadyUsedException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})

# Handlers for Profile-related exceptions


async def handle_profile_not_found(req: Request, ex: ProfileNotFoundException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})


async def handle_profile_already_exists(req: Request, ex: ProfileAlreadyExistsException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})


async def handle_invalid_profile_data(req: Request, ex: InvalidProfileDataException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})

# Handlers for Right-related exceptions


async def handle_right_not_found(req: Request, ex: RightNotFoundException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})


async def handle_right_already_exists(req: Request, ex: RightAlreadyExistsException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})


async def handle_invalid_right_data(req: Request, ex: InvalidRightDataException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})

# Handlers for Category-related exceptions


async def handle_category_not_found(req: Request, ex: CategoryNotFoundException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})


async def handle_category_already_exists(req: Request, ex: CategoryAlreadyExistsException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})


async def handle_invalid_category_data(req: Request, ex: InvalidCategoryDataException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})

# Handlers for SubCategory-related exceptions


async def handle_subcategory_not_found(req: Request, ex: SubCategoryNotFoundException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})


async def handle_subcategory_already_exists(req: Request, ex: SubCategoryAlreadyExistsException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})


async def handle_invalid_subcategory_data(req: Request, ex: InvalidSubCategoryDataException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})
