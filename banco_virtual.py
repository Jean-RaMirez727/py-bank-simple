# primero añadiremos nuevos usuarios a la base de datos

import pandas as pd
import re

preguntar_usuario_nuevo = input("¿Desea crear una nueva cuenta? (si/no): ").lower().strip()

ruta_database = "database/data.csv"
ruta_database_block = "database/data_block.csv"

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
    print("｡☆✼★━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━★✼☆｡")
    print("                                MENU PRINCIPAL")
    print("｡☆✼★━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━★✼☆｡")
    print("1: DEPOSITAR")
    print("2: RETIRAR")
    print("3: VER SALDO")
    print("4: TRANSFERIR SALDO")
    print("5: RETIRAR FONDOS EN OTRA MONEDA")
    print("6: SALIR")
    opcion_usuario = int(input("POR FAVOR SELECCIONE LA OPERACION QUE QUIERE HACER: "))
    if opcion_usuario == 1:
        depositar_dinero(index)
    elif opcion_usuario == 2:
        retirar_dinero(index)
    elif opcion_usuario == 3:
        ver_saldo(index)
    elif opcion_usuario == 4:
        tranferir_dinero(index)
    elif opcion_usuario == 5:
        retirar_dinero_internacional(index)
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

# PARA CAMBIO DE MONEDAS

def retirar_dinero_internacional(index):
    # el usuario debe elegir la moneda donde comienza la conversion
    df = pd.read_csv(ruta_database, encoding="utf-8")
    saldo_actual = df.loc[index, "saldo"] # [argumento]
    print("｡☆✼★━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━★✼☆｡")
    print("                    BIENVENIDO AL SISTEMA DE CONVERSION DE MONEDA")
    print("｡☆✼★━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━★✼☆｡")
    print(f"USTED TIENE UN SALDO DE: {saldo_actual} DOLARES (USD)")
    print("1. PESO CHILENO (CLP)")
    print("2. PESO ARGENTINO (ARS)")
    print("3. EURO (EUR)")
    print("4. LIRA TURC (TRY)")
    print("5. LIRA ESTERLINA (GBP)")
    print("6. REGRESAR AL MENU PRINCIPAL")
    opcion_usuario = int(input("¿DESDE QUE MONEDA USTED DESEA VER SUS FONDOS PARA LA CONVERSION?: "))
    if opcion_usuario == 1:
        retirar_clp(index)
    elif opcion_usuario == 2:
        retirar_ars(index)
    elif opcion_usuario == 3:
        retirar_eur(index)
    elif opcion_usuario == 4:
        retirar_try(index)
    elif opcion_usuario == 5:
        retirar_gbp(index)
    else:
        print("REGRESANDO AL MENU PRINCIPAL...")
        operaciones_banco(index)

