#fastapi dev director.py


from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from routers.auth_director import authetication

router = APIRouter(prefix="/directores", tags=["directores"])


# Definición del modelo Director
class Director(BaseModel):
    id: int
    name: str
    surname: str
    nacionalidad: str

# Lista de directores de ejemplo
director_list = [Director(id=1,name = "Paco", surname="Pérez", nacionalidad="Española"),
                Director(id=2,name = "María", surname="Martínez", nacionalidad="Italiana"),
                Director(id=3,name = "Lucía", surname="Rodríquez", nacionalidad="Francesa"),
                Director(id=4,name = "Ana", surname="González", nacionalidad="Alemana") 
                ]

# Endpoint para obtener la lista de directores
@router.get("/")
def directores():
    return director_list

# Endpoint para obtener un director por su ID         
@router.get("/{id_director}")
def get_director(id_director:int): 
    director = [director for director in director_list if director.id == id_director]

    if director:
        return director[0]
    
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/", status_code=201, response_model=Director)
def add_director(director: Director, authorized = Depends(authetication)):
    director.id = next_id()
    director_list.append(director)
    return director

# Se le pasa un id y un objeto json ya modificado, si existe un objeto con su id se le asigna los nuevos valores
@router.put("/{id}", response_model=Director)
def modify_directores(id : int, director: Director):
    for index, saved_director in enumerate(director_list):
        if saved_director.id == id:
            director.id = id
            director_list[index] = director
            return director
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/{id}")
def delete_user(id: int):
    for saved_director in director_list:
        if saved_director.id == id:
            director_list.remove(saved_director)
            return {"message" : "Director borrado"}
    raise HTTPException(status_code=404, detail="User not found")

def next_id():
    return (max(director_list, key=lambda d : d.id).id + 1)