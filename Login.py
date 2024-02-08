from tkinter import *
import pymysql
from tkinter import messagebox

def centrar_ventana(ventana, ancho, alto):
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()

    x_position = (screen_width - ancho) // 2
    y_position = (screen_height - alto) // 2

    ventana.geometry(f"{ancho}x{alto}+{x_position}+{y_position}")

def usuario_existe(correo, contraseña):
    try:
        bd = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="usuario"
        )
        mcursor = bd.cursor()
        sql = f"SELECT * FROM login WHERE Correo = '{correo}' AND Contraseña = '{contraseña}'"
        mcursor.execute(sql)
        resultado = mcursor.fetchone()

        bd.close()

        return resultado is not None
    except Exception as e:
        print(f"Error al verificar usuario existente: {str(e)}")
        return False

def obtener_rol_usuario(correo):
    try:
        bd = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="usuario"
        )
        mcursor = bd.cursor()
        sql = f"SELECT rol FROM login WHERE Correo = '{correo}'"
        mcursor.execute(sql)
        resultado = mcursor.fetchone()

        bd.close()

        if resultado:
            return resultado[0]
        else:
            return None
    except Exception as e:
        print(f"Error al obtener el rol del usuario: {str(e)}")
        return None

def inserta_datos():
    correo = texto_correo.get()
    contraseña = texto_contraseña.get()
    rol = "administrador"  # Se puede ajustar

    try:
        if usuario_existe(correo, contraseña):
            messagebox.showinfo(message="El usuario ya existe", title="Aviso")
        else:
            bd = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="usuario"
            )
            mcursor = bd.cursor()
            sql = f"INSERT INTO login (Correo, Contraseña, rol) VALUES ('{correo}','{contraseña}','{rol}')"
            mcursor.execute(sql)
            bd.commit()
            messagebox.showinfo(message="Registro Válido", title="Aviso")

    except Exception as e:
        bd.rollback()
        messagebox.showinfo(message=f"Registro No Válido: {str(e)}", title="Aviso")

    finally:
        if 'bd' in locals():
            bd.close()

def iniciar_sesion():
    correo = texto_correo.get()
    contraseña = texto_contraseña.get()

    try:
        if usuario_existe(correo, contraseña):
            rol_usuario = obtener_rol_usuario(correo)

            if rol_usuario == "administrador":
                abrir_interfaz_administrador()
            elif rol_usuario == "secretaria":
                abrir_interfaz_secretaria()
            else:
                messagebox.showinfo(message="Rol no reconocido", title="Aviso")
        else:
            messagebox.showinfo(message="Credenciales incorrectas", title="Aviso")

    except Exception as e:
        print(f"Error al iniciar sesión: {str(e)}")

def abrir_interfaz_administrador():
    # Lógica para abrir la interfaz del administrador
    admin_window = Tk()
    admin_window.title("Panel de Administrador")
    centrar_ventana(admin_window, 1100, 600)
    admin_window.resizable(False, False)
    # Aquí puedes agregar los elementos y funcionalidades específicos del administrador
    admin_window.mainloop()

def abrir_interfaz_secretaria():
    # Lógica para abrir la interfaz de la secretaria
    secretaria_window = Tk()
    secretaria_window.title("Panel de Secretaria")
    centrar_ventana(secretaria_window, 1100, 600)
    secretaria_window.resizable(False, False)
    # Aquí puedes agregar los elementos y funcionalidades específicos de la secretaria
    secretaria_window.mainloop()

# Creación de la interfaz de inicio de sesión
root = Tk()
root.title("Login")

centrar_ventana(root,1100,600)
root.resizable(False, False)

fondo = PhotoImage(file="images/Fondo2.png")
label = Label(root, image=fondo)
label.place(x=0, y=0, relheight=1, relwidth=1)

# Cuadro donde irán los datos de registro
frame_registro = Frame(root, bg="white")
frame_width = 500
frame_height = 400
frame_x = (1100 - frame_width) // 2
frame_y = (600 - frame_height) // 2
frame_registro.place(x=frame_x, y=frame_y, height=frame_height, width=frame_width)

titulo = Label(frame_registro, text="Iniciar Sesión", font=("Ventura Edding", 35), bg="white").place(x=90, y=30)

usuario_correo = Label(frame_registro, text="Correo", font=("Ventura Edding", 10), bg="white").place(x=90, y=120)
texto_correo = Entry(frame_registro, font=("Calibri Light", 10), bg="lightgray")
texto_correo.place(x=90, y=140)

usuario_contraseña = Label(frame_registro, text="Contraseña", font=("Ventura Edding", 10), bg="white").place(x=90, y=180)
texto_contraseña = Entry(frame_registro, show="*", font=("Calibri Light", 10), bg="lightgray")
texto_contraseña.place(x=90, y=200)

alerta_btn = Button(frame_registro, text="Contraseña Olvidada?", font=("Ventura Edding", 8), bd=0).place(x=90, y=250)

# Botón de registro
#registrar_btn = Button(root, text="Registrarse", font=("Ventura Edding", 8), bg="dark gray", bd=0, command=inserta_datos).place(x=400, y=450, width=180, height=40)

# Botón de inicio de sesión
iniciar_sesion_btn = Button(root, text="Iniciar Sesión", font=("Ventura Edding", 8), bg="dark gray", bd=0, command=iniciar_sesion).place(x=450, y=450, width=180, height=40)

root.mainloop()
