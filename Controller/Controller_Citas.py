from Model.Cita import Cita
from Model.Calendar_API import GoogleCalendarManager
from datetime import datetime, timedelta


def Agendar_Cita(Nombre_Evento, Usuario_Invitado, Fecha, Hora):
    print("Controller Agendar Cita")
    print (Nombre_Evento)
    print (Usuario_Invitado)

    # Convertir a formato datetime
    fecha_dt = datetime.strptime(str(Fecha), "%Y-%m-%d %H:%M:%S")

    # Obtener solo año, mes y día
    resultado = fecha_dt.strftime("%Y-%m-%d")


    Fecha_Cita = resultado + " " + str(Hora)
    print (Fecha_Cita)
    # Convertir a formato datetime
    fecha_dt = datetime.strptime(Fecha_Cita, "%Y-%m-%d %H:%M:%S")
    resultado = fecha_dt.strftime("%Y-%m-%dT%H:%M:%S%z")
    resultado = resultado + "-06:00"
    print(resultado )

    fecha_dt_f = datetime.strptime(Fecha_Cita, "%Y-%m-%d %H:%M:%S")
    
    nueva_fecha = fecha_dt_f + timedelta(hours=1)
    resultado_f = nueva_fecha.strftime("%Y-%m-%dT%H:%M:%S%z")
    resultado_f = resultado_f + "-06:00"
    print(resultado_f )
    User = []
    User.append(Usuario_Invitado)
    Calendar = GoogleCalendarManager()
    Calendar.create_event(Nombre_Evento, resultado, resultado_f, "America/Mexico_City", User)
    return True

def Modificar_Cita(ID_Evento, Nombre_Evento, Fecha, Hora):
    print("Controller Modificar Cita")
    print (ID_Evento)
    print (Nombre_Evento)
    print (Fecha)
    print (Hora)

    # Convertir a formato datetime
    fecha_dt = datetime.strptime(str(Fecha), "%Y-%m-%d %H:%M:%S")

    # Obtener solo año, mes y día
    resultado = fecha_dt.strftime("%Y-%m-%d")


    Fecha_Cita = resultado + " " + str(Hora)
    print (Fecha_Cita)
    # Convertir a formato datetime
    fecha_dt = datetime.strptime(Fecha_Cita, "%Y-%m-%d %H:%M:%S")
    resultado = fecha_dt.strftime("%Y-%m-%dT%H:%M:%S%z")
    resultado = resultado + "-06:00"
    print(resultado )

    fecha_dt_f = datetime.strptime(Fecha_Cita, "%Y-%m-%d %H:%M:%S")
    
    nueva_fecha = fecha_dt_f + timedelta(hours=1)
    resultado_f = nueva_fecha.strftime("%Y-%m-%dT%H:%M:%S%z")
    resultado_f = resultado_f + "-06:00"
    print(resultado_f )

    Calendar = GoogleCalendarManager()
    Calendar.update_event(ID_Evento ,Nombre_Evento, resultado, resultado_f)

    return True
    