def retirar_clp(index):
    df = pd.read_csv(ruta_database, encoding="utf-8")
    saldo_actual = df.loc[index, "saldo"] # [argumento]
    saldo_convertido = round(saldo_actual * 966.745, 2)
    minimo_cambio = 9615.38 # PESOS CHILENOS MINIMO
    print(f"USTED HA SELECCIONADO PESO CHILENO EN TOTAL USTED TIENE: {saldo_convertido} CLP")
    print("CONVERTIR PESOS CHILENOS A: ")
    print("1. PESO ARGENTINO (ARS)")
    print("2. EURO (EUR)")
    print("3. LIRA TURCA (TRY)")
    print("4. LIBRA ESTERLINA (GBP)")
    print("5. SALIR AL MENU PRINCIPAL")
    opcion_convertir = int(input("¿A QUE TIPO DE MONEDA USTED DESEA CONVERTIR?: "))
    if opcion_convertir == 1:
        print(f"USTED SELECCIONO PESO CHILENO EN TOTAL USTED TIENE: {saldo_convertido} CLP")
        opcion_escogida = "CLP"
        moneda = "ARS"
        print("LA TASA DE CAMBIO ES: 1 PESO CHILENO = 0.90 PESOS ARGENTINOS")
        print(f"EL MINIMO DE CLP REQUERIDO ES DE AL MENOS: {minimo_cambio}")
        cantidad_convertir = int(input("¿QUE CANTIDAD DE CLP USTED DESEA CONVERTIR A ARS?: ")) # cantidad del usuario en pesos chilenos
        # se convertira a pesos argentinos lo cual hace que solo debamos convertir todo a pesos argentinos
        comprobacion = round(cantidad_convertir * 0.0010, 2) # pesos chilenos convertidos a dolares
        # por ultimo debemos saber si el cambio a pesos argentinos totales es de al menos 10 dolares
        tasa_cambio = 0.90 # PESOS CHILENOS A PESO ARGENTINO
        if saldo_actual >= comprobacion and cantidad_convertir >= minimo_cambio: # comprobamos que nuestro saldo actual si alcance y si es de minimo 10 dolares
            realizar_cambio(cantidad_convertir, comprobacion, index, tasa_cambio, opcion_escogida, moneda, saldo_convertido)
        else:
            print("ERROR VALOR DEMASIADO BAJO PARA REALIZAR OPERACION DE CAMBIO O SALDO INSUFICIENTE VUELVA A INTENTARLO DE NUEVO")
            retirar_clp(index)
    elif opcion_convertir == 2:
        print(f"USTED SELECCIONO PESO CHILENO EN TOTAL USTED TIENE: {saldo_convertido} CLP")
        opcion_escogida = "CLP"
        moneda = "EUR"
        print("LA TASA DE CAMBIO ES: 1 PESO CHILENO = 0.00097 EUROS")
        print(f"EL MINIMO DE CLP REQUERIDO ES DE AL MENOS: {minimo_cambio}")
        cantidad_convertir = int(input("¿QUE CANTIDAD DE CLP USTED DESEA CONVERTIR A EUR?: ")) # cantidad del usuario en pesos chilenos
        # se convertira a pesos argentinos lo cual hace que solo debamos convertir todo a pesos argentinos
        comprobacion = round(cantidad_convertir * 0.0010, 2) # pesos chilenos convertidos a dolares
        # por ultimo debemos saber si el cambio a EUROS totales es de al menos 10 DOLARES
        tasa_cambio = 0.00097 # PESOS CHILENOS A EUROS
        if saldo_actual >= comprobacion and cantidad_convertir >= minimo_cambio: # comprobamos que nuestro saldo actual si alcance y si es de minimo 10 dolares
            realizar_cambio(cantidad_convertir, comprobacion, index, tasa_cambio, opcion_escogida, moneda, saldo_convertido)
        else:
            print("ERROR VALOR DEMASIADO BAJO PARA REALIZAR OPERACION DE CAMBIO O SALDO INSUFICIENTE VUELVA A INTENTARLO DE NUEVO")
            retirar_clp(index)
    elif opcion_convertir == 3:
        print(f"USTED SELECCIONO PESO CHILENO EN TOTAL USTED TIENE: {saldo_convertido} CLP")
        opcion_escogida = "CLP"
        moneda = "TRY"
        print("LA TASA DE CAMBIO ES: 1 PESO CHILENO = 0.034 LIRAS TURCAS")
        print(f"EL MINIMO DE CLP REQUERIDO ES DE AL MENOS: {minimo_cambio}")
        cantidad_convertir = int(input("¿QUE CANTIDAD DE CLP USTED DESEA CONVERTIR A TRY?: ")) # cantidad del usuario en pesos chilenos
        # se convertira a LIRAS TURCAS lo cual hace que solo debamos convertir todo a LIRAS TURCAS
        comprobacion = round(cantidad_convertir * 0.0010, 2) # pesos chilenos convertidos a dolares
        # por ultimo debemos saber si el cambio a LIRAS TURCAS totales es de al menos 10 DOLARES
        tasa_cambio = 0.034 # PESOS CHILENOS A LIRAS TURCAS
        if saldo_actual >= comprobacion and cantidad_convertir >= minimo_cambio: # comprobamos que nuestro saldo actual si alcance y si es de minimo 10 dolares
            realizar_cambio(cantidad_convertir, comprobacion, index, tasa_cambio, opcion_escogida, moneda, saldo_convertido)
        else:
            print("ERROR VALOR DEMASIADO BAJO PARA REALIZAR OPERACION DE CAMBIO O SALDO INSUFICIENTE VUELVA A INTENTARLO DE NUEVO")
            retirar_clp(index)
    elif opcion_convertir == 4:
        print(f"USTED SELECCIONO PESO CHILENO EN TOTAL USTED TIENE: {saldo_convertido} CLP")
        opcion_escogida = "CLP"
        moneda = "GBP"
        print("LA TASA DE CAMBIO ES: 1 PESO CHILENO = 0.00083 LIRAS ESTERLINAS")
        print(f"EL MINIMO DE CLP REQUERIDO ES DE AL MENOS: {minimo_cambio}")
        cantidad_convertir = int(input("¿QUE CANTIDAD DE CLP USTED DESEA CONVERTIR A GBP?: ")) # cantidad del usuario en pesos chilenos
        # se convertira a LIBRAS ESTERLINAS lo cual hace que solo debamos convertir todo a LIBRAS ESTERLINAS
        comprobacion = round(cantidad_convertir * 0.0010, 2) # pesos chilenos convertidos a dolares
        # por ultimo debemos saber si el cambio a LIBRAS ESTERLINAS totales es de al menos 10 DOLARES
        tasa_cambio = 0.00083 # PESOS CHILENOS A LIBRAS ESTERLINAS
        if saldo_actual >= comprobacion and cantidad_convertir >= minimo_cambio: # comprobamos que nuestro saldo actual si alcance y si es de minimo 10 dolares
            realizar_cambio(cantidad_convertir, comprobacion, index, tasa_cambio, opcion_escogida, moneda, saldo_convertido)
        else:
            print("ERROR VALOR DEMASIADO BAJO PARA REALIZAR OPERACION DE CAMBIO O SALDO INSUFICIENTE VUELVA A INTENTARLO DE NUEVO")
            retirar_clp(index)
    else:
        print("SALIENDO AL MENU PRINCIPAL...")
        operaciones_banco(index)

