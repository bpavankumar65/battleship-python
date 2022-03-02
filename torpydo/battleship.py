import random
import os
import colorama
import platform
import time
from typing import List, Optional

from colorama import Fore, Back, Style
from torpydo.ship import Color, Letter, Position, Ship
from torpydo.game_controller import GameController
from torpydo.telemetryclient import TelemetryClient
from torpydo.utils import print_with_color, BColors

print("Starting")

myFleet = []
enemyFleet = []

def main():
    TelemetryClient.init()
    TelemetryClient.trackEvent('ApplicationStarted', {'custom_dimensions': {'Technology': 'Python'}})
    colorama.init()
    print(Fore.YELLOW + r"""
                                    |__
                                    |\/
                                    ---
                                    / | [
                             !      | |||
                           _/|     _/|-++'
                       +  +--|    |--|--|_ |-
                     { /|__|  |/\__|  |--- |||__/
                    +---------------___[}-_===_.'____                 /\
                ____`-' ||___-{]_| _[}-  |     |_[___\==--            \/   _
 __..._____--==/___]_|__|_____________________________[___\==--____,------' .7
|                        Welcome to Battleship                         BB-61/
 \_________________________________________________________________________|""" + Style.RESET_ALL)

    initialize_game()

    start_game()

def start_game():
    global myFleet, enemyFleet
    # clear the screen
    if(platform.system().lower()=="windows"):
        cmd='cls'
    else:
        cmd='clear'   
    os.system(cmd)
    print(r'''
                  __
                 /  \
           .-.  |    |
   *    _.-'  \  \__/
    \.-'       \
   /          _/
   |      _  /
   |     /_\
    \    \_/
     """"""""''')

    current_round = 0

    while True:
        current_round += 1

        print()
        print_with_color("Player, it's your turn. Keep in mind: The game board has size from A to H and 1 to 8", color=BColors.CYAN)

        position = parse_position(input(f"Turn {current_round}: Enter coordinates for your shot (i.e A3):"))

        is_hit = GameController.check_is_hit(enemyFleet, position)
        if is_hit:
            print_with_color(r'''
                \          .  ./
              \   .:"";'.:..""   /
                 (M^^.^~~:.'"").
            -   (/  .    . . \ \)  -
               ((| :. ~ ^  :. .|))
            -   (\- |  \ /  |  /)  -
                 -\  \     /  /-
                   \  \   /  /''', color=BColors.RED)

        print_with_color("Yeah ! Nice hit !" if is_hit else "Miss", color=BColors.RED if is_hit else BColors.BLUE)
        if is_hit:
            GameController.remove_if_hit(enemyFleet, position)
        else:
            if GameController.check_ship_sunk(enemyFleet, position):
                print(Fore.YELLOW + "Left Over Ships : " + Style.RESET_ALL)
                GameController.print_left_over_ships(enemyFleet)

        TelemetryClient.trackEvent('Player_ShootPosition', {'custom_dimensions': {'Position': str(position), 'IsHit': is_hit}})

        print_with_color(
            "Computer is thinking..",
            color=BColors.CYAN
        )
        time.sleep(1.5)

        position = get_random_position()
        is_hit = GameController.check_is_hit(myFleet, position)
        print()
        print_with_color(
            f"Computer shoot in {str(position)} and {'hit your ship!' if is_hit else 'miss'}",
            color=BColors.RED if is_hit else BColors.YELLOW
        ) 

        if is_hit:
            print_with_color(r'''
                \          .  ./
              \   .:"";'.:..""   /
                 (M^^.^~~:.'"").
            -   (/  .    . . \ \)  -
               ((| :. ~ ^  :. .|))
            -   (\- |  \ /  |  /)  -
                 -\  \     /  /-
                   \  \   /  /''', color=BColors.RED)


        TelemetryClient.trackEvent('Computer_ShootPosition', {'custom_dimensions': {'Position': str(position), 'IsHit': is_hit}})

def parse_position(input: str):
    letter = Letter[input.upper()[:1]]
    number = int(input[1:])
    position = Position(letter, number)

    return Position(letter, number)

def get_random_position():
    rows = 8
    lines = 8

    letter = Letter(random.randint(1, lines))
    number = random.randint(1, rows)
    position = Position(letter, number)

    return position

def initialize_game():
    initialize_myFleet()

    initialize_enemyFleet()

def validate_ship_in_field(ship: Ship):
    for position in ship.positions:
        if position.row < 1 or position.row > 8:
            return False
    return True

def validate_overlapping_ships(ships: List[Ship], check_as_well_position: Optional[Position] = None):
    visited_position: List[Position] = []
    
    for ship in ships:
        for position in ship.positions:
            if position in visited_position:
                return False

            visited_position.append(position)

    if check_as_well_position is not None:
        if check_as_well_position in visited_position:
            return False

    return True

