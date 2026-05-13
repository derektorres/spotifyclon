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
        """
            Verifica si la cuenta de correo electrónico ya se encuentra registrada.

            Parameters:
                email (str): Correo electrónico a validar.

            Returns:
                bool: True si el correo ya se encunetra registrado; de lo contrario, False.
        """
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
        """
            Guarda un registro de usuario en la base de datos

            Parameters:
                nombre (str): Nombre del usuario.
                email (str): Correo electrónico del usuario.
                password (str): Contraseña del usuario en texto plano.
                pais (str): País del usuario.

            Returns:
                bool: True si la cuenta se guardó correctamente; de lo contrario, False.
        """
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
        

