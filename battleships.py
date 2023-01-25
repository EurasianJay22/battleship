import random
import time

N = 10
size_of_fleet_in_squares = 0

class Player:
    def __init__(self, name):
        self.attempts = 0
        self.direction_tracker = 0
        self.name = name
        self.ships_grid = [["-"] * N for i in range(N)]
        self.shot_tracker = [["-"] * N for i in range(N)]
        self.hit_count = 0
        self.fleet_size = 0
        self.miss_count = 0
        self.successful_shots = []
        self.missed_shots = []

user = Player("user")
computer = Player("computer")

def main(): 
    # ====== Test statements ======
    #place_ships(computer, 3)
    #place_ships(user, 3)
    #user.ships_grid = [['-', 'S', 'S', 'S', '-'], ['-', '-', '-', '-', '-'], ['-', '-', '-', '-', '-'], ['-', '-', '-', '-', '-'], ['-', '-', '-', '-', '-']]
    #user.fleet_size = 3
    # =============================
    place_ships(computer, 5, 4, 3, 3, 2)
    place_ships(user, 5, 4, 3, 3, 2)
    # Check that the same number of ships was placed for both players
    if user.fleet_size != computer.fleet_size:
        print("Error 1: Fleet sizes do not match. Please restart.")
    else:
        size_of_fleet_in_squares = user.fleet_size
    print("YOUR SHIPS")
    display_grid(user, user.ships_grid)
    time.sleep(1)
    #print("COMPUTER SHIPS")
    #display_grid(computer, computer.ships_grid)
    while True:
        user_turn()
        if user.hit_count == size_of_fleet_in_squares:
            print("WINNER! You have sunk all the enemy's ships")
            return
        computer_turn()
        if computer.hit_count == size_of_fleet_in_squares:
            print("Defeated! The enemy has sunk all your ships")
            return

def computer_turn():
    print("====== OPPONENT'S TURN ======")
    print()
    time.sleep(1)
    if len(computer.successful_shots) == 0:
        # When theres no data from existing hits
        while True:
            target_row = random_row()
            target_column = random_column()
            if computer.shot_tracker[target_row][target_column] == "-":
                break
        perform_strike(computer, user, target_row, target_column)
    else:
        # Use the last successful hit
        last_hit = computer.successful_shots[-1]
        #last_checked_square = last_hit
        strike_row = int(last_hit[0])
        strike_column = int(last_hit[1])
        while True:
            # Determine coords to strike, then break
            # last_hit is a string consisting of RC where R = row index, C = column index
            # Change the direction to look in if the current setting points outside the array
            if last_hit[0] == '0' and computer.direction_tracker % 4 == 0:
                computer.direction_tracker += 1
            if last_hit[1] == str(N - 1) and computer.direction_tracker % 4 == 1:
                computer.direction_tracker += 1
            if last_hit[0] == str(N - 1) and computer.direction_tracker % 4 == 2:
                computer.direction_tracker += 1
            if last_hit[1] == '0' and computer.direction_tracker % 4 == 3:
                computer.direction_tracker += 1
            strike_direction = computer.direction_tracker % 4
            if strike_direction == 0 or strike_direction == 2:
                if strike_direction == 0:
                    strike_row = strike_row - 1
                else:
                    strike_row = strike_row + 1
            else:
                if strike_direction == 1:
                    strike_column = strike_column + 1
                else:
                    strike_column = strike_column - 1
            if computer.shot_tracker[strike_row][strike_column] == "H":
                # Look one square further in the direction of travel
                # Define a helper function that alters coords based on: current coords, strike direction. Returns new coords.
                if computer.direction_tracker % 4 == 0:
                    strike_row -= 1
                elif computer.direction_tracker % 4 == 1:
                    strike_column += 1
                elif computer.direction_tracker % 4 == 2:
                    strike_row += 1
                else:
                    strike_column -= 1
            if computer.shot_tracker[strike_row][strike_column] == "-":
                perform_strike(computer, user, strike_row, strike_column)
                break
            elif computer.shot_tracker[strike_row][strike_column] == "M":
                # Only try a row or column twice before switching to trying the other axis
                computer.miss_count += 1
                if computer.miss_count == 4:
                    computer.miss_count = 0
                    perform_strike(computer, user, random_row(), random_column())
                    break
                if computer.attempts == 0:
                    computer.attempts += 1
                    computer.direction_tracker += 2
                else:
                    computer.attempts = 0
                    computer.direction_tracker += 1
            # If the square inspected is a hit:
                
                #if strike_row < 0 or strike_row >= N:
                    #strike_row = random_row()
                #if strike_column < 0 or strike_column >= N:
                    #strike_column = random_column()
            else:
                strike_row = random_row()
                strike_column = random_column()
    print()
    print("Your opponent's shots so far: ")
    display_grid(computer, computer.shot_tracker)
    print()

