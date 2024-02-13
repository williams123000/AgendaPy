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