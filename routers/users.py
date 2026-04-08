from fastapi import APIRouter, HTTPException, status
from schemas.users import UserCreate, UserRead
from crud.users import get_user_by_email, create_user
from utils.email import send_email_async


router = APIRouter()


@router.post("/register", response_model=UserRead)
async def register(user_in: UserCreate):
    # verify that the user does not already exist
    user = get_user_by_email(user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # save user in the database
    user = create_user(email=user_in.email, password=user_in.password)

    # send email
    await send_email_async(
        subject="Welcome to Aro Bound Ventures",
        recipient=user_in.email,
        body=f"Hello {user_in.email},\n\nThank you for registering",
    )
    return user