def validate_correct_size(ship: Ship):
    return ship.size == len(ship.positions)

def validate_no_gap(positions: List[Position]):
    first_pos = positions[0]
    last_pos  = positions[-1]

    size = len(positions)

    v_range = list(range(min(p.row for p in positions), max(p.row for p in positions)+1))
    h_range = list(range(min(p.column.value for p in positions), max(p.column.value for p in positions)+1))

    if len(v_range) == 1:
        if len(h_range) != size:
            return False

    elif len(h_range) == 1:
        if len(v_range) != size:
            return False

    else:
        return False

    for position in positions:
        if position.column.value not in h_range:
            return False
        if position.row not in v_range:
            return False

    return True

def validate_ships(ships: List[Ship]):
    
    if not all(validate_correct_size(ship) for ship in ships):
        return False
    
    if not all(validate_no_gap(ship.positions) for ship in ships):
        return False
    
    return validate_overlapping_ships(ships)

def print_matrix(ships: List[Ship], positions):
    import numpy
    m = numpy.zeros([8, 8], dtype='int')

    for ship in ships:
        for position in ship.positions:
            m[position.row-1, position.column.value-1] = ship.size

    for position in positions:
        m[position.row-1, position.column.value-1] = 10

    def get(i: int):
        if i == 0:
            color = BColors.BLUE
            text = "~"
        elif i == 2:
            color = BColors.YELLOW
            text = "P"
        
        elif i == 3:
            color = BColors.YELLOW
            text = "D"

        elif i == 4:
            color = BColors.YELLOW
            text = "B"

        elif i == 5:
            color = BColors.YELLOW
            text = "A"

        elif i == 10:
            color = BColors.RED
            text = "X"

        return f"{color}{text}{BColors.ENDC}"

    print("")
    print("  | " + ' | '.join([c for c in "ABCDEFGH"]) + " |")
    for i, r in enumerate(m):
        print(f"{i+1} | " + ' | '.join([get(c) for c in r]) + " |")

    print("  ---------------------------------")
    print("")
    print("\tX: New Position")
    print("\tA: Aircraft Carrier")
    print("\tB: Battleship")
    print("\tS: Submarine")
    print("\tD: Destroyer")
    print("\tP: Patrol Boat")
    print("")
    print("")

    
def initialize_myFleet():
    global myFleet

    myFleet = GameController.initialize_ships()

    print_with_color("Please position your fleet (Game board has size from A to H and 1 to 8) :", color=BColors.CYAN)

    for ship in myFleet:
        print()
        print_with_color(f"Please enter the positions for the {ship.name} (size: {ship.size})", color=BColors.CYAN)

        while True:
            clear = False
            positions = []
            for i in range(ship.size):
                while True:
                    position_input: str = input(f"Enter position {i+1} of {ship.size} (i.e A3) or enter 'clear' to start over:")

                    if position_input == "clear":
                        clear = True
                        break
                    
                    try:
                        position = Position.from_str(position_input)
                    except (ValueError, KeyError):
                        print_with_color(f"\tPosition {position_input} is not a valid input. Game board has size from A to H and 1 to 8", color=BColors.RED)
                        continue

                    if not validate_no_gap(positions + [position]):
                        print_with_color(f"\tYour ship has a hole. It won't swim. Please weld it or build better.", color=BColors.RED)
                        continue

                    elif not validate_overlapping_ships(myFleet, check_as_well_position=position):
                        print_with_color(f"\tAnother ship is on this position. Please try again. If you got stuck enter 'clear' to build the ship from scratch.", color=BColors.RED)
                        continue

                    else:
                        positions.append(position)
                        print_matrix(myFleet, positions)
                        break
                if clear:
                    break
            if clear:
                continue

            ship.positions = positions
            break

    return myFleet

            #TelemetryClient.trackEvent('Player_PlaceShipPosition', {'custom_dimensions': {'Position': position_input, 'Ship': ship.name, 'PositionInShip': i}})

def initialize_enemyFleet():
    global enemyFleet

    enemyFleet = GameController.initialize_ships()

    validated_ships = []

    for ship in enemyFleet:
        while True:

            positions = []
            while len(positions) < ship.size:
                position = get_random_position()
                if validate_no_gap(positions + [position]):
                    positions.append(position)
                

            ship.positions.extend(positions)
            if validate_overlapping_ships(validated_ships + [ship]):
                validated_ships.append(ship)
                break

            ship.positions = []
    print(enemyFleet)


if __name__ == '__main__':
    main()
