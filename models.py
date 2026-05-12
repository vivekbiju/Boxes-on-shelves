import pandas as pd
import numpy as np
import random
from copy import deepcopy

def load_data(f_p1, f_p2, f_p3):
    """Loads product, bay, and shelf data with mm to cm conversion."""
    cf = 0.1 
    products = pd.read_csv(f_p1, sep=r"\s+", header=None, names=['type', 'qty', 'length', 'width', 'height', 'idx'])
    bays = pd.read_csv(f_p2, sep=r"\s+", header=None, names=['w', 'h', 'd', 'avail_h']) * cf
    shelves = pd.read_csv(f_p3, sep=r"\s+", header=None, names=['num', 'thick', 'pos', 't_gap', 'l_gap', 'i_gap', 'r_gap', 'idx'])
    for col in ['thick', 'pos', 't_gap', 'l_gap', 'i_gap', 'r_gap']: 
        shelves[col] *= cf
    return products, bays.iloc[0], shelves

def is_placement_valid(p, shelf, solution, BW, BH, BD):
    """Checks for boundary violations and AABB collisions."""
    ew, el, eh = p['eff_width'], p['eff_length'], p['eff_height']
    y_start = shelf['pos'] + shelf['thick'] + shelf['t_gap']
    
    if (p['x'] < shelf['l_gap'] or p['x'] + ew > BW - shelf['r_gap'] or
        p['y'] < y_start or p['y'] + eh > BH or
        p['z'] < 0 or p['z'] + el > BD): 
        return False

    for o in solution:
        if (p['x'] < o['x'] + o['eff_width'] and p['x'] + ew > o['x'] and
            p['y'] < o['y'] + o['eff_height'] and p['y'] + eh > o['y'] and
            p['z'] < o['z'] + o['eff_length'] and p['z'] + el > o['z']):
            return False
    return True

def generate_initial_population(pop_size, products_df, shelves_df, BW, BH, BD):
    """Creates the initial set of randomized valid solutions."""
    population = []
    prod_list = products_df.to_dict('records')
    shelf_list = shelves_df.to_dict('records')

    for _ in range(pop_size):
        solution = []
        shuffled_prods = random.sample(prod_list, len(prod_list))
        for prod in shuffled_prods:
            placed = False
            shuffled_shelves = random.sample(shelf_list, len(shelf_list))
            for s_idx, shelf in enumerate(shuffled_shelves):
                orient = random.choice([0, 90])
                ew, el = (prod['length'], prod['width']) if orient == 90 else (prod['width'], prod['length'])
                eh = prod['height']
                
                x_max = BW - shelf['r_gap'] - ew
                y_min = shelf['pos'] + shelf['thick'] + shelf['t_gap']
                y_max = BH - eh
                z_max = BD - el

                if x_max > shelf['l_gap'] and y_max > y_min and z_max > 0:
                    p = {
                        'product': prod, 'shelf_map_index': s_idx,
                        'x': random.uniform(shelf['l_gap'], x_max),
                        'y': random.uniform(y_min, y_max),
                        'z': random.uniform(0, z_max),
                        'eff_width': ew, 'eff_length': el, 'eff_height': eh
                    }
                    if is_placement_valid(p, shelf, solution, BW, BH, BD):
                        solution.append(p)
                        placed = True
                        break
        population.append(solution)
    return population