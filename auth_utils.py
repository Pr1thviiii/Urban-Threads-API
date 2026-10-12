import os
import jwt
from dotenv import load_dotenv
from pwdlib import PasswordHash
from fastapi.security import HTTPAuthorizationCredentials , HTTPBearer 
from datetime import datetime , timedelta , timezone
from fastapi import Depends , HTTPException 
from database import get_db
from sqlalchemy.orm import Session 
from models import UserModel

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
TIME = os.getenv("TIME")

user_not_exit = HTTPException(
    status_code=404,
    detail="user not exist"
) 

OAuth2 = HTTPBearer()

pwd_hash = PasswordHash.recommended()

def Hash_Password(plain_pass):
    return pwd_hash.hash(plain_pass)

def Verify_Password(plain_pass,hashed_pass):
    return pwd_hash.verify(plain_pass,hashed_pass)


def create_token(data:dict):
    encoded_data = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(TIME))
    encoded_data.update({"exp": expire})
    encoded_jwt = jwt.encode(encoded_data ,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(
        Credential : HTTPAuthorizationCredentials = Depends(OAuth2),
        db : Session = Depends(get_db)
        ):
    token = Credential.credentials

    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        user = db.get(UserModel,int(user_id))

        if user is None:
            raise user_not_exit

        return user

    except:
        raise user_not_exit

    