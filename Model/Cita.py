# Autor: Williams Chan Pescador

"""
Patron de diseño Adapter en la creación, eliminación y modificación de citas en la base de datos.
Este script hace uso del patrón de diseño Adapter para crear, eliminar y modificar citas en la base de datos.
El patrón Adapter permite que dos interfaces incompatibles trabajen juntas. 
En este caso, se utiliza para adaptar la interfaz de la base de datos a la interfaz de la aplicación.

"""
from Model.Driver_MySQL import Driver_MySQL
import logging

def Create_Appointment_BD(Date, Hour, Price_Service, ID_Vehicle, Event_Google):
    """
    Crea una cita en la base de datos.

    Parámetros:
    - Date (str): Fecha de la cita.
    - Hour (str): Hora de la cita.
    - Price_Service (str): Costo del servicio.
    - ID_Vehicle (str): ID del vehículo.
    - Event_Google (str): Evento de Google.

    Retorna:
    - resultado (list): Resultado de la consulta SQL.

    Si ocurre un error al crear la cita en la base de datos, se imprime el mensaje de error y se retorna None.
    """
    BD = Driver_MySQL()
    try:
        sql = "INSERT INTO Citas (Fecha_Cita, Hora_Cita, Costo_Servicio, ID_Vehicle, Event_Google) VALUES ( '" + Date + "' , '" + Hour + "' , '" + Price_Service  + "' , '" + ID_Vehicle + "' , '" + Event_Google + "');" 
        mcursor = BD.getBD().cursor()
        mcursor.execute(sql)
        resultado = mcursor.fetchall()
        logging.info("Creando una cita en la BD")
        return resultado
    except Exception as e:
        logging.error(f"Error al crear una cita en la BD: {str(e)}")
        return None
    
def Delete_Appointment_BD(ID_Evento):
    """
    Elimina una cita de la base de datos.

    Parámetros:
    - ID_Evento: El ID del evento de Google asociado a la cita a eliminar.

    Retorna:
    - resultado: El resultado de la operación de eliminación en la base de datos.
                 None si ocurre un error.
    """
    BD = Driver_MySQL()
    try:
        sql = f"DELETE FROM Citas WHERE Event_Google = '{ID_Evento}'"
        mcursor = BD.getBD().cursor()
        mcursor.execute(sql)
        resultado = mcursor.fetchall()
        logging.info("Eliminando una cita de la BD")
        return resultado
    except Exception as e:
        logging.error(f"Error al eliminar una cita en la BD: {str(e)}")
        return None
    
def Modify_Appointment_BD(ID_Evento, Date, Hour):
    """
    Modifica una cita en la base de datos.

    Parámetros:
    - ID_Evento (str): ID del evento de Google asociado a la cita.
    - Date (str): Fecha de la cita en formato YYYY-MM-DD.
    - Hour (str): Hora de la cita en formato HH:MM.

    Retorna:
    - resultado (list): Lista de resultados de la consulta SQL.

    Si ocurre un error al modificar la cita en la base de datos, se imprime un mensaje de error y se retorna None.
    """

    BD = Driver_MySQL()
    try:
        sql = f"UPDATE Citas SET Fecha_Cita = '{Date}', Hora_Cita = '{Hour}' WHERE Event_Google = '{ID_Evento}'"
        mcursor = BD.getBD().cursor()
        mcursor.execute(sql)
        resultado = mcursor.fetchall()
        logging.info("Modificando una cita en la BD")
        return resultado
    except Exception as e:
        logging.error(f"Error al modificar una cita en la BD: {str(e)}")
        return None