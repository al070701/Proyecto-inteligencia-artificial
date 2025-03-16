import heapq
import networkx as nx
import random
from DibujoGrafo import InterfazGrafo

# Parámetros
N = 14  # Número de habitaciones/pacientes
tiempo_atencion = 15  # Minutos que tarda atender a un paciente

# Definición de estados de gravedad
gravedades = {"crítico": 5, "medio": 30, "leve": 60}

# Generar habitaciones únicas para los pacientes
habitaciones_disponibles = random.sample(range(1, N + 1), N)  # N habitaciones únicas

# Generar datos aleatorios para los pacientes
pacientes = []
for i in range(N):
    gravedad = random.choice(list(gravedades.keys()))
    tiempo_espera = random.randint(1, 60)  # Minutos de espera aleatorios (evitar división por 0)
    habitacion = habitaciones_disponibles[i]  # Asignar habitación única
    pacientes.append({
        "id": i,
        "gravedad": gravedad,
        "tiempo_espera": tiempo_espera,
        "habitacion": habitacion
    })

# Definición de la función heurística
def heuristica(paciente, habitacion_actual):
    distancia = abs(habitacion_actual - paciente["habitacion"])
    return distancia + (1 / paciente["tiempo_espera"]) + gravedades[paciente["gravedad"]]

# Implementación del algoritmo A*
def a_estrella(pacientes):
    heap = []
    atendidos = set()
    tiempo_total = 0
    orden_atencion = []
    habitacion_actual = 1  # Se asume que el inicio es la habitación 1
    
    # Insertar todos los pacientes en una cola de prioridad basada en la heurística
    for paciente in pacientes:
        heapq.heappush(heap, (heuristica(paciente, habitacion_actual), 0, paciente["id"], paciente))
    
    while heap:
        _, costo_acumulado, _, paciente = heapq.heappop(heap)
        if paciente["id"] in atendidos:
            continue
        
        # Calcular distancia de traslado
        distancia_traslado = abs(habitacion_actual - paciente["habitacion"])
        
        # Atender al paciente
        atendidos.add(paciente["id"])
        tiempo_total += distancia_traslado + tiempo_atencion
        orden_atencion.append((paciente["id"], paciente["gravedad"], distancia_traslado, paciente["tiempo_espera"], tiempo_total, paciente["habitacion"]))
        
        # Actualizar la habitación actual
        habitacion_actual = paciente["habitacion"]
        
        # Actualizar tiempos de espera de los pacientes restantes
        for p in pacientes:
            if p["id"] not in atendidos:
                p["tiempo_espera"] += tiempo_atencion
                nuevo_costo = costo_acumulado + abs(habitacion_actual - p["habitacion"])
                heapq.heappush(heap, (nuevo_costo + heuristica(p, habitacion_actual), nuevo_costo, p["id"], p))
    
    return tiempo_total, orden_atencion

# Ejecutar el algoritmo
total_tiempo, orden_atencion = a_estrella(pacientes)
print(f"Tiempo total requerido para atender a todos los pacientes: {total_tiempo} minutos")
print("\nOrden en que se atendieron los pacientes:")
print("ID | Gravedad | Distancia | Espera Inicial | Habitación | Tiempo Acumulado")
for paciente in orden_atencion:
    print(f"{paciente[0]:2} | {paciente[1]:8} | {paciente[2]:9} | {paciente[3]:14} | {paciente[5]:10} | {paciente[4]:16}")


hospital = nx.DiGraph()
for pacientes in range(N):
    hospital.add_node(f"Paciente{pacientes}")

posiciones = {
    "Paciente0": (-0.8, 1), "Paciente1": (-0.6, 0.65), "Paciente2": (-.3, .9),
    "Paciente3": (-0.2, 0.55), "Paciente4": (-.9, 0.9), "Paciente5": (-1, 0.7),
    "Paciente6": (-0.55, .45), "Paciente7": (-.9, 0.4), "Paciente8": (-0.8, 0.3),
    "Paciente9": (-0.7, 0.55), "Paciente10": (-0.71, 0.05), "Paciente11": (-0.55, .1),
    "Paciente12": (-.3, 0.2), "Paciente13": (-.1, 0.4), "Paciente14": (0, 0.3)
}


interfaz = InterfazGrafo(hospital, posiciones)
interfaz.actualizar_ruta(orden_atencion)
interfaz.ejecutar()

