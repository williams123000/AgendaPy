from Services.Driver_MySQL import Driver_MySQL
import logging

# Service BD Connection
def User_Verify(Email : str, Password : str):
    """
    Verifica si un usuario existe en la base de datos.

    Parámetros:
    - Login: Objeto de la clase Login que contiene el correo electrónico y la contraseña del usuario.

    Retorna:
    - Los datos del usuario si existe.
    - False si ocurre algún error o el usuario no existe.
    """
    BD = Driver_MySQL()
    try:
        sql = f"SELECT * FROM login WHERE Correo = '{Email}' AND Password = '{Password}'"
        mcursor = BD.getBD().cursor()
        mcursor.execute(sql)
        resultado = mcursor.fetchone()
        logging.info("Verificando si el usuario existe")
        if resultado is not None:
            return resultado
        else:
            return False
        
    except Exception as e:
        logging.error(f"Error al verificar usuario existente: {str(e)}")
        return False
    
def Email_Verify(Email : str):
    """
    Verifica si el correo electrónico existe en la base de datos.

    Parámetros:
    - Login: Objeto de la clase Login que contiene la información del correo electrónico a verificar.

    Retorna:
    - True si el correo existe en la base de datos.
    - False si ocurre algún error o el correo no existe en la base de datos.
    """
    BD = Driver_MySQL()
    try:
        sql = f"SELECT * FROM login WHERE Correo = '{Email}'"
        mcursor = BD.getBD().cursor()
        mcursor.execute(sql)
        resultado = mcursor.fetchone()
        logging.info("Verificando si el correo existe")
        if resultado is not None:
            return True
        else:
            return False

    except Exception as e:
        logging.error(f"Error al verificar correo existente: {str(e)}")
        return False
    
def Password_Verify( Email : str , Password : str ):
    """
    Verifica si la contraseña y el correo electrónico proporcionados coinciden en la base de datos.

    Args:
        Login (Login): Objeto Login que contiene la contraseña y el correo electrónico.

    Returns:
        bool: True si la contraseña y el correo electrónico coinciden en la base de datos, False de lo contrario.
    """
    BD = Driver_MySQL()
    try:
        sql = f"SELECT * FROM login WHERE Password = '{Password}' AND Correo = '{Email}'"
        mcursor = BD.getBD().cursor()
        mcursor.execute(sql)
        resultado = mcursor.fetchone()
        logging.info("Verificando si la contraseña existe")
        if resultado is not None:
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"Error al verificar contraseña existente: {str(e)}")
        return False
    
def Update_Password(Password_Update : str, Email : str):
    """
    Método que realiza la actualización de contraseña.
    """
    BD = Driver_MySQL()
    try:
        sql = f"UPDATE login SET Password = '{Password_Update}' WHERE Correo = '{Email}'"
        mcursor = BD.getBD().cursor()
        mcursor.execute(sql)
        BD.getBD().commit()
        logging.info("Actualizando contraseña")
        return True
    except Exception as e:
        logging.error(f"Error al actualizar contraseña: {str(e)}")
        return False
    
def Extract_Role_BD(ID_User : str):
    """
    Método que extrae el turno de un usuario.

    Parámetros:
    - ID_User: ID del usuario.

    Retorna:
    - El turno del usuario si existe.
    - False si ocurre algún error o el usuario no existe.
    """
    BD = Driver_MySQL()
    try:
        sql = f"SELECT * FROM login WHERE Id = '{ID_User}'"
        mcursor = BD.getBD().cursor()
        mcursor.execute(sql)
        resultado = mcursor.fetchone()
        logging.info("Extrayendo turno del usuario")
        if resultado is not None:
            return resultado
        else:
            return False
    except Exception as e:
        logging.error(f"Error al extraer turno del usuario: {str(e)}")
        return False

def Extract_Info_BD(ID_User : str):
    """
    Método que extrae la información de un usuario.

    Parámetros:
    - ID_User: ID del usuario.

    Retorna:
    - La información del usuario si existe.
    - False si ocurre algún error o el usuario no existe.
    """
    BD = Driver_MySQL()
    try:
        sql = f"SELECT * FROM login WHERE Id = '{ID_User}'"
        mcursor = BD.getBD().cursor()
        mcursor.execute(sql)
        resultado = mcursor.fetchone()
        logging.info("Extrayendo información del usuario")
        if resultado is not None:
            return resultado
        else:
            return False
    except Exception as e:
        logging.error(f"Error al extraer información del usuario: {str(e)}")
        return False