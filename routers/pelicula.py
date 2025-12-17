#fastapi dev pelicula.py


from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/peliculas",tags=["peliculas"])

# Modelo pelicula
class Pelicula(BaseModel):
    id: int
    titulo: str
    duracion: int
    id_director: int

# lista de peliculas
pelicula_list = [
    Pelicula(id=1, titulo="El Origen", duracion=148, id_director=1),
    Pelicula(id=2, titulo="Interstellar", duracion=169, id_director=1),
    Pelicula(id=3, titulo="Apocalipsis", duracion=120, id_director=3),
    Pelicula(id=4, titulo="Gladiador", duracion=155, id_director=2),
    Pelicula(id=5, titulo="Matrix", duracion=136, id_director=4)
]

# Endpoint para obtener la lista de peliculas
@router.get("/")
def peliculas():
    return pelicula_list

# Endpoint para obtener un pelicula por su ID         
@router.get("/{id}")
def get_pelicula(id:int): 
    pelicula = [pelicula for pelicula in pelicula_list if pelicula.id == id]

    if pelicula:
        return pelicula[0]
    
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/", status_code=201, response_model=Pelicula)
def add_pelicula(pelicula: Pelicula):
    pelicula.id = next_id()
    pelicula_list.append(pelicula)
    return pelicula

# Se le pasa un id y un objeto json ya modificado, si existe un objeto con su id se le asigna los nuevos valores
@router.put("/{id}", response_model=Pelicula)
def modify_peliculas(id : int, pelicula: Pelicula):
    for index, saved_pelicula in enumerate(pelicula_list):
        if saved_pelicula.id == id:
            pelicula.id = id
            pelicula_list[index] = pelicula
            return pelicula
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/{id}")
def delete_user(id: int):
    for saved_pelicula in pelicula_list:
        if saved_pelicula.id == id:
            pelicula_list.remove(saved_pelicula)
            return {"message" : "Pelicula borrada"}
    raise HTTPException(status_code=404, detail="User not found")

def next_id():
    return (max(pelicula_list, key=lambda p: p.id).id + 1)