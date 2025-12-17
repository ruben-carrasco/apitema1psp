
from datetime import *
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

# Definimos el algoritmo de encriptación
ALGORITHM = "HS256"

# Duración del token
ACCESS_TOKEN_EXPIRE_MINUTES = 1

# Clave que se utilizará como semilla para generar el token
# openssl rand -hex 32
SECRET_KEY = "87ab51098990feb4a2f78da9c911187a71290ebd9e98e56d8b24090815f2ce6f"

# Objeto que se utilizará para el cálculo del hash y
# la verificación de las contraseñas
password_hash = PasswordHash.recommended()

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class Director(BaseModel):
    username : str
    fullname : str
    email : str
    disabled : bool
    
class DirectorBD(Director):
    password : str
    
users_db = {
    "rubencf" : {
        "username" : "rubencf",
        "fullname" : "Ruben Carrasco",
        "email" : "rubencarrasco@gmail.com",
        "disabled" : False,
        "password" : "123456"
    },
    "rubencf54" : {
        "username": "rubencf54",
        "fullname": "Ruben Carrasco",
        "email": "rubencarrasco@gmail.com",
        "disabled": False,
        "password": "$argon2id$v=19$m=65536,t=3,p=4$Y0xncH49umIh/s0pXBfivg$9u6eocNsF2RQknNpnSWqZmTYtRBYbhtfyhd5oidRzo4"
    },
        "rubencf12345" : {
        "username": "rubencf12345",
        "fullname": "Ruben Carrasco",
        "email": "rubencarrasco@gmail.com",
        "disabled":  False,
        "password": "$argon2id$v=19$m=65536,t=3,p=4$GNvZtBgdhrCyWHHK5jbwWw$PZGwrEEAvk5kAvhK5cMmmewc82XgELSD0Q1rLXarm8U"
    }
}

@router.post("/register", status_code=201)
def add_user(user: DirectorBD):
    if user.username not in users_db:
        hashed_password = password_hash.hash(user.password)
        user.password = hashed_password
        users_db[user.username] = user
        return user
    else:
        raise HTTPException(status_code=409, detail="User already exists")
    
    
@router.post("/login", status_code=201)
async def login(form : OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    #Si el usuario existe en el diccionario
    if user_db:
        # lo asignamos a un usuario para trabajar con el
        user = DirectorBD(**user_db)
        try:
            #Verificamos la contraseña y si es correcta generamos el token
            if password_hash.verify(form.password, user.password):
                # Hora actual + tiempo de expiracion
                expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                # Parametros del token: 
                access_token = {"sub" : user.username, "exp":expire}
                # Generamos el token
                token = jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM)
                return {"access_token":token, "token_type":"bearer"}
        except:
                raise HTTPException(status_code=400, detail="Error de autenticación")
        
    raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

async def authetication(token: str = Depends(oauth2)):
    # Obtenemos el usuario desde el token
    try:
        username = jwt.decode(token, SECRET_KEY, algorithm=ALGORITHM).get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Credenciales de autenticación inválidas", headers={"WWWW-Authenticate" : "Bearer"})
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Credenciales de autenticación inválidas", headers={"WWWW-Authenticate" : "Bearer"})