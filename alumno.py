import json
import os

# Importamos solo lo necesario y con cuidado
from app import guardar_datos, cargar_datos as cargar_app_datos

ARCHIVO_DB = "materias.json"          
ARCHIVO_ESTUDIANTE = "horario_estudiante.json" 

def cargar_json(nombre_archivo):
    if os.path.exists(nombre_archivo):
        try:
            with open(nombre_archivo, "r", encoding='utf-8') as archivo:
                return json.load(archivo)
        except:
            return []
    return []

def guardar_json(nombre_archivo, datos):
    with open(nombre_archivo, "w", encoding='utf-8') as archivo:
        json.dump(datos, archivo, indent=4)

def inscribir_materia():
    oferta_materias = cargar_json(ARCHIVO_DB)
    mis_inscripciones = cargar_json(ARCHIVO_ESTUDIANTE)
    
    if not oferta_materias:
        print("No hay oferta de materias cargada.")
        return

    print("\n--- INSCRIPCIÓN ---")
    codigo = input("Ingrese el código o nombre de la materia: ").upper()

    materia_encontrada = None
    for materia in oferta_materias:
        if materia["codigo_materia"] == codigo or materia["materia"].upper() == codigo:
            materia_encontrada = materia
            break 

    if not materia_encontrada:
        print("Materia no encontrada en el catálogo.")
        return

    if not materia_encontrada["activa"]:
        print(f"La materia '{materia_encontrada['materia']}' no está activa.")
        return

    if materia_encontrada["cupo"] <= 0:
        print("No quedan cupos disponibles.")
        return

    for mi_materia in mis_inscripciones:
        if mi_materia["codigo_materia"] == materia_encontrada["codigo_materia"]:
            print("Ya tienes inscrita esta materia.")
            return

    materia_encontrada["cupo"] -= 1
    # Guardamos en la DB general (usamos la función que importamos o la local, ambas sirven)
    guardar_json(ARCHIVO_DB, oferta_materias)

    nueva_inscripcion = {
        "materia": materia_encontrada["materia"],
        "codigo_materia": materia_encontrada["codigo_materia"],
        "dia": materia_encontrada["dia"],
        "bloques": materia_encontrada["bloques"]
    }
    mis_inscripciones.append(nueva_inscripcion)
    guardar_json(ARCHIVO_ESTUDIANTE, mis_inscripciones)

    print(f"¡Inscripción exitosa en {materia_encontrada['materia']}!")

def generar_horario_visual():
    materias_inscritas = cargar_json(ARCHIVO_ESTUDIANTE)

    if not materias_inscritas:
        print("\nNo tienes materias inscritas aún.")
        return
    horario_base = [
        ["HORA",      "LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"], 
        ["7:00-7:45", "---",   "---",    "---",       "---",    "---"],     
        ["7:45-8:30", "---",   "---",    "---",       "---",    "---"],     
        ["8:30-9:15", "---",   "---",    "---",       "---",    "---"],     
        ["9:15-10:00","---",   "---",    "---",       "---",    "---"],     
        ["10:00-10:45","---",  "---",    "---",       "---",    "---"],
        ["10:45-11:30","---",  "---",    "---",       "---",    "---"]
    ]
    mi_horario = [fila[:] for fila in horario_base]

    mapa_dias = {"Lunes": 1, "Martes": 2, "Miércoles": 3, "Miercoles": 3, "Jueves": 4, "Viernes": 5}
    mapa_bloques = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6} 

    print("\nGenerando horario basado en tus inscripciones...")
    
    for materia in materias_inscritas:
        nombre = materia["materia"]
        lista_dias = materia["dia"] 
        lista_bloques = materia["bloques"]

        for dia in lista_dias:
            if dia in mapa_dias:
                columna = mapa_dias[dia] 
                for bloque in lista_bloques:
                    if bloque in mapa_bloques:
                        fila = mapa_bloques[bloque]
                        mi_horario[fila][columna] = nombre[:10] # Cortamos el nombre para que quepa

    print("\n" + "="*80)
    for fila in mi_horario:
        print(f"{fila[0]:12} | {fila[1]:12} | {fila[2]:12} | {fila[3]:12} | {fila[4]:12} | {fila[5]:12}|")
    print("="*80)

def menu_alumno():
    while True:
        print("\n--- SISTEMA ALUMNO UNEFA ---")
        print("1. Inscribir Materia")
        print("2. Ver Horario")
        print("3. Salir")
        
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            inscribir_materia()
        elif opcion == "2":
            generar_horario_visual()
        elif opcion == "3":
            break
        else:
            print("Opción no válida.")

# ESTO ES LO IMPORTANTE: Solo corre si ejecutas alumno.py directamente
if __name__ == "__main__":
    menu_alumno()