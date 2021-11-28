import random
from geopy.distance import geodesic
import math

def metropolis(delta_energy, temperature):
    uni_rand = random.random()

    if delta_energy < 0:
        return True
    else:
        if uni_rand < math.exp(-(delta_energy / temperature)):
            return True
        else:
            return False



def swap(old_path):
    rand_pos = random.randint(0,len(old_path)-1)

    src_val = old_path[rand_pos]
    if rand_pos != len(old_path)-1:
        dest = rand_pos + 1
    if rand_pos == len(old_path)-1:
        dest = 0

    dest_val = old_path[dest]

    old_path[rand_pos] = dest_val
    old_path[dest] = src_val

    return old_path

