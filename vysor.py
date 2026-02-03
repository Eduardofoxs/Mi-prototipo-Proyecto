import json
import os
import time

ARCHIVO_DB = "materias.json"

def cargar_datos():
    if os.path.exists(ARCHIVO_DB):
        try:
            with open(ARCHIVO_DB, 'r', encoding='utf-8') as archivo:
                return json.load(archivo)
        except:
            return []
    return []

def limpiar_pantalla():

    os.system('cls' if os.name == 'nt' else 'clear')

def iniciar_monitor():
    print("Iniciando monitor de base de datos...")
    time.sleep(1)
    
    while True:

        limpiar_pantalla()

        materias = cargar_datos()
        
        print("="*60)
        print(f"MONITOR DE: {ARCHIVO_DB}")
        print("    (Presiona Ctrl + C para salir)")
        print("="*60)
        
        if not materias:
            print("El archivo está vacío o no existe.")
        else:
            print(f"{'CÓDIGO':<10} | {'MATERIA':<20} | {'CUPO':<5} | {'ESTADO'}")
            print("-" * 60)
            
            for m in materias:
                # Color visual simple: Si hay cupo muestra numero, si es 0 avisa
                cupo_visual = f"{m['cupo']}" if m['cupo'] > 0 else " LLENO"
                estado = "ON" if m['activa'] else "OFF"
                
                print(f"{m['codigo_materia']:<10} | {m['materia']:<20} | {cupo_visual:<7} | {estado}")
        
        print("="*60)
        print(f"Última actualización: {time.strftime('%H:%M:%S')}")
        time.sleep(3)

if __name__ == "__main__":
    iniciar_monitor()