from ..db.models.pelicula import Pelicula # Modelo Pydantic para Pelicula
from ..db.client import db_client         # Cliente de la base de datos (MongoDB)
from ..db.schemas.pelicula import pelicula_schema, peliculas_schema # Esquemas de conversión

#fastapi dev pelicula.py
from fastapi import APIRouter, HTTPException, status
# from apirest.routers.auth_pelicula import authetication # Se comentó por simplicidad, si la necesitas, descoméntala.

from bson import ObjectId # para la id de MongoDB convertida de str a ObjectId

# Nombre del router con el prefijo y tag
router = APIRouter(prefix="/peliculasdb", tags=["peliculasdb"])

# --- Funciones Auxiliares ---

# método que devuelve una pelicula si la encuentra por id
def search_pelicula_id(id: str):
    try:
        # Busca en la colección 'peliculas'
        pelicula = pelicula_schema(db_client.sample_mflix.peliculas.find_one({"_id" : ObjectId(id)}))
        
        #Devolvemos el objeto convertido a Pelicula
        return Pelicula(**pelicula) # los dos asteriscos desempaquetan el diccionario en un objeto Pelicula
    except:
        return {"error": "Pelicula not found"}
    
def search_pelicula_titulo(titulo: str):
    # La búsqueda me devuelve un objeto del tipo de la base de datos.
    # Necesitamos convertirlo a un objeto Pelicula.
    try:
        # Si algo va mal en la búsqueda dentro de la base de datos se lanzará una excepción,
        # así que la controlamos
        # Se busca en la colección 'peliculas'
        pelicula = pelicula_schema(db_client.sample_mflix.peliculas.find_one({"titulo": titulo}))
        
        # Retorna un objeto Pelicula (asumiendo que 'Pelicula' es el modelo Pydantic)
        return Pelicula(**pelicula)
    except:
        # En caso de no encontrar la pelicula
        return {"error": "Pelicula not found"}


# --- Endpoints ---

# Endpoint para obtener la lista de peliculas
@router.get("/", response_model=list[Pelicula])
#El metodo find devuelve los registros de la base de datos, que convertidos a lista de diccionarios JSON
def peliculas():
    return peliculas_schema(db_client.sample_mflix.peliculas.find())

# Endpoint para obtener una pelicula por su ID (path parameter)         
@router.get("/{id_pelicula}", response_model=Pelicula)
def pelicula(id_pelicula:str): 
    return search_pelicula_id(id_pelicula)

# Método get tipo query. Sólo busca por id
@router.get("", response_model=Pelicula)
async def pelicula(id: str):
    return search_pelicula_id(id)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Pelicula)
async def add_pelicula(pelicula: Pelicula):
    # 1. Comprobamos si la pelicula existe (por título en este caso)
    existe = search_pelicula_titulo(pelicula.titulo)
    
    # lo que implica que la pelicula NO existe y debemos insertarla.
    if type(existe) == Pelicula:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="La pelicula ya existe en la base de datos."
        )
        
    # La pelicula NO existe, procedemos a la inserción
    # Convertimos la pelicula a un diccionario
    pelicula_dict = pelicula.model_dump()
        
    # Eliminamos el campo id
    del pelicula_dict["id"]

    # Añadimos la pelicula a nuestra base de datos (colección 'peliculas')
    id = db_client.sample_mflix.peliculas.insert_one(pelicula_dict).inserted_id

    # Añadimos el campo id a nuestro diccionario
    pelicula_dict["id"] = str(id)

    # Devolvemos el objeto Pelicula recién creado
    return Pelicula(**pelicula_dict)
        

# Se le pasa un id y un objeto json ya modificado, si existe un objeto con su id se le asigna los nuevos valores
@router.put("/{id}", response_model=Pelicula)
async def modify_peliculas(id : str, pelicula: Pelicula):
    # convertimos la pelicula a diccionario
    pelicula_dict = pelicula.model_dump()
    
    #borramos el id para enviar la modificacion sin id.
    del pelicula_dict["id"]
    
    try:
        #buscamos por id y reemplazamos con el nuevo objeto diccionario
        db_client.sample_mflix.peliculas.find_one_and_replace({"_id" : ObjectId(id)}, pelicula_dict)
        
        # devolvemos el objeto para saber que se modifico
        return search_pelicula_id(id)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pelicula no encontrada")

@router.delete("/{id}", response_model=Pelicula)
async def delete_pelicula(id: str):
    #buscamos y borramos la pelicula
    pelicula = db_client.sample_mflix.peliculas.find_one_and_delete({"_id" : ObjectId(id)})
    
    if not pelicula:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pelicula no encontrada")
 
    # devolvemos el objeto que borramos
    return Pelicula(**pelicula_schema(pelicula))