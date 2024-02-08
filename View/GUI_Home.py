import flet as ft
from Controller.Controller_Usuario import Login
from Model.Calendar_API import GoogleCalendarManager
import datetime
from Controller.Controller_Citas import Agendar_Cita , Modificar_Cita

class Cita(ft.UserControl):
    def __init__(self, Name_Event, Hour_Start, Hour_End):
        super().__init__()
        self.Name_Event = Name_Event
        self.Hour_Start = Hour_Start
        self.Hour_End = Hour_End

def GUI_Home(page: ft.Page):
    

    page.window_width = 1100
    page.window_height = 600
    page.window_resizable = False
    page.window_center()

    page.title = "Home - AutoCar"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    

    page.fonts = {
        "Product Sans Regular": "settings/Product Sans Regular.ttf",
        "Product Sans Bold" : "settings/Product Sans Bold.ttf"
    }

    page.theme = ft.Theme(font_family="Product Sans Regular")
        
    def open_dlg_modal(e):
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    def close_dlg(e):
        dlg_modal.open = False
        page.update()

    def change_date(e):
        print(f"Date picker changed, value is {date_picker.value}")

    def date_picker_dismissed(e):
        print(f"Date picker dismissed, value is {date_picker.value}")

    date_picker = ft.DatePicker(
        on_change=change_date,
        on_dismiss=date_picker_dismissed,
        first_date=datetime.datetime(2023, 10, 1),
        last_date=datetime.datetime(2024, 10, 1),
    )

    page.overlay.append(date_picker)

    def change_time(e):
        print(f"Time picker changed, value (minute) is {time_picker.value.minute}")

    def dismissed(e):
        print(f"Time picker dismissed, value is {time_picker.value}")

    time_picker = ft.TimePicker(
        confirm_text="Confirm",
        error_invalid_text="Time out of range",
        help_text="Pick your time slot",
        on_change=change_time,
        on_dismiss=dismissed,
    )

    page.overlay.append(time_picker)

    date_button_hour = ft.ElevatedButton(
        "Hora de la cita",
        icon=ft.icons.ACCESS_TIME,
        on_click=lambda _: time_picker.pick_time(),
    )


    Name_Event = ft.TextField(label="Nombre del Evento")
    User_Invited = ft.TextField(label="Email del cliente")
    

    date_button_date = ft.ElevatedButton(
        "Fecha de la cita",
        icon=ft.icons.DATE_RANGE,
        on_click=lambda _: date_picker.pick_date(),
    )

    Column_Create_Cite = ft.Column(
        controls=[ft.Text("Datos ingresados para realizar la cita: "),Name_Event, User_Invited, date_button_date, date_button_hour],
        height=250,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    def Agendar_Cita_View(e):
        print ("View Agendar cita")
        
        if Agendar_Cita(Name_Event.value, User_Invited.value, date_picker.value, time_picker.value):
            close_dlg(e)
            page.remove(Page_Main)
            GUI_Home(page)
            


    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Crear cita"),
        content= Column_Create_Cite,
        actions=[
            ft.TextButton("Confirmar", on_click=Agendar_Cita_View),
            ft.TextButton("Cancelar", on_click=close_dlg),
            ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
        
    )

    
    def Reagendar_Cita(e):
        print("Reagendar cita")
        print(e.control.data)
        #Modificar_Cita(e.control.data)
        ID_Event = e.control.data

        def open_dlg_modal_reagendar(e):

            print(e.control.data)
            page.dialog = dlg_modal_reagendar
            dlg_modal_reagendar.open = True
            page.update()

        def Confirmar_Reagendar_Cita(e):
            print ("View Agendar cita")
            print(ID_Event)
            print(Name_Event.value)
            Modificar_Cita(ID_Event, Name_Event.value, date_picker.value, time_picker.value)
            dlg_modal_reagendar.open = False
            page.remove(Page_Main)
            GUI_Home(page)

        dlg_modal_reagendar = ft.AlertDialog(
            modal=True,
            title=ft.Text("Reagendar cita"),
            content= Column_Create_Cite,
            actions=[
                ft.TextButton("Confirmar", on_click=Confirmar_Reagendar_Cita),
                ft.TextButton("Cancelar", on_click=close_dlg),
                ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

        open_dlg_modal_reagendar(e)
        
    Text = ft.Text("Citas", size=30, color="#ffffff")
    

    def Cancelar_Cita(e):
        print(e.control.data)
        Calendar.delete_event(e.control.data)
        page.remove(Page_Main)
        GUI_Home(page)
        print("Cancelar cita")
        
    Button_NewCite = ft.ElevatedButton(text="Crear cita", icon="add", on_click=open_dlg_modal,
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

    Menu_Principal = ft.Row(
        controls=[Text, Button_NewCite],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
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

    print("Recovery Events")
    Calendar = GoogleCalendarManager()
    Eventos = Calendar.list_upcoming_events()
    print(Eventos)
    for Evento, Valor in Eventos.items():
        print("ID Evento: ", Evento)
        C_Event = ft.Container(
            bgcolor=ft.colors.WHITE,
            padding= ft.padding.only(left=30, top=20, right=20, bottom=20),
            
            border_radius=30,
            width=400,
            height=120
        )

        Event = ft.Column(
            controls=[],
            spacing=5
        )
        
        for subclave, subdatos in Valor.items():
            print(f"  {subclave}: {subdatos}")
            if subclave == "Nombre_Evento":
                Date_Event = ft.Text(subdatos, size=25, color=ft.colors.BLACK)
                Event.controls.insert(0, Date_Event)
            else:
                Date_Event = ft.Text(subdatos, size=10, color=ft.colors.GREY)
                Event.controls.append(Date_Event)

        pb = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(icon=ft.icons.EDIT_CALENDAR, text="Reagendar cita", on_click=Reagendar_Cita, data=Evento),
            ft.PopupMenuItem(),  # divider
            ft.PopupMenuItem(icon=ft.icons.FREE_CANCELLATION, text="Cancelar cita", on_click=Cancelar_Cita, data=Evento),
        ]
        
    )
        
        Row_Event = ft.Row(
            controls=[Event, pb],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        C_Event.content = Row_Event
        List_Events.controls.append(C_Event)
    

    

    
    Column = ft.Column(
        controls=[Menu_Principal, List_Events],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment = ft.CrossAxisAlignment.START,
        spacing=40,
        
    )


    

    Menu = ft.Container(
        content=Column,
        blur=ft.Blur(300, 300, ft.BlurTileMode.REPEATED),
        padding=40,
        alignment=ft.alignment.center,
        #alignment=ft.MainAxisAlignment.CENTER,
        width=1000,
        height=500,
        border_radius=50,
        #border=ft.border.all(5, ft.colors.PURPLE)
    )

    Page_Main = ft.Container(
        content=Menu,
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
        Page_Main,
    )


#ft.app(target=GUI_Home, assets_dir="assets")