from Services.Adapters.Adapter_User import Read_User
import logging

class User:
    def __init__(self):
        self.ID = None
        self.Name = None
        self.Last_Name = None
        self.Phone = None
        self.Address = None
        self.URL_Photo = None
        self.Shift = None

    def Read_Data(self):
        """
        Método que realiza la lectura de datos.
        """
        Response = Read_User(self.ID)
        if Response:
            self.Name = Response[1]
            self.Last_Name = Response[2]
            self.Phone = Response[3]
            self.Address = Response[4]
            self.URL_Photo = Response[5]
            self.Shift = Response[6]
            return True
        else:
            return False