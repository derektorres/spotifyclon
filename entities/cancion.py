from persistence.db import get_connection
import pymysql


class Artista ():
    def __init__(self, id: int, nombre:str, duracion_segundos:int, genero:str, artista_id:int, album_id:int, is_active: bool):
        self.id= id
        self.nombre = nombre
        self.duracion_segundos = duracion_segundos
        self.genero = genero
        self.artista_id = artista_id
        self.album_id = album_id
        self._is_active = bool(is_active)
        
