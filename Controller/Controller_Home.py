# Autor: Williams Chan Pescador

from Model.User import User
from Model.Login import Login

def Controller_Create_User(ID_User):
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
    Login_.Extract_Role()

    # Se realiza la creación de un usuario
    return User_.Name, User_.Last_Name, Login_.Role, User_.URL_Photo