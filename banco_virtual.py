# primero añadiremos nuevos usuarios a la base de datos

import pandas as pd
import re

preguntar_usuario_nuevo = input("¿Desea crear una nueva cuenta? (si/no): ").lower().strip()

ruta_database = "C:/Users/juani/OneDrive/Escritorio/Banco en Linea/database/data.csv"
ruta_database_block = "C:/Users/juani/OneDrive/Escritorio/Banco en Linea/database/data_block.csv"

# APARTADO DE FUNCIONES

def nuevo_usuario():
    # en este caso queremos que los nuevos usuarios no sean iguales a otros si no habran conflictos

    usuario_nuevo = input("Por favor inserte su nuevo nombre de usuario: ").strip()

    df = pd.read_csv(ruta_database, encoding="utf-8") # leemos el database actual

    if usuario_nuevo in df["usuario"].values:
        print("el usuario que quieres registrar ya existe, por favor inserte un nombre de usuario diferente")
        nuevo_usuario()
    else:
        crear_password(usuario_nuevo)

def comprobar_usuario():
    # en este punto queremos inciar sesion
    
    df = pd.read_csv(ruta_database, encoding="utf-8") # volvemos a leer la base de datos
    
    print("｡☆✼★━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━★✼☆｡")
    print("                          ¡BIENVENID@ AL INICIO DE SESION!")
    print("｡☆✼★━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━★✼☆｡")
    usuario_input = input("Ingrese su nombre de usuario: ")
    # queremos corroborar primero que el usuario si se encuentre, en caso que no se vuelve a repetir el codigo ya se sabe que control c rompe todo
    
    if usuario_input in df["usuario"].values:
        indice = df[df["usuario"] == usuario_input].index[0]
        comprobar_password(indice, df)
    else:
        print("NO SE ENCONTRO SU NOMBRE DE USUARIO EN NUESTRA DATA O SE ENCUENTRA BLOQUEADO, INTENTELO DE NUEVO")
        comprobar_usuario()

def comprobar_password(index, dataframe, conteo_intentos=0):
    password_input = input("Por favor inserta tu contraseña: ")
    if dataframe.at[index, "password"] == password_input:
        print("¡INICIO DE SESION EXITOSO!")
        operaciones_banco(index)
        return 0  # No hay intentos fallidos, por lo que se reinicia el contador
    else:
        conteo_intentos += 1 # sumamos uno
        print("INICIO DE SESION FALLIDO INTENTE DE NUEVO") # si llega a fallar
        
        if conteo_intentos > 2: # ignorado hasta tener el valor nuevo
            conteo_intentos = 0
            bloquear_usuario(index)
            
        else:
            conteo_intentos = comprobar_password(index, dataframe, conteo_intentos) # tambien se ejecuta en este caso
    return conteo_intentos

def bloquear_usuario(index):
    df = pd.read_csv(ruta_database, encoding="utf-8")
    df_block = pd.read_csv(ruta_database_block, encoding="utf-8") # el csv nuevo
    df_original = pd.read_csv(ruta_database, encoding="utf-8")
    cuenta = df.iloc[index].copy() # los datos copiados
    cuenta_format = {"usuario": [cuenta["usuario"]], "password": [cuenta["password"]], "seguridad": [cuenta["seguridad"]], "saldo": [int(cuenta["saldo"])]}
    df_nuevo = pd.DataFrame(cuenta_format)
    unir_datos = pd.concat([df_block, df_nuevo], ignore_index=True)
    # ahora debemos unir los datos en un nuevo dataframe que sera escrito
    unir_datos.to_csv(ruta_database_block, encoding='utf-8', index=False)
    # terminar con la eliminacion de los datos en el df original
    df_cuenta_eliminada = df_original.drop(index)
    df_cuenta_eliminada.to_csv(ruta_database, encoding='utf-8', index=False)
    print("CUENTA BLOQUEADA POR MUCHOS INTENTOS")
    print("SALIENDO DEL SISTEMA...")
    
# FUNCION QUE EJECUTA UN SISTEMA POR OPCIONES PARA HACER OPERACIONES CORRESPONDIENTES
def operaciones_banco(index):
    # en esta parte sacaremos un menu donde se tenga que seleccionar entre 4 opciones y si se inserta otro numero se pregunta de nuevo
    print("｡☆✼★━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━★✼☆｡")
    print("                                MENU PRINCIPAL")
    print("｡☆✼★━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━★✼☆｡")
    print("1: DEPOSITAR")
    print("2: RETIRAR")
    print("3: VER SALDO")
    print("4: TRANSFERIR SALDO")
    print("5: SALIR")
    opcion_usuario = int(input("POR FAVOR SELECCIONE LA OPERACION QUE QUIERE HACER: "))
    if opcion_usuario == 1:
        depositar_dinero(index)
    elif opcion_usuario == 2:
        retirar_dinero(index)
    elif opcion_usuario == 3:
        ver_saldo(index)
    elif opcion_usuario == 4:
        tranferir_dinero(index)
    else:
        salir_sistema()
