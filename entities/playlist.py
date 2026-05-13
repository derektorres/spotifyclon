from persistence.db import get_connection
import pymysql


class User ():
    def __init__(self, id: int, nombre:str, usuario_id:int, is_active: bool):
        self.id= id
        self.nombre = nombre
        self.usuario_id = usuario_id
        self._is_active = bool(is_active)

    