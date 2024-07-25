from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.models.requests.user import UserParticular, UserProfessional
from app.services.user_service import UserService

router = APIRouter()

@router.post("/register_users/", response_model=UserParticular)
async def register_user(user_data: UserParticular, userservice: UserService = Depends(UserService)):
    db_user = UserService.get_user_by_email(user_data.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # +
    # await send_otp_email(new_user.email, otp_code, background_tasks)

    # return new_user

@router.post("/register_professionnel/", response_model=UserProfessional)
async def register_professionel(user_data: UserProfessional, userservice: UserService = Depends(UserService)):
    db_user = UserService.get_user_by_email(user_data.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

# @router.get("/users/", response_model=List[User])
# def get_all_users(service: UserService = Depends()):
#     return service.get_all_users()

# @router.get("/users/{user_id}", response_model=User)
# def get_user_by_id(user_id: int, service: UserService = Depends()):
#     user = service.get_user_by_id(user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

# @router.put("/users/{user_id}", response_model=User)
# def update_user(user_id: int, user: UserBase, service: UserService = Depends()):
#     updated_user = service.update_user(user)
#     if not updated_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return updated_user

# @router.delete("/users/{user_id}", response_model=bool)
# def delete_user(user_id: int, service: UserService = Depends()):
#     success = service.delete_user(user_id)
#     if not success:
#         raise HTTPException(status_code=404, detail="User not found")
#     return success

# @router.post("/users/reset_password/", response_model=User)
# def reset_password(email: str, new_password: str, service: UserService = Depends()):
#     user = service.reset_password(email, new_password)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found or invalid OTP")
#     return user

# @router.post("/users/update_password/", response_model=User)
# def update_password(user_id: int, new_password: str, service: UserService = Depends()):
#     user = service.get_user_by_id(user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     updated_user = service.update_password(user, new_password)
#     return updated_user
