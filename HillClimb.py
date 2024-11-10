import numpy as np
import matplotlib.pyplot as plt
import random

def matrixBeolvas(filename):
    matrix = []
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        for line in lines:
            matrix.append([int(x) for x in line.split()])
    except Exception as e:
        print(e)
    return matrix


def get_global_maximum(matrix):
    max_value = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > max_value:
                max_value = matrix[i][j]

    return  max_value

def get_neighbors(x, y, rows, cols):
    neighbors = []
    if x > 0: neighbors.append((x-1, y))
    if x < rows-1: neighbors.append((x+1, y)) 
    if y > 0: neighbors.append((x, y-1))
    if y < cols-1: neighbors.append((x, y+1))  
    return neighbors


def hill_climb(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    counter = 0

    current_pos = (random.randint(0, rows-1), random.randint(0, cols-1))
    path = [current_pos]
    
   
    global_max_value = get_global_maximum(matrix)
   
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')


    x = np.arange(cols)
    y = np.arange(rows)
    x, y = np.meshgrid(x, y)

    z = np.array(matrix)

    ax.plot_surface(x, y, z, cmap='terrain', alpha=0.7)

    visited = np.zeros((30, 30), dtype=bool)


    point = ax.scatter(current_pos[1], current_pos[0], matrix[current_pos[0]][current_pos[1]], color='black', s=50)

    while matrix[current_pos[0]][current_pos[1]] != global_max_value:
        counter+=1
        visited[current_pos[0]][current_pos[1]] = True

        neighbors = get_neighbors(current_pos[0], current_pos[1], rows, cols)

        best_neighbor = None
        best_value = 0
        for neighbor in neighbors:
            x, y = neighbor
            if matrix[x][y] > best_value and not visited[x][y]:
                best_value = matrix[x][y]
                best_neighbor = neighbor
        
       
        if best_value <= matrix[current_pos[0]][current_pos[1]]:
            unvisited_cells = np.argwhere(visited == False)
            if len(unvisited_cells) == 0:
                print("Nincs több mezö")
                break 
            current_pos = random.choice(unvisited_cells)

        else:
            current_pos = best_neighbor
            path.append(current_pos)

        point.remove()
        point = ax.scatter(current_pos[1], current_pos[0], matrix[current_pos[0]][current_pos[1]], color='black', s=50, label="Jelenlegi poz")

        
        plt.pause(0.1)

    print(f"Globális maximum megtalálva: {counter}")
    global palya
    EredmenyMentes(palya+'_eredmeny.txt',counter)

    ax.set_title('Pálya 3D megjelenítése')
    ax.set_xlabel('X tengely')
    ax.set_ylabel('Y tengely')
    ax.set_zlabel('Magasság')

    plt.show()

    

def EredmenyMentes(filename, counter):
    try:
       
        
        with open(filename, 'a') as file:
            file.write(f"Globális maximum megtalálva: {counter} lépéssel." + '\n') 

        with open(filename, 'r') as file:
            lines = file.readlines()

        total_Steps = 0
        total_Records = 0
        for line in lines:
            try:
                val = int(line.split(' lépéssel.')[0].split()[-1])
                total_Steps += val
                total_Records += 1
            except ValueError:
                pass

        average_Steps = total_Steps / total_Records

        with open(filename, 'a') as file:
            file.write(f"Átlag lépésszám : {average_Steps:.2f}\n")

    except Exception as e:
        print(e)


palya = 'palya10'
matrix = matrixBeolvas(palya+'.txt')
#for _ in range(200):
hill_climb(matrix)


