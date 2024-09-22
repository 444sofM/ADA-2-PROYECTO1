import math

def calculate_extremism(agents):
    """Calcula el extremismo basado en las opiniones de los agentes."""
    n = len(agents)
    sum_squared_opinions = sum(opinion ** 2 for opinion, _ in agents)
    return math.sqrt(sum_squared_opinions) / n  # Dividir después de la raíz

def calculate_effort(agents, strategy):
    """Calcula el esfuerzo basado en las estrategias aplicadas."""
    effort = sum(abs(opinion) * (1 - receptivity) for (opinion, receptivity), mod in zip(agents, strategy) if mod == 1)
    return effort

def apply_strategy(agents, strategy):
    """Aplica la estrategia de moderación a los agentes."""
    moderated_agents = [(0, receptivity) if mod == 1 else (opinion, receptivity) for (opinion, receptivity), mod in zip(agents, strategy)]
    return moderated_agents

def modexPD(agentes, R_max):
    n = len(agentes)
    dp = [[float('inf')] * (R_max + 1) for _ in range(n + 1)]
    dp[0][0] = 0  # Extremismo es cero cuando no hay agentes

    # track[i][r] almacena si en el estado dp[i][r], el agente i fue moderado (1) o no (0)
    track = [[-1] * (R_max + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        opinion_i, receptividad_i = agentes[i - 1]
        esfuerzo_moderacion = int(math.ceil(abs(opinion_i) * (1 - receptividad_i)))

        for r in range(R_max + 1):
            # No moderar al agente i
            if dp[i - 1][r] + opinion_i ** 2 < dp[i][r]:
                dp[i][r] = dp[i - 1][r] + opinion_i ** 2
                track[i][r] = 0  # No se moderó

            # Moderar al agente i si se puede
            if r >= esfuerzo_moderacion:
                if dp[i - 1][r - esfuerzo_moderacion] < dp[i][r]:
                    dp[i][r] = dp[i - 1][r - esfuerzo_moderacion]
                    track[i][r] = 1  # Se moderó

    # Encontrar el mínimo extremismo posible dentro del esfuerzo permitido
    extremismo_min = min(dp[n][:R_max + 1])
    r_mejor = dp[n][:R_max + 1].index(extremismo_min)

    # Reconstruir la estrategia óptima
    estrategia = [0] * n
    i = n
    r = r_mejor
    while i > 0:
        if track[i][r] == 1:
            estrategia[i - 1] = 1  # Se moderó
            esfuerzo_moderacion = int(math.ceil(abs(agentes[i - 1][0]) * (1 - agentes[i - 1][1])))
            r -= esfuerzo_moderacion
        else:
            estrategia[i - 1] = 0  # No se moderó
        i -= 1

    esfuerzo_total = calculate_effort(agentes, estrategia)
    agentes_moderados = apply_strategy(agentes, estrategia)
    extremismo = calculate_extremism(agentes_moderados)
    return estrategia, esfuerzo_total, extremismo

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

print(f"Datos: {datos}, R_max: {rmax}")  # Línea para depuración

# Ejecutar la función modexPD con los datos y R_max
resultado = modexPD(datos, rmax)
print(resultado)



