import json
import os

ARCHIVO_ESTUDIANTE = "horario_estudiante.json"

horario_base = [
    ["HORA",      "LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"], 
    ["7:00-7:45", "---",   "---",    "---",       "---",    "---"],     
    ["7:45-8:30", "---",   "---",    "---",       "---",    "---"],     
    ["8:30-9:15", "---",   "---",    "---",       "---",    "---"],     
    ["9:15-10:00","---",   "---",    "---",       "---",    "---"],     
]

def cargar_materias_inscritas():
    if os.path.exists(ARCHIVO_ESTUDIANTE):
        with open(ARCHIVO_ESTUDIANTE, "r") as f:
            return json.load(f)
    return []

def generar_horario_visual():
    materias_inscritas = cargar_materias_inscritas()

    mi_horario = [fila[:] for fila in horario_base]

    mapa_dias = {
        "Lunes": 1, 
        "Martes": 2, 
        "Miércoles": 3, "Miercoles": 3, 
        "Jueves": 4, 
        "Viernes": 5
    }
    mapa_bloques = {
        0: 1, 
        1: 2, 
        2: 3, 
        3: 4
    }
    print("\nGenerando horario basado en tus inscripciones...")
    
    for materia in materias_inscritas:
        nombre = materia["materia"]
        lista_dias = materia["dia"] 
        lista_bloques = materia["bloques"]

        for dia in lista_dias:
            if dia in mapa_dias:
                columna_destino = mapa_dias[dia] 

                for bloque in lista_bloques:
                    if bloque in mapa_bloques:
                        fila_destino = mapa_bloques[bloque]
                        mi_horario[fila_destino][columna_destino] = nombre

    print("\n" + "="*60)
    for fila in mi_horario:
        print(f"{fila[0]:12} | {fila[1]:10} | {fila[2]:10} | {fila[3]:10} | {fila[4]:10} | {fila[5]:10}|")
    print("="*60)

generar_horario_visual()
