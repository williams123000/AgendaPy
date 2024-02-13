# Autor: Williams Chan Pescador

from Model.User import User
from Model.Login import Login
from Services.Adapters.Adapter_MiPerfil import Update_URL_Photo_BD
from Services.Cloudinary_API import Upload_Photo_CloudinaryAPI
import logging

def Controller_Info_User(ID_User):
    """
    Método que realiza la creación de un usuario.

    Parámetros:
    - ID_User: ID del usuario.

    Retorna:
    - True si el usuario se creó correctamente.
    - False si el usuario no se creó correctamente.
    """
    # Model Connection
    # Se crea un objeto de la clase User
    User_ = User()
    User_.ID = ID_User
    User_.Read_Data()

    Login_ = Login()
    Login_.ID = ID_User
    Login_.Extract_Info()

    # Se realiza la creación de un usuario
    return User_.Name, User_.Last_Name, User_.URL_Photo, User_.Phone, User_.Address, Login_.Role, Login_.Email

def Controller_Update_Password(Email, Password):
    """
    Método que realiza la actualización de contraseña.

    Parámetros:
    - Email: Correo del usuario.
    - Password: Contraseña del usuario.

    Retorna:
    - True si la contraseña se actualizó correctamente.
    - False si la contraseña no se actualizó correctamente.
    """
    # Model Connection
    # Se crea un objeto de la clase Login
    Login_ = Login()
    Login_.Email = Email
    Login_.Password = Password

    # Se realiza la actualización de contraseña
    return Login_.Update_Password()

def Controller_Update_Photo(Path_Photo, ID_User):
    """
    Método que realiza la actualización de la foto de perfil.

    Parámetros:
    - ID_User: ID del usuario.
    - URL_Photo: URL de la foto de perfil.

    Retorna:
    - True si la foto de perfil se actualizó correctamente.
    - False si la foto de perfil no se actualizó correctamente.
    """
    # Model Connection
    # Se crea un objeto de la clase User
    URL = Upload_Photo_CloudinaryAPI(Path_Photo)
    
            
    result = Update_URL_Photo_BD(URL, ID_User)
    logging.info("Actualizando URL de la foto")

    return True

def Update_Password(Password_Current : str, Password_Update : str, Email : str):
    Login_ = Login()
    Login_.Email = Email
    Login_.Password = Password_Current
    if Login_.Verify_Password_Current():
        logging.info("Contraseña actual correcta")
        Login_.Password = Password_Update
        if Login_.Modify_Password():
            logging.info("Contraseña actualizada")
            return True
        else:
            return False