def retirar_ars(index):
    df = pd.read_csv(ruta_database, encoding="utf-8")
    saldo_actual = df.loc[index, "saldo"] # [argumento]
    saldo_convertido = round(saldo_actual * 863.67, 2) # saldo obtenido en pesos argentinos
    minimo_cambio = 8636.71 # PESOS ARGENTINOS MINIMOS
    print(f"USTED HA SELECCIONADO PESO ARGENTINO EN TOTAL USTED TIENE: {saldo_convertido} ARS")
    print("CONVERTIR PESOS ARGENTINOS A: ")
    print("1. PESO CHILENO (CLP)")
    print("2. EURO (EUR)")
    print("3. LIRA TURCA (TRY)")
    print("4. LIBRA ESTERLINA (GBP)")
    print("5. SALIR AL MENU PRINCIPAL")
    opcion_convertir = int(input("¿A QUE TIPO DE MONEDA USTED DESEA CONVERTIR?: "))
    if opcion_convertir == 1:
        print(f"USTED SELECCIONO PESO ARGENTINO EN TOTAL USTED TIENE: {saldo_convertido} ARS")
        opcion_escogida = "ARS"
        moneda = "CLP"
        print("LA TASA DE CAMBIO ES: 1 PESO ARGENTINO = 1.12 PESOS CHILENOS")
        print(f"EL MINIMO DE ARS REQUERIDO ES DE AL MENOS: {minimo_cambio}")
        cantidad_convertir = int(input("¿QUE CANTIDAD DE ARS USTED DESEA CONVERTIR A CLP?: ")) # cantidad del usuario en pesos argentinos
        comprobacion = round(cantidad_convertir * 0.0012, 2) # pesos argentinos convertidos a dolares
        # por ultimo debemos saber si el cambio a pesos argentinos totales es de al menos 10 dolares
        tasa_cambio = 1.10 # PESOS ARGENTINOS A PESOS CHILENOS
        if saldo_actual >= comprobacion and cantidad_convertir >= minimo_cambio: # comprobamos que nuestro saldo actual si alcance y si es de minimo 10 dolares
            realizar_cambio(cantidad_convertir, comprobacion, index, tasa_cambio, opcion_escogida, moneda, saldo_convertido)
        else:
            print("ERROR VALOR DEMASIADO BAJO PARA REALIZAR OPERACION DE CAMBIO O SALDO INSUFICIENTE VUELVA A INTENTARLO DE NUEVO")
            retirar_ars(index)
    elif opcion_convertir == 2:
        print(f"USTED SELECCIONO PESO ARGENTINO EN TOTAL USTED TIENE: {saldo_convertido} ARS")
        opcion_escogida = "ARS"
        moneda = "EUR"
        print("LA TASA DE CAMBIO ES: 1 PESO ARGENTINO = 0.0011 EUROS")
        print(f"EL MINIMO DE ARS REQUERIDO ES DE AL MENOS: {minimo_cambio}")
        cantidad_convertir = int(input("¿QUE CANTIDAD DE ARS USTED DESEA CONVERTIR A EURO?: "))
        comprobacion = round(cantidad_convertir * 0.0012, 2) # pesos argentinos convertidos a dolares
        tasa_cambio = 0.0011 # PESOS ARGENTINOS A EUROS
        if saldo_actual >= comprobacion and cantidad_convertir >= minimo_cambio: # comprobamos que nuestro saldo actual si alcance y si es de minimo 10 dolares
            realizar_cambio(cantidad_convertir, comprobacion, index, tasa_cambio, opcion_escogida, moneda, saldo_convertido)
        else:
            print("ERROR VALOR DEMASIADO BAJO PARA REALIZAR OPERACION DE CAMBIO O SALDO INSUFICIENTE VUELVA A INTENTARLO DE NUEVO")
            retirar_ars(index)
    elif opcion_convertir == 3:
        print(f"USTED SELECCIONO PESO ARGENTINO EN TOTAL USTED TIENE: {saldo_convertido} ARS")
        opcion_escogida = "ARS"
        moneda = "TRY"
        print("LA TASA DE CAMBIO ES: 1 PESO ARGENTINO = 0.037 LIRAS TURCAS")
        print(f"EL MINIMO DE ARS REQUERIDO ES DE AL MENOS: {minimo_cambio}")
        cantidad_convertir = int(input("¿QUE CANTIDAD DE ARS USTED DESEA CONVERTIR A LIRAS TURCAS?: "))
        comprobacion = round(cantidad_convertir * 0.0012, 2) # pesos argentinos convertidos a dolares
        tasa_cambio = 0.037 # PESOS ARGENTINOS A LIRAS TURCAS
        if saldo_actual >= comprobacion and cantidad_convertir >= minimo_cambio: # comprobamos que nuestro saldo actual si alcance y si es de minimo 10 dolares
            realizar_cambio(cantidad_convertir, comprobacion, index, tasa_cambio, opcion_escogida, moneda, saldo_convertido)
        else:
            print("ERROR VALOR DEMASIADO BAJO PARA REALIZAR OPERACION DE CAMBIO O SALDO INSUFICIENTE VUELVA A INTENTARLO DE NUEVO")
            retirar_ars(index)
    elif opcion_convertir == 4:
        print(f"USTED SELECCIONO PESO ARGENTINO EN TOTAL USTED TIENE: {saldo_convertido} ARS")
        opcion_escogida = "ARS"
        moneda = "GBP"
        print("LA TASA DE CAMBIO ES: 1 PESO ARGENTINO = 0.037 LIBRAS ESTERLINAS")
        print(f"EL MINIMO DE ARS REQUERIDO ES DE AL MENOS: {minimo_cambio}")
        cantidad_convertir = int(input("¿QUE CANTIDAD DE ARS USTED DESEA CONVERTIR A LIBRAS ESTERLINAS?: "))
        comprobacion = round(cantidad_convertir * 0.0012, 2) # pesos argentinos convertidos a dolares
        tasa_cambio = 0.00093
        if saldo_actual >= comprobacion and cantidad_convertir >= minimo_cambio: # comprobamos que nuestro saldo actual si alcance y si es de minimo 10 dolares
            realizar_cambio(cantidad_convertir, comprobacion, index, tasa_cambio, opcion_escogida, moneda, saldo_convertido)
        else:
            print("ERROR VALOR DEMASIADO BAJO PARA REALIZAR OPERACION DE CAMBIO O SALDO INSUFICIENTE VUELVA A INTENTARLO DE NUEVO")
            retirar_ars(index)        
    else:
        print("SALIENDO AL MENU PRINCIPAL...")
        operaciones_banco(index)
        
