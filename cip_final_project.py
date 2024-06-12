from tkinter import *
import random
import time
#code cleaned up using "black" code formatter

# initializing the canvas
root = Tk()
root.title("Game of Life")
W = 800  # canvas width
H = 800  # canvas height
DELAY_TIME = 0.2
canvas = Canvas(root, width=W, height=H, bg="white")
canvas.pack()


def create_square(
    canvas, start_x, start_y, length, color
):  # create a rectangle with black outlines
    canvas = canvas
    """canvas.create_rectangle(start_x-2, start_y-2, start_x+2+length, start_y+2+length, fill="black")"""
    canvas.create_rectangle(
        start_x,
        start_y,
        start_x + length,
        start_y + length,
        fill=color,
        outline="black",
    )


def round_to_nearest_tenth(n):
    return round(n / 10) * 10


# generating the grid
x = 0
y = 0
PAUSE_TIME = 1 / 50
length = 20
while y < H:
    while x < W:
        create_square(canvas, x, y, length, "dark blue")
        x += length
    y += length
    x = 0


# generating database for cells information
database = {}
x = 0
y = 0
cell = 0
while y < H:
    while x < W:
        cell_data = []
        cell_data.append(x)
        cell_data.append(y)
        cell_data.append("dead")
        database[cell] = cell_data
        x += length
        cell += 1
    y += length
    x = 0
print(database)


"""#user clicking to change color of cells --> failed
while True:
    if click:
        x_clicked = round_to_nearest_tenth(int(click[0]))
        print(x_clicked)
        y_clicked = round_to_nearest_tenth(int(click[1]))
        print(y_clicked)
        for cell in database.keys():
            data = database[cell]
            x_coordinate = data[0]
            y_coordinate = data[1]
            if (x_coordinate < x_clicked and x_clicked < x_coordinate+length) and (y_coordinate < y_clicked and y_clicked < y_coordinate+length):
                data[2] = "filled"
                create_square(canvas, x_coordinate, y_coordinate, length, "green")"""


# draw a 3x3 square on the grid to create star
def make_square_for_star(canvas, x, y):
    canvas = canvas
    for j in range(3):
        for i in range(3):
            create_square(canvas, x, y, length, "yellow")
            # updating the state of the yellow squares to alive
            for cell in database.keys():
                if database[cell][0] == x and database[cell][1] == y:
                    database[cell][2] = "alive"
            x += length
        y += length
        x -= 3 * length


