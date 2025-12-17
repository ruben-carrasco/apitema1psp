# Función de serialización para una ÚNICA película
def pelicula_schema(pelicula) -> dict:
    """
    Convierte un documento (document) de MongoDB al formato JSON/dict
    requerido por Pydantic/FastAPI para el modelo Pelicula.
    """
    return {
        # Conversión de ID de MongoDB (ObjectId) a 'id' (str)
        "id" : str(pelicula["_id"]),
        
        # Mapeo directo de campos
        "titulo" : pelicula["titulo"],
        "duracion" : pelicula["duracion"],
        
        # Mapeo directo de la ID del Director asociado (asumida como string/int guardado en BD)
        "id_director" : pelicula["id_director"]
    }


# Función de serialización para MÚLTIPLES películas
def peliculas_schema(peliculas) -> list:
    """
    Aplica 'pelicula_schema' a una lista de documentos de películas obtenida de MongoDB.
    """
    # Se utiliza una list comprehension para aplicar la serialización a toda la lista.
    return [pelicula_schema(pelicula) for pelicula in peliculas]