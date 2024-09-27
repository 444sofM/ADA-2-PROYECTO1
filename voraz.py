import math
def rocV(agents, R_max): 
    """Algoritmo voraz que prioriza |opinion| / (1 - receptividad) dentro del esfuerzo permitido,
    respetando el índice original de la lista de agentes."""

#Guardar los índices originales antes de ordenar
    agents_with_index = [(index, opinion, receptivity) for index, (opinion, receptivity) in enumerate(agents)]

#Ordenar los agentes según |opinion| / (1 - receptividad)
    agents_sorted = sorted(agents_with_index, key=lambda x: abs(x[1]) / (1 - x[2]), reverse=True)

    estrategia = [0] * len(agents)  # Inicialmente, ningún agente está moderado
    esfuerzo_total = 0
    extremismo_total = 0

    for index, opinion, receptivity in agents_sorted:
        # Calcular el costo de moderación usando la función techo
        costo_moderacion = math.ceil(abs(opinion) * (1 - receptivity))
        # Si aún queda presupuesto, moderamos al agente
        if esfuerzo_total + costo_moderacion <= R_max:
            esfuerzo_total += costo_moderacion
            estrategia[index] = 1  # Marcamos al agente como moderado en su índice original
            extremismo_total += 0  # El extremismo de este agente se reduce a 0
        else:
            extremismo_total += opinion ** 2  # No se modera, su extremismo sigue igual

#Calcular el extremismo de la red después de aplicar la estrategia
    extremismo_red_moderada = math.sqrt(extremismo_total) / len(agents)

    return estrategia, esfuerzo_total, extremismo_red_moderada