def crear_password(usuario_nuevo):
    df = pd.read_csv(ruta_database, encoding="utf-8") # leemos el database actual
    password_nuevo = input("Inserte su nueva contraseña: ") # se que puedo usar expresiones regulares pero aun me faltaba algunas cosas, cuando tenga tiempo lo hago
    patron = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    if re.search(patron, password_nuevo):
        artista_favorito = input("Inserte el nombre de su artista favorito, usaremos esta informacion en caso de recuperacion de cuenta: ")
        nueva_fila = pd.DataFrame({"usuario": [usuario_nuevo], "password": [password_nuevo], "seguridad": [artista_favorito], "saldo": 2000})
        df = pd.concat([df, nueva_fila], ignore_index=True) # con los nuevos datos creamos una nueva fila
        df.to_csv(ruta_database, encoding='utf-8', index=False) # debemos guardar los cambios
        de_nuevo = input("¿Desea crear otra cuenta? (si/no): ").lower()
        if de_nuevo == "si":
            nuevo_usuario()
        else:
            comprobar_usuario()
    else:
        print("LA CONTRASEÑA DEBE TENER AL MENOS LAS SIGUIENTES CONDICIONES: ")
        print("- Al menos una letra minúscula")
        print("- Al menos una letra mayúscula")
        print("- Al menos un dígito")
        print("- Al menos un carácter especial")
        print("- Longitud mínima de 8 caracteres")
        usuario_nuevo = crear_password(usuario_nuevo)
    return usuario_nuevo
def depositar_dinero(index):
    df = pd.read_csv(ruta_database, encoding="utf-8")
    saldo = df.loc[index, "saldo"] # [argumento]
    saldo_aumentar = (input("¿CUANTO SALDO DESEA DEPOSITAR A SU CUENTA?: "))
    if saldo_aumentar.isdigit():
        saldo += int(saldo_aumentar)
        df.loc[index, "saldo"] = saldo
        df.to_csv(ruta_database, encoding='utf-8', index=False)
        print("¡DINERO DEPOSITADO CON EXITO!")
        print("VOLVIENDO AL MENU PRINCIPAL...")
        operaciones_banco(index)
    else:
        print("ERROR VALOR NO NUMERICO, INTENTELO DE NUEVO")
        index = depositar_dinero(index)
    return index
def retirar_dinero(index):
    df = pd.read_csv(ruta_database, encoding="utf-8")
    saldo = df.loc[index, "saldo"] # [argumento]
    print(f"SU SALDO ACTUAL ES: {saldo}")
    saldo_retirar = int(input("CUANTO DINERO DESEA RETIRAR EN EFECTIVO?: "))
    if saldo_retirar <= saldo:
        saldo -= saldo_retirar
        df.loc[index, "saldo"] = saldo
        df.to_csv(ruta_database, encoding='utf-8', index=False)
        print("¡LA OPERACION FUE REALIZADA CON EXITO!")
        print("PUEDE ACERCARSE A UN CAJERO AUTOMATICA A RETIRAR SU DINERO EN EFECTIVO, USE SU TARJETA Y CONFIRME EL RETIRO DE DINERO EN EFECTIVO")
        print("VOLVIENDO AL MENU PRINCIPAL...")
        operaciones_banco(index)
    else:
        print("ERROR SALDO INSUFICIENTE O VALOR NO NUMERICO, INTENTELO DE NUEVO")
        index = retirar_dinero(index)
    return index
def ver_saldo(index):
    df = pd.read_csv(ruta_database, encoding="utf-8")
    saldo = df.loc[index, "saldo"] # [argumento]
    print(f"TU SALDO ACTUAL ES: {saldo}")
    operaciones_banco(index)
def tranferir_dinero(index):
    df = pd.read_csv(ruta_database, encoding="utf-8")
    df_filtrado = df.drop(index)
    saldo = df.loc[index, "saldo"] # [argumento]
    print(f"SU SALDO ACTUAL ES: {saldo}")
    # seleccionaremos una cuenta que este registrado en la database y haremos un aumento de saldo y disminucion de la misma
    otro_usuario = input("PARA TRANFERIR DINERO A OTRA CUENTA ESPECIFIQUE EL NOMBRE DE CUENTA A QUIEN DESEA DEPOSITAR: ")
    # tambien debemos mostrar el saldo actual para transferencia, ya veremos en caso que el saldo no sea suficiente mas adelante
    if otro_usuario in df_filtrado["usuario"].values:
        print("LA CUENTA FUE ENCONTRADA")
        indice_usuario = df[df["usuario"] == otro_usuario].index[0]
        valor_depositar = int(input(f"¿CUANTO DESEA DEPOSITAR A LA CUENTA {otro_usuario}?: "))
        if valor_depositar <= saldo:
            # en este punto sabemos que se puede depositar ese total de dinero a la otra cuenta, asi que hacemos la operacion, 1 restar de mi cuenta
            saldo -= valor_depositar
            df.loc[index, "saldo"] = saldo
            # despues sumar a la otra cuenta
            saldo_tranfiriendo = df.loc[indice_usuario, "saldo"] # [argumento]
            saldo_tranfiriendo += valor_depositar
            df.loc[indice_usuario, "saldo"] = saldo_tranfiriendo
            df.to_csv(ruta_database, encoding='utf-8', index=False)
            # bueno si se pudo, entonces dejamos como operacion terminada y volvemos al menu principal
            print("¡LA OPERACION FUE REALIZADA CON EXITO!")
            print("VOLVIENDO AL MENU PRINCIPAL...")
            operaciones_banco(index)
        else:
            print("ERROR SALDO INSUFICIENTE O VALOR NO NUMERICO, INTENTELO DE NUEVO")
            index = tranferir_dinero(index)
    else:
        print("NO ENCONTRAMOS NINGUNA CUENTA QUE CORRESPONDA AL NOMBRE DE USUARIO QUE INSERTO INTENTE DE NUEVO")
        index = tranferir_dinero(index)
    return index
def salir_sistema():
    print("¡MUCHAS GRACIAS POR USAR ESTE PROGRAMA!")
if preguntar_usuario_nuevo == "si":
    nuevo_usuario()
else:
    comprobar_usuario()
