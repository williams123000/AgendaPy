# Autor: Williams Chan Pescador

from datetime import datetime, timedelta
from Model.Appointment import Appointment
from Services.Adapters.Adapter_Vehicle import Extract_Vehicles_6M_BD, Extract_Auto_BD
from Services.Adapters.Adapter_Appointment import Extract_Appointments_API
import logging

def Extract_Appointments():
    """
    Extrae las citas del calendario de Google.

    Retorna:
        list: Lista de eventos próximos del calendario.
    """
    logging.info("Extraer citas del calendario de Google")
    return Extract_Appointments_API()

def Delete_Appointment(ID_Evento):
    """
    Elimina una cita del calendario de Google y de la base de datos.

    Parámetros:
    - ID_Evento: El ID del evento de la cita a eliminar.

    Retorna:
    - True si la cita fue eliminada correctamente.
    """
    Appointment_ =  Appointment()
    Appointment_.Event_Google = ID_Evento
    Appointment_.Delete()
    logging.info("Eliminar la cita del evento en API Google Calendar y de la BD de MySQL con el ID_Evento" + str(ID_Evento) )
    return True

def Create_Appointment(ID_Vehicle, Usuario_Invitado, Fecha, Hora):
    """
    Crea una cita para un vehículo en el calendario de Google.

    Parámetros:
    - ID_Vehicle (str): ID del vehículo.
    - Usuario_Invitado (str): Usuario invitado para la cita.
    - Fecha (str): Fecha de la cita en formato "YYYY-MM-DD".
    - Hora (str): Hora de la cita en formato "HH:MM:SS".

    Retorna:
    - bool: True si la cita se creó correctamente.

    """

    # Obtener el precio del vehiculo por el ID del vehiculo en la base de datos
    Vehicle = Extract_Auto_BD(ID_Vehicle)

    # Obtener el precio del vehiculo
    Price_Vehicle = Vehicle[0][10]

    # Obtener el precio del servicio que es el 5% del precio del vehiculo
    Price_Service = float(Price_Vehicle) * 0.005

    # Generar el nombre del evento
    Nombre_Evento = str(Vehicle[0][1]) + " - Service"

    # Generar la descripcion del evento
    Description ="""
<div>
    <h2>Detalles de la Cita</h2>
    <strong>Nombre del Cliente:</strong> {nombre_cliente}<br />
    <strong>Número Telefónico:</strong> {numero_telefonico}<br />
    <strong>Marca del Vehículo:</strong> {marca_vehiculo}<br />
    <strong>Modelo del Vehículo:</strong> {modelo_vehiculo}<br />
    <strong>Año del Vehículo:</strong> {ano_vehiculo}<br />
    <strong>Color del Vehículo:</strong> {color_vehiculo}<br />
    <strong>Costo del Vehículo:</strong> ${costo_vehiculo}<br />
    <strong>Costo del Servicio:</strong> ${costo_servicio}<br />
</div>""".format(
        nombre_cliente = str(Vehicle[0][1]).replace("\n", ""),
        numero_telefonico = str(Vehicle[0][2]).replace("\n", ""),
        marca_vehiculo = str(Vehicle[0][3]).replace("\n", ""),
        modelo_vehiculo = str(Vehicle[0][4]).replace("\n", ""),
        ano_vehiculo = str(Vehicle[0][5]).replace("\n", ""),
        color_vehiculo = str(Vehicle[0][6]).replace("\n", ""),
        costo_vehiculo = str(Vehicle[0][10]).replace("\n", ""),
        costo_servicio = str(Price_Service).replace("\n", "")
    )


    # Convertir a formato datetime
    fecha_dt = datetime.strptime(str(Fecha), "%Y-%m-%d %H:%M:%S")

    # Obtener solo año, mes y día
    resultado = fecha_dt.strftime("%Y-%m-%d")

    Fecha_Cita = resultado + " " + str(Hora)

    # Convertir a formato datetime
    fecha_dt = datetime.strptime(Fecha_Cita, "%Y-%m-%d %H:%M:%S")
    resultado = fecha_dt.strftime("%Y-%m-%dT%H:%M:%S%z")
    resultado = resultado + "-06:00"

    fecha_dt_f = datetime.strptime(Fecha_Cita, "%Y-%m-%d %H:%M:%S")
    
    nueva_fecha = fecha_dt_f + timedelta(hours=1)
    resultado_f = nueva_fecha.strftime("%Y-%m-%dT%H:%M:%S%z")
    resultado_f = resultado_f + "-06:00"

    User = []
    User.append(Usuario_Invitado)
    



    Appointment_ =  Appointment()
    Appointment_.Date = Fecha
    Appointment_.Time = Hora
    Appointment_.Cost_Service = Price_Service
    Appointment_.ID_Vehicle = ID_Vehicle
    #Appointment_.Event_Google = Event_Google
    Appointment_.Name_Event = Nombre_Evento
    Appointment_.Time_Start = resultado
    Appointment_.Time_End = resultado_f
    Appointment_.User = User
    Appointment_.Description = Description
    Appointment_.Create()
    logging.info("Crear la cita en el evento en API Google Calendar y de la BD de MySQL con el ID_Vehicle" + str(ID_Vehicle) )

    return True

def Modify_Appointment(ID_Evento, Fecha, Hora):
    """
    Modifica una cita en el calendario y en la base de datos.

    Parámetros:
    - ID_Evento: ID del evento a modificar.
    - Fecha: Fecha de la cita en formato "YYYY-MM-DD".
    - Hora: Hora de la cita en formato "HH:MM:SS".

    Retorna:
    - True si la modificación fue exitosa.

    """

    # Convertir a formato datetime
    fecha_dt = datetime.strptime(str(Fecha), "%Y-%m-%d %H:%M:%S")

    # Obtener solo año, mes y día
    resultado = fecha_dt.strftime("%Y-%m-%d")

    Fecha_Cita = resultado + " " + str(Hora)

    # Convertir a formato datetime
    fecha_dt = datetime.strptime(Fecha_Cita, "%Y-%m-%d %H:%M:%S")
    resultado = fecha_dt.strftime("%Y-%m-%dT%H:%M:%S%z")
    resultado = resultado + "-06:00"

    fecha_dt_f = datetime.strptime(Fecha_Cita, "%Y-%m-%d %H:%M:%S")
    
    nueva_fecha = fecha_dt_f + timedelta(hours=1)
    resultado_f = nueva_fecha.strftime("%Y-%m-%dT%H:%M:%S%z")
    resultado_f = resultado_f + "-06:00"

    Appointment_ =  Appointment()
    Appointment_.Date = Fecha
    Appointment_.Time = Hora
    Appointment_.Event_Google = ID_Evento
    Appointment_.ID = ID_Evento
    Appointment_.Time_Start = resultado
    Appointment_.Time_End = resultado_f
    Appointment_.Update()
    logging.info("Modificar la cita en el evento en API Google Calendar y de la BD de MySQL con el ID_Evento" + str(ID_Evento) )

    return True

def Extract_Vehicles():
    """
    Extrae los vehículos de la base de datos.

    Retorna:
    - list: Lista de vehículos.
    """
    Vehicles = Extract_Vehicles_6M_BD()
    return Vehicles