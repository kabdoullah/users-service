from fastapi import Request
from fastapi.responses import JSONResponse
from .custom_exception import (
    InvalidCredentialsException, UserNotFoundException, UserAlreadyExistsException,
    InvalidPasswordException, UserNotValidException, EmptyInputException,
    InvalidTokenException, CustomBadGatewayException, SameUsernamePasswordException,
    InactiveUserException, EmailAlreadyUsedException, PhoneAlreadyUsedException
)
import logfire

async def handle_invalid_credentials(req: Request, ex: InvalidCredentialsException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail}, headers=ex.headers)

async def handle_user_not_found(req: Request, ex: UserNotFoundException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})

async def handle_user_already_exists(req: Request, ex: UserAlreadyExistsException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})

async def handle_invalid_password(req: Request, ex: InvalidPasswordException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})


async def handle_user_not_valid(req: Request, ex: UserNotValidException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})

async def handle_empty_input(req: Request, ex: EmptyInputException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})

async def handle_invalid_token(req: Request, ex: InvalidTokenException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})

async def handle_custom_bad_gateway(req: Request, ex: CustomBadGatewayException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})

async def handle_same_username_password(req: Request, ex: SameUsernamePasswordException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})

async def handle_inactive_user(req: Request, ex: InactiveUserException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})

async def handle_email_already_used(req: Request, ex: EmailAlreadyUsedException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})

async def handle_phone_already_used(req: Request, ex: PhoneAlreadyUsedException):
    return JSONResponse(status_code=ex.status_code, content={"message": ex.detail})
