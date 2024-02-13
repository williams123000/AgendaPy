# Autor: Williams Chan Pescador

from Model.Login import Login
from Services.Proxy.Proxy_Login import  Proxy_Login, Create_Keys_Session, Access_Schedule , Exit_App
import logging

def Controller_Event_Login(Email : str, Password : str):
    """
    Método que realiza la validación de inicio de sesión.

    Parámetros:
    - Email: Correo electrónico del usuario.
    - Password: Contraseña del usuario.

    Retorna:
    - True si el inicio de sesión es exitoso.
    - False si el inicio de sesión falla.
    """
    
    # Model Connection
    # Se crea un objeto de la clase Login

    User = Login()
    User.Email = Email
    User.Password = Password

    if User.Login():
        # Si la validación es exitosa, se asigna el ID de usuario global y se redirige a la vista principal de la aplicación.
        return True, User.ID
    # Se realiza la validación de inicio de sesión
    else:
        return False, None
    
def Controller_Access_Schedule(ID_Usuario : int):
    """
    Método que realiza la validación de inicio de sesión.

    Parámetros:
    - ID_Usuario: ID del usuario.

    Retorna:
    - True si la clave de sesión es válida.
    - False si la clave de sesión es inválida.
    """
    # Proxy Login Connection
    # Se utiliza Proxy_Login para autenticar el inicio de sesión.

    if Access_Schedule(ID_Usuario):
        # Si la validación es exitosa, se asigna el ID de usuario global y se redirige a la vista principal de la aplicación.
        Create_Keys_Session(ID_Usuario)
        return True
    else:
        return False  
    
def Controller_Event_Recovery_Password(Email : str):
    """
    Método que realiza la recuperación de contraseña.

    Parámetros:
    - Email: Correo electrónico del usuario.

    Retorna:
    - True si el correo electrónico existe en la base de datos.
    - False si el correo electrónico no existe en la base de datos.
    """
    
    # Model Connection
    # Se crea un objeto de la clase Login
    User = Login()
    User.Email = Email

    # Se realiza la recuperación de contraseña
    return User.Recovery_Password()

def Controller_Event_Logout():

    """
    Método que realiza la salida de la aplicación.

    Parámetros:
    - Ninguno.

    Retorna:
    - Ninguno.
    """
    # Proxy Login Connection
    # Se utiliza Proxy_Login para autenticar el inicio de sesión.
    Exit_App()
    return None

def Controller_Verify_Proxy_Login():
    """
    Método que realiza la validación de inicio de sesión.

    Parámetros:
    - ID_Usuario: ID del usuario.

    Retorna:
    - True si la clave de sesión es válida.
    - False si la clave de sesión es inválida.
    """
    # Proxy Login Connection
    # Se utiliza Proxy_Login para autenticar el inicio de sesión.
    Validate, ID_Usuario = Proxy_Login()
    if Validate:
        
        logging.info(f"El usuario con ID {ID_Usuario} ha iniciado sesion anteriormente.")
        # Si la validación es exitosa, se asigna el ID de usuario global y se redirige a la vista principal de la aplicación.
        return ID_Usuario
    else:
        return None
    
def Update_Keys_Session(ID_Usuario : str):
    """
    Método que realiza la actualización de las claves de sesión.

    Parámetros:
    - ID_Usuario: ID del usuario.

    Retorna:
    - Ninguno.
    """
    # Proxy Login Connection
    # Se utiliza Proxy_Login para autenticar el inicio de sesión.
    Create_Keys_Session(ID_Usuario)
    return None