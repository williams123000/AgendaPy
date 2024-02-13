from Services.Adapters.Adapter_Login import User_Verify, Email_Verify, Password_Verify, Update_Password, Extract_Role_BD, Extract_Info_BD
import logging
import random
import string
from Services.Service_Email import Send_Email_Recovery

class Login:
    def __init__(self):
        self.ID = None
        self.Email = None
        self.Password = None
        self.Role = None

    # Adapter Connection
    def Login(self):
        """
        Método que realiza la validación de inicio de sesión.
        """
        logging.info("Validando inicio de sesion")
        Response = User_Verify(self.Email, self.Password)
        if Response:
            self.ID = Response[0]
            self.Role = Response[3]
            return True
        else:
            return False
        
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
        Método que realiza la recuperación de contraseña.
        """
        logging.info("Recuperando contraseña")
        if Email_Verify(self.Email):
            Random_Password = self.generate_random_password()
            Send_Email_Recovery(self.Email, Random_Password)
            self.Password = Random_Password
            if Update_Password(self.Password, self.Email):
                return True
            else:
                return False
        else:
            return False
    
    def Update_Password(self):
        """
        Método que realiza la actualización de contraseña.
        """
        logging.info("Actualizando contraseña")
        if Password_Verify(self.Email, self.Password):
            if Update_Password(self.Password, self.Email):
                return True
            else:
                return False
        else:
            return False
        
    def Verify_Password_Current(self):
        """
        Método que verifica la contraseña actual de un usuario.

        Retorna:
        - bool: True si la contraseña es correcta.
                False si la contraseña no es correcta.
        """
        logging.info("Verificando contraseña actual")
        return Password_Verify(self.Email, self.Password)
    
    def Modify_Password(self):
        """
        Método que modifica la contraseña de un usuario.

        Retorna:
        - bool: True si la contraseña se modificó correctamente.
                False si la contraseña no se modificó correctamente.
        """
        logging.info("Modificando contraseña")
        return Update_Password(self.Password, self.Email)


    def Extract_Role(self):
        """
        Método que extrae el turno de un usuario.

        Retorna:
        - str: Rol del usuario.
        """
        Response = Extract_Role_BD(self.ID)
        self.Role = Response[3]
        logging.info("Extrayendo turno")

    def Extract_Info(self):
        """
        Método que extrae la información de un usuario.

        Retorna:
        - str: Rol del usuario.
        """
        Response = Extract_Info_BD(self.ID)
        self.Email = Response[1]
        self.Role = Response[3]
        logging.info("Extrayendo información")
        