def retirar_eur(index):
    df = pd.read_csv(ruta_database, encoding="utf-8")
    saldo_actual = df.loc[index, "saldo"] # [argumento]
    saldo_convertido = round(saldo_actual * 0.94, 2) # saldo obtenido en euros
    minimo_cambio = 9.37 # minimo EUROS
    print(f"USTED HA SELECCIONADO EURO EN TOTAL USTED TIENE: {saldo_convertido} EUR")
    print("CONVERTIR EUROS A: ")
    print("1. PESO CHILENO (CLP)")
    print("2. PESO ARGENTINO (ARS)")
    print("3. LIRA TURCA (TRY)")
    print("4. LIBRA ESTERLINA (GBP)")
    print("5. SALIR AL MENU PRINCIPAL")
    opcion_convertir = int(input("¿A QUE TIPO DE MONEDA USTED DESEA CONVERTIR?: "))
    if opcion_convertir == 1:
        print(f"USTED SELECCIONO EUROS EN TOTAL USTED TIENE: {saldo_convertido} EUR")
        opcion_escogida = "EUR"
        moneda = "CLP"
        print("LA TASA DE CAMBIO ES: 1 EURO = 1018.09 PESOS CHILENOS")
        print(f"EL MINIMO DE EUR REQUERIDO ES DE AL MENOS: {minimo_cambio}")
        cantidad_convertir = int(input("¿QUE CANTIDAD DE EUR USTED DESEA CONVERTIR A CLP?: ")) # cantidad del usuario en EUROS
        comprobacion = round(cantidad_convertir * 1.07, 2) # EUROS convertidos a dolares
        tasa_cambio = 1018.09 # EUROS A PESOS CHILENOS
        if saldo_actual >= comprobacion and cantidad_convertir >= minimo_cambio: # comprobamos que nuestro saldo actual si alcance y si es de minimo 10 dolares
            realizar_cambio(cantidad_convertir, comprobacion, index, tasa_cambio, opcion_escogida, moneda, saldo_convertido)
        else:
            print("ERROR VALOR DEMASIADO BAJO PARA REALIZAR OPERACION DE CAMBIO O SALDO INSUFICIENTE VUELVA A INTENTARLO DE NUEVO")
            retirar_eur(index)
    elif opcion_convertir == 2:
        print(f"USTED SELECCIONO EUROS EN TOTAL USTED TIENE: {saldo_convertido} EUR")
        opcion_escogida = "EUR"
        moneda = "ARS"
        print("LA TASA DE CAMBIO ES: 1 EUR = 921.67 PESOS ARGENTINOS")
        print(f"EL MINIMO DE EUR REQUERIDO ES DE AL MENOS: {minimo_cambio}")
        cantidad_convertir = int(input("¿QUE CANTIDAD DE EUR USTED DESEA CONVERTIR A ARS?: "))
        comprobacion = round(cantidad_convertir * 1.07, 2) # EUROS convertidos a dolares
        tasa_cambio = 921.67 # para convertir de EURO A PESO ARGENTINO
        if saldo_actual >= comprobacion and cantidad_convertir >= minimo_cambio: # comprobamos que nuestro saldo actual si alcance y si es de minimo 10 dolares
            realizar_cambio(cantidad_convertir, comprobacion, index, tasa_cambio, opcion_escogida, moneda, saldo_convertido)
        else:
            print("ERROR VALOR DEMASIADO BAJO PARA REALIZAR OPERACION DE CAMBIO O SALDO INSUFICIENTE VUELVA A INTENTARLO DE NUEVO")
            retirar_eur(index)
    elif opcion_convertir == 3:
        print(f"USTED SELECCIONO EUROS EN TOTAL USTED TIENE: {saldo_convertido} EUR")
        opcion_escogida = "EUR"
        moneda = "TRY"
        print("LA TASA DE CAMBIO ES: 1 EURO = 34.54 LIRAS TURCAS")
        print(f"EL MINIMO DE EUR REQUERIDO ES DE AL MENOS: {minimo_cambio}")
        cantidad_convertir = int(input("¿QUE CANTIDAD DE EUR USTED DESEA CONVERTIR A LIRAS TURCAS?: "))
        comprobacion = round(cantidad_convertir * 1.07, 2) # EUROS convertidos a dolares
        tasa_cambio = 34.54 # EUROS A LIRAS TURCAS
        if saldo_actual >= comprobacion and cantidad_convertir >= minimo_cambio: # comprobamos que nuestro saldo actual si alcance y si es de minimo 10 dolares
            realizar_cambio(cantidad_convertir, comprobacion, index, tasa_cambio, opcion_escogida, moneda, saldo_convertido)
        else:
            print("ERROR VALOR DEMASIADO BAJO PARA REALIZAR OPERACION DE CAMBIO O SALDO INSUFICIENTE VUELVA A INTENTARLO DE NUEVO")
            retirar_eur(index)
    elif opcion_convertir == 4:
        print(f"USTED SELECCIONO EUROS EN TOTAL USTED TIENE: {saldo_convertido} EUR")
        opcion_escogida = "EUR"
        moneda = "GBP"
        print("LA TASA DE CAMBIO ES: 1 EURO = 0.037 LIBRAS ESTERLINAS")
        print(f"EL MINIMO DE EUR REQUERIDO ES DE AL MENOS: {minimo_cambio}")
        cantidad_convertir = int(input("¿QUE CANTIDAD DE EUR USTED DESEA CONVERTIR A LIBRAS ESTERLINAS?: "))
        comprobacion = round(cantidad_convertir * 1.07, 2) # EUROS convertidos a dolares
        tasa_cambio = 0.86 # EUROS A LIBRAS ESTERLINAS
        if saldo_actual >= comprobacion and cantidad_convertir >= minimo_cambio: # comprobamos que nuestro saldo actual si alcance y si es de minimo 10 dolares
            realizar_cambio(cantidad_convertir, comprobacion, index, tasa_cambio, opcion_escogida, moneda, saldo_convertido)
        else:
            print("ERROR VALOR DEMASIADO BAJO PARA REALIZAR OPERACION DE CAMBIO O SALDO INSUFICIENTE VUELVA A INTENTARLO DE NUEVO")
            retirar_eur(index)        
    else:
        print("SALIENDO AL MENU PRINCIPAL...")
        operaciones_banco(index)

