#!/bin/env python3
# "Omelette? Egg!" Game Program
#
# MIT License
#
# Copyright (c) 2026 EditorOne XI
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Laboratory Activity Task: (Done)
# - Implemented CRUD application. (Create, Read, Update, Delete)
# - Implemented 4 Pillars of Python OOP:
#   - Encapsulation
#   - Inheritance
#   - Polymorphism
#   - Abstraction

from platform import system
from random import randint
from scores import EGG_NAMES, EGG_SCORE, OMELETTE_EGG_SCORE, OMELETTE_RETURN_SCALE, Egg, Player
from subprocess import run

# VARIABLES
REVIEW_MESSAGE="REVIEW YOUR EGGS FIRST BEFORE CONTINUING o_O"
get_egg_selectindex: list[int] = [] # Duplication input checker
players: list[Player] = []
start_choice: int | str

# FUNCTIONS
# clear terminal for Unix/Windows
def clear():
    if system() == "Windows":
        run(["cls"], shell=True)
    else:
        print("\033c", end="")

def press_continue():
    input("Press ENTER to continue...")

def header_omelette():
    # Egg ASCII Art Reference: https://textart.sh/topic/egg
    print("""==================================================
                 ██████████████████        
               ██                ██      
           ████    ░░░░░░░░        ████  
           ██      ░░      ░░░░        ██  
       ████  ░░          ░░░░        ██
       ██      ░░          ░░░░        ██
       ██        ░░▒▒░░  ░░░░░░░░        ██
       ██░░        ░░░░░░░░░░░░        ░░██
       ██░░        ░░░░░░░░        ░░██  
       ██░░░░                    ░░██    
           ████░░░░            ░░░░██      
               ████░░░░░░░░░░░░████        
                   ████████████            

       Welcome to Guess the Omelette? Eggs!
==================================================
""")

def omelette_egg_game_info():
    print(f"""
<< GUIDE >> 

The 'Omelette? Eggs!' Game is played by guessing the opponents'
favorite Egg Dishes and outplay them. If you were able to guess their
egg dishes, you can score '{EGG_SCORE} * amplifier' points and lose {EGG_SCORE}
points otherwise to each egg guess.

There is also the core scoring of the game itself, which is "Omelette
Return", in which achieving this allows you to win the game itself.
Omelette Return only increments when your total score in a challenge
is {OMELETTE_RETURN_SCALE} points and above.

The program automatically initiates create player if players are less than
two. This is intended to ensure immediate challenges.
""")

def close_game() -> None:
    print("""
Thank you for playing this game! Or did you?
Program Wrote by Onemig Dincol.
Python Object-oriented programming Laboratory Activity.
""")
    exit(0)

def is_valid_egg_index(index: int, offset: int = 0) -> bool:
    return index - offset >= 0 and index - offset < len(EGG_NAMES)

# For input() that accepts digits only
def is_not_int(value: str) -> bool:
    if not value or not value.isdigit():
        return True
    return False

def print_egg_names():
    temp = '\nList of Egg Dishes:\n'
    space = ' '
    for i in range(len(EGG_NAMES)):
        egg = EGG_NAMES[i]
        display_num = i + 1
        temp += f"[{display_num:2d}] {egg}{space * (25 - len(egg))}"
        if display_num % 3 == 0 or display_num == len(EGG_NAMES):
            print(temp)
            temp = ''
    print('')
    del egg, temp, space

def assign_player() -> bool | Player:
    print("Available Players:\n[1] Back")
    for i in range(len(players)):
        print(f"[{i + 2}] {players[i].name}")
    print('')
    while True:
        player_index = input("Select Player #?: ")
        if is_not_int(player_index):
            continue
        player_index = int(player_index)
        if player_index == 1:
            return False
        elif player_index - 2 not in [n for n in range(len(players))]:
            continue
        else:
            return players[player_index - 2]

def generate_egg() -> Egg:
    while True:
        index_input = input("Select an Egg #?: ")
        if is_not_int(index_input):
            continue
        egg_index = int(index_input)
        if not is_valid_egg_index(egg_index, 1):
            egg_index = randint(1, len(EGG_NAMES))
            print("Random Egg!")
        if egg_index in get_egg_selectindex:
            print("Already exists! Try again.")
        else: break 
    egg_select = EGG_NAMES[egg_index - 1]
    get_egg_selectindex.append(egg_index)
    egg_sauce = input(f"Enter sauce/add-on name for {egg_select} (Optional): ")
    egg_sause_str = f"with {egg_sauce} in it" if egg_sauce else "without any sauce/add-on"
    print(f"""
You cooked {egg_select} {egg_sause_str}.
That seems delicious!
""")
    new_egg = Egg(egg_select, egg_sauce)
    del index_input, egg_index, egg_select, egg_sauce, egg_sause_str
    return new_egg

def create_player():
    clear()
    header_omelette()
    while True:
        new_name = input("Enter your player name: ")
        if new_name in [p.name for p in players]:
            print(f"Player with name '{new_name}' already exists. Try a different name.")
            continue
        break
    players.append(Player(new_name))
    latest_player = players[len(players) - 1]
    print(f"Your player name is {latest_player.name}, remarkable!")
    print("Choose Your 5 Favorite Egg Dishes below.")
    print_egg_names()
    get_egg_selectindex.clear()
    for i in range(5):
        latest_player.add_egg(generate_egg())
    latest_player.get_eggs()
    del new_name, latest_player
    print(REVIEW_MESSAGE)
    press_continue()
    clear()

