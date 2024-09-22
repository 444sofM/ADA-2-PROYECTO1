import math

def calculate_extremism(agents):
    """Calcula el extremismo basado en las opiniones de los agentes."""
    n = len(agents)
    sum_squared_opinions = sum(opinion ** 2 for opinion, _ in agents)
    return math.sqrt(sum_squared_opinions) / n

def calculate_effort(agents, strategy):
    """Calcula el esfuerzo basado en las estrategias aplicadas."""
    effort = sum(abs(opinion) * (1 - receptivity) for (opinion, receptivity), mod in zip(agents, strategy) if mod == 1)
    return effort

def apply_strategy(agents, strategy):
    """Aplica la estrategia de moderación a los agentes."""
    moderated_agents = [(0, receptivity) if mod == 1 else (opinion, receptivity) for (opinion, receptivity), mod in zip(agents, strategy)]
    return moderated_agents

def modexGreedy(agents, R_max):
    """Algoritmo voraz para moderar las opiniones más extremas dentro del esfuerzo permitido."""
    # Ordenar los agentes por la magnitud de sus opiniones de manera descendente
    sorted_agents = sorted(enumerate(agents), key=lambda x: abs(x[1][0]), reverse=True)
    
    n = len(agents)
    strategy = [0] * n
    current_effort = 0

    for i, (index, (opinion, receptivity)) in enumerate(sorted_agents):
        effort_to_moderate = abs(opinion) * (1 - receptivity)
        
        if current_effort + effort_to_moderate <= R_max:
            # Moderar esta opinión si el esfuerzo está dentro del límite
            strategy[index] = 1
            current_effort += effort_to_moderate

    moderated_agents = apply_strategy(agents, strategy)
    extremism = calculate_extremism(moderated_agents)
    
    return strategy, current_effort, extremism

# Leer datos desde el archivo
with open('Pruebas/Prueba3.txt', 'r') as file:
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

# Ejecutar la función modexGreedy con los datos y R_max
greedy_result = modexGreedy(datos, rmax)
print(greedy_result)
