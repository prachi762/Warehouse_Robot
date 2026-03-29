def is_dominated(pareto_list, cost, energy, value):

    for c, e, v in pareto_list:
        if c <= cost and e >= energy and v >= value:
            return True
    return False


def update_pareto(pareto_list, cost, energy, value):

    new_list = []

    for c, e, v in pareto_list:
        if not (cost <= c and energy >= e and value >= v):
            new_list.append((c, e, v))

    new_list.append((cost, energy, value))
    return new_list
