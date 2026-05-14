from persistence.db import get_connection
import pymysql

class Playlist:
    def __init__(self, id: int, nombre: str, usuario_id: int, is_active: bool):
        self.id = id
        self.nombre = nombre
        self.usuario_id = usuario_id
        self._is_active = bool(is_active)

    @staticmethod
    def get_by_user(usuario_id: int) -> list:
        """Obtiene todas las playlists de un usuario"""
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            
            sql = "SELECT id, nombre, usuario_id, is_active FROM playlists WHERE usuario_id = %s AND is_active = 1"
            cursor.execute(sql, (usuario_id,))
            rows = cursor.fetchall()
            
            playlists = []
            for row in rows:
                obj = Playlist(
                    id=row["id"],
                    nombre=row["nombre"],
                    usuario_id=row["usuario_id"],
                    is_active=row["is_active"]
                )
                playlists.append(obj)

            cursor.close()
            connection.close()
            return playlists
        except Exception as ex:
            print(f"Error al obtener playlists: {ex}")
            return []

    @staticmethod
    def save(nombre: str, usuario_id: int) -> bool:
        """Guarda una nueva playlist en la base de datos"""
        try:
            connection = get_connection()
            cursor = connection.cursor()
            
            sql = "INSERT INTO playlists (nombre, usuario_id, is_active) VALUES (%s, %s, 1)"
            cursor.execute(sql, (nombre, usuario_id))
            
            connection.commit() 
            cursor.close()
            connection.close()
            return True
        except Exception as ex:
            print(f"Error al guardar la playlist: {ex}")
            return False
        
    @staticmethod
    def agregar_cancion(playlist_id: int, cancion_id: int) -> bool:
        try:
            connection = get_connection()
            cursor = connection.cursor()
            
            sql = "INSERT INTO playlist_canciones (playlist_id, cancion_id, created_at, updated_at) VALUES (%s, %s, NOW(), NOW())"
            
            cursor.execute(sql, (playlist_id, cancion_id))
            
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Exception as ex:
            print(f"Error al agregar canción a la playlist: {ex}")
            return False