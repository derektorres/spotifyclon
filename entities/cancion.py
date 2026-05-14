from persistence.db import get_connection
import pymysql


class Cancion():
    def __init__(self, id: int, nombre: str, duracion_segundos: int, genero: str, artista_id: int, album_id: int, is_active: bool):
        self.id = id
        self.nombre = nombre
        self.duracion_segundos = duracion_segundos
        self.genero = genero
        self.artista_id = artista_id
        self.album_id = album_id 
        self._is_active = bool(is_active)

    @property
    def is_active(self):
        return self._is_active
    
    @staticmethod
    def save(nombre: str, duracion_segundos: int, genero: str, artista_id: int, album_id: int = None) -> bool:
        try:
            connection = get_connection()
            cursor = connection.cursor()

            sql = """
                INSERT INTO canciones (nombre, duracion_segundos, genero, artista_id, album_id, is_active) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            cursor.execute(sql, (nombre, duracion_segundos, genero, artista_id, album_id, 1))

            connection.commit()

            cursor.close()
            connection.close()

            return True

        except Exception as ex:
            print(f"Error saving cancion: {ex}")
            return False





    @staticmethod
    def get_all() -> list:
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            sql = """
                SELECT c.id, c.nombre, c.duracion_segundos, c.genero, c.artista_id, a.nombre as artista_nombre 
                FROM canciones c
                INNER JOIN artistas a ON c.artista_id = a.id
                WHERE c.is_active = 1
                ORDER BY c.duracion_segundos DESC
            """
            
            cursor.execute(sql)
            rows = cursor.fetchall()

            lista_canciones = []
            for row in rows:

                obj = Cancion(
                    id=row["id"],
                    nombre=row["nombre"],
                    duracion_segundos=row["duracion_segundos"],
                    genero=row["genero"],
                    artista_id=row["artista_id"],
                    album_id=None, 
                    is_active=True
                )
                obj.artista_nombre = row["artista_nombre"] 
                lista_canciones.append(obj)

            cursor.close()
            connection.close()
            return lista_canciones

        except Exception as ex:
            print(f"Error al obtener canciones: {ex}")
            return []