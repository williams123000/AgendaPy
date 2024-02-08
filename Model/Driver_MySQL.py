import pymysql
from dotenv import load_dotenv
import os
# Load environment variables from the .env file
dontenv_path = os.path.join(os.path.dirname(__file__),'../settings', '.env')
load_dotenv(dontenv_path)

class Driver_MySQL:
    def __init__(self):
        print(os.getenv("DATABASE_HOST"))
        print(os.getenv("DATABASE_USERNAME"))
        print(os.getenv("DATABASE_PASSWORD"))
        print(os.getenv("DATABASE"))
        self.bd = pymysql.connect(
            host=os.getenv("DATABASE_HOST"),
            user=os.getenv("DATABASE_USERNAME"),
            password=os.getenv("DATABASE_PASSWORD"),
            database=os.getenv("DATABASE"),
            ssl={
                'ca': './settings/cert.pem',  # Ruta al certificado CA
            }
        )
        

    def getBD(self):
        return self.bd