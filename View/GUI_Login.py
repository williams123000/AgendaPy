import flet as ft
from Controller.Controller_Usuario import Login , Recovery
from View.GUI_Home import GUI_Home

def main(page: ft.Page):
    page.window_width = 1100
    page.window_height = 600
    page.window_resizable = False
    page.window_center()
    
    page.padding = 0
    page.title = "Login - AutoCar"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.fonts = {
        "Product Sans Regular": "settings/Product Sans Regular.ttf",
        "Product Sans Bold" : "settings/Product Sans Bold.ttf"
    }

    page.theme = ft.Theme(font_family="Product Sans Regular")

    Text = ft.Text("Iniciar sesión", size=30, color="#ffffff")
    Email = ft.TextField(label="Email", label_style = ft.TextStyle(color="#ffffff"),focused_color = "#ffffff",color="#ffffff", border_color="#ffffff", cursor_color="#ffffff", selection_color="#ffffff")
    Password = ft.TextField(label="Password", label_style = ft.TextStyle(color="#ffffff"),focused_color = "#ffffff",color="#ffffff", border_color="#ffffff", cursor_color="#ffffff", selection_color="#ffffff", password=True, can_reveal_password=True)
    
    def Action_Login(e):
        if Email.value == "" or Password.value == "":
            dlg = ft.AlertDialog( title=ft.Text("Datos no ingresados", text_align="CENTER"), content= ft.Text("Por favor ingresa tus datos.", text_align="CENTER"),on_dismiss=lambda e: print("Dialog dismissed!"))
            page.dialog = dlg
            dlg.open = True
            page.update()
            return
        if Login(Email.value, Password.value):
            page.remove(Page_Main)
            GUI_Home(page)
        else:
            dlg = ft.AlertDialog( title=ft.Text("Usuario no registrado", text_align="CENTER"), content= ft.Text("Por favor valida tus datos de acceso.", text_align="CENTER"),on_dismiss=lambda e: print("Dialog dismissed!"))
            page.dialog = dlg
            dlg.open = True
            page.update()
            

        page.update()

    Login_Button = ft.ElevatedButton("Iniciar Sesión", icon="login", on_click=Action_Login,
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

    def open_dlg_modal(e):
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    def close_dlg(e):
        dlg_modal.open = False
        page.update()

    Email_Recovery = ft.TextField(label="Email para recuperar", label_style = ft.TextStyle(color="#000000"),focused_color = "#000000",color="#000000", border_color="#000000", cursor_color="#000000", selection_color="#000000")
    column_dlg = ft.Column(
        controls=[
            ft.Text("Introduce tu Email para restablecer la contraseña:"),
            Email_Recovery,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment = ft.CrossAxisAlignment.START,
        height=100,
        spacing=20
    )

    def Action_Recovery(e):
        if Email_Recovery.value == "":
            dlg = ft.AlertDialog( title=ft.Text("Datos no ingresados", text_align="CENTER"), content= ft.Text("Por favor ingresa tu Email.", text_align="CENTER"),on_dismiss=lambda e: print("Dialog dismissed!"))
            page.dialog = dlg
            dlg.open = True
            page.update()
            return
        
        if Recovery(Email_Recovery.value):
            dlg = ft.AlertDialog( title=ft.Text("Correo enviado", text_align="CENTER"), content= ft.Text("Se ha enviado un correo para restablecer tu contraseña.", text_align="CENTER"),on_dismiss=lambda e: print("Dialog dismissed!"))
            page.dialog = dlg
            dlg.open = True
            page.update()
        else:
            dlg = ft.AlertDialog( title=ft.Text("Correo no enviado", text_align="CENTER"), content= ft.Text("El correo ingresado no existe.", text_align="CENTER"),on_dismiss=lambda e: print("Dialog dismissed!"))
            page.dialog = dlg
            dlg.open = True

            page.update()


    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Recuperación de contraseña"),
        content=column_dlg,
        actions=[
            ft.TextButton("Confirmar", on_click=Action_Recovery),
            ft.TextButton("Cancelar", on_click=close_dlg),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )

    

    Recovery_Password = ft.TextButton("¿Olvidaste tu contraseña?", on_click=open_dlg_modal,
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
                #ft.MaterialState.DRAGGED: ft.colors.PURPLE
            },
            
            
        )
    )

    Row = ft.Row(
        controls=[
            ft.Column(
                controls = [
                    Login_Button, 
                    Recovery_Password
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment = ft.CrossAxisAlignment.CENTER
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )
    
    Column = ft.Column(
        controls=[Text, Email, Password,Row],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
        spacing=40
    )

    Menu = ft.Container(
        content=Column,
        blur=ft.Blur(300, 300, ft.BlurTileMode.REPEATED),
        padding=40,
        alignment=ft.alignment.center,
        width=400,
        height=450,
        border_radius=50,
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


#ft.app(target=main, assets_dir="assets")