import os
import json
import time

# Importamos los módulos (asumiendo que ya tienes tus archivos alumno.py y coodinador.py)
import alumno
import coodinador

if __name__ == "__main__":
    
    # --- CARGA DE USUARIOS (Sin funciones, directo al flujo) ---
    usuarios_db = {}
    if os.path.exists("usuarios.json"):
        try:
            with open("usuarios.json", 'r', encoding='utf-8') as archivo:
                usuarios_db = json.load(archivo)
        except:
            print("Error: No se pudo leer usuarios.json")
            usuarios_db = {}
    else:
        print("Advertencia: No existe el archivo usuarios.json")

    # --- CICLO PRINCIPAL DEL LOGIN ---
    while True:
        # Limpiar pantalla (compatible con Windows y Linux/Mac)
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

        print("=========================================")
        print("   SISTEMA DE GESTIÓN UNEFA - 2026")
        print("=========================================")
        print("1. Coordinador")
        print("2. Alumno")
        print("3. Profesor")
        print("4. Salir")
        print("=========================================")
        
        opcion_rol = input("Seleccione su perfil (1-4): ")

        if opcion_rol == "4":
            print("Cerrando sistema... ¡Hasta luego!")
            break

        # Definimos el rol esperado según la opción
        rol_esperado = ""
        if opcion_rol == "1":
            rol_esperado = "coordinador"
        elif opcion_rol == "2":
            rol_esperado = "alumno"
        elif opcion_rol == "3":
            rol_esperado = "profesor"
        else:
            input("Opción no válida. Presione Enter para intentar de nuevo...")
            continue # Vuelve al inicio del while

        print(f"\n--- INGRESO: {rol_esperado.upper()} ---")

        # --- VALIDACIÓN DE TIPO DE DOCUMENTO ---
        # Solo pedimos V/E/P si NO es el usuario especial 'admin'
        # Pero primero pedimos el dato general para ver qué es
        
        prefijo_doc = ""
        # Lógica para pedir V/E/P
        while True:
            tipo_input = input("Tipo de Documento (V/E/P) [o 'A' para Admin]: ").upper()
            if tipo_input in ["V", "E", "P"]:
                prefijo_doc = tipo_input
                break
            elif tipo_input == "A":
                # Caso especial para entrar como 'admin' (que está en tu json)
                prefijo_doc = "ADMIN"
                break
            else:
                print("Error: Debe escribir V, E o P.")
        
        usuario_ingresado = input("Ingrese Cédula/Usuario: ")
        clave_ingresada = input("Ingrese Contraseña: ")

        # --- LÓGICA DE VERIFICACIÓN (El Corazón del Login) ---
        usuario_valido = False
        
        # 1. ¿Existe el usuario en el JSON?
        if usuario_ingresado in usuarios_db:
            datos_usuario = usuarios_db[usuario_ingresado]
            
            # 2. ¿La clave coincide?
            if datos_usuario["clave"] == clave_ingresada:
                
                # 3. ¿El rol coincide con el que seleccionó en el menú?
                if datos_usuario["rol"] == rol_esperado:
                    usuario_valido = True
                else:
                    print(f"\nError: Este usuario no tiene permisos de {rol_esperado}.")
            else:
                print("\nError: Contraseña incorrecta.")
        else:
            print("\nError: Usuario no encontrado en la base de datos.")

        # --- REDIRECCIÓN ---
        if usuario_valido:
            print(f"\n¡Bienvenido, usuario {usuario_ingresado}!")
            time.sleep(1.5) # Pequeña pausa para que se vea el mensaje

            # Limpiamos pantalla antes de entrar al módulo
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')

            if rol_esperado == "coordinador":
                coodinador.menu_coordinador()
            
            elif rol_esperado == "alumno":
                # NOTA: Si usaste mi código anterior de alumno.py, 
                # este menú te volverá a pedir la cédula.
                # Si quisieras pasarla directo, tendrías que modificar menu_alumno para recibir argumentos.
                # Por ahora, respetamos la estructura de archivos que tienes.
                alumno.menu_alumno()
                
            elif rol_esperado == "profesor":
                print("El módulo de profesor aún está en construcción.")
                input("Presione Enter para volver...")
        
        else:
            # Si falló el login
            input("\nPresione Enter para volver a intentar...")
