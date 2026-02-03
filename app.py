import json
import os

ARCHIVO_DB = "materias.json"

bhoras = {
    0: "7:00 - 7:45", 1: "7:45 - 8:30", 2: "8:30 - 9:15", 3: "9:15 - 10:00",
    4: "10:00 - 10:45", 5: "10:45 - 11:30", 6: "11:30 - 12:15", 7: "12:15 - 13:00"
}

datos_iniciales = [
    {
        "codigo_materia": "MAT0101", "materia": "Matematicas I", 
        "dia": [], "cupo": 0, "bloques": [], "seccion": "", "activa": False
    },
    {
        "codigo_materia": "FIS0101", "materia": "Fisica I", 
        "dia": [], "cupo": 0, "bloques": [], "seccion": "D1", "activa": False
    },
    {
        "codigo_materia": "QUI0101", "materia": "Quimica I", 
        "dia": [], "cupo": 0, "bloques": [], "seccion": "D1", "activa": False
    },
    {
        "codigo_materia": "LOG0101", "materia": "Geometría analítica",
        "dia": [], "cupo": 0, "bloques": [], "seccion": "D1", "activa": False
    }
]

def cargar_datos():
    if os.path.exists(ARCHIVO_DB):
        try:
            with open(ARCHIVO_DB, "r", encoding='utf-8') as archivo:
                return json.load(archivo)
        except:
            return datos_iniciales
    else:
        # Retornamos datos iniciales si no existe, sin imprimir nada para no ensuciar la terminal
        return datos_iniciales

def guardar_datos(lista_materias):
    with open(ARCHIVO_DB, "w", encoding='utf-8') as archivo:
        json.dump(lista_materias, archivo, indent=4)

def crearoferta_materias():
    oferta_materias = cargar_datos() # Cargamos los datos DENTRO de la función
    print ("\n--- CREAR OFERTA DE MATERIAS ---")

    codigo = input("Ingrese el código de la materia: ")
    materia_encontrada = None
    
    for materia in oferta_materias:
        if materia["codigo_materia"] == codigo:
            materia_encontrada = materia
            break
        elif materia["materia"] == codigo:
            materia_encontrada = materia
            break 
            
    if not materia_encontrada:
        print(" Código no encontrado en el catálogo.")
        return 

    print(f" Editando: {materia_encontrada['materia']}")

    dia_input = input("Ingrese el día (ej, Lunes): ").capitalize()
    if dia_input in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]:
        materia_encontrada["dia"] = [dia_input]
        print(f"   -> Día {dia_input} guardado.")
    else:
        print(" Día inválido.")
        return

    try:
        cupo = int(input("Ingrese el cupo (Máx 50): "))
        if cupo <= 0: 
            print(" El cupo debe ser positivo.")
            return
        elif cupo > 50: 
            print(" El cupo máximo es 50.")
            return
        else: 
            materia_encontrada["cupo"] = cupo
            print(f"   -> Cupo {cupo} guardado.")
    except ValueError:
        print(" Error: Ingrese solo números.")
        return

    entrada_bloques = input("Ingrese los bloques horarios (ej. 0,1): ")
    try:
        lista_bloques = [int(x) for x in entrada_bloques.split(",")]
        bloques_validos = []
        for num in lista_bloques:
            if num in bhoras:
                bloques_validos.append(num)
            else:
                print(f" Bloque {num} no existe.")
        
        if bloques_validos:
            materia_encontrada["bloques"] = bloques_validos 
            print("Bloques guardados.")
        else:
            print(" No se guardaron bloques válidos.")
            return
    except ValueError:
        print(" Error en formato de horas.")
        return

    seccion = input("Ingrese la sección (Enter para default): ")
    if seccion != "":
        materia_encontrada["seccion"] = seccion 

    materia_encontrada["activa"] = True 

    print("\n--- ASÍ QUEDÓ TU MATERIA ---")
    print(f"Materia: {materia_encontrada['materia']}")
    print(f"Código:  {materia_encontrada['codigo_materia']}")
    print(f"Cupo:    {materia_encontrada['cupo']}")
    print(f"Día:     {materia_encontrada['dia']}")
    print(f"Bloques: {materia_encontrada['bloques']}")
    print(f"Activa:  {materia_encontrada['activa']}")
    
    guardar_datos(oferta_materias)
    print(" ¡Cambios guardados en materias.json!")

# ESTO ES LO IMPORTANTE: Solo corre si ejecutas app.py directamente
if __name__ == "__main__":
    crearoferta_materias()