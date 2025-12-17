from pydantic import BaseModel
from typing import Optional

# Definición del modelo Pelicula
class Pelicula(BaseModel):
    # La ID es opcional (None por defecto) ya que la inserta la base de datos (MongoDB)
    id: Optional[str] = None 
    titulo: str
    duracion: int
    id_director: str