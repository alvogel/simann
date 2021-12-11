import random
from geopy.distance import geodesic
import math


###### algorithm ######
def calc_cost(path_tmp, distance_lookup_table): #berechnet die "Energie" der Konfiguration path_tmp mithilfe des distance_lookup_table

    cost = 0

    for idx, c in enumerate(path_tmp):

        first = path_tmp[idx]

        if idx != len(path_tmp) - 1:
            second = path_tmp[idx + 1]
        if idx == len(path_tmp) - 1:
            second = path_tmp[0]

        cost += distance_lookup_table[first][second]

    return cost

def metropolis(delta_energy, temperature): #gibt zurück, ob die Konfiguration beibehalten wird (True) oder nicht (False) und benutzt dabei den Metropolis Algorithmus
    uni_rand = random.random()

    if delta_energy < 0: #gibt True zurück, wenn die Energie der neuen Konfiguration kleiner ist als die der alten Konfiguration
        return True
    else:
        if uni_rand < math.exp(-(delta_energy / temperature)): #gibt True mit einer Wkeit math.exp(-(delta_energy / temperature)) zurück
            return True
        else: 
            return False

###### flip-types ######
def swap_row(old_path): #erstellt neuen Weg, indem die Position von zwei zufällig ausgewählten aufeinanderfolgenden Städten in der Liste getauscht wird
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

def swap_random(old_path): #erstellt neuen Weg, indem die Position von zwei zufällig ausgewählten Städten in der Liste getauscht werden
    rand_pos1 = random.randint(0,len(old_path)-1)
    rand_pos2 = random.randint(0,len(old_path)-1)
    
    value1 = old_path[rand_pos1]
    
    old_path[rand_pos1] = old_path[rand_pos2]
    old_path[rand_pos2] = value1
    
    return old_path

def revert_part(old_path): #erstellt neuen Weg, indem ein Stück des Weges zwischen zwei zufällig ausgewählten Städten umgedreht wird
    rand_pos1 = random.randint(0,len(old_path)-1)
    rand_pos2 = random.randint(0,len(old_path)-1)
    
    if rand_pos1 < rand_pos2:
        step_direction = 1
    else:
        step_direction = -1
    
    path_in_between_reversed = list(reversed(old_path[rand_pos1:rand_pos2:step_direction]))
    
    old_path[rand_pos1:rand_pos2:step_direction] = path_in_between_reversed
    
    return old_path
    
###### grafic output ######
def coord_to_screen(lat_n, lat_e, max_e, min_e, min_n, max_n): #rechnet Längen/Breitengrade in x- und y-Koordinaten um

    screen_y = 600 - (((lat_e - (((max_e - min_e) / 2)+min_e)) * 60 + 300))
    screen_x = ((lat_n - (((max_n - min_n) / 2)+min_n)) * 60 + 335)

    return (screen_x, screen_y)