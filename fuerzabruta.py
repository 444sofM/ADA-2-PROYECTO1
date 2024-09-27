import itertools
import math

def calculate_extremism(agents):
    """Calcula el extremismo basado en las opiniones de los agentes."""
   
    n = len(agents)
    sum_squared_opinions = sum(opinion ** 2 for opinion, _ in agents)
    return math.sqrt(sum_squared_opinions ) /n

def calculate_effort(agents, strategy):
    """Calcula el esfuerzo basado en las estrategias aplicadas."""
    effort = sum(math.ceil(abs(opinion) * (1 - receptivity)) for (opinion, receptivity), mod in zip(agents, strategy) if mod == 1)
    return effort

def apply_strategy(agents, strategy):
    """Aplica la estrategia de moderación a los agentes."""
    moderated_agents = [(0, receptivity) if mod == 1 else (opinion, receptivity) for (opinion, receptivity), mod in zip(agents, strategy)]
    return moderated_agents

def rocFB(agents, R_max):
    """Encuentra la mejor estrategia de moderación que minimiza el extremismo dentro del esfuerzo permitido."""
    n = len(agents)
    best_strategy = None
    min_extremism = float('inf')
    
    # Generar todas las posibles estrategias
    for strategy in itertools.product([0, 1], repeat=n):
        effort = calculate_effort(agents, strategy)
        if effort <= R_max:
            moderated_agents = apply_strategy(agents, strategy)
            extremism = calculate_extremism(moderated_agents)
            if extremism < min_extremism:
                min_extremism = extremism
                best_strategy = strategy
    
    if best_strategy is None:
        return "No applicable strategy within given effort."
    
    return best_strategy, calculate_effort(agents, best_strategy), min_extremism

# Leer datos desde el archivo
with open('Pruebas/Prueba1.txt', 'r') as file:
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

""" print(f"Datos: {datos}, R_max: {rmax}")  # Debugging line

# Ejecutar la función rocFB con los datos y R_max
fuerzab = rocFB(datos, rmax)
print(fuerzab)
 """