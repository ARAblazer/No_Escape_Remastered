"""Interface class built using curses' CLI tools"""


# Imports
import curses
from curses.textpad import rectangle
from time import sleep

curses.initscr()

# Colors
curses.start_color()

# Colors have to be initialized as text, background pairs
# Adding 8 makes the colors bright
curses.init_pair(1, curses.COLOR_RED + 8, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_YELLOW + 8, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_CYAN + 8, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_MAGENTA + 8, curses.COLOR_BLACK)
curses.init_pair(5, curses.COLOR_GREEN + 8, curses.COLOR_BLACK)
curses.init_pair(6, curses.COLOR_BLUE + 8, curses.COLOR_BLACK)

RED = curses.color_pair(1)
YELLOW = curses.color_pair(2)
CYAN = curses.color_pair(3)
PURPLE = curses.color_pair(4)
GREEN = curses.color_pair(5)
BLUE = curses.color_pair(6)


class Interface:
    """
    Parameters:
        height (int): height of the display in rows
        display_width (int): width of the display (left side of screen) in columns
        repr_height (int): height of the game repr in rows
        result_height (int): height of the result window in rows
        map_width (int): width of the map window (right side of screen) in columns

    Methods:
        base_display(self): draws outline of the CLI
        game_display(self, game): handles drawing of game repr in the repr_window
        result_display(self, result): handles drawing of the command result in the result_window
        update_map(self, _map, rooms_discovered): updates the map display, redrawing each room and various ornaments
        start_level(self, level_name, *args, level_function=None, end=False): starts a level and displays a title
        main_loop(self, game, checkpoint, trigger_room): main display loop, clears and updates all windows as necessary
    """
    def __init__(self, height, display_width, repr_height, result_height, map_width):
        self.height = height
        self.display_width = display_width
        self.repr_height = repr_height
        self.result_height = result_height
        self.map_width = map_width

        self.display_window = curses.newwin(self.height, self.display_width, 0, 0)
        self.repr_window = curses.newwin(self.repr_height, self.display_width - 2, 1, 1)
        self.result_window = curses.newwin(self.result_height, self.display_width - 2, self.repr_height + 2, 1)
        self.map_window = curses.newwin(self.height, self.map_width, 0, self.display_width)

        # Hide the cursor
        curses.curs_set(False)

    def base_display(self):
        """Basic display for the CLI"""
        # Draws a border around the game display (left side)
        self.display_window.border()
        # Separator line between the game repr and the result display
        self.display_window.addstr(self.repr_height + 1, 0, '├')
        self.display_window.hline(self.repr_height + 1, 1, curses.ACS_HLINE, self.display_width - 2)
        self.display_window.addstr(self.repr_height + 1, self.display_width - 1, '┤')
        # Input box
        rectangle(self.display_window, self.height - 4, 1, self.height - 2, self.display_width - 2)
        self.display_window.refresh()

        # Draws a border around the map window (right side)
        self.map_window.border()
        self.map_window.refresh()

    def game_display(self, game):
        """
        Method for displaying the game repr

        Parameters:
            game (Game): game object whose repr will be displayed
        """
        for index, line in enumerate(repr(game).split('\n')):
            # The first line is always the room name
            if index == 0:
                line = line.split(' the ')
                self.repr_window.addstr(index, 0, line[0])
                self.repr_window.addstr(index, len(line[0]), ' the ')
                # Room name is blue
                self.repr_window.addstr(index, len(line[0]) + len(' the '), line[1], BLUE)
            # If the second line starts with the letter Y, it is an item
            elif index == 1 and line[0] == 'Y':
                line = line.split(' a ')
                self.repr_window.addstr(index, 0, line[0])
                self.repr_window.addstr(index, len(line[0]), ' a ')

                # Item name color changes based on what item it is
                if line[1].strip() == 'key':
                    color = YELLOW
                elif line[1].strip() == 'hammer':
                    color = GREEN
                elif line[1].strip() == 'sword':
                    color = CYAN
                elif line[1].strip() == 'monster':
                    color = RED
                else:
                    color = PURPLE

                self.repr_window.addstr(index, len(line[0]) + len(' a '), line[1], color)

            else:
                self.repr_window.addstr(index, 0, line)
        self.repr_window.refresh()

    def result_display(self, result):
        """
        Method that displays and updates the result screen

        Parameters:
            result (str): result message to be displayed
        """
        # If there is a result message, display it
        if result is not None:
            # Item messages are treated specially
            if 'You got the' in result:
                result = result.split(' the ')
                self.result_window.addstr(result[0])
                self.result_window.addstr(0, len(result[0]), ' the ')

                # Item names are displayed in their respective colors
                if result[1].strip() == 'key!':
                    color = YELLOW
                elif result[1].strip() == 'hammer!':
                    color = GREEN
                elif result[1].strip() == 'sword!':
                    color = CYAN
                else:
                    color = PURPLE

                self.result_window.addstr(0, len(result[0]) + len(' the '), result[1][:-1], color)
                self.result_window.addstr(0, len(result[0]) + len(' the ' + result[1][:-1]), '!')
            else:
                self.result_window.addstr(result)

            self.result_window.refresh()

    def update_map(self, _map, rooms_discovered):
        """
        Function that updates the map window

        Parameters:
            _map (Map): map object for referencing specific room attributes to be drawn
            rooms_discovered (list(list)): list containing lists of pertinent info about each discovered room

        """
        map = _map

        def draw_room_ornaments():
            """Helper method for displaying room ornaments like items and exits"""
            if 'n' in room[3]:
                self.map_window.addstr(room_y * 3 + 1, room_x * 6 + 4 + n_placement, '╨')
            if 's' in room[3]:
                self.map_window.addstr((room_y * 3 + 3) + (3 * (room_height - 1)), room_x * 6 + 4 + s_placement, '╥')
            if 'e' in room[3]:
                self.map_window.addstr(room_y * 3 + 2 + e_placement, (room_x * 6 + 6) + (6 * (room_width - 1)), '╞═')
            if 'w' in room[3]:
                self.map_window.addstr(room_y * 3 + 2 + w_placement, room_x * 6 + 1, '═╡')
            if 'item' in map.rooms[room[2]]:
                if map.rooms[room[2]]['item'] == 'key':
                    color = YELLOW
                elif map.rooms[room[2]]['item'] == 'hammer':
                    color = GREEN
                elif map.rooms[room[2]]['item'] == 'sword':
                    color = CYAN
                elif map.rooms[room[2]]['item'] == 'monster':
                    color = RED
                else:
                    color = PURPLE

                self.map_window.addstr(room_y * 3 + 2, room_x * 6 + 4, '●', color)

        self.map_window.clear()

        x, y = map.rooms[map.current_room]['coords']
        if 'width' in map.rooms[map.current_room]:
            width = map.rooms[map.current_room]['width']
        else:
            width = 1
        if 'height' in map.rooms[map.current_room]:
            height = map.rooms[map.current_room]['height']
        else:
            height = 1

        # portal rooms do not appear on the map
        if map.current_room != 'Portal':
            rooms_discovered.append(
                [
                    x, y,
                    map.current_room,
                    map.rooms[map.current_room],
                    # Functions for converting room coordinates into their upper-left and lower-right corners:
                    # Upper-left: (6x + 3, 3y + 1)
                    # Lower-right: (6x + 6, 3y + 3)
                    f'rectangle(self.map_window, '
                    f'{y * 3 + 1}, '
                    f'{x * 6 + 2}, '
                    f'{(y * 3 + 3) + (3 * (height - 1))}, '
                    f'{(x * 6 + 6) + (6 * (width - 1))}'
                    f')'
                ]
            )

        self.map_window.border()

        for room in rooms_discovered:
            room_x, room_y = room[0], room[1]
            room_height = room[3]['height'] if 'height' in room[3] else 1
            room_width = room[3]['width'] if 'width' in room[3] else 1
            # Exit placements are used for rooms with widths or heights other than 1 for shifting the exit character to
            # the correct place on the display as to line up with the next room
            n_placement = room[3]['n_placement'] if 'n_placement' in room[3] else 0
            s_placement = room[3]['s_placement'] if 's_placement' in room[3] else 0
            e_placement = room[3]['e_placement'] if 'e_placement' in room[3] else 0
            w_placement = room[3]['w_placement'] if 'w_placement' in room[3] else 0

            # The current room with be drawn green to show the player where they currently are
            if room[2] == map.current_room:
                self.map_window.attron(GREEN)
                eval(room[4])
                draw_room_ornaments()
                self.map_window.attroff(GREEN)
            else:
                eval(room[4])
                draw_room_ornaments()

        self.map_window.refresh()

    def start_level(self, level_name, *args, level_function=None, end=False):
        """
        Function to display messages at the beginning of a level

        Parameters:
            level_name (str): name of the level to be displayed
            level_function (Function): function to be called to start the level
            end (bool) (optional): whether or not the message needs to be escaped with the letter 'q'
        """

        curses.noecho()

        # Clear all displays
        self.repr_window.clear()
        self.result_window.clear()
        self.map_window.clear()

        self.base_display()
        # Display the level name
        self.display_window.addstr(2, (self.display_width - len(level_name)) // 2, level_name, curses.A_BOLD)
        self.display_window.refresh()

        if not end:
            sleep(2)
            self.display_window.clear()
            if level_function is not None:
                curses.wrapper(level_function, *args)
        else:
            while self.display_window.getkey() != 'q':
                continue

    def main_loop(self, game, checkpoint, trigger_room):
        """Main game loop function"""
        rooms_discovered = []
        # Displays pressed keys
        curses.echo()

        # Update all windows
        self.base_display()
        self.game_display(game)
        self.update_map(game.map, rooms_discovered)

        while True:
            # Resize the terminal every iteration (prevents crashes from the window being resized)
            curses.resizeterm(self.height, self.display_width + self.map_width)
            # Hide the cursor
            curses.curs_set(False)

            # If the player enters the trigger room, exit the game loop
            if game.map.current_room == trigger_room:
                break

            # Make the cursor visible before getting input
            curses.curs_set(True)
            # getstr returns a byte value, this code formats that into a plain string by removing the "b''" literal
            command = str(self.display_window.getstr(self.height - 3, 2, 36)).replace("'", '')[1:]
            curses.curs_set(False)

            # Clear all displays
            self.display_window.clear()
            self.repr_window.clear()
            self.result_window.clear()

            # If the player passes a command, the result message will be based on how that command gets parsed
            if command:
                result = game.parse_command(command)
            else:
                result = None

            # If the player dies, update the display and ask them to restart
            death = game.check_death('monster')

            # Update all windows
            self.base_display()
            self.game_display(game)
            self.result_display(result)
            self.update_map(game.map, rooms_discovered)

            if death[0] is not None:
                self.result_window.addstr(0, 0, death[0][:death[0].index('monster')])
                self.result_window.addstr('monster', RED)
                self.result_window.addstr(death[0][death[0].index('monster') + len('monster'):])
                self.result_window.refresh()

                if death[1]:
                    self.result_window.addstr(1, 0, 'Restart? (y/n)')
                    self.result_window.refresh()

                    while True:
                        curses.curs_set(True)
                        restart = str(self.display_window.getstr(self.height - 3, 2, self.display_width - 4))
                        restart = restart.replace("'", '')[1:].lower()

                        match restart:
                            case 'y' | 'yes':
                                curses.wrapper(checkpoint)
                                return
                            case 'n' | 'no':
                                exit()
                            case _:
                                self.result_window.addstr(2, 0, 'Invalid input')
                                self.result_window.refresh()
                # Display death message
                else:
                    sleep(2)
                    self.update_map(game.map, rooms_discovered)
