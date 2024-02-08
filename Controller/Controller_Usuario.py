from Model.Usuario import Usuario

def Login(Email : str, Password : str):
    User_Current = Usuario()
    User_Current.correo = Email
    User_Current.password = Password
    if User_Current.Usuario_Existe():
        print("Usuario existe")
        return True
    else:
        print("No existe")
        return False
    
def Recovery(Email : str):
    print("Recuperando contraseña")
    User_Current = Usuario()
    User_Current.correo = Email
    if User_Current.Usuario_Existe_Correo():
        print("Usuario existe")
        if User_Current.Recovery_Password():
            print("Correo enviado")
            return True
        else:
            print("Correo no enviado")
            return False
    else:
        print("No existe")
        return False