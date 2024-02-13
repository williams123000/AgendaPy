# Autor: Williams Chan Pescador

"""
Patrón Singleton en la creación y gestión de páginas con ft.app

Este script ilustra el uso del patrón Singleton al crear una sola página con ft.app y actualizarla, alterarla o modificarla según las vistas necesarias.
El patrón Singleton asegura que solo haya una instancia de una clase en toda la ejecución del programa. 
En este caso, se utiliza para garantizar que solo haya una instancia de la página en la aplicación, lo que facilita su gestión y actualización.
"""


from Services.Proxy.Proxy_Login import Proxy_Login
import flet as ft
import logging

# Configurar el nivel de registro para el logger de Flet para evitar mensajes innecesarios. Solo se muestran los mensajes de advertencia y error.
logging.getLogger('flet_runtime').setLevel(logging.WARNING)
logging.getLogger('flet_core').setLevel(logging.WARNING)

# Se configura el nivel de registro de la aplicación.
logging.basicConfig(filename='settings/Log.log',filemode='w', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == "__main__":

    # Proxy Login Connection
    # Se utiliza Proxy_Login para autenticar el inicio de sesión.
    Validate, ID_User = Proxy_Login()

    if Validate:
        # Si la validación es exitosa, se asigna el ID de usuario global y se redirige a la vista principal de la aplicación.
        logging.info("Inicio de sesion exitoso.")
        # Importar la vista principal de la aplicación y la carga.
        from View.GUI_Home import GUI_Home
        logging.info("Carga de la vista principal de la aplicacion.")
        ft.app(target=GUI_Home, assets_dir="assets")
    else:
        logging.error("Inicio de sesion fallido.")
        # Si la validación falla, se muestra la vista de inicio de sesión para que el usuario vuelva a intentarlo.
        logging.info("Carga de la vista de inicio de sesion.")
        from View.GUI_Login import GUI_Login 
        ft.app(target=GUI_Login, assets_dir="assets")