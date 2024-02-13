from Services.Driver_MySQL import Driver_MySQL
import logging

def Read_User(ID_User):
    """
    Método que realiza la lectura de datos de un usuario.

    Parámetros:
    - ID_User: ID del usuario.

    Retorna:
    - Los datos del usuario si existe.
    - False si ocurre algún error o el usuario no existe.
    """
    BD = Driver_MySQL()
    try:
        sql = f"SELECT * FROM Usuarios WHERE Id = '{ID_User}'"
        mcursor = BD.getBD().cursor()
        mcursor.execute(sql)
        resultado = mcursor.fetchone()
        logging.info("ADAPTER - Leyendo datos del usuario")
        if resultado is not None:
            return resultado
        else:
            return False
        
    except Exception as e:
        logging.error(f"ADAPTER - Error al leer datos del usuario: {str(e)}")
        return False
    
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