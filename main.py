import random

map_block = "~"
map_mina = "x"
map = [[[map_block, 0] for x in range(10)] for y in range(10)]
indent = 2

# x / # / count;
def show_map():
    global map
    global indent
    global map_block
    
    print()
    print(" ", sep="", end="")
    for i in range(0, len(map[0])):
        print("  ", i + 1, sep="", end="")
    print()
    
    for i in range(0, len(map)):
        print(i + 1, sep="", end="")
        for j in range(0, len(map[0])):

            if i + 1 >= 10 and j + 1 == 1: #making indent
                pass
            else:
                print(" ", sep="", end="")

            show_block = map_block
            if map[i][j][1] == 1:
                show_block = map[i][j][0]
            print(" ", show_block, sep="", end="")
        print()
    print()


def fill_mines():
    global map
    global map_block
    global map_mina
    count = random.randint(15, 20)
    count_copy = count

    while count > 0:
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        if map[x][y][0] == map_block:
            map[x][y][0] = map_mina
            count = count - 1
    return count_copy


def calculate_minas():
    global map_block
    global map_mina
    global map
    operations = [0, 1, -1]
    count_minas = 0

    for i in range(len(map)):
        for j in range(len(map[0])):
            count = 0
            if map[i][j][0] != map_mina:
                    for op_x in operations:
                        for op_y in operations:
                            if i + op_x >= 0 and i + op_x <= 9 and j + op_y >= 0 and j +op_y <= 9:
                                if map[i + op_x][j + op_y][0] == map_mina:
                                    count += 1
                    map[i][j][0] = count
# x y: +1+1 +1+0 +1-1 +0-1 -1-1 -1+0 -1+1 +0+1


def open_zeros(y, x):
    global map
    operations = [0, -1, 1]
    map[y][x][1] = 2
    for op_x in operations:
        for op_y in operations:
            if y + op_y >= 0 and y + op_y <= 9 and x + op_x >= 0 and x + op_x <= 9: #checking limit
                if map[y + op_y][x + op_x][0] == 0 and map[y + op_y][x + op_x][1] != 2:
                    open_zeros(y+op_y, x+op_x)


def is_nearby_opened_zero(i, j):
    operations = [0, -1, 1]
    global map

    for op_x in operations:
        for op_y in operations:
            if i + op_x >= 0 and i + op_x <= 9 and j + op_y >= 0 and j + op_y <= 9:
                if map[i+op_x][j+op_y][0] == 0 and map[i+op_x][j+op_y][1] == 2:
                    return 1
    return 0
            
            

def open_all_zeros_connected(y, x):
    global map
    global map_block
    global map_mina
    
    open_zeros(y, x)
    show_map()
    
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j][1] == 0 and map[i][j][0] != map_mina and map[i][j][0] != 0 and is_nearby_opened_zero(i, j) == 1:
                map[i][j][1] = 1
    show_map()

    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j][1] == 2:
                map[i][j][1] = 1


blocks_left = len(map) * len(map[0]) - fill_mines()
show_map()
calculate_minas()
show_map()

while blocks_left > 0:
    print("Choose the block (y,x): ", sep="", end="")
    y, x = (int(i) for i in input().split())
    y = y - 1
    x = x - 1
    print(y, x)
    if map[y][x][1] == 1:
        print("You have already opened this one")
        continue
    elif map[y][x][0] == map_mina:
        print("Shit happens...")
        for i in range(len(map)):
            for j in range(len(map[0])):
                if map[i][j][0] == map_mina:
                    map[i][j][1] = 1
        show_map()
        break
    elif map[y][x][0] != 0:
        map[y][x][1] = 1
    else: # == 0
        open_all_zeros_connected(y, x)
    show_map()
    blocks_left = blocks_left - 1 # not in every case should be done

'''
cases:
1) choose mina - show all (1) and minas
2) choose 0 block - show all (1) + block + all connected 0 blocks
3)choose 1/2/... block - show it
'''
#correct print map: when fail, when continue
#counting minuses nearby
#opening map

