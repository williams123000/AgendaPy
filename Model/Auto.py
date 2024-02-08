from Model.Driver_MySQL import Driver_MySQL


class Auto:
    def __init__(self, ID_Vehicle, Name_Owner, Phone, Vehicle_Brand, Model_Vehicle, Year, Color, Type_Vehicle, Date_Purchase, Hour_Purchase, Cost_Purchase):
        self.ID_Vehicle = ID_Vehicle
        self.Name_Owner = Name_Owner
        self.Phone = Phone
        self.Vehicle_Brand = Vehicle_Brand
        self.Model_Vehicle = Model_Vehicle
        self.Year = Year
        self.Color = Color
        self.Type_Vehicle = Type_Vehicle
        self.Date_Purchase = Date_Purchase
        self.Hour_Purchase = Hour_Purchase
        self.Cost_Purchase = Cost_Purchase

def Extract_Autos_BD():
    BD = Driver_MySQL()
    try:
        sql = "SELECT * FROM Vehicles"
        mcursor = BD.getBD().cursor()
        mcursor.execute(sql)
        resultado = mcursor.fetchall()
        return resultado
    except Exception as e:
        print(f"Error al obtener los autos de la BD: {str(e)}")
        return None

Response = Extract_Autos_BD()

for i in Response:
    print(i)