def edit_player():
    sel_player = assign_player()
    if not sel_player:
        press_continue()
        clear()
        return
    print(f"""
Actions for {sel_player.name}?
[1] Change Eggs
[2] Remove Player
[3] Back
""")
    sel_edit = int(input("Select Action #?: ") or 3)
    match sel_edit:
        case 1:
            clear()
            get_egg_selectindex.clear()
            sel_player.clear_eggs()
            print(f"Changing {sel_player.name}'s Eggs:")
            print_egg_names()
            for i in range(5):
                sel_player.add_egg(generate_egg())
            sel_player.get_eggs()
            print(REVIEW_MESSAGE)
        case 2:
            players.remove(sel_player)
            print(f"Removed {sel_player.name} to the Player List.")
        case _:
            pass
    del sel_player, sel_edit
    press_continue()
    clear()

def score_summary():
    if len_player < 1:
        print("No one is a chef yet!")
    else:
        sel_player = assign_player()
        if not sel_player:
            print("Invalid input!")
        else:
            print(f"\nAssessing {sel_player.name}'s Scores:")
            omelette = [sel_player, sel_player.omelette_egg()]
            omelette.extend([egg for egg in sel_player.get_eggs(True)])
            # POLYMORPHISM, and Omelette Return exits the game.
            for o in omelette:
                if o.get_score() == OMELETTE_EGG_SCORE:
                    close_game()
            print("Data Summary Sequence: Player Score, Omelette Return, Egg Scores,")
            del omelette
        del sel_player
        press_continue()
        clear()

def game_queue():
    len_player = len(players)
    print("""
Click enter to set opponent or your player to the latest created
player. Assigning opponent as your player aborts the game
immediately. Choose your opponent first before your player.
""")
    print("Choose Opponent:")
    prev_player = assign_player() or players[len_player - 2]
    print("\nChoose your Player:")
    curr_player = assign_player() or players[len_player - 1]
    if prev_player == curr_player:
        print("Cannot make a match to the same player. Game Over.")
        return
    egg_names_found: list[str] = []
    get_egg_selectindex.clear()
    press_continue()
    clear()
    print(f"""
*** GAME QUEUE: {curr_player.name} VS {prev_player.name} ***

What are {prev_player.name}'s Favorite Eggs?!""")
    print_egg_names()
    for i in range(5):
        print(f"({i + 1}/5)")
        egg_index = int(input("Select Egg #?: ") or randint(1, len(EGG_NAMES)))
        egg_index = egg_index if is_valid_egg_index(egg_index, 1) else EGG_NAMES.index("Omelette") + 1
        if egg_index in get_egg_selectindex:
            curr_player.punishment()
            print("You have answered the same correct answer. Score Deducted!\n")
            continue
        egg_select = EGG_NAMES[egg_index - 1]
        egg_sauce = input("Egg sauce/add-on? (Optional): ")
        queue_egg = Egg(egg_select, egg_sauce)
        has_match = prev_player.has_egg(queue_egg)
        if has_match:
            curr_player.add_score(EGG_SCORE, has_match.score_amp)
            egg_names_found.append(has_match.name)
            get_egg_selectindex.append(egg_index)
            print(f"You scored {EGG_SCORE * has_match.score_amp} points. Good Job!\n")
        else:
            curr_player.deduct_score(EGG_SCORE)
            print(f"You lost {EGG_SCORE} points. Try again!\n")
    # Manage scores to eggs too
    for egg in prev_player.get_eggs(True):
        if egg.name not in egg_names_found:
            egg.add_score(1)
        else:
            egg.deduct_score(1)
    print("*** GAME OVER! ***")
    prev_player.get_eggs()
    curr_player.get_score(True)
    del len_player, prev_player, curr_player, egg_names_found, egg_index, egg_select, egg_sauce, queue_egg, has_match

# MAIN PROCESS
clear()
header_omelette()
print("""[1] Start
[2] How to Play?
[3] Exit Program
""")
start_choice = input("Select #?: ")
start_choice = int(start_choice) if start_choice.isdigit() else 0

if start_choice == 2:
    start_choice = 1
    omelette_egg_game_info()
    press_continue()

while start_choice == 1:
    len_player = len(players)
    if len(players) > 1:
        header_omelette()
        print(f"""[1] Challenge
[2] Create Player
[3] Modify Player
[4] Player Score Summary
[5] Exit Program
""")
        while True:
            menu_choice = input("Select Option #?: ")
            if is_not_int(menu_choice):
                continue
            else:
                break
        match int(menu_choice):
            case 1:
                game_queue()
                press_continue()
                clear()
            case 2:
                create_player()
            case 3:
                edit_player()
            case 4:
                score_summary()
            case _:
                break
    else:
        create_player()
    del len_player

del REVIEW_MESSAGE, get_egg_selectindex, players, start_choice
close_game()
