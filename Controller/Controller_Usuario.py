# Autor: Williams Chan Pescador

from Model.Usuario import Usuario , Update_URL_Photo_BD, Update_Password_BD, Validate_Password
import cloudinary
import cloudinary.api
import cloudinary.uploader
from dotenv import load_dotenv
import os
import logging

dontenv_path = os.path.join(os.path.dirname(__file__),'../settings', '.env')
load_dotenv(dontenv_path)

def Login(Email : str, Password : str):
    User_Current = Usuario()
    User_Current.correo = Email
    User_Current.password = Password
    if User_Current.Usuario_Existe():
        logging.info("Usuario existe")
        return True
    else:
        logging.info("Usuario no existe")
        return False
    
def Recovery(Email : str):
    User_Current = Usuario()
    User_Current.correo = Email
    if User_Current.Usuario_Existe_Correo():
        logging.info("Usuario existe")
        if User_Current.Recovery_Password():
            logging.info("Correo enviado")
            return True
        else:
            logging.info("Correo no enviado")
            return False
    else:
        logging.info("Usuario no existe")
        return False
    
def Extraer_ID_Usuario(Email : str):
    User_Current = Usuario()
    User_Current.correo = Email
    logging.info("Extrayendo ID de usuario")
    return User_Current.Obtener_ID()

def Update_Photo(Path_Photo : str, ID_User : str):
    
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True,
    )

    result = cloudinary.uploader.upload(
        Path_Photo,
        folder="AgendaPy",
        resource_type="image")
            
    result = Update_URL_Photo_BD(result['url'], ID_User)
    logging.info("Actualizando URL de la foto")

    return True

def Update_Password(Password_Current : str, Password_Update : str, ID_User : str):
    if Validate_Password(ID_User, Password_Current):
        logging.info("Contraseña actual correcta")
        Update_Password_BD(Password_Update, ID_User)
        logging.info("Contraseña actualizada")
        return True
    else:
        return False
