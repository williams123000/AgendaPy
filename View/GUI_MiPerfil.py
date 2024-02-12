import flet as ft
from Controller.Controller_Usuario import Update_Photo, Update_Password
from Model.Usuario import Extract_Info_User_BD, Extract_Info_Login_BD
from Services.Proxy.Proxy_Login import Proxy_Login , Exit_App , Create_Keys_Session
import logging

def GUI_MiPerfil(page: ft.Page):
    # Se valida si el usuario ya ha iniciado sesión con el proxy.
    Validate, ID_User = Proxy_Login()

    if ID_User != None:
        # Si el inicio de sesión es exitoso, se guarda el ID del usuario en la sesión de la página.
        Create_Keys_Session(ID_User)
        logging.info(f"El usuario con ID {ID_User} ha iniciado sesion anteriormente.")

        # Se guarda el ID del usuario en la sesión de la página.
        page.session.set("ID_Usuario", ID_User)
        page.data = True

    # Se extraen los datos del usuario de la sesión de la página.
    Data_User = Extract_Info_User_BD(page.session.get("ID_Usuario"))
    Data_User = list(Data_User)
    Data_Login = Extract_Info_Login_BD(page.session.get("ID_Usuario"))
    Data_User.append(Data_Login[0])

    page.window_width = 1100
    page.window_height = 600
    page.window_resizable = False
    page.window_center()

    page.title = "Mi Perfil - AutoCar"
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
            
    def Update_Password_Event(e):

        def Update_Password_Modal_Open(e):
            page.dialog = Update_Password_Modal
            Update_Password_Modal.open = True
            page.update()

        def Update_Password_Modal_Close(e):
            Update_Password_Modal.open = False
            page.update()

        def Update_Password_Confirm(e):
            logging.info("Actualizando contraseña - ID: " + str(Data_User[0][0]) + " -")
            if (len(Password_Current.value) < 8) or (len(Password_Update.value) < 8) :
                dlg = ft.AlertDialog( title=ft.Text("No tienen más de 8 caracteres, prueba con otra contraseña", text_align="CENTER"), content= ft.Text("La contraseña debe de ser de 8 caracteres o más.", text_align="CENTER"))
                page.dialog = dlg
                dlg.open = True
                page.update()
            else:
                if Update_Password(Password_Current.value, Password_Update.value, Data_User[0][0]):
                    Update_Password_Modal.open = False
                    logging.info("Contraseña actualizada - ID: " + str(Data_User[0][0]) + " -")
                    page.remove(Window)
                    page.data = True
                    GUI_MiPerfil(page)
                else:
                    dlg = ft.AlertDialog( title=ft.Text("Valida tu contraseña actual", text_align="CENTER"), content= ft.Text("La contraseña actual no es correcta.", text_align="CENTER"))
                    page.dialog = dlg
                    dlg.open = True
                    page.update()
                    return

        Password_Current = ft.TextField(
            label="Contraseña actual",
        )

        Password_Update = ft.TextField(
            label="Contraseña nueva",
            helper_text="Debe de ser de 8 caracteres o más.",
        )

        Update_Password_Widgets = ft.Column(
            controls=[
                Password_Current,
                Password_Update
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=400,
            height=180,
        )


        Update_Password_Modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Actualizar contraseña de acceso"),
            content= Update_Password_Widgets,
            actions=[
                ft.TextButton("Confirmar", on_click=Update_Password_Confirm),
                ft.TextButton("Cancelar", on_click=Update_Password_Modal_Close),
                ],
            actions_alignment=ft.MainAxisAlignment.END,
            
        )

        Update_Password_Modal_Open(e)

    def Update_Photo_Event(e):
        

        def Update_Photo_Modal_Open(e):
            page.dialog = Update_Photo_Modal
            Update_Photo_Modal.open = True
            page.update()

        def Update_Photo_Modal_Close(e):
            Update_Photo_Modal.open = False
            page.update()

        def Update_Photo_Confirm(e):
            global selected_files
            

            if Update_Photo(selected_files, Data_User[0][0]):
                logging.info("Foto de perfil actualizada - ID: " + str(Data_User[0][0]) + " -")
                Update_Photo_Modal.open = False
                page.remove(Window)
                page.data = True
                GUI_MiPerfil(page)

        def pick_files_result(e: ft.FilePickerResultEvent):
            global selected_files
            selected_files =  e.files[0].path
        

        
        pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
        selected_files = None
        
        page.overlay.append(pick_files_dialog)


        

        Create_Appointment_Widgets = ft.Column(
            controls=[
                ft.Text("Selecciona tu imagen nueva:"),
                ft.ElevatedButton(
                    "Imagen",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=False
                    ),
                ),
            ],
            height=140,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        Update_Photo_Modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Actualizar foto de perfil         "),
            content= Create_Appointment_Widgets,
            actions=[
                ft.TextButton("Confirmar", on_click=Update_Photo_Confirm),
                ft.TextButton("Cancelar", on_click=Update_Photo_Modal_Close),
                ],
            actions_alignment=ft.MainAxisAlignment.END,
            
        )

        Update_Photo_Modal_Open(e)
        

    def NavigationBar_Event(e):
        if e.control.selected_index == 1:
            page.drawer.open = False
            page.remove(Window)
            page.data = True
            from View.GUI_Home import GUI_Home
            GUI_Home(page)

        if e.control.selected_index == 2:
            page.remove(Window)
            page.drawer.open = False
            Exit_App()
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
                                    foreground_image_url= Data_User[0][5],
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
                        ft.Text(Data_User[0][1], size=15, color=ft.colors.BLACK, font_family="Product Sans Bold"),
                        ft.Text(Data_User[1][3], size=13, color=ft.colors.BLACK, font_family="Product Sans Bold"),
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
        controls=[
            ft.IconButton(icon=ft.icons.MENU, icon_color= ft.colors.WHITE,on_click=NavigationBar_Open),
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(Data_User[0][1], size=25, color="#ffffff"),
                        ft.Text(Data_User[0][2], size=25, color="#ffffff"),
                        ft.CircleAvatar(foreground_image_url= Data_User[0][5], radius=25 )  
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                height=50,
                padding=0,
                margin=0
            ),
                     
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        height=50,
    )

    page.data = False
    if page.data == False:
        page.remove(Wait, Wait_Text)

    Password_Edit = ft.TextField(
        label="Contraseña",
        label_style = ft.TextStyle(color="#ffffff"),focused_color = "#ffffff",color="#ffffff", border_color="#ffffff", cursor_color="#ffffff", selection_color="#ffffff"
    )

    Widgets = ft.Column(
        controls=[
            Header, 
            ft.Divider(thickness=2, color="#ffffff", height=5),
            ft.Text("Acciones de la cuenta: ", size=20, color="#ffffff"),
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.SECURITY,
                                icon_color=ft.colors.WHITE,
                                icon_size=60,
                                on_click=Update_Password_Event,
                            ),
                            ft.Text("Cambiar contraseña", size=15, color="#ffffff"),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Column(
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.IMAGE,
                                icon_color=ft.colors.WHITE,
                                icon_size=60,
                                on_click=Update_Photo_Event,
                            ),
                            ft.Text("Cambiar foto", size=15, color="#ffffff"),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                
                spacing=20,
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            ),
            ft.Divider(thickness=2, color="#ffffff", height=5),
            ft.Text("Tus datos: ", size=20, color="#ffffff"),
            ft.Row(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Email: ", size=15, color="#ffffff"),
                            ft.Text(Data_User[1][1], size=15, color="#ffffff"),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=20,
                    ),
                    ft.Row(
                        controls=[
                            ft.Text("Rol: ", size=15, color="#ffffff"),
                            ft.Text(Data_User[1][3], size=15, color="#ffffff"),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=20,
                    ),
                    ft.Row(
                        controls=[
                            ft.Text("Telefono: ", size=15, color="#ffffff"),
                            ft.Text(Data_User[0][3], size=15, color="#ffffff"),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=20,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                spacing=20,
            ),
            ft.Row(
                controls=[
                    ft.Text("Direccion: ", size=15, color="#ffffff"),
                    ft.Text(Data_User[0][4], size=15, color="#ffffff"),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=20,
            ),
        ],
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
