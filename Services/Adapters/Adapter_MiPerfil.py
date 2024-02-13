from Services.Driver_MySQL import Driver_MySQL
import logging

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