from pydantic import BaseModel
from typing import Optional

# Definición del modelo Director
class Director(BaseModel):
    id: Optional[str] = None #id opcional porque se lo mete la BD
    name: str
    surname: str
    nacionalidad: str