def retirar_try(index):
    df = pd.read_csv(ruta_database, encoding="utf-8")
    saldo_actual = df.loc[index, "saldo"] # [argumento]
    saldo_convertido = round(saldo_actual * 0.94, 2) # saldo obtenido en liras turcas
    minimo_cambio = 323.63 # minimo liras turcas
    print(f"USTED HA SELECCIONADO LIRA TURCA EN TOTAL USTED TIENE: {saldo_convertido} TRY")
    print("CONVERTIR LIRAS TURCAS A: ")
    print("1. PESO CHILENO (CLP)")
    print("2. PESO ARGENTINO (ARS)")
    print("3. EURO (EUR)")
    print("4. LIBRA ESTERLINA (GBP)")
    print("5. SALIR AL MENU PRINCIPAL")
    opcion_convertir = int(input("¿A QUE TIPO DE MONEDA USTED DESEA CONVERTIR?: "))
    if opcion_convertir == 1:
        print(f"USTED SELECCIONO LIRAS TURCAS EN TOTAL USTED TIENE: {saldo_convertido} TRY")
        opcion_escogida = "TRY"
        moneda = "CLP"
        print("LA TASA DE CAMBIO ES: 1 LIRA TURCA = 29.48 PESOS CHILENOS")
        print(f"EL MINIMO DE TRY REQUERIDO ES DE AL MENOS: {minimo_cambio}")
        cantidad_convertir = int(input("¿QUE CANTIDAD DE TRY USTED DESEA CONVERTIR A CLP?: ")) # cantidad del usuario en liras turcas
        comprobacion = round(cantidad_convertir * 0.031, 2) # liras turcas convertidos a dolares
        tasa_cambio = 29.48 # LIRAS TURCAS A PESOS CHILENOS
        if saldo_actual >= comprobacion and cantidad_convertir >= minimo_cambio: # comprobamos que nuestro saldo actual si alcance y si es de minimo 10 dolares
            realizar_cambio(cantidad_convertir, comprobacion, index, tasa_cambio, opcion_escogida, moneda, saldo_convertido)
        else:
            print("ERROR VALOR DEMASIADO BAJO PARA REALIZAR OPERACION DE CAMBIO O SALDO INSUFICIENTE VUELVA A INTENTARLO DE NUEVO")
            retirar_try(index)
    elif opcion_convertir == 2:
        print(f"USTED SELECCIONO EUROS EN TOTAL USTED TIENE: {saldo_convertido} EUR")
        opcion_escogida = "TRY"
        moneda = "ARS"
        print("LA TASA DE CAMBIO ES: 1 TRY = 26.69 PESOS ARGENTINOS")
        print(f"EL MINIMO DE TRY REQUERIDO ES DE AL MENOS: {minimo_cambio}")
        cantidad_convertir = int(input("¿QUE CANTIDAD DE TRY USTED DESEA CONVERTIR A PESOS ARGENTINOS?: "))
        comprobacion = round(cantidad_convertir * 0.031, 2) # liras turcas convertidos a dolares
        tasa_cambio = 26.69 # para convertir de lira turca a peso argentino
        if saldo_actual >= comprobacion and cantidad_convertir >= minimo_cambio: # comprobamos que nuestro saldo actual si alcance y si es de minimo 10 dolares
            realizar_cambio(cantidad_convertir, comprobacion, index, tasa_cambio, opcion_escogida, moneda, saldo_convertido)
        else:
            print("ERROR VALOR DEMASIADO BAJO PARA REALIZAR OPERACION DE CAMBIO O SALDO INSUFICIENTE VUELVA A INTENTARLO DE NUEVO")
            retirar_try(index)
    elif opcion_convertir == 3:
        print(f"USTED SELECCIONO LIRAS TURCAS EN TOTAL USTED TIENE: {saldo_convertido} TRY")
        opcion_escogida = "TRY"
        moneda = "EUR"
        print("LA TASA DE CAMBIO ES: 1 LIRA TURCA = 0.029 EUROS")
        print(f"EL MINIMO DE TRY REQUERIDO ES DE AL MENOS: {minimo_cambio}")
        cantidad_convertir = int(input("¿QUE CANTIDAD DE TRY USTED DESEA CONVERTIR A EUROS?: "))
        comprobacion = round(cantidad_convertir * 0.031, 2) # liras turcas convertidos a dolares
        tasa_cambio = 0.029 # LIRAS TURCAS A EUROS
        if saldo_actual >= comprobacion and cantidad_convertir >= minimo_cambio: # comprobamos que nuestro saldo actual si alcance y si es de minimo 10 dolares
            realizar_cambio(cantidad_convertir, comprobacion, index, tasa_cambio, opcion_escogida, moneda, saldo_convertido)
        else:
            print("ERROR VALOR DEMASIADO BAJO PARA REALIZAR OPERACION DE CAMBIO O SALDO INSUFICIENTE VUELVA A INTENTARLO DE NUEVO")
            retirar_try(index)
    elif opcion_convertir == 4:
        print(f"USTED SELECCIONO LIRAS TURCAS EN TOTAL USTED TIENE: {saldo_convertido} TRY")
        opcion_escogida = "TRY"
        moneda = "GBP"
        print("LA TASA DE CAMBIO ES: 1 LIRA TURCA = 0.025 LIBRAS ESTERLINAS")
        print(f"EL MINIMO DE TRY REQUERIDO ES DE AL MENOS: {minimo_cambio}")
        cantidad_convertir = int(input("¿QUE CANTIDAD DE TRY USTED DESEA CONVERTIR A GBP?: "))
        comprobacion = round(cantidad_convertir * 0.031, 2) # liras turcas convertidos a dolares
        tasa_cambio = 0.025 # LIRAS TURCAS A LIBRAS ESTERLINAS
        if saldo_actual >= comprobacion and cantidad_convertir >= minimo_cambio: # comprobamos que nuestro saldo actual si alcance y si es de minimo 10 dolares
            realizar_cambio(cantidad_convertir, comprobacion, index, tasa_cambio, opcion_escogida, moneda, saldo_convertido)
        else:
            print("ERROR VALOR DEMASIADO BAJO PARA REALIZAR OPERACION DE CAMBIO O SALDO INSUFICIENTE VUELVA A INTENTARLO DE NUEVO")
            retirar_try(index)        
    else:
        print("SALIENDO AL MENU PRINCIPAL...")
        operaciones_banco(index)

