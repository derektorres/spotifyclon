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

    @staticmethod
    def save(nombre: str, nacionalidad: str, fecha_nacimiento: str, oyentes_mensuales: int) -> bool:
        
        try:
            connection = get_connection()
            cursor = connection.cursor()

            sql = """
                INSERT INTO artistas (nombre, nacionalidad, fecha_nacimiento, oyentes_mensuales, is_active) 
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(sql, (nombre, nacionalidad, fecha_nacimiento, oyentes_mensuales, 1))

            connection.commit()

            cursor.close()
            connection.close()

            return True

        except Exception as ex:
            print(f"Error saving artist: {ex}")
            return False    
        
    @staticmethod
    def get_all_ordered() -> list:
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            sql = """
                SELECT id, nombre, nacionalidad, fecha_nacimiento, oyentes_mensuales, is_active 
                FROM artistas 
                WHERE is_active = 1 
                ORDER BY oyentes_mensuales DESC
            """

            cursor.execute(sql)
            rows = cursor.fetchall()
            lista_artistas = []
            for row in rows:
                obj = Artista(
                    id=row["id"],
                    nombre=row["nombre"],
                    nacionalidad=row["nacionalidad"],
                    fecha_nacimiento=str(row["fecha_nacimiento"]),
                    oyentes_mensuales=row["oyentes_mensuales"],
                    is_active=bool(row["is_active"])
                )
                lista_artistas.append(obj)

            cursor.close()
            connection.close()

            return lista_artistas

        except Exception as ex:
            print(f"Error al obtener artistas: {ex}")
            return []