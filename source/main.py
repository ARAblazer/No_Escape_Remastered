"""Entry point for the game"""
# NOTE: Curses coordinates are (y, x) as opposed to the standard (x, y)

# Imports
import json
from time import sleep

from game import Game
from interface import Interface
from map import Map
from player import Player

# Dimension constants
HEIGHT = 32
DISPLAY_WIDTH = 41
MAP_WIDTH = 75
REPR_HEIGHT = 5
RESULT_HEIGHT = 11


# NOTE: stdscr is used by the curses wrapper. It is unused here, but is required for the code to run
def level_one(stdscr):
    """First level of the game"""
    stdscr.clear()
    # Creates room dictionary from a JSON file
    with open('levels/level_one.json') as rooms_file:
        rooms = json.load(rooms_file)

    # Initialize game with empty inventory in the Dark Room
    game = Game(Player([]), Map(rooms, 'Dark Room'))

    # Player must reach the Stairwell to leave the level
    interface.main_loop(game, level_one, 'Stairwell')

    interface.result_window.clear()
    interface.result_window.addstr('You ascend the stairs...')
    interface.result_window.refresh()
    sleep(2)

    interface.start_level('LEVEL TWO', game, level_function=level_two)


def level_two(stdscr, game):
    """
    Second level of the game

    Parameters:
        game (Game) game object inherited from the first level to allow the inventory to carry over
    """
    stdscr.clear()
    with open('levels/level_two.json') as rooms_file:
        rooms = json.load(rooms_file)

    game.map = Map(rooms, 'Stairwell')

    interface.main_loop(game, level_one, 'Elevator Shaft')

    interface.result_window.clear()
    interface.result_window.addstr('You step into the elevator only to')
    interface.result_window.addstr(1, 0, 'realize it is just an empty shaft.')
    interface.result_window.refresh()
    sleep(2)
    interface.result_window.addstr(2, 0, 'You fall...')
    interface.result_window.refresh()
    sleep(5)
    interface.result_window.clear()
    interface.result_window.addstr(3, 0, 'You awaken to find yourself in the \nCellar with none of your items.')
    interface.result_window.refresh()
    sleep(3)

    interface.start_level('LEVEL THREE', level_function=level_three)


def level_three(stdscr):
    """Third level of the game"""
    stdscr.clear()
    with open('levels/level_three.json') as rooms_file:
        rooms = json.load(rooms_file)

    game = Game(Player([]), Map(rooms, 'Cellar'))

    interface.main_loop(game, level_three, 'Exit')

    interface.result_window.clear()
    interface.result_window.addstr('You crawl through the tunnel towards')
    interface.result_window.addstr(1, 0, 'the light.')
    interface.result_window.refresh()
    sleep(2)
    interface.result_window.addstr(1, 11, 'You emerge and feel the ')
    interface.result_window.addstr(2, 0, 'sunlight on your skin at long last.')
    interface.result_window.refresh()
    sleep(5)

    # This message displays until the game is closed
    interface.start_level('CONGRATULATIONS! YOU ESCAPED!', end=True)


if __name__ == '__main__':
    # Global window initialization
    interface = Interface(HEIGHT, DISPLAY_WIDTH, REPR_HEIGHT, RESULT_HEIGHT, MAP_WIDTH)

    # Title display
    interface.start_level('NO ESCAPE')

    interface.result_window.addstr('Commands:\n'
                                   '  go [direction] (n, s, e, or w)\n'
                                   '  get [item]\n'
                                   '  use [item] (only for certain items)\n'
                                   '  help (displays this list)\n\n'
                                   'Press ENTER to continue')

    interface.result_window.refresh()

    # Leave the title screen when the player hits enter (ordinal code 10)
    while interface.result_window.getch() != 10:
        continue

    interface.start_level('LEVEL ONE', level_function=level_one)
