import sys
import random
from colorama import Fore, Style, init
import string
import types

# Initialize colorama
init()

# Constants
consts = types.SimpleNamespace()
consts.CHAR_HIT = "X"
consts.CHAR_WATER = "."
consts.CHAR_MISS = "-"
consts.BOARD_SIZE = 10
consts.SHIP_TYPES = {
    "Aircraft Carrier": 5,
    "Battleship": 4,
    "Submarine": 3,
    "Destroyer": 3,
    "Patrol Boat": 2,
}

# Function to convert alphabetic y-coordinate to numeric coordinate
def convert_alphabetic_to_numeric(letter: str):
    return ord(letter.upper()) - ord("A")

# Function to convert numeric y-coordinate to alphabetic coordinate
def convert_numeric_to_alphabetic(numeric: int):
    return chr(ord("A") + numeric)

def format_cell(cell: str, show_ships) -> str:
    match cell:
        case consts.CHAR_HIT: 
            return Fore.RED + cell + Style.RESET_ALL
        case consts.CHAR_MISS: 
            return Fore.WHITE + cell + Style.RESET_ALL
        case consts.CHAR_WATER: 
            return Fore.CYAN + cell + Style.RESET_ALL
        case _: 
            return Fore.YELLOW + cell + Style.RESET_ALL if show_ships else Fore.CYAN + consts.CHAR_WATER + Style.RESET_ALL


# Function to initialize an empty game board
def initialize_board():
    board = []
    for _ in range(consts.BOARD_SIZE):
        row = [consts.CHAR_WATER] * consts.BOARD_SIZE
        board.append(row)
    return board


# Function to randomly place ships on the board
def place_ships(board):
    for ship, length in consts.SHIP_TYPES.items():
        placed = False
        while not placed:
            x = random.randint(0, consts.BOARD_SIZE - 1)
            y = random.randint(0, consts.BOARD_SIZE - 1)
            orientation = random.choice(["horizontal", "vertical"])
            if orientation == "horizontal" and x + length <= consts.BOARD_SIZE:
                valid = True
                for i in range(length):
                    if board[y][x + i] != consts.CHAR_WATER:
                        valid = False
                        break
                if valid:
                    for i in range(length):
                        board[y][x + i] = ship[0]
                    placed = True
            elif orientation == "vertical" and y + length <= consts.BOARD_SIZE:
                valid = True
                for i in range(length):
                    if board[y + i][x] != consts.CHAR_WATER:
                        valid = False
                        break
                if valid:
                    for i in range(length):
                        board[y + i][x] = ship[0]
                    placed = True


# Function to print the player and computer boards side by side
def print_board(player_board, computer_board):
    print("Player's Board    Computer's Board")
    print(
        "  "
        + " ".join(str(i) for i in range(consts.BOARD_SIZE))
        + "       "
        + " ".join(str(i) for i in range(consts.BOARD_SIZE))
    )
    for i, (player_row, computer_row) in enumerate(
        zip(player_board, computer_board)
    ):  
        player_row_display = [
            format_cell(cell, True) for cell in player_row
        ]
        computer_row_display = [
            format_cell(cell, False)
            for cell in computer_row
        ]
        
        print(
            convert_numeric_to_alphabetic(i)
            + " "
            + " ".join(player_row_display)
            + "     "
            + convert_numeric_to_alphabetic(i)
            + " "
            + " ".join(computer_row_display)
        )


# Function to check if a position is valid on the board
def is_valid_position(x, y):
    return 0 <= x < consts.BOARD_SIZE and 0 <= y < consts.BOARD_SIZE


# Function to display game rules
def display_rules():
    rules = """
    BATTLESHIP GAME RULES:

    1. The game is played on a 10x10 grid.
    2. Each player has a fleet of 5 ships to place on their board.
        The ships are: Aircraft Carrier (5), Battleship (4), Submarine (3),
        Destroyer (3), and Patrol Boat (2).
    3. Players take turns guessing the coordinates to attack on the opponent's board.
    4. If a player's guess hits a ship, it's a "Hit!" and the opponent marks it as such.
        If it misses, it's a "Miss!" and the opponent marks it as such.
    5. The first player to sink all of the opponent's ships wins the game.
    
    Have fun playing Battleship!
    """  # noqa violation_error

    print(rules)


