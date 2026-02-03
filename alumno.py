import json
import os

# Importamos solo lo necesario de app.py
# (Asegurate que app.py esté en la misma carpeta)
from app import guardar_datos, cargar_datos as cargar_app_datos

ARCHIVO_DB = "materias.json"
MAX_UC_PERMITIDAS = 50  # Límite de unidades de crédito definido en tu proyecto

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

def inscribir_materia(archivo_usuario):
    oferta_materias = cargar_json(ARCHIVO_DB)
    mis_inscripciones = cargar_json(archivo_usuario) # Cargamos SU archivo personal
    
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

    # Verificar si ya tiene la materia inscrita
    for mi_materia in mis_inscripciones:
        if mi_materia["codigo_materia"] == materia_encontrada["codigo_materia"]:
            print("Ya tienes inscrita esta materia.")
            return

    # --- NUEVA VALIDACIÓN: UNIDADES DE CRÉDITO (UC) ---
    # Calculamos cuántas UC tiene ya inscritas sumando desde la oferta
    total_uc_inscritas = 0
    
    for inscrita in mis_inscripciones:
        # Buscamos la materia en la oferta para saber sus UC oficiales
        for m in oferta_materias:
            if m["codigo_materia"] == inscrita["codigo_materia"]:
                # Si el json no tiene "uc", asumimos 3 por defecto
                total_uc_inscritas += m.get("uc", 3)
                break
    
    # Obtenemos las UC de la materia nueva (3 si no existe el campo)
    uc_nueva = materia_encontrada.get("uc", 3)
    
    print(f"UC Actuales: {total_uc_inscritas} + Nueva: {uc_nueva} = Total: {total_uc_inscritas + uc_nueva}")
    
    if total_uc_inscritas + uc_nueva > MAX_UC_PERMITIDAS:
        print(f"¡Error! No puedes inscribir más de {MAX_UC_PERMITIDAS} UC.")
        return
    # --- FIN VALIDACIÓN UC ---

    # --- INICIO DE VALIDACIÓN DE CRUCE DE HORARIOS ---
    hay_cruce = False 
    
    for inscrita in mis_inscripciones:
        # 1. ¿Coinciden los días?
        dias_coinciden = False
        dia_conflicto = ""
        
        for dia_nuevo in materia_encontrada["dia"]:
            for dia_inscrito in inscrita["dia"]:
                if dia_nuevo == dia_inscrito:
                    dias_coinciden = True
                    dia_conflicto = dia_nuevo
                    break 
            if dias_coinciden:
                break
        
        # 2. Si los días coinciden, revisamos si chocan las horas (bloques)
        if dias_coinciden:
            for bloque_nuevo in materia_encontrada["bloques"]:
                for bloque_inscrito in inscrita["bloques"]:
                    if bloque_nuevo == bloque_inscrito:
                        hay_cruce = True
                        print(f"¡Error! Choque de horario con '{inscrita['materia']}'.")
                        print(f"Conflicto en: {dia_conflicto}, bloque {bloque_nuevo}.")
                        break 
            if hay_cruce:
                break

    if hay_cruce:
        return 
    # --- FIN DE VALIDACIÓN ---

    # Si todo está bien, procedemos a inscribir
    materia_encontrada["cupo"] -= 1
    
    # Guardamos el cambio de cupo en la DB general
    guardar_json(ARCHIVO_DB, oferta_materias)

    nueva_inscripcion = {
        "materia": materia_encontrada["materia"],
        "codigo_materia": materia_encontrada["codigo_materia"],
        "dia": materia_encontrada["dia"],
        "bloques": materia_encontrada["bloques"]
    }
    mis_inscripciones.append(nueva_inscripcion)
    
    # Guardamos en el archivo personal del usuario
    guardar_json(archivo_usuario, mis_inscripciones)

    print(f"¡Inscripción exitosa en {materia_encontrada['materia']}!")

def retirar_materia(archivo_usuario):
    mis_inscripciones = cargar_json(archivo_usuario)
    oferta_materias = cargar_json(ARCHIVO_DB) # Cargamos la oferta para devolver el cupo

    if not mis_inscripciones:
        print("\nNo tienes materias inscritas para retirar.")
        return

    print("\n--- RETIRAR MATERIA ---")
    # Mostrar lista numerada
    print(f"{'CÓDIGO':<10} | {'MATERIA'}")
    print("-" * 30)
    for m in mis_inscripciones:
        print(f"{m['codigo_materia']:<10} | {m['materia']}")
    print("-" * 30)

    codigo = input("Ingrese el código de la materia a retirar: ").upper()

    # Buscar en inscripciones del alumno
    materia_a_borrar = None
    indice_borrar = -1
    
    for i, m in enumerate(mis_inscripciones):
        if m["codigo_materia"] == codigo:
            materia_a_borrar = m
            indice_borrar = i
            break
    
    if not materia_a_borrar:
        print("Error: No tienes inscrita esa materia.")
        return

    # 1. Eliminar de la lista del alumno
    mis_inscripciones.pop(indice_borrar)
    guardar_json(archivo_usuario, mis_inscripciones)

    # 2. Devolver el cupo a la base de datos general
    encontrada_en_db = False
    for m in oferta_materias:
        if m["codigo_materia"] == codigo:
            m["cupo"] += 1
            encontrada_en_db = True
            break
    
    if encontrada_en_db:
        guardar_json(ARCHIVO_DB, oferta_materias)
        print(f"Materia {codigo} retirada. Cupo devuelto al sistema.")
    else:
        print(f"Materia retirada de tu horario, pero no se encontró en el catálogo (no se devolvió cupo).")

def generar_horario_visual(archivo_usuario):
    materias_inscritas = cargar_json(archivo_usuario) 

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
                        # Validamos que no se salga del rango por si acaso
                        if fila < len(mi_horario):
                            mi_horario[fila][columna] = nombre[:10] 

    print("\n" + "="*80)
    for fila in mi_horario:
        print(f"{fila[0]:12} | {fila[1]:12} | {fila[2]:12} | {fila[3]:12} | {fila[4]:12} | {fila[5]:12}|")
    print("="*80)

def menu_alumno():
    cedula = input("\nIngrese su Cédula de Identidad para gestionar su horario: ")
    archivo_personal = f"horario_{cedula}.json"
    
    while True:
        print(f"\n--- SISTEMA ALUMNO UNEFA (Usuario: {cedula}) ---")
        print("1. Inscribir Materia")
        print("2. Ver Horario")
        print("3. Retirar Materia")
        print("4. Salir")
        
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            inscribir_materia(archivo_personal)
        elif opcion == "2":
            generar_horario_visual(archivo_personal)
        elif opcion == "3":
            retirar_materia(archivo_personal)
        elif opcion == "4":
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu_alumno()
