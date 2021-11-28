"""Game class for handling inputs and game logic"""


class Game:
    """
    Parameters:
        player (Player): player object containing information like the inventory and item use logic
        _map (Map): map object that contains the rooms and movement logic
    """
    def __init__(self, player, _map):
        self.player = player
        self.map = _map

    def __repr__(self):
        # Custom repr for the game containing all pertinent information
        if 'item' in self.map.rooms[self.map.current_room]:
            item_line = f'You see a {self.map.rooms[self.map.current_room]["item"]}\n'
        else:
            item_line = ''

        return f'You are in the {self.map.current_room}\n' \
               f'{item_line}' \
               f'Inventory: {sorted(self.player.inventory)}\n'

    def parse_command(self, command):
        """
        Method for interpreting player inputs and performing their respective actions

        Parameters:
            command (str): command to be interpreted

        Returns:
            str: message returned by the method called by the command
        """
        match command.split():
            # Move or go in a direction
            case [('move' | 'go'), direction]:
                return self.map.move(direction[0].lower(), self.player.inventory)
            # Get or take an item
            case [('get' | 'take'), *item_words]:
                # Allows for item names with spaces in them
                item = ''.join([f'{word} ' for word in item_words]).strip()
                return self.player.get(item, self.map.rooms[self.map.current_room])
            # Use item
            case ['use', *item_words]:
                item = ''.join([f'{word} ' for word in item_words]).strip()
                return self.player.use(item, self.map.rooms[self.map.current_room])
            # Display commands again
            case ['help']:
                return 'Commands:\n' \
                       '  go [direction] (n, s, e, or w)\n' \
                       '  get [item]\n' \
                       '  use [item] (only for certain items)\n' \
                       '  help (displays this list)'

            # These are debug commands
            # gives player all items listed
            case ['give', *items]:
                # Comma separation between items allows for spaced item names
                items = ' '.join(items).split(', ')
                for item in items:
                    self.player.inventory.append(item)
            # Teleport to a specified room
            case ['tp', *room_words]:
                room = ''.join([f'{word} ' for word in room_words]).strip()
                if room in self.map.rooms:
                    self.map.current_room = room
                else:
                    return 'That room does not exist'
            # Sets the player's sword durability to a specified value
            case ['durset', durability]:
                try:
                    self.player.sword_durability = int(durability)
                except ValueError:
                    return 'Not a number'

            case _:
                return 'Invalid input'

    def check_death(self, killer):
        """
        Method for handling when a player enters a room with a 'killer' item

        Parameters:
            killer (str): item that is deemed to 'kill' the player upon entering the room

        Returns:
            tuple(str, bool): first value is a result message displayed if the player kills the killer or the player is
                              killed, second value is whether the player died or not
        """
        # 'killers' are just items that will kill the player when they enter the room
        if 'item' in self.map.rooms[self.map.current_room]:
            if killer in self.map.rooms[self.map.current_room]['item']:
                # The sword allows the player to defeat the killer, but loses durability for each use
                if 'sword' not in self.player.inventory and 'cracked sword' not in self.player.inventory:
                    return f'A {killer} has got you... GAME OVER!', True
                else:
                    message = f'There is a {killer}! But you slay it \nwith your sword.'
                    del self.map.rooms[self.map.current_room]['item']
                    self.player.sword_durability -= 1

                    # When the sword's reaches 1 durability, it cracks
                    if self.player.sword_durability == 1:
                        self.player.inventory.remove('sword')
                        self.player.inventory.append('cracked sword')
                        message += ' Your sword cracks.'
                    # If the sword's durability drops to 0, it breaks
                    elif self.player.sword_durability <= 0:
                        self.player.inventory.remove('cracked sword')
                        message += ' Your sword shatters.'

                    return message, False

        return None, False
