import pygame
import itertools
import csv
from functions import *

t = 1000
steps = 0
success_counter = 0

cities = []

l = list(range(0,10))
print(l)

start = random.randint(0,len(l)-1)
end = random.randint(0,len(l)-1)
tri = 0

if start > end:
    tri = end
    start = tri
    end = start

print(start)
print(end)


left = list(l[:start])
slice = list(reversed(l[start:end]))
right = list(l[end:])
print(left)
print(slice)
print(right)

result = left + slice + right

print(result)

exit()


with open('cities.dat', newline='', encoding='utf-8') as csvfile:
    cities_raw = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in cities_raw:
        city = []
        #print(row)

        degree_north = int(row[1]) + int(row[2])/60 + int(row[3])/3600
        degree_east = int(row[5]) + int(row[6])/60 + int(row[7])/3600

        city.append(row[0])
        city.append(degree_north)
        city.append(degree_east)

        cities.append(city)

min_n = min(cities, key=lambda k: k[1])[1]
max_n = max(cities, key=lambda k: k[1])[1]

min_e = min(cities, key=lambda k: k[2])[2]
max_e = max(cities, key=lambda k: k[2])[2]

path = list(range(0,len(cities)))
print(path)

def coord_to_screen(lat_n, lat_e):

    screen_y = 600 - (((lat_e - (((max_e - min_e) / 2)+min_e)) * 60 + 300))
    screen_x = ((lat_n - (((max_n - min_n) / 2)+min_n)) * 60 + 335)

    return (screen_x, screen_y)

distance_lookup_table = []

for i in cities:
    column = []
    for j in cities:
        distance = geodesic((i[1], i[2]), (j[1], j[2])).kilometers
        column.append(distance)

    distance_lookup_table.append(column)

def calc_cost(cities, path_tmp):

    cost = 0

    for idx, c in enumerate(path_tmp):

        first = path_tmp[idx]

        if idx != len(path_tmp) - 1:
            second = path_tmp[idx + 1]
        if idx == len(path_tmp) - 1:
            second = path_tmp[0]

        cost += distance_lookup_table[first][second]
        #cost += geodesic((cities[first][1], cities[first][2]), (cities[second][1], cities[second][2])).kilometers

    return cost

pygame.init()
screen = pygame.display.set_mode((600, 670))
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


    if steps % 7500 == 0 or success_counter == 750:
        t *= 0.95
        success_counter = 0

    screen.fill((0,0,0))

    #screen.blit(carImg, (0, 0))

    old_path = path.copy()
    cost_old_path = calc_cost(cities, old_path)
    new_path = swap(path.copy())
    cost_new_path = calc_cost(cities, new_path)

    delta_e = cost_new_path - cost_old_path

    if cost_new_path < cost_old_path:
        success_counter += 1

    if metropolis(delta_e, t):
        path = new_path

    else:
        path = old_path

    #print("Entfernung: "+str(int(calc_cost(cities, path)))+" km")

    steps += 1

    if steps % 1000 == 0:

        print("Entfernung: " + str(int(calc_cost(cities, path))) + " km "+str(t))

        for key,val in enumerate(cities):
            #print(key)
            color = (0, 128, 255)
            if val[0] == "Berlin":
                color = (255,0,0)
            pygame.draw.circle(screen,  color, coord_to_screen(val[1], val[2]), 3)

            for idx,c in enumerate(path):

                first = path[idx]

                if idx != len(path) - 1:
                    second = path[idx+1]
                if idx == len(path) - 1:
                    second = path[0]

                pygame.draw.line(screen, (0, 128, 255), coord_to_screen(cities[first][1], cities[first][2]), coord_to_screen(cities[second][1], cities[second][2]))



        pygame.display.flip()