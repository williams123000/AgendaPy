from Model.Driver_MySQL import Driver_MySQL

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import string

class Usuario:
    def __init__(self):
        self.correo = ""
        self.password = ""
        self.rol = ""
        
    def Usuario_Existe(self):
        BD = Driver_MySQL()
        try:
            sql = f"SELECT * FROM login WHERE Correo = '{self.correo}' AND Password = '{self.password}'"
            mcursor = BD.getBD().cursor()
            mcursor.execute(sql)
            resultado = mcursor.fetchone()
            return resultado is not None

        except Exception as e:
            print(f"Error al verificar usuario existente: {str(e)}")
            return False
    
    def Usuario_Existe_Correo(self):
        BD = Driver_MySQL()
        try:
            sql = f"SELECT * FROM login WHERE Correo = '{self.correo}'"
            mcursor = BD.getBD().cursor()
            mcursor.execute(sql)
            resultado = mcursor.fetchone()
            return resultado is not None

        except Exception as e:
            print(f"Error al verificar usuario existente: {str(e)}")
            return False

    def Obtener_Rol(self, BD : Driver_MySQL):
        try:
            sql = f"SELECT rol FROM login WHERE Correo = '{self.correo}'"
            mcursor = BD.getBD().cursor()
            mcursor.execute(sql)
            resultado = mcursor.fetchone()

            if resultado:
                return resultado[0]
            else:
                return None
        except Exception as e:
            print(f"Error al obtener el rol del usuario: {str(e)}")
            return None
        
    def Insertar_Usuario(self, BD : Driver_MySQL):
        try:
            if self.Usuario_Existe():
                return False
            else:
                sql = f"INSERT INTO login (Correo, Password, rol) VALUES ('{self.correo}','{self.password}','{self.rol}')"
                mcursor = BD.getBD().cursor()
                mcursor.execute(sql)
                BD.getBD().commit()
                return True
        except Exception as e:
            BD.getBD().rollback()
            return False
        
    def Iniciar_Sesion(self):
        try:
            if self.Usuario_Existe():
                self.rol = self.Obtener_Rol()

                return self.rol
            
        except Exception as e:
            print(f"Error al iniciar sesión: {str(e)}")
    
    def Cambiar_Contraseña(self, nueva_contraseña):
        try:
            BD = Driver_MySQL()
            sql = f"UPDATE login SET Password = '{nueva_contraseña}' WHERE Correo = '{self.correo}'"
            mcursor = BD.getBD().cursor()
            mcursor.execute(sql)
            BD.getBD().commit()
            return True
        except Exception as e:
            BD.getBD().rollback()
            return False

    # Función para generar una contraseña aleatoria
    def generate_random_password(self, length=8):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for i in range(length))
    
    def Recovery_Password(self):
       # Configura los detalles del servidor SMTP de Gmail
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'williamspvp1234@gmail.com'
        smtp_password = 'fjzcdfvaeaejhsfp'

        # Configura el correo
        from_address = 'williamspvp1234@gmail.com'
        to_address = self.correo
        subject = 'Recuperación de contraseña'
        random_password = self.generate_random_password()
        self.Cambiar_Contraseña(random_password)
        body = f"""Estimado usuario,

Hemos recibido una solicitud para restablecer tu contraseña. 
Tu nueva contraseña temporal es: {random_password}

Por favor, inicia sesión con esta contraseña y cámbiala inmediatamente.

Atentamente,
El equipo de soporte"""

        # Crea el objeto del correo
        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = to_address
        msg['Subject'] = subject

        # Adjunta el cuerpo del correo
        msg.attach(MIMEText(body, 'plain'))

        # Inicia una conexión al servidor SMTP de Gmail
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        # Inicia sesión en el servidor SMTP de Gmail
        server.login(smtp_username, smtp_password)

        # Envía el correo
        server.sendmail(from_address, to_address, msg.as_string())

        # Cierra la conexión al servidor SMTP de Gmail
        server.quit() 

        return True