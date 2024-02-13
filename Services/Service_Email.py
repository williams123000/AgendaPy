import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging

def Send_Email_Recovery(Email_Send : str, Password_Send : str):
    """
    Envía un correo electrónico al usuario con una contraseña temporal para recuperar su contraseña.

    Returns:
    bool: True si el correo electrónico se envió correctamente, False en caso contrario.
    """
        
    # Configura los detalles del servidor SMTP de Gmail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'williamspvp1234@gmail.com'
    smtp_password = 'fjzcdfvaeaejhsfp'

    # Configura el correo
    from_address = 'williamspvp1234@gmail.com'
    to_address = Email_Send
    subject = 'Recuperación de contraseña'
    
    body = f"""Estimado usuario,

Hemos recibido una solicitud para restablecer tu contraseña. 
Tu nueva contraseña temporal es: {Password_Send}

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
    logging.info("Enviando correo de recuperacion de contraseña")

    return True