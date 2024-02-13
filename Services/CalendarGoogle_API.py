# Autor: Williams Chan Pescador

"""
Patron de diseño Adapter en la API de Google Calendar
Este script hace uso del patrón de diseño Adapter para acceder a la API de Google Calendar.
El patrón Adapter permite que dos interfaces incompatibles trabajen juntas. 
En este caso, se utiliza para adaptar la interfaz de la API de Google Calendar a la interfaz de la aplicación.
"""
import os.path
import datetime as dt
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime
import logging

SCOPES = ["https://www.googleapis.com/auth/calendar"]

class GoogleCalendarManager:
    def __init__(self):
        logging.info("Inicializar el administrador de Google Calendar")
        self.service = self._authenticate()

    def _authenticate(self):
            """
            Autentica y devuelve las credenciales necesarias para acceder a la API de Calendar.

            Returns:
                googleapiclient.discovery.Resource: Objeto de recurso de la API de Calendar autenticado.
            """
            logging.info("Autenticar y devolver las credenciales necesarias para acceder a la API de Calendar")
            creds = None

            if os.path.exists("./Model/token.json"):
                creds = Credentials.from_authorized_user_file("./Model/token.json", SCOPES)

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file("./Model/client_secret_app_escritorio_oauth.json", SCOPES)
                    creds = flow.run_local_server(port=0)

                # Guarda las credenciales para la próxima ejecución
                with open("./Model/token.json", "w") as token:
                    token.write(creds.to_json())

            return build("calendar", "v3", credentials=creds)

    def list_upcoming_events(self, max_results=10):
            """
            Devuelve un diccionario con los próximos eventos del calendario.

            Parámetros:
            - max_results (int): El número máximo de eventos a devolver. Por defecto es 10.

            Retorna:
            - dict: Un diccionario con los próximos eventos del calendario. Cada evento está representado por un ID único y contiene información como la fecha de inicio, fecha de finalización y nombre del evento.
            """
            logging.info("Devolver un diccionario con los próximos eventos del calendario")
            now = dt.datetime.utcnow().isoformat() + "Z"
            tomorrow = (dt.datetime.now() + dt.timedelta(days=5)).replace(hour=23, minute=59, second=0, microsecond=0).isoformat() + "Z"

            events_result = self.service.events().list(
                calendarId='primary', timeMin=now, timeMax=tomorrow,
                maxResults=max_results, singleEvents=True,
                orderBy='startTime'
            ).execute()
            events = events_result.get('items', [])
            Eventos = {}
            if not events:
                logging.info("No se encontraron eventos próximos.")
            else:
                for event in events:
                    Evento = {}
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    end = event['end'].get('dateTime', event['end'].get('date'))
                    Fecha_Formateada = datetime.fromisoformat(start)
                    
                    Fecha_Formateada = Fecha_Formateada.strftime("%d - %b - %Y    %I:%M %p")

                    Evento['inicio'] = Fecha_Formateada
                    Fecha_Formateada = datetime.fromisoformat(end)
                    
                    Fecha_Formateada = Fecha_Formateada.strftime("%d - %b - %Y    %I:%M %p")
                    Evento['final'] = Fecha_Formateada
                    Evento['Nombre_Evento'] = event['summary']
                    Eventos[event['id']] =Evento
            
            return Eventos

    def create_event(self, summary, start_time, end_time, timezone, attendees=None, Description = None):
            """
            Crea un evento en el calendario.

            Parámetros:
            - summary: El resumen del evento.
            - start_time: La fecha y hora de inicio del evento en formato ISO 8601.
            - end_time: La fecha y hora de finalización del evento en formato ISO 8601.
            - timezone: La zona horaria del evento.
            - attendees: Una lista de correos electrónicos de los asistentes al evento (opcional).
            - Description: La descripción del evento (opcional).

            Retorna:
            - El ID del evento creado.

            Lanza:
            - HttpError: Si ocurre un error al crear el evento.
            """
            logging.info("Crear un evento en el calendario")
            event = {
                'summary': summary,
                'start': {
                    'dateTime': start_time,
                    'timeZone': timezone,
                },
                'end': {
                    'dateTime': end_time,
                    'timeZone': timezone,
                }
            }
            
            if Description:
                event["description"] = Description

            if attendees:
                event["attendees"] = [{"email": email} for email in attendees]

            try:
                event = self.service.events().insert(calendarId="primary", body=event).execute()
                return event.get('id')
            except HttpError as error:
                logging.error(f"Se ha producido un error: {error}")

    def update_event(self, event_id, start_time=None, end_time=None):
        """
        Actualiza un evento existente en el calendario.

        Parámetros:
        - event_id: ID del evento a actualizar.
        - start_time: (opcional) Nueva fecha y hora de inicio del evento.
        - end_time: (opcional) Nueva fecha y hora de finalización del evento.

        Retorna:
        - updated_event: El evento actualizado.
        """
        logging.info("Actualizar un evento existente en el calendario")
        event = self.service.events().get(calendarId='primary', eventId=event_id).execute()
        if start_time:
            event['start']['dateTime'] = start_time
        if end_time:
            event['end']['dateTime'] = end_time
        updated_event = self.service.events().update(
            calendarId='primary', eventId=event_id, body=event).execute()
        return updated_event

    def delete_event(self, event_id):
        """
        Elimina un evento del calendario.

        Parámetros:
        - event_id: ID del evento a eliminar.

        Retorna:
        - True si el evento se eliminó correctamente, False en caso contrario.
        """
        logging.info("Eliminar un evento del calendario")
        self.service.events().delete(calendarId='primary', eventId=event_id).execute()
        return True