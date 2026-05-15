from werkzeug.security import generate_password_hash, check_password_hash
from persistence.db import get_connection
import pymysql
from flask_login import UserMixin 

class User (UserMixin):
    def __init__(self, id: int, nombre:str, email:str, password:str, pais:str, is_active: bool):
        self.id= id
        self.nombre = nombre
        self.email = email
        self.password = password
        self.pais = pais
        self._is_active = bool(is_active)


    @property
    def is_active(self):
        return self._is_active


    @staticmethod 
    def check_login(email, password):
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = "SELECT id, nombre, email, password, pais, is_active FROM usuarios WHERE email = %s"
            cursor.execute(sql, (email,))
            user_data = cursor.fetchone()

            cursor.close()
            connection.close()
            
            if user_data and user_data["password"] == password:
                return User(
                    id=user_data["id"],
                    nombre=user_data["nombre"],
                    email=user_data["email"],
                    password=user_data["password"],
                    pais=user_data["pais"],
                    is_active=bool(user_data["is_active"])
                )
            return None
            
        except Exception as ex:
            print(f"Error en login: {ex}")
            return None
    
    @staticmethod
    def save(nombre: str, email: str, password: str, pais: str) -> bool:
        connection = get_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute("START TRANSACTION;")

            sql_user = """
                INSERT INTO usuarios (nombre, email, password, pais, is_active) 
                VALUES (%s, %s, %s, %s, 1)
            """
            cursor.execute(sql_user, (nombre, email, password, pais))

            cursor.execute("SELECT LAST_INSERT_ID();")
            nuevo_id = cursor.fetchone()[0]

            sql_playlist = """
                INSERT INTO playlists (nombre, usuario_id, is_active) 
                VALUES ('Mis Favoritos', %s, 1)
            """
            cursor.execute(sql_playlist, (nuevo_id,))
            cursor.execute("COMMIT;")
            
            cursor.close()
            connection.close()
            return True

        except Exception as ex:
            print(f"ERROR EN TRANSACCIÓN: {ex}")
            cursor.execute("ROLLBACK;")
            cursor.close()
            connection.close()
            return False
    
    @staticmethod
    def check_email_exists(email: str) -> bool:
        try:
            connection = get_connection()
            cursor = connection.cursor()
            
            sql = "SELECT id FROM usuarios WHERE email = %s"
            cursor.execute(sql, (email,))
            
            resultado = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            return resultado is not None

        except Exception as ex:
            print(f"Error al verificar email: {ex}")
            return True