import math

def calculate_extremism(agents):
    """Calcula el extremismo basado en las opiniones de los agentes."""
    n = len(agents)
    sum_squared_opinions = sum(opinion ** 2 for opinion, _ in agents)
    return math.sqrt(sum_squared_opinions) / n

def calculate_effort(agents, strategy):
    """Calcula el esfuerzo basado en las estrategias aplicadas."""
    # Usar la función techo (math.ceil) para calcular el esfuerzo
    effort = sum(math.ceil(abs(opinion) * (1 - receptivity)) for (opinion, receptivity), mod in zip(agents, strategy) if mod == 1)
    return effort

def apply_strategy(agents, strategy):
    """Aplica la estrategia de moderación a los agentes."""
    moderated_agents = [(0, receptivity) if mod == 1 else (opinion, receptivity) for (opinion, receptivity), mod in zip(agents, strategy)]
    return moderated_agents

def voraz_modex(agents, R_max): 
    """Algoritmo voraz que prioriza |opinion| / (1 - receptividad) dentro del esfuerzo permitido."""
    # Crear una lista de diccionarios para compatibilidad con voraz_modex
    agentes_ordenados = sorted(agents, key=lambda x: abs(x[0]) / (1 - x[1]), reverse=True)
    
    estrategia = [0] * len(agents)  # Inicialmente, ningún agente está moderado
    esfuerzo_total = 0
    extremismo_total = 0
    
    for i, (opinion, receptividad) in enumerate(agentes_ordenados):
        # Calcular el costo de moderación usando la función techo
        costo_moderacion = math.ceil(abs(opinion) * (1 - receptividad))
        
        # Si aún queda presupuesto, moderamos al agente
        if esfuerzo_total + costo_moderacion <= R_max:
            esfuerzo_total += costo_moderacion
            estrategia[i] = 1  # Marcamos al agente como moderado
            extremismo_total += 0  # El extremismo de este agente se reduce a 0
        else:
            extremismo_total += opinion ** 2  # No se modera, su extremismo sigue igual
    
    # Calcular el extremismo de la red después de aplicar la estrategia
    extremismo_red_moderada = math.sqrt(extremismo_total) / len(agents)
    
    return estrategia, esfuerzo_total, extremismo_red_moderada

# Leer datos desde el archivo
with open('Pruebas/Prueba45.txt', 'r') as file:
    leer = file.readlines()

# Leer la cantidad de agentes
agentnumber = int(leer[0].strip())

# Leer el valor máximo de esfuerzo permitido
rmax = int(leer[-1].strip())

# Convertir las líneas en una lista de tuplas, omitiendo la primera línea
datos = []
for line in leer[1:agentnumber + 1]:
    line = line.strip()
    if line:
        # Convertir la línea a una tupla (opinion, receptivity)
        elementos = line.split(',')
        datos.append((int(elementos[0]), float(elementos[1])))

print(f"Datos: {datos}, R_max: {rmax}")  # Línea para depuración

# Ejecutar la función voraz_modex con los datos y R_max
greedy_result = voraz_modex(datos, rmax)
print(greedy_result)
