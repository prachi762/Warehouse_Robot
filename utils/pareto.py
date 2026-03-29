def is_dominated(pareto_list, cost, energy):

    for c, e in pareto_list:
        if c <= cost and e >= energy:
            return True
    return False


def update_pareto(pareto_list, cost, energy):

    new_list = []

    for c, e in pareto_list:
        if not (cost <= c and energy >= e):
            new_list.append((c, e))

    new_list.append((cost, energy))
    return new_list
