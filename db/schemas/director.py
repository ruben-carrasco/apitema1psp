# Función de serialización para un ÚNICO director
def director_schema(director) -> dict:
    """
    Convierte un documento (document) de MongoDB (que es un diccionario de Python)
    al formato que necesita Pydantic y FastAPI (JSON/dict).
    
    El paso más importante es la conversión del '_id' de MongoDB.
    """
    return {
        # 1. Conversión de ID: 
        #    - MongoDB usa '_id' (tipo ObjectId).
        #    - Pydantic/FastAPI espera 'id' (tipo str).
        #    - Lo convertimos a cadena (str) para evitar errores de serialización JSON.
        "id" : str(director["_id"]),
        
        # 2. Mapeo directo de campos:
        "name" : director["name"],
        "surname" : director["surname"],
        "nacionalidad" : director["nacionalidad"]
    }


# Función de serialización para MÚLTIPLES directores
def directores_schema(directores) -> list:
    """
    Recorre una lista iterable de documentos de directores obtenida de MongoDB
    y aplica 'director_schema' a cada uno para obtener una lista de diccionarios JSON serializables.
    """
    # Se utiliza una list comprehension (comprensión de listas) para eficiencia.
    return [director_schema(director) for director in directores]