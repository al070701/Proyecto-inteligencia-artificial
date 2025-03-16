import heapq
import random

# Parámetros
N = 15  # Número de habitaciones/pacientes
tiempo_atencion = 16  # Minutos que tarda atender a un paciente

# Definición de estados de gravedad
gravedades = {"crítico": 5, "medio": 30, "leve": 60}

# Generar datos aleatorios para los pacientes
pacientes = []
for i in range(N):
    gravedad = random.choice(list(gravedades.keys()))
    tiempo_espera = random.randint(0, 60)  # Minutos de espera aleatorios hasta 60 min
    pacientes.append({
        "id": i,
        "gravedad": gravedad,
        "tiempo_espera": tiempo_espera,
        "tiempo_traslado": random.randint(1, 10)  # Minutos aleatorios de traslado
    })

# Definición de la función heurística
def heuristica(paciente):
    return paciente["tiempo_traslado"] - paciente["tiempo_espera"] + gravedades[paciente["gravedad"]]

# Implementación del algoritmo A*
def a_estrella(pacientes):
    heap = []
    atendidos = set()
    tiempo_total = 0
    orden_atencion = []
    
    # Insertar todos los pacientes en una cola de prioridad basada en la heurística
    for paciente in pacientes:
        print(heuristica(paciente))
        heapq.heappush(heap, (heuristica(paciente), paciente["id"], paciente))
    
    while heap:
        _, _, paciente = heapq.heappop(heap)
        if paciente["id"] in atendidos:
            continue
        
        # Atender al paciente
        atendidos.add(paciente["id"])
        tiempo_total += paciente["tiempo_traslado"] + tiempo_atencion
        orden_atencion.append((paciente["id"], paciente["gravedad"], paciente["tiempo_traslado"], paciente["tiempo_espera"], tiempo_total))
        
        # Actualizar tiempos de espera de los pacientes restantes
        for p in pacientes:
            if p["id"] not in atendidos:
                p["tiempo_espera"] += tiempo_atencion
                heapq.heappush(heap, (heuristica(p), p["id"], p))
    
    return tiempo_total, orden_atencion

# Ejecutar el algoritmo
tiempo_final, orden_atencion = a_estrella(pacientes)
print(f"Tiempo total requerido para atender a todos los pacientes: {tiempo_final} minutos")
print("\nOrden en que se atendieron los pacientes:")
print("ID | Gravedad | Traslado | Espera Inicial | Tiempo Acumulado")
for paciente in orden_atencion:
    print(f"{paciente[0]:2} | {paciente[1]:8} | {paciente[2]:8} | {paciente[3]:14} | {paciente[4]:16}")