# Converts the array coordinates into a display corresponding to the user's grid
def display_coordinates(array_row, array_column):
    display_row = chr(array_row + ord("A"))
    display_column = array_column + 1
    coordinates = "" + display_row + str(display_column)
    return coordinates

def display_grid(player, grid):
    # Construct top border for table
    print("+--", end="")
    for i in range(N):
        print("---", end="")
    print("--+")
    # Left border of table for column headings row
    print("|   ", end="")
    # Column headings
    for i in range(N):
        print(" {column} ".format(column=i+1), end="")
    if N >= 10:
        print("|")
    else:
        print(" |")
    # Each row of the grid, inc border and row label
    for i in range(N):
        print("| {row} ".format(row=chr(i + ord("A"))), end="")
        for j in range(N):
            print(" {square} ".format(square=grid[i][j]), end="")
        print(" |")
    # Construct bottom border for grid
    print("+--", end="")
    for i in range(N):
        print("---", end="")
    print("--+")

def get_row(coordinates):
    row_index = ord(coordinates[0]) - ord('A')
    return row_index

def get_column(coordinates):
    column_index = int(coordinates[1]) - 1
    return column_index

def random_column():
    return random.randint(0, N - 1)

def random_row():
    return random.randint(0, N - 1)

def perform_strike(attacker, defender, row, column):
    if defender.ships_grid[row][column] == "S":
        attacker.shot_tracker[row][column] = "H"
        defender.ships_grid[row][column] = "H"
        attacker.hit_count += 1
        coordinates = display_coordinates(row, column)
        attacker.successful_shots.append("" + str(row) + str(column))
        print("HIT on {coordinates}".format(coordinates = coordinates)) 
    elif defender.ships_grid[row][column] == "H":
        print("These coordinates have already been hit! ({coordinates})".format(coordinates = display_coordinates(row, column)))
    else:
        attacker.shot_tracker[row][column] = "M"
        coordinates = display_coordinates(row, column)
        attacker.missed_shots.append("" + str(row) + str(column))
        print("Miss on {coordinates}".format(coordinates = display_coordinates(row, column)))
    return

def place_ships(player, *ships):
    for ship in ships:
        # Work out max row for vertical placement / max column for horizontal placement
        max = N - ship
        # Vertical or horizontal? Even = vertical, Odd = horizontal
        orientation = random.randint(2, 4) % 2
        # Add the potential coordinates to a dictionary so as to check them before initialising the values in the list
        while True:
            ship_coordinates = {}
            if orientation == 0:
                # Choose row for first square
                row = random.randint(0, max)
                # Choose column
                column = random_column()
                counter = 0
                while counter < ship:
                    ship_coordinates[row] = column
                    #player.ships_grid[row][column] = "S"
                    counter += 1
                    row += 1
            else:
                # Choose row
                row = random_row()
                # Choose column for first square
                column = random.randint(0, max)
                counter = 0
                while counter < ship:
                    # Columns have to be the keys as they change value in the horizontal
                    ship_coordinates[column] = row
                    #player.ships_grid[row][column] = "S"
                    counter += 1
                    column += 1
            squares_already_occupied = 0
            for row, column in ship_coordinates.items():
                # Switch the values if they're horizontal cf line 143
                if orientation == 1:
                    corrected_row = column
                    corrected_column = row
                else:
                    corrected_row = row
                    corrected_column = column
                if player.ships_grid[corrected_row][corrected_column] == "S":
                    squares_already_occupied += 1
                else:
                    continue
            if squares_already_occupied == 0:
                for row, column in ship_coordinates.items():
                    if orientation == 1:
                        corrected_row = column
                        corrected_column = row
                    else:
                        corrected_row = row
                        corrected_column = column
                    player.ships_grid[corrected_row][corrected_column] = "S"
                player.fleet_size += ship
                break
            else:
                continue
    return

def user_turn():
    print("====== YOUR TURN ======")
    print()
    print("Your shots so far:")
    print("H = Hit, M = Miss")
    display_grid(user, user.shot_tracker)
    while True:
        # Get the row to target
        target_row = input("Enter the row to strike (e.g. A): ")
        if len(target_row) > 1:
            print("Row must be a single letter")
            continue
        # Convert the target row into a number corresponding to an array index
        target_row = target_row.upper()
        target_row = ord(target_row) - ord("A")
        if target_row < 0 or target_row >= N:
            print("Row must be a letter between A and " + chr(ord("A") + N - 1))
            continue
        else:
            break
    # Once a valid row is obtained, get the column coordinate
    while True:
            target_column = input("Enter the column to strike (e.g. 1): ")
            if int(target_column) > N or int(target_column) < 1:
                print("Column must be a number between 1 and " + str(N))
                continue
            else:
                # Convert to the array index
                target_column = int(target_column) - 1
                break
    perform_strike(user, computer, target_row, target_column)
    
main()
    

    