# Function to show the start menu
def show_start_menu():
    print(
        r"""
   ____              __    __    ___                   __                 
  /\  _`\           /\ \__/\ \__/\_ \                 /\ \      __           
  \ \ \L\ \     __  \ \ ,_\ \ ,_\//\ \      __    ____\ \ \___ /\_\  _____   
   \ \  _ <'  /'__`\ \ \ \/\ \ \/ \ \ \   /'__`\ /',__\\ \  _ `\/\ \/\ '__`\ 
    \ \ \L\ \/\ \L\.\_\ \ \_\ \ \_ \_\ \_/\  __//\__, `\\ \ \ \ \ \ \ \ \L\ \\
     \ \____/\ \__/.\_\\ \__\\ \__\/\____\ \____\/\____/ \ \_\ \_\ \_\ \ ,__/
      \/___/  \/__/\/_/ \/__/ \/__/\/____/\/____/\/___/   \/_/\/_/\/_/\ \ \/ 
                                                                       \ \_\ 
                                                   
        Welcome to Battleship!

        1. Start Game
        2. Rules
        3. Exit
    """
    )


# Main Menu
def main():
    show_start_menu()
    while True:
        choice = input("Enter your choice: ")

        if choice == "1":
            start_game()
        elif choice == "2":
            display_rules()
        elif choice == "3":
            print("Thanks for playing Battleship!")
            sys.exit()
        else:
            print("Invalid choice. Try again.")


# Function to start the game
def start_game():
    # Initialize game board
    player_board = initialize_board()
    computer_board = initialize_board()

    # Place ships on the board
    place_ships(player_board)
    place_ships(computer_board)

    # Initialize used coordinates list
    used_coordinates = []
    used_coordinates_computer = []

    # Game loop
    while True:
        print_board(player_board, computer_board)

        # Player's Move
        print("Player's Move")
        player_shot_valid = False
        while not player_shot_valid:
            try:
                y_input = (
                    input("Enter y-coordinate (A-J): or 'Exit' to quit: ")
                    .strip()
                    .upper()
                )
                if y_input == "EXIT":
                    print("Thanks for playing Battleship!")
                    sys.exit()

                # Validate the y-coordinate input
                if len(y_input) == 1 and "A" <= y_input <= "J":
                    y = convert_alphabetic_to_numeric(y_input)
                else:
                    print(
                        "Please enter a single letter from A to J for the y-coordinate."
                    )
                    continue

                x_input = (
                    input("Enter x-coordinate (0-9): or type 'exit' to quit: ")
                    .strip()
                    .upper()
                )
                if x_input == "EXIT":
                    print("Thanks for playing Battleship!")
                    sys.exit()
                try:
                    x = int(x_input)
                except ValueError:
                    print(
                        "Invalid x-coordinate. Please enter a number from 0 to 9."
                    )
                    continue

                # Check if x-coordinate is valid
                if is_valid_position(x, y) and (x, y) not in used_coordinates:
                    used_coordinates.append((x, y))  # Record the shot
                    player_shot_valid = True

                # Check for hit or miss
                if computer_board[y][x] != consts.CHAR_WATER:
                    print("Hit!")
                    computer_board[y][x] = consts.CHAR_HIT
                else:
                    print("Miss!")
                    computer_board[y][x] = consts.CHAR_MISS

                # Check if player has won
                if all(
                    consts.CHAR_HIT in cell
                    for row in computer_board
                    for cell in row
                    if cell not in [consts.CHAR_WATER, consts.CHAR_MISS, consts.CHAR_HIT]
                ):
                    print_board(player_board, computer_board)
                    print("Congratulations! You won!")
                    sys.exit()

            except ValueError as e:
                print(e)

            # Computer's move
            print("Computer's Move")
            computer_shot_valid = False
            while not computer_shot_valid:
                x, y = (
                    random.randint(0, consts.BOARD_SIZE - 1),
                    random.randint(0, consts.BOARD_SIZE - 1),
                )
                if (x, y) not in used_coordinates_computer:
                    used_coordinates_computer.append((x, y))
                    computer_shot_valid = True
                    print(
                        f"Computer targeted {convert_numeric_to_alphabetic(y)}{x}"
                    )

            # Check for hit or miss
            if player_board[y][x] != Fore.CYAN + consts.CHAR_WATER + Style.RESET_ALL:
                print(
                    "Computer hit your ship "
                    + convert_numeric_to_alphabetic(y)
                    + str(x)
                    + "!"
                )
                player_board[y][x] = consts.CHAR_HIT
            else:
                print(
                    "Computer missed "
                    + convert_numeric_to_alphabetic(y)
                    + str(x)
                    + "!"
                )
                player_board[y][x] = consts.CHAR_MISS

            # Check if computer has won
            if all(
                consts.CHAR_HIT in cell
                for row in player_board
                for cell in row
                if cell not in [consts.CHAR_WATER, consts.CHAR_MISS, consts.CHAR_HIT]
            ):
                print_board(player_board, computer_board)
                print("Game Over! Computer won!")
                sys.exit()


# If the program is run (instead of imported), run the game:
if __name__ == "__main__":
    main()
