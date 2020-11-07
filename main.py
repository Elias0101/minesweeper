import random

map_block = "~"
map_mine = "x"
map_flag = "?"
map = [[[map_block, 0] for x in range(10)] for y in range(10)]
#for second value ( = 0 in the beggining ):
# 0 - closed
# 1 - opened
# 2 - for flag
# 3 - temporary for opening connected to zero

# x / # / count;
def show_map():
    global map
    global map_block
    global map_flag
    show_block = map_block
    
    #x line (1,2,3...)
    print()
    print(" ", sep="", end="")
    for i in range(0, len(map[0])):
        print("  ", i + 1, sep="", end="")
    print()
    
    #y line (1,2,3.. + elements of map)
    for i in range(0, len(map)):
        print(i + 1, sep="", end="")
        for j in range(0, len(map[0])):
        
            if i + 1 >= 10 and j + 1 == 1: #making indent
                pass
            else:
                print(" ", sep="", end="")

            if map[i][j][1] == 1:
                show_block = map[i][j][0]
            elif map[i][j][1] == 2:
                show_block = map_flag
            else:
                show_block = map_block
            print(" ", show_block, sep="", end="")
        print()
    print()


def fill_mines():
    global map
    global map_block
    global map_mine
    count = random.randint(15, 20)
    count_copy = count

    while count > 0:
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        if map[x][y][0] == map_block:
            map[x][y][0] = map_mine
            count = count - 1
    return count_copy


def calculate_mines():
    global map_block
    global map_mine
    global map
    operations = [0, 1, -1]
    count_minas = 0

    for i in range(len(map)):
        for j in range(len(map[0])):
            count = 0
            if map[i][j][0] != map_mine:
                    for op_x in operations:
                        for op_y in operations:
                            if i + op_y >= 0 and i + op_y <= 9 and j + op_x >= 0 and j + op_x <= 9:
                                if map[i + op_y][j + op_x][0] == map_mine:
                                    count += 1
                    map[i][j][0] = count
# x y: +1+1 +1+0 +1-1 +0-1 -1-1 -1+0 -1+1 +0+1
# +0+0 included


def open_zeros(y, x):
    global map
    operations = [0, -1, 1]
    map[y][x][1] = 3

    for op_x in operations:
        for op_y in operations:
            if y + op_y >= 0 and y + op_y <= 9 and x + op_x >= 0 and x + op_x <= 9: #checking limit
                if map[y + op_y][x + op_x][0] == 0 and map[y + op_y][x + op_x][1] != 3:
                    open_zeros(y+op_y, x+op_x)


def is_nearby_opened_zero(i, j):
    operations = [0, -1, 1]
    global map

    for op_x in operations:
        for op_y in operations:
            if i + op_y >= 0 and i + op_y <= 9 and j + op_x >= 0 and j + op_x <= 9:
                if map[i + op_y][j + op_x][1] == 3:
                    return 1
    return 0
            
            

def open_all_zeros_connected(y, x):
    global map
    global map_block
    global map_mine
    
    open_zeros(y, x)
    
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j][1] == 0 and map[i][j][0] != map_mine and map[i][j][0] != 0 and is_nearby_opened_zero(i, j) == 1: #too many conditions ?
                map[i][j][1] = 1

    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j][1] == 3:
                map[i][j][1] = 1


def count_opened_blocks():
    global map
    count = 0

    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j][1] == 1:
                count += 1
    return count


def show_all_mines():
    global map
    global map_mine

    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j][0] == map_mine:
                map[i][j][1] = 1
    show_map()


def add_flag(y, x):
    global map
    
    if map[y][x][1] == 1:
        print("This block is already opened")
    elif map[y][x][1] == 2:
        map[y][x][1] = 0
    else:
        map[y][x][1] = 2


mines_amount = fill_mines()
blocks_amount = len(map) * len(map[0]) - mines_amount
calculate_mines()
opened_blocks_amount = 0

#f1,2 ; 1,2 ; f1,2 (delete flag)
while opened_blocks_amount != blocks_amount:
    show_map()
    print("--Possible commands--")
    print("1) '1,2' - open block at the intersection\n1 vertical and 2 horizontal")
    print("2) 'f1,2' - put or delete a flag on the corresponding block\n(where you suppose the mine is located)")
    print("Write your command: ", sep="", end="")

    command = input()
    flag = 0
    y = 0
    x = 0
    
    if len(command) != 0 and command[0] == 'f':
        flag = 1
        command = command[1:]

    try:
        if len(command) < 3 or command.find(",") == -1:
            raise
        y, x = (int(i) - 1 for i in command.split(',')) # validating needed!!!
        if y < 0 or x < 0 or y > len(map) - 1 or x > len(map) - 1:
            raise
    except:
        print()
        print("Wrong command format. Watch 'Read.me' file for examples")
        continue
    print("flag:", flag)
    print("y, x: ", y, x)
    
    if flag == 1:
        add_flag(y, x)
    elif map[y][x][1] == 1:
        print("You have already opened this one")
        continue
    elif map[y][x][0] == map_mine:
        print("Shit happens...")
        show_all_mines()
        break
    elif map[y][x][0] != 0: #maybe change for str for better understanding
        map[y][x][1] = 1
    else: # == 0
        open_all_zeros_connected(y, x)
    opened_blocks_amount = count_opened_blocks()

show_map()
print()
print("---RESULTS---")
print("You opened ", opened_blocks_amount, "blocks from ", blocks_amount, "available")

'''
cases:
1) choose mina - show all (1) and minas
2) choose 0 block - show all (1) + block + all connected 0 blocks
3)choose 1/2/... block - show it
'''
#correct print map: when fail, when continue
#counting minuses nearby
#opening map

