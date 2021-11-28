"""Map class for handling player movement and storing room attributes such as items and statuses"""


class Map:
    """
    Parameters:
        rooms (dict): a dictionary containing all information for each room in the map
        starting_room (str): The room that the player starts in

    Methods:
        move(self, direction, player_inventory): Moves the player in a desired direction
    """

    def __init__(self, rooms, starting_room):
        self.rooms = rooms
        self.current_room = starting_room

    def move(self, direction, player_inventory):
        """
        Method for moving the player within the map

        Parameters:
            direction (str): direction of the player's movement (n, s, e, or w)
            player_inventory (list): player's inventory, used for removing keys once they are used

        Returns:
            str: message regarding the status of the room or an error depending on the situation
        """
        # 'Strange' rooms don't let you leave them until you use the Strange Tome
        if 'status' in self.rooms[self.current_room] and self.rooms[self.current_room]['status'] == 'strange':
            return 'The room feels strange...'
        # Make sure the direction entered is an exit in the room
        elif direction in self.rooms[self.current_room]:
            next_room = self.rooms[self.current_room][direction]
            # If the room has no status, just move
            if 'status' not in self.rooms[next_room]:
                self.current_room = next_room
            # Locked rooms do not let you enter unless you have a key
            elif self.rooms[next_room]['status'] == 'locked':
                if 'key' in player_inventory:
                    self.current_room = next_room
                    player_inventory.remove('key')
                    del self.rooms[self.current_room]['status']
                    return 'You unlocked the door'

                else:
                    return 'That door is locked'
            # Bound rooms cannot be entered unless you have the requisite 'unbind' item
            elif self.rooms[next_room]['status'] == 'bound':
                if self.rooms[next_room]['unbind'] in player_inventory:
                    self.current_room = next_room
                    del self.rooms[self.current_room]['status']
                    return 'You remove the magical barrier...'

                else:
                    return 'A magical barrier blocks your path'
            # If the room the player is in and the room they are trying to enter both have the 'oneway' status, a
            # message will be displayed hinting that they cannot go back the way they came
            elif 'status' in self.rooms[self.current_room]:
                if self.rooms[next_room]['status'] == 'oneway' and self.rooms[self.current_room]['status'] == 'oneway':
                    self.current_room = next_room
                    return 'You hear a dry click behind you'
            else:
                self.current_room = next_room
        else:
            return 'You can\'t go there!'
