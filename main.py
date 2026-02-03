import os
import alumno      
import coodinador   

def limpiar_pantalla():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def menu_principal():
    while True:
        limpiar_pantalla()
        print("   SISTEMA DE GESTIÓN UNEFA - 2026")
        print("Seleccione su perfil de usuario:")
        print("1. Coordinador")
        print("2. Alumno")
        print("3. Salir del Sistema")
        
        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            limpiar_pantalla()
            coodinador.menu_coordinador()
            
        elif opcion == "2":
            limpiar_pantalla()
            print("--- ACCESO ALUMNO ---")
            nombre = input("Ingrese su nombre para entrar: ")
            print(f"Bienvenido, {nombre}")
            alumno.menu_alumno()

        elif opcion == "3":
            print("Cerrando sistema... ¡Hasta luego!")
            break
        else:
            input("Opción no válida. Presione Enter...")

if __name__ == "__main__":
    menu_principal()