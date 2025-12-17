from fastapi import FastAPI

from routers import director
from routers import pelicula
from routers import auth_director
from routers import director_db
from routers import pelicula_db

app = FastAPI()

#Routers
app.include_router(director.router)
app.include_router(pelicula.router)
app.include_router(auth_director.router)
app.include_router(director_db.router)
app.include_router(pelicula_db.router)