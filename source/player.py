"""Player class mostly for interacting with items"""


class Player:
    """
    Parameters:
        inventory (list): list containing all items in the player's inventory
        sword_durability (int) (optional): durability of the player's sword

    Methods:
        get(self, item, current_room): allows player to pick up an item that is in the room
        use(self, item, current_room): allows player to use an item in their inventory, only works for certain items
    """
    def __init__(self, inventory, sword_durability=2):
        self.inventory = inventory
        self.sword_durability = sword_durability

    def get(self, item, current_room):
        """
        Method for picking up items in the room

        Parameters:
            item (str): name of the item to be picked up
            current_room (dict): room dictionary of the room the player is in

        Returns:
            str: result message either saying they got the item or an error
        """
        # Make sure the item is in the room
        if 'item' in current_room:
            if item.lower() == current_room['item'].lower():
                item = current_room['item']
                # Add the item to the player's inventory and remove it from the room
                self.inventory.append(item)
                del current_room['item']

                if item == 'sword':
                    self.sword_durability = 2

                return f'You got the {item}!'
            else:
                return 'That item isn\'t here!'
        else:
            return 'There isn\'t an item here!'

    def use(self, item, current_room):
        """
        Method for using certain items

        Parameters:
            item (str): Item to be used
            current_room (dict): room dictionary of the room the player is in

        Returns:
            str: result message either saying that the item was used and its effect or an error
        """
        # Make sure the player has the item
        if item in self.inventory:
            if item == 'hammer':
                # Repair the sword and remove the hammer from the player's inventory
                if 'cracked sword' in self.inventory:
                    self.sword_durability = 2
                    self.inventory.remove('cracked sword')
                    self.inventory.append('sword')
                    self.inventory.remove('hammer')
                    return 'You repaired your sword!'

                elif 'sword' in self.inventory:
                    return 'Your sword is not broken'

                else:
                    return 'You need a sword to repair!'

            elif item == 'Strange Tome':
                # Remove 'strange' status from a room
                if 'status' in current_room and current_room['status'] == 'strange':
                    del current_room['status']
                    return 'The room became normal'

                else:
                    return 'You can\'t use that here!'
        else:
            return 'You do not have that item'