# I asked ChatGPT for help for this part :)))) Generate random multiples of 10 within a range
def generate_random_multiples_of_ten(max_val):
    min_val = 0
    if min_val % length != 0 or max_val % length != 0:
        raise ValueError("min_val and max_val must be multiples of 20")
    random_number = random.randint(min_val // length, max_val // length) * length
    return random_number


# create a list containing random coordinates of squares
NO_OF_STARS = 10


def get_coordinates():
    coordinates_list = []
    for i in range(NO_OF_STARS):
        coordinates = []
        x = generate_random_multiples_of_ten(W - length * 2)
        y = generate_random_multiples_of_ten(H - length * 2)
        coordinates.append(x)
        coordinates.append(y)
        coordinates_list.append(coordinates)
    return coordinates_list


# draw NO_OF_STARS squares on the canvas to create stars
coordinates_pairs = get_coordinates()
for pair in coordinates_pairs:
    make_square_for_star(canvas, pair[0], pair[1])


def get_neighbor_cell(cell):
    global database
    x = database[cell][0]
    y = database[cell][1]
    state = database[cell][2]
    neighbor_cell = [
        [x + length, y, state],
        [x - length, y],
        [x, y + length],
        [x, y - length],
        [x + length, y + length],
        [x - length, y + length],
        [x + length, y - length],
        [x - length, y - length],
    ]
    for coordinate in neighbor_cell:
        if 0 <= coordinate[0] < W and 0 <= coordinate[1] < H:
            pass
        else:
            neighbor_cell.remove(coordinate)
    return neighbor_cell


def generate_new_database():
    global database
    new_database = {}
    # programming the game of life rule
    for cell in database:
        alive = 0
        neighbor_cells = get_neighbor_cell(cell)
        for neighbor_cell in neighbor_cells:
            for _ in database:
                if (
                    database[_][0] == neighbor_cell[0]
                    and database[_][1] == neighbor_cell[1]
                    and database[_][2] == "alive"
                ):
                    alive += 1
        if database[cell][2] == "alive":
            # If the cell is alive, then it stays alive if it has either 2 or 3 live neighbors
            if alive == 2 or alive == 3:
                new_database[cell] = [database[cell][0], database[cell][1], "alive"]
            else:
                new_database[cell] = [database[cell][0], database[cell][1], "dead"]
        else:
            # If the cell is dead, then it springs to life only in the case that it has 3 live neighbors
            if alive == 3:
                new_database[cell] = [database[cell][0], database[cell][1], "alive"]
            else:
                new_database[cell] = [database[cell][0], database[cell][1], "dead"]
    return new_database

    '''if (database[cell][0] == 0 and database[cell][1] != 0 and database[cell][1] != H-length): #the leftmost column
        neighbor_states = [database[cell+1][2], database[cell+W/length][2],
                        database[cell+W/length+1][2], database[cell-W/length][2], database[cell-W/length+1][2]] #the rightmost column
    elif (database[cell][0] == W-length and database[cell][1] != 0 and database[cell][1] != H-length):
        neighbor_states = [database[cell-1][2], database[cell+W/length][2],
                            database[cell+W/length-1][2], database[cell-W/length][2] ,database[cell-W/length-1][2]]     
    elif database[cell][1] == 0 and database[cell][0] != 0 and database[cell][0] != W-length: #the uppermost row
        neighbor_states = [database[cell+1][2], database[cell-1][2], database[cell+W/length][2],
                            database[cell+W/length+1][2], database[cell+W/length-1][2]]
    elif database[cell][1] == H-length and database[cell][0] != 0 and database[cell][0] != W-length: #the lowest row
        neighbor_states = [database[cell+1][2], database[cell-1][2], database[cell-W/length][2], 
                            database[cell-W/length+1][2], database[cell-W/length][2]]
    elif database[cell][0] == 0 and database[cell][1] == 0: #0,0
        neighbor_states = [database[cell+1][2], database[cell+W/length][2], database[cell+W/length+1][2]]
    elif database[cell][0] == W-length and database[cell][1] == 0:
        neighbor_states = [database[cell-1][2], database[cell+W/length][2], database[cell+W/length-1][2]]
    elif database[cell][0] == 0 and database[cell][1] == H-length:
        neighbor_states = [database[cell+1][2],database[cell-W/length][2], database[cell-W/length+1][2]]
    elif database[cell][0] == W-length and database[cell][1] == H-length:
        neighbor_states = [database[cell-1][2], database[cell-W/length][2], database[cell-W/length-1][2]]    
    else:    
        neighbor_states = [database[cell+1][2], database[cell-1][2], database[cell+W/length][2],
                        database[cell+W/length+1][2], database[cell+W/length-1][2],
                        database[cell-W/length][2], database[cell-W/length+1][2],
                        database[cell-W/length-1][2]]

    if database[cell][2] == "alive":
    #If the cell is alive, then it stays alive if it has either 2 or 3 live neighbors
        if alive == 2 or alive == 3:
            pass
        else:
            database[cell][2] = "dead"
    else:
    #If the cell is dead, then it springs to life only in the case that it has 3 live neighbors
        if alive == 3:
            database[cell][2] = "alive"'''
    """print(" ")
    print(database)"""


# updating the board according to the rule
def update_canvas():
    for data in database.values():
        if data[2] == "alive":
            create_square(canvas, data[0], data[1], length, "yellow")
        else:
            create_square(canvas, data[0], data[1], length, "dark blue")
    root.update()


def main():
    global database
    update_canvas()
    time.sleep(DELAY_TIME * 2)
    while True:
        database = generate_new_database()
        update_canvas()
        time.sleep(DELAY_TIME)


root.after(0, main)
root.mainloop()