def retirar_gbp(index):
    df = pd.read_csv(ruta_database, encoding="utf-8")
    saldo_actual = df.loc[index, "saldo"] # [argumento]
    saldo_convertido = round(saldo_actual * 0.80, 2) # saldo obtenido en libras esterlinas
    minimo_cambio = 8.03 # minimo liras turcas
    print(f"USTED HA SELECCIONADO LIBRA ESTERLINA EN TOTAL USTED TIENE: {saldo_convertido} GBP")
    print("CONVERTIR LIBRAS ESTERLINAS A: ")
    print("1. PESO CHILENO (CLP)")
    print("2. PESO ARGENTINO (ARS)")
    print("3. EURO (EUR)")
    print("4. LIRA TURCA (TRY)")
    print("5. SALIR AL MENU PRINCIPAL")
    opcion_convertir = int(input("¿A QUE TIPO DE MONEDA USTED DESEA CONVERTIR?: "))
    if opcion_convertir == 1:
        print(f"USTED SELECCIONO LIBRA ESTERLINA EN TOTAL USTED TIENE: {saldo_convertido} GBP")
        opcion_escogida = "GBP"
        moneda = "CLP"
        print("LA TASA DE CAMBIO ES: 1 LIBRA ESTERLINA = 1188.44 PESOS CHILENOS")
        print(f"EL MINIMO DE GBP REQUERIDO ES DE AL MENOS: {minimo_cambio}")
        cantidad_convertir = int(input("¿QUE CANTIDAD DE GBP USTED DESEA CONVERTIR A CLP?: ")) # cantidad del usuario en liras turcas
        comprobacion = round(cantidad_convertir * 1.25, 2) # LIBRAS ESTERLINAS A DOLARES
        tasa_cambio = 1188.44 # LIBRAS ESTERLINAS A PESOS CHILENOS
        if saldo_actual >= comprobacion and cantidad_convertir >= minimo_cambio: # comprobamos que nuestro saldo actual si alcance y si es de minimo 10 dolares
            realizar_cambio(cantidad_convertir, comprobacion, index, tasa_cambio, opcion_escogida, moneda, saldo_convertido)
        else:
            print("ERROR VALOR DEMASIADO BAJO PARA REALIZAR OPERACION DE CAMBIO O SALDO INSUFICIENTE VUELVA A INTENTARLO DE NUEVO")
            retirar_gbp(index)
    elif opcion_convertir == 2:
        print(f"USTED HA SELECCIONADO LIBRAS ESTERLINAS EN TOTAL USTED TIENE: {saldo_convertido} GBP")
        opcion_escogida = "GBP"
        moneda = "ARS"
        print("LA TASA DE CAMBIO ES: 1 GBP = 1075.87 PESOS ARGENTINOS")
        print(f"EL MINIMO DE GBP REQUERIDO ES DE AL MENOS: {minimo_cambio}")
        cantidad_convertir = int(input("¿QUE CANTIDAD DE GBP USTED DESEA CONVERTIR A PESOS ARGENTINOS?: "))
        comprobacion = round(cantidad_convertir * 1.25, 2) # libras esterlinas a DOLARES
        tasa_cambio = 1075.87 # para convertir de lira turca a peso argentino
        if saldo_actual >= comprobacion and cantidad_convertir >= minimo_cambio: # comprobamos que nuestro saldo actual si alcance y si es de minimo 10 dolares
            realizar_cambio(cantidad_convertir, comprobacion, index, tasa_cambio, opcion_escogida, moneda, saldo_convertido)
        else:
            print("ERROR VALOR DEMASIADO BAJO PARA REALIZAR OPERACION DE CAMBIO O SALDO INSUFICIENTE VUELVA A INTENTARLO DE NUEVO")
            retirar_gbp(index)
    elif opcion_convertir == 3:
        print(f"USTED HA SELECCIONADO LIBRAS ESTERLINAS EN TOTAL USTED TIENE: {saldo_convertido} GBP")
        opcion_escogida = "GBP"
        moneda = "EUR"
        print("LA TASA DE CAMBIO ES: 1 LIBRA ESTERLINA = 1.17 EUROS")
        print(f"EL MINIMO DE GBP REQUERIDO ES DE AL MENOS: {minimo_cambio}")
        cantidad_convertir = int(input("¿QUE CANTIDAD DE GBP USTED DESEA CONVERTIR A EUROS?: "))
        comprobacion = round(cantidad_convertir * 1.25, 2) # libras esterlinas convertidos a dolares
        tasa_cambio = 1.17 # LIRAS TURCAS A EUROS
        if saldo_actual >= comprobacion and cantidad_convertir >= minimo_cambio: # comprobamos que nuestro saldo actual si alcance y si es de minimo 10 dolares
            realizar_cambio(cantidad_convertir, comprobacion, index, tasa_cambio, opcion_escogida, moneda, saldo_convertido)
        else:
            print("ERROR VALOR DEMASIADO BAJO PARA REALIZAR OPERACION DE CAMBIO O SALDO INSUFICIENTE VUELVA A INTENTARLO DE NUEVO")
            retirar_gbp(index)
    elif opcion_convertir == 4:
        print(f"USTED HA SELECCIONADO LIBRAS ESTERLINAS EN TOTAL USTED TIENE: {saldo_convertido} GBP")
        opcion_escogida = "GBP"
        moneda = "TRY"
        print("LA TASA DE CAMBIO ES: 1 LIBRA ESTERLINA = 40.31 LIRAS TURCAS")
        print(f"EL MINIMO DE GBP REQUERIDO ES DE AL MENOS: {minimo_cambio}")
        cantidad_convertir = int(input("¿QUE CANTIDAD DE GBP USTED DESEA CONVERTIR A TRY?: "))
        comprobacion = round(cantidad_convertir * 1.25, 2) # liras turcas convertidos a dolares
        tasa_cambio = 40.31 # LIBRAS ESTERLINAS A LIRAS TURCAS
        if saldo_actual >= comprobacion and cantidad_convertir >= minimo_cambio: # comprobamos que nuestro saldo actual si alcance y si es de minimo 10 dolares
            realizar_cambio(cantidad_convertir, comprobacion, index, tasa_cambio, opcion_escogida, moneda, saldo_convertido)
        else:
            print("ERROR VALOR DEMASIADO BAJO PARA REALIZAR OPERACION DE CAMBIO O SALDO INSUFICIENTE VUELVA A INTENTARLO DE NUEVO")
            retirar_gbp(index)        
    else:
        print("SALIENDO AL MENU PRINCIPAL...")
        operaciones_banco(index)

