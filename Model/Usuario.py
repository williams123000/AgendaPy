"""
Patron de diseño Adapter en la creación, eliminación y modificación de usuarios en la base de datos.
Este script hace uso del patrón de diseño Adapter para crear, eliminar y modificar usuarios en la base de datos.
El patrón Adapter permite que dos interfaces incompatibles trabajen juntas.
En este caso, se utiliza para adaptar la interfaz de la base de datos a la interfaz de la aplicación.
"""


from Model.Driver_MySQL import Driver_MySQL

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import string
import logging

class Usuario:
    def __init__(self):
        self.correo = ""
        self.password = ""
        self.rol = ""
        logging.info("Creando un usuario")
        
    def Usuario_Existe(self):
            """
            Verifica si un usuario existe en la base de datos.

            Returns:
                bool: True si el usuario existe, False en caso contrario.
            """
            BD = Driver_MySQL()
            try:
                sql = f"SELECT * FROM login WHERE Correo = '{self.correo}' AND Password = '{self.password}'"
                mcursor = BD.getBD().cursor()
                mcursor.execute(sql)
                resultado = mcursor.fetchone()
                logging.info("Verificando si el usuario existe")
                return resultado is not None

            except Exception as e:
                logging.error(f"Error al verificar usuario existente: {str(e)}")
                return False
    
    def Usuario_Existe_Correo(self):
        """
        Verifica si existe un usuario con el correo electrónico especificado.

        Returns:
            bool: True si existe un usuario con el correo electrónico especificado, False de lo contrario.
        """
        BD = Driver_MySQL()
        try:
            sql = f"SELECT * FROM login WHERE Correo = '{self.correo}'"
            mcursor = BD.getBD().cursor()
            mcursor.execute(sql)
            resultado = mcursor.fetchone()
            logging.info("Verificando si el usuario existe")
            return resultado is not None

        except Exception as e:
            logging.error(f"Error al verificar usuario existente: {str(e)}")
            return False

    def Obtener_Rol(self, BD : Driver_MySQL):
            """
            Obtiene el rol del usuario desde la base de datos.

            Parámetros:
            - BD (Driver_MySQL): Objeto que representa la conexión a la base de datos.

            Retorna:
            - str o None: El rol del usuario si se encuentra en la base de datos, None en caso contrario.
            """
            try:
                sql = f"SELECT rol FROM login WHERE Correo = '{self.correo}'"
                mcursor = BD.getBD().cursor()
                mcursor.execute(sql)
                resultado = mcursor.fetchone()
                logging.info("Obteniendo el rol del usuario")
                if resultado:
                    return resultado[0]
                else:
                    return None
            except Exception as e:
                return None
        
    def Insertar_Usuario(self, BD : Driver_MySQL):
            """
            Inserta un nuevo usuario en la base de datos.

            Parámetros:
            - BD (Driver_MySQL): Objeto que representa la conexión a la base de datos.

            Retorna:
            - bool: True si el usuario se insertó correctamente, False en caso contrario.
            """
            
            try:
                if self.Usuario_Existe():
                    return False
                else:
                    sql = f"INSERT INTO login (Correo, Password, rol) VALUES ('{self.correo}','{self.password}','{self.rol}')"
                    mcursor = BD.getBD().cursor()
                    mcursor.execute(sql)
                    BD.getBD().commit()
                    logging.info("Insertando un nuevo usuario en la BD")
                    return True
            except Exception as e:
                BD.getBD().rollback()
                logging.error(f"Error al insertar un nuevo usuario en la BD: {str(e)}")
                return False
        
    def Iniciar_Sesion(self):
            """
            Realiza el inicio de sesión del usuario.

            Returns:
                str: El rol del usuario si el inicio de sesión es exitoso.
            
            Raises:
                Exception: Si ocurre algún error durante el inicio de sesión.
            """
            try:
                if self.Usuario_Existe():
                    self.rol = self.Obtener_Rol()
                    logging.info("Iniciando sesion")
                    return self.rol
                
            except Exception as e:
                logging.error(f"Error al iniciar sesión: {str(e)}")
    
    def Cambiar_Contraseña(self, nueva_contraseña):
            """
            Actualiza la contraseña del usuario en la base de datos.

            Parámetros:
            - nueva_contraseña (str): La nueva contraseña que se desea establecer.

            Retorna:
            - bool: True si la contraseña se actualizó correctamente, False en caso contrario.
            """
            try:
                BD = Driver_MySQL()
                sql = f"UPDATE login SET Password = '{nueva_contraseña}' WHERE Correo = '{self.correo}'"
                mcursor = BD.getBD().cursor()
                mcursor.execute(sql)
                BD.getBD().commit()
                logging.info("Cambiando la contraseña del usuario")
                return True
            except Exception as e:
                BD.getBD().rollback()
                return False

    # Función para generar una contraseña aleatoria
    def generate_random_password(self, length=8):
        """
        Genera una contraseña aleatoria de la longitud especificada.

        Parámetros:
        - length (int): Longitud de la contraseña generada (por defecto es 8).

        Retorna:
        - str: Contraseña aleatoria generada.
        """
        characters = string.ascii_letters + string.digits
        logging.info("Generando una contraseña aleatoria")
        return ''.join(random.choice(characters) for i in range(length))
    
    def Recovery_Password(self):
        """
        Envía un correo electrónico al usuario con una contraseña temporal para recuperar su contraseña.

        Returns:
            bool: True si el correo electrónico se envió correctamente, False en caso contrario.
        """
        
       # Configura los detalles del servidor SMTP de Gmail
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'williamspvp1234@gmail.com'
        smtp_password = 'fjzcdfvaeaejhsfp'

        # Configura el correo
        from_address = 'williamspvp1234@gmail.com'
        to_address = self.correo
        subject = 'Recuperación de contraseña'
        random_password = self.generate_random_password()
        self.Cambiar_Contraseña(random_password)
        body = f"""Estimado usuario,

Hemos recibido una solicitud para restablecer tu contraseña. 
Tu nueva contraseña temporal es: {random_password}

Por favor, inicia sesión con esta contraseña y cámbiala inmediatamente.

Atentamente,
El equipo de soporte"""

        # Crea el objeto del correo
        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = to_address
        msg['Subject'] = subject

        # Adjunta el cuerpo del correo
        msg.attach(MIMEText(body, 'plain'))

        # Inicia una conexión al servidor SMTP de Gmail
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        # Inicia sesión en el servidor SMTP de Gmail
        server.login(smtp_username, smtp_password)

        # Envía el correo
        server.sendmail(from_address, to_address, msg.as_string())

        # Cierra la conexión al servidor SMTP de Gmail
        server.quit() 
        logging.info("Enviando correo de recuperacion de contraseña")

        return True
    
    def Obtener_ID(self):
            """
            Obtiene el ID del usuario basado en su correo electrónico.

            Returns:
                int or None: El ID del usuario si se encuentra en la base de datos, None en caso contrario.
            """
            try:
                BD = Driver_MySQL()
                sql = f"SELECT ID FROM login WHERE Correo = '{self.correo}'"
                mcursor = BD.getBD().cursor()
                mcursor.execute(sql)
                resultado = mcursor.fetchone()
                logging.info("Obteniendo el ID del usuario")
                if resultado:
                    return resultado[0]
                else:
                    return None
            except Exception as e:
                logging.error(f"Error al obtener el ID del usuario: {str(e)}")
                return None

