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


    def check_email_exists(email) -> bool:
        
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT email from usuarios WHERE email = %s"
        cursor.execute(sql, (email,))

        row = cursor.fetchone()

        cursor.close()
        connection.close()
        return row is not None
    
    @staticmethod
    def save(nombre: str, email: str, password: str, pais: str) -> bool:
        
        try:
            connection = get_connection()
            cursor = connection.cursor()

            sql = """
                INSERT INTO usuarios (nombre, email, password, pais, is_active) 
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(sql, (nombre, email, password, pais, 1))

            connection.commit()

            cursor.close()
            connection.close()

            return True

        except Exception as ex:
            print(f"Error saving user: {ex}")
            return False


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
            print(f"Error login user: {ex}")
            return None