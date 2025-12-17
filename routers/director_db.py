from ..db.models.director import Director
from ..db.client import db_client
from ..db.schemas.director import director_schema, directores_schema

#fastapi dev director.py
from fastapi import APIRouter, Depends, HTTPException
from proyecto.routers.auth_director import authetication

from bson import ObjectId #para la id del director convertila de str a ObjectId

router = APIRouter(prefix="/directoresdb", tags=["directoresdb"])

# Endpoint para obtener la lista de directores
@router.get("/", response_model=list[Director])
#El metodo find devuelve los registros de la base de datos, que convertidos a lista de diccionarios JSON
def directores():
    return directores_schema(db_client.sample_mflix.directores.find())

# Endpoint para obtener un director por su ID         
@router.get("/{id_director}", response_model=Director)
def director(id_director:str): 
    return search_director_id(id_director)

# Método get tipo query. Sólo busca por id
@router.get("", response_model=Director)
async def director(id: str):
    return search_director_id(id)

@router.post("/", status_code=201, response_model=Director)
async def add_director(director: Director):
    # 1. Comprobamos si el director existe
    existe = search_director(director.name, director.surname)
    
    # lo que implica que el director NO existe y debemos insertarlo.
    if type(existe) == Director:
        raise HTTPException(
            status_code=409, 
            detail="El director ya existe en la base de datos."
        )
        
    # El director NO existe, procedemos a la inserción
    # Convertimos el director a un diccionario
    director_dict = director.model_dump()
        
    # Eliminamos el campo id
    del director_dict["id"]

    # Añadimos el director a nuestra base de datos
    id = db_client.sample_mflix.directores.insert_one(director_dict).inserted_id

    # Añadimos el campo id a nuestro diccionario
    director_dict["id"] = str(id)

    # Devolvemos el objeto Director recién creado
    return Director(**director_dict)
        


# Se le pasa un id y un objeto json ya modificado, si existe un objeto con su id se le asigna los nuevos valores
@router.put("/{id}", response_model=Director)
async def modify_directores(id : str, director: Director):
    # convertimos el director a diccionario
    director_dict = director.model_dump()
    
    #borramos el id para enviar la modificacion sin id.
    del director_dict["id"]
    
    try:
        #buscamos por id y reemplazamos con el nuevo objeto diccionario
        db_client.sample_mflix.directores.find_one_and_replace({"_id" : ObjectId(id)}, director_dict)
        
        # devolvemos el objeto para saber que se modifico
        return search_director_id(id)
    except:
        raise HTTPException(status_code=404, detail="Director no encontrado")

@router.delete("/{id}", response_model=Director)
async def delete_director(id: str):
    #buscamos y borramos el director
    director = db_client.sample_mflix.directores.find_one_and_delete({"_id" : ObjectId(id)})
    
    if not director:
     raise HTTPException(status_code=404, detail="Director no encontrado")
 
    # devolvemos el objeto que borramos
    return Director(**director_schema(director))



# metodo que devuelve un director si lo encuentra por id
def search_director_id(id: str):
    try:
        director = director_schema(db_client.sample_mflix.directores.find_one({"_id" : ObjectId(id)}))
        
        #Devolvemos el objeto convertido a director 
        return Director(**director) # los dos asteriscos desempaquetan el diccionario en un objeto director
    except:
        return {"error": "Director not found"}
    
def search_director(name: str, surname: str):
    # La búsqueda me devuelve un objeto del tipo de la base de datos.
    # Necesitamos convertirlo a un objeto Director.
    try:
        # Si algo va mal en la búsqueda dentro de la base de datos se lanzará una excepción,
        # así que la controlamos
        # Se busca en la colección 'directorEs'
        director = director_schema(db_client.sample_mflix.directores.find_one({"name": name, "surname": surname}))
        
        # Retorna un objeto Director (asumiendo que 'Director' es el modelo Pydantic)
        return Director(**director)
    except:
        # En caso de no encontrar al director
        return {"error": "Director not found"}