import pygame
import itertools
import csv
from functions import *

t = 70
steps = 0
success_counter = 0

cities = [] #will have following structure: [['Aachen', 50.77611111111111, 6.084444444444444], ['Augsburg', 48.37222222222222, 10.9]....]

######import data cities######
with open('cities.dat', newline='', encoding='utf-8') as csvfile:
    cities_raw = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in cities_raw:
        city = []

        degree_north = int(row[1]) + int(row[2])/60 + int(row[3])/3600
        degree_east = int(row[5]) + int(row[6])/60 + int(row[7])/3600

        city.append(row[0])
        city.append(degree_north)
        city.append(degree_east)

        cities.append(city)

#Ermittlung maximale und minimale Koordinaten für die Darstellung mit pygame
min_n = min(cities, key=lambda k: k[1])[1]
max_n = max(cities, key=lambda k: k[1])[1]

min_e = min(cities, key=lambda k: k[2])[2]
max_e = max(cities, key=lambda k: k[2])[2]

#Weg, nach welchem die Städte besucht werden
path = list(range(0,len(cities)))
print(path) 

distance_lookup_table = []

#Erstellt Einträge für die Entfernung aller Städte zueinander dij mit Form: [[d11,d12,d12,...],[d21,d22,d23,..]..]
for i in cities:
    column = []
    for j in cities:
        distance = geodesic((i[1], i[2]), (j[1], j[2])).kilometers
        column.append(distance)

    distance_lookup_table.append(column)

#Initialisierung Pygamefenster
pygame.init()
screen = pygame.display.set_mode((600, 670))
done = False

###### Schleife ######
while not done:
    for event in pygame.event.get(): #Beendigung Pygame ausgabe nach Abschluss der Berechnungen
        if event.type == pygame.QUIT:
            done = True

    #Temperatur wird nach 7500 Veränderungen des path oder nach 750 erfolgreichen Veränderungen, bei denen der Weg verringert wurde, verringert
    if steps % 7500 == 0 or success_counter == 750: 
        t *= 0.99
        success_counter = 0

    screen.fill((0,0,0))

    #screen.blit(carImg, (0, 0))
    
    #Vergleich alter und neuer Pfad
    old_path = path.copy()
    cost_old_path = calc_cost(old_path, distance_lookup_table)
    new_path = revert_part(path.copy())
    cost_new_path = calc_cost(new_path, distance_lookup_table)
    
    delta_e = cost_new_path - cost_old_path

    if cost_new_path < cost_old_path:
        success_counter += 1

    if metropolis(delta_e, t):
        path = new_path

    else:
        path = old_path

    #print("Entfernung: "+str(int(calc_cost(cities, path)))+" km")

    steps += 1
    
    ######Grafikausgabe#####
    if steps % 7500 == 0:

        print("Entfernung: " + str(int(calc_cost(path, distance_lookup_table))) + " km "+str(t) + " step " + str(steps))

        for key,val in enumerate(cities):
            #print(key)
            color = (0, 128, 255)
            if val[0] == "Berlin":
                color = (255,0,0)
            pygame.draw.circle(screen,  color, coord_to_screen(val[1], val[2], max_e, min_e, min_n, max_n), 3)

            for idx,c in enumerate(path):

                first = path[idx]

                if idx != len(path) - 1:
                    second = path[idx+1]
                if idx == len(path) - 1:
                    second = path[0]

                pygame.draw.line(screen, (0, 128, 255), coord_to_screen(cities[first][1], cities[first][2], max_e, min_e, min_n, max_n), coord_to_screen(cities[second][1], cities[second][2],max_e, min_e, min_n, max_n))



        pygame.display.flip()