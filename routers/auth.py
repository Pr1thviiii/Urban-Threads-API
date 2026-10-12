from fastapi import APIRouter, Depends , HTTPException
from schemas import UserRequest , UserResponse
from database import get_db
from sqlalchemy.orm import Session
from models import UserModel 
from sqlalchemy import select
from auth_utils import Hash_Password , Verify_Password , user_not_exit , create_token , get_current_user


router = APIRouter(prefix="/auth",tags=["Auth"])

@router.post("/register",response_model=UserResponse,status_code=201)
def register(data : UserRequest, db:Session = Depends(get_db)):
    query = select(UserModel).where(UserModel.email == data.email)
    existing = db.scalars(query).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="User Already Exist"
        )
    hashed_password = Hash_Password(data.password)
    
    new_user = UserModel(
        email = data.email,
        password = hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login",status_code=200)
def login(data:UserRequest,db:Session = Depends(get_db)):
    query = select(UserModel).where(UserModel.email== data.email)
    user = db.scalars(query).first()

    if user is None or not Verify_Password(data.password,user.password):
        raise HTTPException(
            status_code=401,
            detail="invalid email or password"
        )

    data_pack = {
        "sub" : str(user.id)
    }
    token = create_token(data=data_pack)
    return {
        "access_token" : token,
        "token_type" : "Bearer"
    }
    

@router.patch("/{id}/make-admin",status_code=200)
def make_admin(id:int,db:Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    user = db.get(UserModel,current_user.id)

    if user is None :
        raise user_not_exit

    if user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You're not allowed to perfrom this operation"
        )
    
    new_user = db.get(UserModel,id)
    if new_user:
        new_user.role = "admin"
        db.commit()
        return {f"{new_user.email} , is offically an admin now."}

    else:
        raise user_not_exit




    
    
