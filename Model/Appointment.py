from Services.Adapters.Adapter_Appointment import Create_Appointment, Delete_Appointment_BD, Update_Appointment

class Appointment:
    def __init__(self):
        self.ID = None
        self.Date = None
        self.Time = None
        self.Cost_Service = None
        self.ID_Vehicle = None
        self.Event_Google = None
        ### Variables para API Google Calendar
        self.Name_Event = None
        self.Time_Start = None
        self.Time_End = None
        self.User = None
        self.Description = None

    def Create(self):
        """
        Crea una cita en la base de datos.

        Retorna:
        - True si la creación fue exitosa.
        """
        Create_Appointment(self.Date, self.Time, self.Cost_Service, self.ID_Vehicle, self.Name_Event, self.Time_Start, self.Time_End, self.User, self.Description)
        
    
    def Delete(self):
        """
        Elimina una cita de la base de datos.

        Retorna:
        - True si la eliminación fue exitosa.
        """
        Delete_Appointment_BD(self.Event_Google)
        

    def Update(self):
        """
        Modifica una cita en la base de datos.

        Retorna:
        - True si la modificación fue exitosa.
        """
        Update_Appointment(self.Event_Google, self.Date, self.Time, self.Time_Start, self.Time_End)
