import datetime
from cryptography.fernet import Fernet

import os
import logging

from Model.Driver_MySQL import Driver_MySQL
from Model.Usuario import Extract_Info_User_BD

"""
Patrón Proxy en la validación de la sesión de las keys

El script hace uso del patrón Proxy para validar la sesión de las keys a través de la función `Proxy_Login`. 
Este patrón se encarga de controlar el acceso a otro objeto, actuando como un intermediario. 
En este contexto, el Proxy valida la sesión antes de permitir el acceso a determinadas funcionalidades de la aplicación.

"""
def Proxy_Login ():
    logging.info("Validando sesion de las Keys por el Proxy")    
    if os.path.getsize("settings/keys.key") == 0:
        # Verificar si el archivo está vacío
        logging.warning("Archivo que almacena las keys de la sesion esta vacio, es necesario iniciar sesion nuevamente")
        return False, None
    else:
        # Leer las keys
        with open('settings/keys.key', 'r') as file:
            data = file.read()

        lineas = data.split('\n')

        # Inicializa las variables para almacenar las keys de la sesión
        Key_ = None
        Session_In = None
        Session_Out = None
        ID_User = None

        for linea in lineas:
            if linea.startswith('KEY='):
                Key_ = linea.replace("KEY=", "")
            elif linea.startswith('SESSION_IN='):
                Session_In = linea.replace("SESSION_IN=", "")
            elif linea.startswith('SESSION_OUT='):
                Session_Out = linea.replace("SESSION_OUT=", "")
            elif linea.startswith('ID_USER='):
                ID_User = linea.replace("ID_USER=", "")

        # Crea la key para desencriptar las keys de la sesión
        Key = Fernet(Key_[2:-1].encode())
        
        # Desencripta las keys de la sesión
        HOUR_IN = Key.decrypt(Session_In[2:-1].encode()).decode()
        HOUR_OUT = Key.decrypt(Session_Out[2:-1].encode()).decode()

        # Obtiene la fecha y hora actual
        date_now_ = datetime.datetime.now()
        date_now : str = date_now_.strftime("%Y-%m-%d %H:%M:%S")
        date_now = datetime.datetime.strptime(date_now, "%Y-%m-%d %H:%M:%S")
        HOUR_OUT = datetime.datetime.strptime(HOUR_OUT, "%Y-%m-%d %H:%M:%S")

        if date_now  < HOUR_OUT:
            # Si la fecha y hora actual es menor a la fecha y hora de salida de la sesión, la sesión es válida
            logging.info("Sesión válida por las Keys del Proxy")
            return True, ID_User
        else:
            # Si la fecha y hora actual es mayor a la fecha y hora de salida de la sesión, la sesión es inválida
            logging.info("Sesion invalida por las Keys del Proxy, es necesario iniciar sesion nuevamente")
            return False, None
 
def Exit_App():
    """
    Esta función se encarga de salir de la aplicación y guardar un archivo vacío llamado 'keys.key' en la carpeta 'settings'.
    """

    # Se cierra la aplicación.
    # Se abre el archivo 'keys.key' en modo escritura y se escribe un string vacío.
    with open('settings/keys.key', 'w') as archivo:
        archivo.write('')

    logging.info("Se vacio el archivo 'keys.key'.")
    logging.info("Se ha cerrado la aplicacion.")

def Create_Keys_Session(ID_Usuario):
    """
    Genera una clave de sesión y guarda la información en un archivo de configuración.

    Parámetros:
    - ID_Usuario: El ID del usuario para el cual se está creando la clave de sesión.

    Retorna:
    Esta función no retorna ningún valor.

    """
    with open('settings/keys.key', 'w') as archivo:
        archivo.write('')

    # Genera una clave de sesión
    key = Fernet.generate_key()

    # Crea un objeto Fernet con la clave generada
    k = Fernet(key)

    # Obtiene la fecha y hora actual
    date_now_ = datetime.datetime.now()
    date_now : str = date_now_.strftime("%Y-%m-%d %H:%M:%S")

    # Obtiene la fecha y hora de salida de la sesión
    date_our_ = datetime.datetime.now()
    date_our = date_our_ + datetime.timedelta(minutes=5)
    date_our : str = date_our.strftime("%Y-%m-%d %H:%M:%S")

    # Encripta la fecha y hora actual y la fecha y hora de salida de la sesión
    date_now = k.encrypt(date_now.encode())

    # Encripta la fecha y hora de salida de la sesión
    date_our = k.encrypt(date_our.encode())
    
    # Guarda la clave de sesión y la información de la sesión en un archivo de configuración
    with open("settings/keys.key", "w") as key_file:
        key_file.write("KEY="+str(key))
        key_file.write("\n")
        key_file.write("SESSION_IN="+str(date_now))
        key_file.write("\n")
        key_file.write("SESSION_OUT="+str(date_our))
        key_file.write("\n")
        key_file.write("ID_USER="+str(ID_Usuario))
        key_file.write("\n")

    logging.info("Se ha actualizado la clave de sesion y se ha guardado la informacion en un archivo de configuracion settings/keys.key.")

def Access_Schedule(ID_Usuario):
    logging.info("Validando el horario de acceso del usuario - ID: " + str(ID_Usuario) + " -")
    Response_BD = Extract_Info_User_BD(ID_Usuario)
    
    Hour_Current = datetime.datetime.now().time()

    Schedule = Response_BD[0][6]

    if Schedule == "Full":
        logging.info("El usuario tiene acceso a cualquier horario")
        return True
    elif Schedule == "Matutino":
        if Hour_Current > datetime.time(8, 0, 0) and Hour_Current < datetime.time(15, 0, 0):
            logging.info("El usuario tiene acceso al horario matutino")
            return True
        else:
            logging.info("El usuario no tiene acceso al horario matutino")
            return False
    elif Schedule == "Vespertino":
        if Hour_Current > datetime.time(15, 0, 0) and Hour_Current < datetime.time(18, 0, 0):
            logging.info("El usuario tiene acceso al horario vespertino")
            return True
        else:
            logging.info("El usuario no tiene acceso al horario vespertino")
            return False
    
        