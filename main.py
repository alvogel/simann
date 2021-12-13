import math
import json 
import pygame
import itertools
import csv
from functions import *
import time
import sys

cities = []  # will have following structure: [['Aachen', 50.77611111111111, 6.084444444444444], ['Augsburg', 48.37222222222222, 10.9]....]

######import data cities######
with open('cities40.dat', newline='', encoding='utf-8') as csvfile:
    cities_raw = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in cities_raw:
        city = []

        degree_north = int(row[1]) + int(row[2]) / 60 + int(row[3]) / 3600
        degree_east = int(row[5]) + int(row[6]) / 60 + int(row[7]) / 3600

        city.append(row[0])
        city.append(degree_north)
        city.append(degree_east)

        cities.append(city)

# Ermittlung maximale und minimale Koordinaten für die Darstellung mit pygame
min_n = min(cities, key=lambda k: k[1])[1]
max_n = max(cities, key=lambda k: k[1])[1]

min_e = min(cities, key=lambda k: k[2])[2]
max_e = max(cities, key=lambda k: k[2])[2]

# Weg, nach welchem die Städte besucht werden
path = list(range(0, len(cities)))
print(path)

distance_lookup_table = []

# Erstellt Einträge für die Entfernung aller Städte zueinander dij mit Form: [[d11,d12,d12,...],[d21,d22,d23,..]..]
for i in cities:
    column = []
    for j in cities:
        distance = geodesic((i[1], i[2]), (j[1], j[2])).kilometers
        column.append(distance)

    distance_lookup_table.append(column)

# Initialisierung Pygamefenster
pygame.init()
screen = pygame.display.set_mode((600, 670))


def search_shortest_path(start_path, flip_type, name_prefix, start_temperature = 100, cooling_factor = 0.9, break_p = 0.01):

    temperature = start_temperature
    city_count = len(start_path)
    fav_length = 9999999
    fav_path = []
    fav_time = 0
    fav_step = 0
    starttime = time.time()
    path_history = []
    path = start_path
    steps = 0
    success_counter = 0
    

    while math.exp(-10/temperature) > break_p:

        # Temperatur wird nach 7500 Veränderungen des path oder nach 750 erfolgreichen Veränderungen, bei denen der Weg verringert wurde, verringert
        if steps % (city_count*100) == 0 or success_counter == (city_count*10):

            temperature *= cooling_factor
            success_counter = 0

        screen.fill((0, 0, 0))


        # Vergleich alter und neuer Pfad
        old_path = path.copy()
        cost_old_path = calc_cost(old_path, distance_lookup_table)

        if flip_type == "swap_random":
            new_path = swap_random(path.copy())
        elif flip_type == "revert_part":
            new_path = revert_part(path.copy())

        cost_new_path = calc_cost(new_path, distance_lookup_table)

        delta_e = cost_new_path - cost_old_path

        if cost_new_path < cost_old_path:
            success_counter += 1

        if metropolis(delta_e, temperature):
            path = new_path

        else:
            path = old_path

        if cost_new_path < fav_length:
            fav_length = cost_new_path
            fav_path = path
            fav_time = time.time() - starttime
            fav_step = steps

        #print("fav: "+str(fav_length)+" km")

        steps += 1



        ######Grafikausgabe#####
        if steps % (city_count*100) == 0:

            runtime = time.time() - starttime

            ###Abspeichern der Path_history
            path_history_entry = []
            path_history_entry.append(int(calc_cost(path, distance_lookup_table)))
            path_history_entry.append(temperature)
            path_history_entry.append(runtime)
            path_history_entry.append(steps)
            path_history_entry.append(path)

            path_history.append(path_history_entry)
            
    
    
            print(
                "Entfernung: " + str(int(calc_cost(path, distance_lookup_table))) + " km " + str(temperature) + " step " + str(steps)+"-"+str(math.exp(-10/temperature)))

            for key, val in enumerate(cities):
                # print(key)
                color = (0, 128, 255)
                if val[0] == "Berlin":
                    color = (255, 0, 0)
                pygame.draw.circle(screen, color, coord_to_screen(val[1], val[2], max_e, min_e, min_n, max_n), 3)

                for idx, c in enumerate(path):

                    first = path[idx]

                    if idx != len(path) - 1:
                        second = path[idx + 1]
                    if idx == len(path) - 1:
                        second = path[0]

                    pygame.draw.line(screen, (0, 128, 255),
                                     coord_to_screen(cities[first][1], cities[first][2], max_e, min_e, min_n, max_n),
                                     coord_to_screen(cities[second][1], cities[second][2], max_e, min_e, min_n, max_n))

            pygame.display.flip()
            
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


        

    ######writing down whole path_history######
    file_name_history = str(name_prefix)+"_history_"+ flip_type +"_c"+ str(cooling_factor) + "_breakp_" + str(break_p) + "_starting_temp_"+ str(start_temperature) +".json"
    with open(file_name_history,"w") as write:
        json.dump(path_history,write)
    write.close()
    
    
    file_name_fav = "fav_"+flip_type+"_c"+str(cooling_factor)+"_breakp_"+ str(break_p) + "_starting_temp_"+ str(start_temperature) + ".json"
    data_fav_entry = [fav_length,fav_time,fav_step,time.ctime(),fav_path]
    with open(file_name_fav,"a") as write:
        json.dump(data_fav_entry,write)
        write.write("\n")
    write.close()
    


for i in range(0,60):
    temperature = 70
    flip_type1 = "revert_part"
    flip_type2 = "swap_random"
    cooling_factor = 0.85
    break_p = 0.01 #gibt Bedingung, an der die Schleife aufhören soll nach einem kürzeren Weg zu suchen; Wenn die Wkeit bei einer Wegänderung von 10km diesen Pfad anzunehmen unter break_p liegt, dann hört das Programm auf
    
    search_shortest_path(path, flip_type1, i, start_temperature=temperature, cooling_factor=cooling_factor, break_p = break_p)
    search_shortest_path(path, flip_type2, i, start_temperature=temperature, cooling_factor=cooling_factor, break_p = break_p)
