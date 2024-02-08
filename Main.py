from Model.Driver_MySQL import Driver_MySQL
from View.GUI_Login import main as GUI_Login
import flet as ft

if __name__ == "__main__":
    ft.app(target=GUI_Login, assets_dir="assets")