from Services.Driver_MySQL import Driver_MySQL
import logging

def Extract_Vehicles_6M_BD():
    """
    Extrae los autos de la base de datos que han sido comprados en los últimos 6 meses y no tienen citas programadas.

    Returns:
        list: Lista de autos que cumplen con los criterios de selección.
            Cada elemento de la lista es una tupla con los datos del auto.
    """
    BD = Driver_MySQL()
    try:
        sql = "SELECT * FROM Vehicles WHERE Date_Purchase BETWEEN DATE_SUB(CURDATE(), INTERVAL 6 MONTH) AND DATE_SUB(DATE_ADD(CURDATE(), INTERVAL 1 WEEK), INTERVAL 6 MONTH) AND ID_Vehicle NOT IN (SELECT ID_Vehicle FROM Citas);"
        mcursor = BD.getBD().cursor()
        mcursor.execute(sql)
        resultado = mcursor.fetchall()
        logging.info("Extrayendo autos de la BD")

        return resultado
    except Exception as e:
        logging.error(f"Error al obtener los autos de la BD: {str(e)}")
        return None
    
def Extract_Auto_BD(ID_Vehicle):
    """
    Extrae la información de un auto de la base de datos según su ID_Vehicle.

    Parámetros:
    - ID_Vehicle: El ID del vehículo a extraer de la base de datos.

    Retorna:
    - resultado: Una lista con la información del auto extraído de la base de datos.
    - None si ocurre un error al obtener el auto de la base de datos.
    """

    BD = Driver_MySQL()
    try:
        sql = f"SELECT * FROM Vehicles WHERE ID_Vehicle = {ID_Vehicle}"
        mcursor = BD.getBD().cursor()
        mcursor.execute(sql)
        resultado = mcursor.fetchall()
        logging.info("Extrayendo auto de la BD")
        return resultado
    except Exception as e:
        logging.error(f"Error al obtener el auto de la BD: {str(e)}")
        return None