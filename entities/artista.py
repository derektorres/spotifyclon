from persistence.db import get_connection
import pymysql


class Artista ():
    def __init__(self, id: int, nombre:str, nacionalidad:str, fecha_nacimiento:str, oyentes_mensuales:int, is_active: bool):
        self.id= id
        self.nombre = nombre
        self.nacionalidad = nacionalidad
        self.fecha_nacimiento = fecha_nacimiento
        self.oyentes_mensuales = oyentes_mensuales
        self._is_active = bool(is_active)

        