def realizar_cambio(convertir, cantidadUSD, index, tasa, opcion, moneda, total_dinero):
    df = pd.read_csv(ruta_database, encoding="utf-8")
    saldo_actual = df.loc[index, "saldo"]
    comision = saldo_actual * 0.01
    cantidad_dinero = round(convertir * tasa, 2)
    descuento_total = comision + cantidadUSD
    saldo_restante = saldo_actual - descuento_total
    print(f"SU SALDO ACTUAL ES DE: {total_dinero} {opcion} / {saldo_actual} USD")
    print(f"SU SALDO DESPUES DE LA OPERACION SERIA: {round(total_dinero - cantidadUSD, 2)} {opcion} / {round(saldo_restante, 2)} USD")
    preguntar = input(f"¿DESEA HACER LA OPERACION DE CAMBIO DE {convertir} {opcion} POR {cantidad_dinero} {moneda}? (si/no): ").lower()
    if preguntar == "si":
        df.loc[index, "saldo"] = round(saldo_restante, 2)
        df.to_csv(ruta_database, encoding='utf-8', index=False)
        print(f"LA OPERACION FUE REALIZADA CON EXITO, PUEDE RETIRAR EN SU BANCO O CAJERO AUTOMATICO MAS CERCANO LA CANTIDAD DE: {cantidad_dinero} {moneda}")
        # como solo debemos restar la cantidad de pesos chilenos insertados ya que esto es una simulacion, la cantidad de pesos argentinos seria retirado en ucajero    normalmente pero este no es un sistema de esos solo es un simulador ajaja
        # PREGUNTAR SI QUIERE HACER OTRA OPERACION EN ESE CASO VOLVER AL MENU DE CAMBIO
        repetir = input("¿DESEA REALIZAR OTRA OPERACION DE CAMBIO? (si/no): ").strip().lower()
        if repetir == "si":
            retirar_dinero_internacional(index)
        else:
            print("TERMINANDO OPERACIONES Y CERRANDO SISTEMA...")
    else:
        print("CANCELANDO OPERACION Y VOLVIENDO AL MENU PRINCIPAL")
        operaciones_banco(index)

def salir_sistema():
    print("¡MUCHAS GRACIAS POR USAR ESTE PROGRAMA!")
if preguntar_usuario_nuevo == "si":
    nuevo_usuario()
else:
    comprobar_usuario()
