# Autor: Williams Chan Pescador

import flet as ft
from Controller.Controller_Usuario import Login , Recovery, Extraer_ID_Usuario
from cryptography.fernet import Fernet
import datetime
import logging

from Services.Proxy.Proxy_Login import Create_Keys_Session, Access_Schedule

def GUI_Login(page: ft.Page):

    # Configuración de la ventana
    page.window_width = 1100
    page.window_height = 600
    page.window_resizable = False
    page.bgcolor = "#564970"
    page.window_center()
    page.padding = 0
    page.title = "Login - AutoCar"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Configuración de las fuentes
    page.fonts = {
        "Product Sans Regular": "settings/Product Sans Regular.ttf",
        "Product Sans Bold" : "settings/Product Sans Bold.ttf"
    }

    # Configuración de la fuente por defecto
    page.theme = ft.Theme(font_family="Product Sans Regular")

    # Crear los widgets de la ventana
    
    Email = ft.TextField(label="Email", label_style = ft.TextStyle(color="#ffffff"),focused_color = "#ffffff",color="#ffffff", border_color="#ffffff", cursor_color="#ffffff", selection_color="#ffffff")
    Password = ft.TextField(label="Contraseña", label_style = ft.TextStyle(color="#ffffff"),focused_color = "#ffffff",color="#ffffff", border_color="#ffffff", cursor_color="#ffffff", selection_color="#ffffff", password=True, can_reveal_password=True)
    
    # Función para iniciar sesión
    def Login_Event(e):
        logging.info("Inicia el evento de inicio de sesion.")

        if Email.value == "" or Password.value == "":
            logging.error("Datos no ingresados.")

            dlg = ft.AlertDialog( title=ft.Text("Datos no ingresados", text_align="CENTER"), content= ft.Text("Por favor ingresa tus datos.", text_align="CENTER"))
            page.dialog = dlg
            dlg.open = True
            page.update()
            return
        
        if Login(Email.value, Password.value):
            logging.info("Usuario registrado.")

            ID_Usuario = Extraer_ID_Usuario(Email.value)
            page.session.set("ID_Usuario", ID_Usuario)

            
            logging.info("Se ha obtenido el ID del usuario: " + str(ID_Usuario))

            if Access_Schedule(ID_Usuario):

                page.remove(Window)
                logging.info("Se ha eliminado la ventana de inicio de sesion.")

                page.data = True
                logging.info("Se ha actualizado la pagina. Se envio los datos para su validacion de carga.")

                Create_Keys_Session(ID_Usuario)
                
                logging.info("Se cargo la vista principal de la aplicacion. ID_Usuario: " + str(ID_Usuario))
                from View.GUI_Home import GUI_Home
                GUI_Home(page)

            else:
                Not_Access_Dialog = ft.AlertDialog(
                    title=ft.Text("Estas fuera de tu horario de trabajo", text_align="CENTER"),
                )
                page.dialog = Not_Access_Dialog
                Not_Access_Dialog.open = True
                page.update()
                logging.info("No tiene acceso por el horario ID_Usuario: " + str(ID_Usuario) + ".")

        else:
            logging.error("Usuario no registrado.")
            dlg = ft.AlertDialog( title=ft.Text("Usuario no registrado", text_align="CENTER"), content= ft.Text("Por favor valida tus datos de acceso.", text_align="CENTER"))
            page.dialog = dlg
            dlg.open = True
            page.update()

        page.update()

    # Botón para iniciar sesión
    Login_Button = ft.ElevatedButton("Iniciar Sesión", icon="login", on_click=Login_Event,
        style=ft.ButtonStyle(
            color={
                ft.MaterialState.HOVERED: '#2B1330',
                ft.MaterialState.FOCUSED: '#2B1330',
                ft.MaterialState.DEFAULT: '#2B1330'
            }, 
            bgcolor={ft.MaterialState.FOCUSED: '#2B1330'},
            overlay_color={
                ft.MaterialState.HOVERED: '#C1A1C9',
                ft.MaterialState.PRESSED: '#5B3C63',
            },
        )
    )

    # Función para abrir el diálogo modal de recuperación de contraseña
    def RecoveryPassword_Event_Modal_Open(e):
        page.dialog = RecoveryPassword_Modal
        RecoveryPassword_Modal.open = True
        page.update()
    
    # Función para cerrar el diálogo modal de recuperación de contraseña
    def RecoveryPassword_Event_Modal_Close(e):
        RecoveryPassword_Modal.open = False
        page.update()

    # Crear los widgets del diálogo modal
    Email_Recovery = ft.TextField(label="Email para recuperar contraseña", label_style = ft.TextStyle(color="#000000"),focused_color = "#000000",color="#000000", border_color="#000000", cursor_color="#000000", selection_color="#000000")
    
    # Crear la columna de los widgets: Email_Recovery
    RecoveryPassword_Widgets = ft.Column(
        controls=[
            ft.Text("Introduce tu correo para restablecer la contraseña:"),
            Email_Recovery,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment = ft.CrossAxisAlignment.START,
        height=100,
        spacing=20
    )

    # Función para recuperar la contraseña
    def RecoveryPassword_Event(e):
        logging.info("Inicia el evento de recuperacion de contraseña.")

        if Email_Recovery.value == "":
            logging.error("Datos no ingresados.")
            dlg = ft.AlertDialog( title=ft.Text("Datos no ingresados", text_align="CENTER"), content= ft.Text("Por favor ingresa tu Email.", text_align="CENTER"))
            page.dialog = dlg
            dlg.open = True
            page.update()
            return
        
        if Recovery(Email_Recovery.value):
            logging.info("Correo enviado al usuario. Emal: " + Email_Recovery.value + ".")

            dlg = ft.AlertDialog( title=ft.Text("Correo enviado", text_align="CENTER"), content= ft.Text("Se ha enviado un correo para restablecer tu contraseña.", text_align="CENTER"))
            page.dialog = dlg
            dlg.open = True
            page.update()

        else:
            logging.error("Correo no enviado. No existe el correo: " + Email_Recovery.value + ".")
            dlg = ft.AlertDialog( title=ft.Text("Correo no enviado", text_align="CENTER"), content= ft.Text("El correo ingresado no existe.", text_align="CENTER"))
            page.dialog = dlg
            dlg.open = True
            page.update()

    # Diálogo modal
    RecoveryPassword_Modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Recuperación de contraseña"),
        content=RecoveryPassword_Widgets,
        actions=[
            ft.TextButton("Confirmar", on_click=RecoveryPassword_Event),
            ft.TextButton("Cancelar", on_click=RecoveryPassword_Event_Modal_Close),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Botón para recuperar la contraseña
    RecoveryPassword_Button = ft.TextButton("¿Olvidaste tu contraseña?", on_click=RecoveryPassword_Event_Modal_Open,
        style=ft.ButtonStyle(
            color={
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.FOCUSED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.WHITE
            }, 
            bgcolor={ft.MaterialState.FOCUSED: '#2B1330'},
            overlay_color={
                ft.MaterialState.HOVERED: ft.colors.TRANSPARENT,
                ft.MaterialState.PRESSED: ft.colors.TRANSPARENT,
            },
        )
    )

    # Crear la columna de los widgets: Login_Button y Recovery_Password
    Buttons = ft.Row(
        controls=[
            ft.Column(
                controls = [
                    Login_Button, 
                    RecoveryPassword_Button
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment = ft.CrossAxisAlignment.CENTER
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Crear la columna de los widgets: Text, Email, Password, Buttons
    Widgets = ft.Column(
        controls=[
            ft.Text("Iniciar sesión", size=30, color="#ffffff"),
            Email,
            Password,
            Buttons
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
        spacing=40
    )

    # Crear el contenedor
    Container = ft.Container(
        content=Widgets,
        blur=ft.Blur(300, 300, ft.BlurTileMode.REPEATED),
        padding=40,
        alignment=ft.alignment.center,
        width=400,
        height=450,
        border_radius=50,
    )

    # Crear el contenedor principal
    Window = ft.Container(
        content=Container,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=['#2A1330', '#8B8BBF'],
        ),
        alignment=ft.alignment.center,
        width=1100,
        height=570,
    )

    # Agregar la página principal a la ventana
    page.add(
        Window
    )

    logging.info("Finaliza la carga de la vista de inicio de sesion.")