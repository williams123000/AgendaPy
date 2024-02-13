import flet as ft
import datetime
import logging

from Controller.Controller_Citas import Create_Appointment, Extract_Vehicles
from Controller.Controller_Login import Update_Keys_Session, Controller_Verify_Proxy_Login, Controller_Event_Logout
from Controller.Controller_Home import Controller_Create_User

def GUI_Citas(page: ft.Page):
    # Se valida si el usuario ya ha iniciado sesión con el proxy.
    ID_User = Controller_Verify_Proxy_Login()

    if ID_User != None:
        # Si el inicio de sesión es exitoso, se guarda el ID del usuario en la sesión de la página.
        Update_Keys_Session(ID_User)
        logging.info(f"El usuario con ID {ID_User} ha iniciado sesion anteriormente.")

        # Se guarda el ID del usuario en la sesión de la página.
        page.session.set("ID_Usuario", ID_User)
        page.data = True

    # Se extraen los datos del usuario de la sesión de la página.
    Name_User, Last_Name_User, Role_User , URL_Photo_User = Controller_Create_User(page.session.get("ID_Usuario"))    

    page.window_width = 1100
    page.window_height = 600
    page.window_resizable = False
    page.window_center()

    page.title = "Generacion de Citas (Clientes pendientes) - AutoCar"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.fonts = {
        "Product Sans Regular": "settings/Product Sans Regular.ttf",
        "Product Sans Bold" : "settings/Product Sans Bold.ttf"
    }

    page.theme = ft.Theme(font_family="Product Sans Regular")

    Wait_Text = ft.Text("Cargando", size=30, color="#ffffff")
    Wait = ft.ProgressRing(color="#ffffff")

    if page.data == True:
        page.add(
            Wait,
            Wait_Text
        )
            
    def Create_Appointment_Event(e):
        ID_Vehicle = e.control.data

        def Create_Appointment_Modal_Open(e):
            page.dialog = Create_Appointment_Modal
            Create_Appointment_Modal.open = True
            page.update()

        def Create_Appointment_Modal_Close(e):
            Create_Appointment_Modal.open = False
            page.update()

        def Create_Appointment_Confirm(e):
            logging.info("Creacion de cita confirmada. Se procede a crear la cita en la base de datos. - ID_Vehicle: " + str(ID_Vehicle) + " - ID_User: " + str(page.session.get("ID_Usuario")) + " -")
            if Create_Appointment(ID_Vehicle, User_Invited.value, Date.value, Time.value):
                logging.info("Cita creada exitosamente. ID_Vehicle: " + str(ID_Vehicle) + " - ID_User: " + str(page.session.get("ID_Usuario")) + " -")  
                Create_Appointment_Modal.open = False
                page.remove(Window)
                page.data = True
                GUI_Citas(page)

        User_Invited = ft.TextField(label="Email del cliente")

        Date = ft.DatePicker(
            first_date=datetime.datetime(2023, 10, 1),
            last_date=datetime.datetime(2024, 10, 1),
        )

        page.overlay.append(Date)

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

        Create_Appointment_Widgets = ft.Column(
            controls=[
                ft.Text("Datos ingresados para realizar la cita: "),
                User_Invited, 
                Date_Button, 
                Time_Button
            ],
            height=180,
            width=350,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        Create_Appointment_Modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Crear cita"),
            content= Create_Appointment_Widgets,
            actions=[
                ft.TextButton("Confirmar", on_click=Create_Appointment_Confirm),
                ft.TextButton("Cancelar", on_click=Create_Appointment_Modal_Close),
                ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        Create_Appointment_Modal_Open(e)

    def NavigationBar_Event(e):
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
            from View.GUI_Home import GUI_Home
            GUI_Home(page)

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
                    label="Agenda de citas",
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
        controls=[ft.IconButton(icon=ft.icons.MENU, icon_color= ft.colors.WHITE,on_click=NavigationBar_Open),ft.Text("Clientes pendientes", size=30, color="#ffffff")],
        alignment=ft.MainAxisAlignment.START
    )

    List_Vehicles = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        scroll="HIDDEN",
        width=900,
        height=350,
        wrap=True,
        spacing=10,
        run_spacing=10
    )
    Vehicles = Extract_Vehicles()
    
    page.data = False
    if page.data == False:
        page.remove(Wait, Wait_Text)

    for Vehicle in Vehicles:
        # Se crea un contenedor para cada vehículo.
        Vehicle_Container = ft.Container(
            bgcolor=ft.colors.WHITE,
            padding= ft.padding.only(left=30, top=20, right=20, bottom=20),
            border_radius=30,
            width=400,
            height=120
        )
        
        # Se crea una columna que contendrá los datos del vehículo.
        Vehicle_Column = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(Vehicle[1], size=15, color=ft.colors.BLACK),
                        ft.Text(Vehicle[2], size=10, color=ft.colors.GREY),
                    ],
                    width=250,
                    spacing=10
                ),
                ft.Row(
                    controls=[
                        ft.Text(Vehicle[3], size=10, color=ft.colors.BLACK),
                        ft.Text(Vehicle[4], size=10, color=ft.colors.GREY),
                        ft.Text(Vehicle[7], size=10, color=ft.colors.GREY),
                    ],
                    width=250,
                    spacing=7
                ),
                
                
                ft.Text(Vehicle[8], size=10, color=ft.colors.GREY),
                ft.Text(Vehicle[10], size=10, color=ft.colors.GREY),
            ],
            spacing=5
        )

        # Se crea la fila que contendrá el contenedor del vehículo y el botón de opción.
        Row_Vehicle = ft.Row(
            controls=[
                Vehicle_Column,
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(icon=ft.icons.EDIT_CALENDAR, text="Agendar cita", on_click= Create_Appointment_Event ,data=Vehicle[0])
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        # Se añade la fila al contenedor del vehículo.
        Vehicle_Container.content = Row_Vehicle

        # Se añade el contenedor del vehículo a la lista de vehículos.
        List_Vehicles.controls.append(Vehicle_Container)
    

    
    Widgets = ft.Column(
        controls=[Header, ft.Divider(thickness=2, color="#ffffff", height=5), List_Vehicles],
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
