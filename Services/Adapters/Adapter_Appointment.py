"""
Patron de diseño Adapter en la extracción de citas de la base de datos y el uso de la API de Google Calendar.
Este script hace uso del patrón de diseño Adapter para extraer las citas de la base de datos y de la API de Google Calendar.
El patrón Adapter permite que dos interfaces incompatibles trabajen juntas. En este caso, se utiliza para adaptar la interfaz de la base de datos a la interfaz de la aplicación.
"""

from Services.Driver_MySQL import Driver_MySQL
from Services.CalendarGoogle_API import GoogleCalendarManager

import logging

def Extract_Appointments_API():
    """
    Extrae las citas del calendario de Google.

    Retorna:
        list: Lista de eventos próximos del calendario.
    """
    logging.info("Extraer citas del calendario de Google")
    return GoogleCalendarManager().list_upcoming_events()

def Create_Appointment(Date, Hour, Price_Service, ID_Vehicle, Nombre_Evento, resultado, resultado_f, User, Description):
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
    Calendar = GoogleCalendarManager()
    Event_Google = Calendar.create_event(Nombre_Evento, resultado, resultado_f, "America/Mexico_City", User, Description)
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
    GoogleCalendarManager().delete_event(ID_Evento)
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
    
def Update_Appointment(ID_Evento, Date, Hour, resultado, resultado_f):
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
    Calendar = GoogleCalendarManager()
    Calendar.update_event(ID_Evento , resultado, resultado_f)

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