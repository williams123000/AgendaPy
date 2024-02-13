# Autor: Williams Chan Pescador

import flet as ft
import datetime
import logging

from Controller.Controller_Citas import Modify_Appointment , Extract_Appointments , Delete_Appointment
from Controller.Controller_Login import Controller_Verify_Proxy_Login, Controller_Access_Schedule, Controller_Event_Logout
from Controller.Controller_Home import Controller_Create_User


def GUI_Home(page: ft.Page):
    logging.info("Se ha creado una instancia de la clase GoogleCalendarManager.")

    # Se valida si el usuario ya ha iniciado sesión con el proxy.
    ID_User = Controller_Verify_Proxy_Login()

    if ID_User != None:
        # Si el inicio de sesión es exitoso, se guarda el ID del usuario en la sesión de la página.
        if not Controller_Access_Schedule(ID_User):
            page.remove(Window)
            from View.GUI_Login import GUI_Login
            GUI_Login(page)

        # Se guarda el ID del usuario en la sesión de la página.
        page.session.set("ID_Usuario", ID_User)
        page.data = True


    # Extraer datos del usuario para la página
    Name_User, Last_Name_User, Role_User , URL_Photo_User = Controller_Create_User(page.session.get("ID_Usuario"))    

    # Configuración de la ventana
    page.window_width = 1100
    page.window_height = 600
    page.window_resizable = False
    page.window_center()
    page.padding = 0
    page.bgcolor = "#564970"
    page.title = "Home - AutoCar"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Se definen las fuentes que se utilizarán en la página.
    page.fonts = {
        "Product Sans Regular": "settings/Product Sans Regular.ttf",
        "Product Sans Bold" : "settings/Product Sans Bold.ttf"
    }

    # Se definen los estilos que se utilizarán en la página.
    page.theme = ft.Theme(font_family="Product Sans Regular")

    # Se crea un widget ProgressRing y un Text para mostrar un mensaje de carga en lo que se obtienen los datos.
    Wait_Text = ft.Text("Cargando", size=30, color="#ffffff")
    Wait_Widget = ft.ProgressRing(color="#ffffff")

    # Se agregan los widgets al contenedor de la página. Mientras se obtienen los datos, se mostrará el mensaje de carga.
    if page.data == True:
        logging.info("Se esta cargando los datos de la API Google Calendar.")
        page.add(
            Wait_Widget,
            Wait_Text
        )

    # Se crea un evento para reagendar la cita
    def Reschudele_Appointment_Event(e):

        # Se obtiene el ID del evento que se desea reagendar. 
        ID_Event = e.control.data
        logging.info(f"Se ha seleccionado el evento con ID {ID_Event} para reagendar.")

        # Se crea el evento para abrir el modal de reagendar cita.
        def Reschudele_Appointment_Modal_Open(e):
            page.dialog = Reschudele_Appointment_Modal
            Reschudele_Appointment_Modal.open = True
            page.update()

        # Se crea el evento para cerrar el modal de reagendar cita.
        def Reschudele_Appointment_Modal_Close(e):
            Reschudele_Appointment_Modal.open = False
            page.update()

        # Se crea el evento para confirmar la reagendación de la cita.
        def Reschudele_Appointment_Confirm(e):
            # Se modifica la cita con los datos ingresados llam
            Modify_Appointment(ID_Event, Date.value, Time.value)

            logging.info(f"Se ha confirmado la reagendacion de la cita con ID {ID_Event}. - ID_Usuario: {ID_User} - ")

            Reschudele_Appointment_Modal.open = False
            page.remove(Window)
            GUI_Home(page)

        # Se crean los widgets que se mostrarán en el modal de reagendar cita.

        # Se crea un campo de fecha para seleccionar la fecha de la cita.
        Date = ft.DatePicker(
            first_date=datetime.datetime(2023, 10, 1),
            last_date=datetime.datetime(2024, 10, 1),
        )

        page.overlay.append(Date)

        # Se crea un campo de tiempo para seleccionar la hora de la cita.
        Time = ft.TimePicker(
            confirm_text="Confirm",
            error_invalid_text="Time out of range",
            help_text="Pick your time slot",
        )

        page.overlay.append(Time)

        Date_Button = ft.ElevatedButton(
            "Fecha de la cita",
            icon=ft.icons.DATE_RANGE,
            on_click=lambda _: Date.pick_date(),
        )
        
        Time_Button = ft.ElevatedButton(
            "Hora de la cita",
            icon=ft.icons.ACCESS_TIME,
            on_click=lambda _: Time.pick_time(),
        )

        Reschudele_Appointment_Widgets = ft.Column(
            controls=[
                ft.Text("Datos ingresados para reagendar la cita: "), 
                Time_Button, 
                Date_Button
            ],
            height=150,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        Reschudele_Appointment_Modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Reagendar cita"),
            content= Reschudele_Appointment_Widgets,
            actions=[
                ft.TextButton("Confirmar", on_click=Reschudele_Appointment_Confirm),
                ft.TextButton("Cancelar", on_click=Reschudele_Appointment_Modal_Close),
                ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        Reschudele_Appointment_Modal_Open(e)

    # Se crea un evento para cancelar la cita
    def Cancel_Appointment_Event(e):
        
        if Delete_Appointment(e.control.data):
            logging.info(f"Se ha cancelado la cita con ID {e.control.data} - | ID_Usuario: {ID_User} |")
            page.remove(Window)
            GUI_Home(page)
        

    def NavigationBar_Event(e):
        # Se eligio la opcion de ir a Citas pendientes
        if e.control.selected_index == 0:
            page.drawer.open = False
            page.remove(Window)
            page.data = True
            from View.GUI_MiPerfil import GUI_MiPerfil
            GUI_MiPerfil(page)

        if e.control.selected_index == 1:
            page.drawer.open = False
            page.remove(Window)
            page.data = True
            from View.GUI_Citas import GUI_Citas
            GUI_Citas(page)

        # Se eligio la opcion de cerrar sesion
        if e.control.selected_index == 2:
            page.remove(Window)
            page.drawer.open = False
            Controller_Event_Logout()

            from View.GUI_Login import GUI_Login
            GUI_Login(page)


    page.drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(height=12),
            ft.Column(
                controls=[
                    ft.Stack(
                        [   
                            ft.CircleAvatar(
                                color=ft.colors.BLACK,
                                bgcolor=ft.colors.BLACK,
                                radius=40,
                            ),
                            ft.Container(
                                content=ft.CircleAvatar(
                                foreground_image_url= URL_Photo_User,
                                radius=38,
                                
                            )
                                ,
                                alignment=ft.alignment.center,
                            )
                            ,
                            ft.Container(
                                content=ft.CircleAvatar(bgcolor=ft.colors.GREEN, radius=10),
                                alignment=ft.alignment.bottom_left,

                                width=80,
                                height=70,
                            ),
                        ],
                        width=80,
                        height=80,
                    ),
                    ft.Text(Name_User + " " + Last_Name_User, size=15, color=ft.colors.BLACK, font_family="Product Sans Bold"),
                    ft.Text(Role_User, size=13, color=ft.colors.BLACK, font_family="Product Sans Bold"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.PERSON),
                label="Mi Perfil",
                selected_icon=ft.icons.PERSON,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.DIRECTIONS_CAR),
                label="Clientes pendientes",
                selected_icon=ft.icons.DIRECTIONS_CAR,
                
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.LOGOUT),
                label="Cerrar sesión",
                selected_icon=ft.icons.LOGOUT,
            ),
        ],
        on_change=NavigationBar_Event,
        selected_index=-1,
    )

    def NavigationBar_Open(e):
        page.drawer.open = True
        page.drawer.update()

    Header = ft.Row(
        controls=[
            ft.IconButton(icon=ft.icons.MENU, icon_color= ft.colors.WHITE,on_click=NavigationBar_Open),
            ft.Text("Citas agendadas", size=30, color="#ffffff")
        ],
        alignment=ft.MainAxisAlignment.START 
    )

    List_Events = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        scroll="HIDDEN",
        width=900,
        height=350,
        wrap=True,
        spacing=10,
        run_spacing=10
    )

    Events = Extract_Appointments()
    
    if page.data == True:
        page.remove(Wait_Widget)
        page.remove(Wait_Text)
        page.data = False

    # Se recorren los eventos y se crean los widgets correspondientes.
    for Event, Values in Events.items():
        # Se crea un contenedor que contendrá los datos del evento.
        Event_Card = ft.Container(
            bgcolor=ft.colors.WHITE,
            padding= ft.padding.only(left=30, top=20, right=20, bottom=20),
            border_radius=30,
            width=400,
            height=120
        )

        # Se crea una columna que contendrá los datos del evento.
        Event_Column = ft.Column(spacing=5)
        
        # Se recorren los valores del evento y se crean los widgets correspondientes.
        for SubKey, SubData in Values.items():
            if SubKey == "Nombre_Evento":
                Event_Column.controls.insert(0, ft.Text(SubData, size=25, color=ft.colors.BLACK))
            else:
                Event_Column.controls.append(ft.Text(SubData, size=10, color=ft.colors.GREY))
        
        # Se crea una fila que contendrá la columna con los datos del evento y un menú emergente.
        Event_Row = ft.Row(
            controls=[
                Event_Column, 
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(icon=ft.icons.EDIT_CALENDAR, text="Reagendar cita", on_click=Reschudele_Appointment_Event, data=Event),
                        ft.PopupMenuItem(),
                        ft.PopupMenuItem(icon=ft.icons.FREE_CANCELLATION, text="Cancelar cita", on_click=Cancel_Appointment_Event, data=Event),
                    ]
                    
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        # Se agrega la fila al contenedor del evento.
        Event_Card.content = Event_Row

        # Se agrega el contenedor del evento a la lista de eventos.
        List_Events.controls.append(Event_Card)

    # Se crea la columna que contendrá los widgets de la página.
    Widgets = ft.Column(
        controls=[Header, ft.Divider(thickness=2, color="#ffffff", height=5),List_Events],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment = ft.CrossAxisAlignment.START,
        spacing=20,
    )

    # Se crea un contenedor principal que contendrá el contenido de la página.
    Container = ft.Container(
        content=Widgets,
        blur=ft.Blur(300, 300, ft.BlurTileMode.REPEATED),
        padding=40,
        alignment=ft.alignment.center,
        width=1000,
        height=500,
        border_radius=50,
    )

    # Se crea un contenedor tipo ventana que contendrá el contenedor principal.
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

    page.add(
        Window,
    )