import random
import numpy as np
from copy import deepcopy

def evaluate(solution, shelves_df, BW, BH, BD):
    """Calculates space utilization (max) and load imbalance (min)."""
    if not solution: return 0.0, 0.0
    total_vol = 0
    shelf_loads = {}
    for p in solution:
        p_vol = p['product']['width'] * p['product']['length'] * p['product']['height']
        total_vol += p_vol
        s_idx = p['shelf_map_index']
        shelf_loads[s_idx] = shelf_loads.get(s_idx, 0) + p_vol
    
    utilization = total_vol / (BW * BH * BD) if (BW * BH * BD) > 0 else 0
    load_balance = np.std(list(shelf_loads.values())) if shelf_loads else 0
    return utilization, -load_balance

def fast_non_dominated_sort(population, fitness_values):
    """Sorts population into Pareto fronts based on dominance."""
    size = len(population)
    dom_counts = [0] * size
    dominated_indices = [[] for _ in range(size)]
    fronts = [[]]

    for i in range(size):
        for j in range(size):
            if i == j: continue
            if (fitness_values[i][0] >= fitness_values[j][0] and fitness_values[i][1] >= fitness_values[j][1] and
               (fitness_values[i][0] > fitness_values[j][0] or fitness_values[i][1] > fitness_values[j][1])):
                dominated_indices[i].append(j)
            elif (fitness_values[j][0] >= fitness_values[i][0] and fitness_values[j][1] >= fitness_values[i][1] and
                 (fitness_values[j][0] > fitness_values[i][0] or fitness_values[j][1] > fitness_values[i][1])):
                dom_counts[i] += 1
        if dom_counts[i] == 0: fronts[0].append(i)

    curr = 0
    while fronts[curr]:
        next_front = []
        for p in fronts[curr]:
            for q in dominated_indices[p]:
                dom_counts[q] -= 1
                if dom_counts[q] == 0: next_front.append(q)
        if not next_front: break
        fronts.append(next_front); curr += 1
    return fronts

def crossover(parent1, parent2):
    """Performs single-point crossover between placement lists."""
    if not parent1 or not parent2 or len(parent1) < 2 or len(parent2) < 2:
        return deepcopy(parent1), deepcopy(parent2)
    cp = random.randint(1, min(len(parent1), len(parent2)) - 1)
    return deepcopy(parent1[:cp] + parent2[cp:]), deepcopy(parent2[:cp] + parent1[cp:])

def mutate(solution, rate, shelves_df, BW, BH, BD):
    """Mutates a solution by nudging a box or flipping orientation."""
    if not solution or random.random() > rate: return solution
    mutated = deepcopy(solution)
    idx = random.randint(0, len(mutated) - 1)
    p = mutated[idx]
    if random.random() < 0.5:
        p['eff_width'], p['eff_length'] = p['eff_length'], p['eff_width']
    else:
        p['x'] = max(0, min(p['x'] + random.uniform(-2, 2), BW - p['eff_width']))
        p['z'] = max(0, min(p['z'] + random.uniform(-2, 2), BD - p['eff_length']))
    return mutated