def Extract_Info_User_BD(ID_User):
    """
    Extrae la información de un usuario de la base de datos.

    Parámetros:
    - ID_User: El ID del usuario a consultar en la base de datos.

    Retorna:
    - resultado: Una lista con los datos del usuario obtenidos de la base de datos.
                 Si ocurre un error, retorna None.
    """

    BD = Driver_MySQL()
    try:
        sql = "SELECT * FROM Usuarios WHERE Id = " + str(ID_User)
        mcursor = BD.getBD().cursor()
        mcursor.execute(sql)
        resultado = mcursor.fetchall()
        logging.info("Extrayendo la informacion del usuario de la BD")
        return resultado
    except Exception as e:
        logging.error(f"Error al obtener los usuarios de la BD: {str(e)}")
        return None
    
def Extract_Info_Login_BD(ID_User):
        """
        Extrae la información de inicio de sesión de un usuario desde la base de datos.

        Parámetros:
        - ID_User: El ID del usuario para el cual se desea obtener la información de inicio de sesión.

        Retorna:
        - Una lista de tuplas que contiene la información de inicio de sesión del usuario.
            Cada tupla contiene los campos de la tabla 'login' de la base de datos.

        Si ocurre un error al obtener los usuarios de la base de datos, se imprime un mensaje de error y se retorna None.
        """
        BD = Driver_MySQL()
        try:
                sql = "SELECT * FROM login WHERE Id = " + str(ID_User)
                mcursor = BD.getBD().cursor()
                mcursor.execute(sql)
                resultado = mcursor.fetchall()
                logging.info("Extrayendo la informacion de inicio de sesion del usuario de la BD")
                return resultado
        except Exception as e:
                logging.error(f"Error al obtener los usuarios de la BD: {str(e)}")
                return None
    
