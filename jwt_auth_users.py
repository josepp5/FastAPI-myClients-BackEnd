from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from config import Customer, engine

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 30
SECRET = "secreto"

app = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool
    
    
class UserDB(User):
    password: str
    
    
users_db = {
    "jose": {
        "username": "jose",
        "full_name": "Jose Poveda",
        "email": "jose@gmail.com",
        "password": "$2a$12$st6W3ELTNcGxzp66qrkmDOgYQESAE8TD4vHR/UjXTvITn04HgTYEm",
        "disabled": "false"
        },
    "juan": {
        "username": "juan",
        "full_name": "juan Poveda",
        "email": "juan@gmail.com",
        "password": "$2a$12$st6W3ELTNcGxzp66qrkmDOgYQESAE8TD4vHR/UjXTvITn04HgTYEm",
        "disabled": "false"
        },
    "luis": {
        "username": "luis",
        "full_name": "luis Poveda",
        "email": "luis@gmail.com",
        "password": "$2a$12$st6W3ELTNcGxzp66qrkmDOgYQESAE8TD4vHR/UjXTvITn04HgTYEm",
        "disabled": "false"
        }
    }

async def auth_user(token:str = Depends(oauth2)):
    print("auth_user() called")
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticacion invalidas",
            headers={"WWW-Authenticate": "Bearer"})
    
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        print(f"El usuario autenticado es: {username}")
        if username is None:
            raise exception
        
    except JWTError:
        raise exception
    
    user = search_user(username)
    print(f"Usuario autenticado correctamente: {user.username}")
    return search_user(username)
    
    
async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        ) 
    return user

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=" El usuario no es correcto"
        )
    
    user = search_user_db(form.username)
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta"
        )

    access_token = {"sub": user.username,
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}
    
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}
 

@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user  