def Update_URL_Photo_BD(URL_Photo, ID_User):
    """
    Actualiza la URL de la foto de un usuario en la base de datos.

    Parámetros:
    - URL_Photo (str): La nueva URL de la foto.
    - ID_User (int): El ID del usuario.

    Retorna:
    - resultado (tuple): El resultado de la ejecución de la consulta SQL.
                         None si ocurre un error.

    """
    BD = Driver_MySQL()
    try:
        sql = "UPDATE Usuarios SET URL_Foto = '" + str(URL_Photo) + "' WHERE Id = " + str(ID_User)
        mcursor = BD.getBD().cursor()
        mcursor.execute(sql)
        resultado = mcursor.fetchall()
        logging.info("Actualizando la URL de la foto del usuario")
        return resultado
    except Exception as e:
        logging.error(f"Error al actualizar la URL de la foto en la BD: {str(e)}")
        return None
    
def Validate_Password(ID_User, Password_Current):
    """
    Valida si la contraseña actual proporcionada coincide con la contraseña almacenada en la base de datos para el usuario especificado.

    Parámetros:
    - ID_User (int): El ID del usuario.
    - Password_Current (str): La contraseña actual proporcionada por el usuario.

    Retorna:
    - True si la contraseña actual coincide con la contraseña almacenada en la base de datos.
    - False si la contraseña actual no coincide con la contraseña almacenada en la base de datos.
    - None si ocurre un error al obtener la contraseña de la base de datos.
    """
    
    BD = Driver_MySQL()
    try:
        sql = "SELECT Password FROM login WHERE Id = " + str(ID_User)
        mcursor = BD.getBD().cursor()
        mcursor.execute(sql)
        resultado = mcursor.fetchall()
        logging.info("Validando la contraseña actual del usuario")
        if resultado[0][0] == Password_Current:
            return True
        else:
            return False
    except Exception as e:
        return None
    
def Update_Password_BD(Password, ID_User):
    """
    Actualiza la contraseña de un usuario en la base de datos.

    Args:
        Password (str): La nueva contraseña del usuario.
        ID_User (int): El ID del usuario cuya contraseña se actualizará.

    Returns:
        list: Una lista de tuplas que representan los resultados de la consulta SQL.

    Raises:
        Exception: Si ocurre algún error al actualizar la contraseña en la base de datos.
    """

    BD = Driver_MySQL()
    try:
        sql = "UPDATE login SET Password = '" + str(Password) + "' WHERE Id = " + str(ID_User)
        mcursor = BD.getBD().cursor()
        mcursor.execute(sql)
        resultado = mcursor.fetchall()
        logging.info("Actualizando la contraseña del usuario")
        return resultado
    except Exception as e:
        logging.error(f"Error al actualizar la contraseña en la BD: {str(e)}")
        return None