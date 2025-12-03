"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: DeAundre Black

AI Usage: [Syntax, Structure, careless errors in my code]

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20


# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

# AI Usage: Used AI (ChatGPT) to help structure/finish functions if I had errors or if I didn't have the correct formatting

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory

    Args:
        character: Character dictionary
        item_id: Unique item identifier

    Returns: True if added successfully
    Raises: InventoryFullError if inventory is at max capacity
    """
    # TODO: Implement adding items
    # Check if inventory is full (>= MAX_INVENTORY_SIZE)
    # Add item_id to character['inventory'] list

    inventory = character.get("inventory", [])  # checks character inventory

    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Character inventory at maximum capacity. Unable to add more items")

    inventory.append(item_id)

    character["inventory"] = inventory


def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory

    Args:
        character: Character dictionary
        item_id: Item to remove

    Returns: True if removed successfully
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement item removal
    # Check if item exists in inventory
    # Remove item from list

    inventory = character.get("inventory", [])

    # Check if item exists
    if item_id not in inventory:
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory.")

    # Remove it
    inventory.remove(item_id)
    character["inventory"] = inventory

    return True


def has_item(character, item_id):
    """
    Check if character has a specific item

    Returns: True if item in inventory, False otherwise
    """
    # TODO: Implement item check

    if item_id in character["inventory"]:
        return True

    else:
        return False


def count_item(character, item_id):
    """
    Count how many of a specific item the character has

    Returns: Integer count of item
    """
    # TODO: Implement item counting
    # Use list.count() method

    return character["inventory"].count(item_id)


def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory

    Returns: Integer representing available slots
    """
    current_size = len(character["inventory"])
    return MAX_INVENTORY_SIZE - current_size

    # TODO: Implement space calculation


def clear_inventory(character):
    """
    Remove all items from inventory

    Returns: List of removed items
    """

    removed_items = character["inventory"][:]  # copy so we don’t lose items
    character["inventory"].clear()  # empty inventory
    return removed_items

    # TODO: Implement inventory clearing
    # Save current inventory before clearing
    # Clear character's inventory list


# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory

    Args:
        character: Character dictionary
        item_id: Item to use
        item_data: Item information dictionary from game_data

    Item types and effects:
    - consumable: Apply effect and remove from inventory
    - weapon/armor: Cannot be "used", only equipped

    Returns: String describing what happened
    Raises: 
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'consumable'
    """
    # TODO: Implement item usage
    # Check if character has the item
    # Check if item type is 'consumable'
    # Parse effect (format: "stat_name:value" e.g., "health:20")
    # Apply effect to character
    # Remove item from inventory

    if item_id not in character["inventory"]:
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory")

    if item_data["type"] != "consumable":
        raise InvalidItemTypeError("Item type cannot be used")

    # Parse effect such as "health:20"
    stat, value = item_data["effect"].split(":")
    value = int(value)

    character[stat] = min(character.get("max_" + stat, float('inf')), character[stat] + value)

    character["inventory"].remove(item_id)

    return f"Used {item_id}, {stat} increased by {value}"


def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon

    Args:
        character: Character dictionary
        item_id: Weapon to equip
        item_data: Item information dictionary

    Weapon effect format: "strength:5" (adds 5 to strength)

    If character already has weapon equipped:
    - Unequip current weapon (remove bonus)
    - Add old weapon back to inventory

    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'weapon'
    """
    # Ensure the item exists in the character's inventory
    if item_id not in character["inventory"]:
        raise ItemNotFoundError(f"Weapon '{item_id}' not found in inventory")

    # Ensure the item type is 'weapon'
    if item_data.get("type") != "weapon":
        raise InvalidItemTypeError(f"Item '{item_id}' is not a weapon")

    # If the character already has a weapon equipped, unequip it first
    old_weapon_id = character.get("equipped_weapon")
    if old_weapon_id:
        # Remove old weapon effects if needed (assumes a separate function handles stat removal)
        unequip_weapon(character)
        # Add old weapon back to inventory
        character["inventory"].append(old_weapon_id)

    # Equip the new weapon: store just the ID in 'equipped_weapon'
    character["equipped_weapon"] = item_id

    # Apply weapon effects (example: "strength:5")
    effect = item_data.get("effect")
    if effect:
        stat, value = effect.split(":")
        value = int(value)
        if stat in character:
            character[stat] += value

    # Remove the weapon from inventory since it's now equipped
    character["inventory"].remove(item_id)

    return f"{character['name']} has equipped {item_id}"

    # TODO: Implement weapon equipping
    # Check item exists and is type 'weapon'
    # Handle unequipping current weapon if exists
    # Parse effect and apply to character stats
    # Store equipped_weapon in character dictionary
    # Remove item from inventory


def equip_armor(character, item_id, item_data):
    """
    Equip armor

    Args:
        character: Character dictionary
        item_id: Armor to equip
        item_data: Item information dictionary

    Armor effect format: "max_health:10" (adds 10 to max_health)

    If character already has armor equipped:
    - Unequip current armor (remove bonus)
    - Add old armor back to inventory

    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'armor'
    """

    if item_id not in character["inventory"]:
        raise ItemNotFoundError(f"Armor '{item_id}' not found in inventory")

    item = item_data

    # Must be armor
    if item["type"] != "armor":
        raise InvalidItemTypeError(f"Item '{item_id}' is not armor")

    # If armor already equipped, remove its effect first
    if character.get("equipped_armor"):
        old_armor = character["equipped_armor"]
        old_data = item_data[old_armor]
        stat, value = old_data["effect"].split(":")
        character[stat] -= int(value)

        # Return old armor to inventory
        character["inventory"].append(old_armor)

    # Apply new armor effect
    stat, value = item["effect"].split(":")
    character[stat] += int(value)

    # Set equipped armor
    character["equipped_armor"] = item_id

    # Remove from inventory
    character["inventory"].remove(item_id)

    return f"Equipped {item_id}, {stat} increased by {value}"

    # TODO: Implement armor equipping
    # Similar to equip_weapon but for armor


def unequip_weapon(character, item_data):
    """
    Remove equipped weapon and return it to inventory

    Returns: Item ID that was unequipped, or None if no weapon equipped
    Raises: InventoryFullError if inventory is full
    """

    equipped = character.get("equipped_weapon")

    if not equipped:
        return None  # nothing to unequip

    # Check inventory space
    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("Inventory is full")

    weapon_data = item_data[equipped]
    stat, value = weapon_data["effect"].split(":")
    character[stat] -= int(value)  # remove stat bonus

    # Return weapon to inventory
    character["inventory"].append(equipped)

    # Clear equipped weapon
    character["equipped_weapon"] = None

    return equipped

    # TODO: Implement weapon unequipping
    # Check if weapon is equipped
    # Remove stat bonuses
    # Add weapon back to inventory
    # Clear equipped_weapon from character


def unequip_armor(character, item_data):
    """
    Remove equipped armor and return it to inventory

    Returns: Item ID that was unequipped, or None if no armor equipped
    Raises: InventoryFullError if inventory is full
    """

    equipped = character.get("equipped_armor")

    if not equipped:
        return None

    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("Inventory is full")

    armor_data = item_data[equipped]
    stat, value = armor_data["effect"].split(":")
    character[stat] -= int(value)

    character["inventory"].append(equipped)
    character["equipped_armor"] = None

    return equipped

    # TODO: Implement armor unequipping


# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop

    Args:
        character: Character dictionary
        item_id: Item to purchase
        item_data: Item information with 'cost' field

    Returns: True if purchased successfully
    Raises:
        InsufficientResourcesError if not enough gold
        InventoryFullError if inventory is full
    """

    # Get item cost
    cost = item_data["cost"]

    # Check if character has enough gold
    if character["gold"] < cost:
        raise InsufficientResourcesError(f"You do not have enough gold to purchase {item_id} (cost: {cost})")

    # Ensure the inventory key exists
    if 'inventory' not in character:
        character['inventory'] = []

    if len(character["inventory"]) >= 20:
        raise InventoryFullError("Your inventory is full. Cannot buy any more items")

    # Deduct gold (for a successful purchase)
    character['gold'] -= cost
    # Add purchased item to inventory
    character['inventory'].append(item_id)
    return True

    # TODO: Implement purchasing
    # Check if character has enough gold
    # Check if inventory has space
    # Subtract gold from character
    # Add item to inventory


def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost

    Args:
        character: Character dictionary
        item_id: Item to sell
        item_data: Item information with 'cost' field

    Returns: Amount of gold received
    Raises: ItemNotFoundError if item not in inventory
    """

    # Ensure inventory exists
    if 'inventory' not in character or item_id not in character['inventory']:
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory.")

    # Remove item from inventory
    character['inventory'].remove(item_id)

    # Gain half of the item's cost
    cost = item_data["cost"]
    gold_gained = cost // 2

    character['gold'] += gold_gained

    return gold_gained

    # TODO: Implement selling
    # Check if character has item
    # Calculate sell price (cost // 2)
    # Remove item from inventory
    # Add gold to character


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value

    Args:
        effect_string: String in format "stat_name:value"

    Returns: Tuple of (stat_name, value)
    Example: "health:20" → ("health", 20)
    """
    stat, value = effect_string.split(":")
    return stat, int(value)

    # TODO: Implement effect parsing
    # Split on ":"
    # Convert value to integer


def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character

    Valid stats: health, max_health, strength, magic

    Note: health cannot exceed max_health
    """

    # Apply the stat increase
    character[stat_name] += value

    # Health cannot exceed max_health
    if stat_name == "health":
        if character["health"] > character["max_health"]:
            character["health"] = character["max_health"]

    # TODO: Implement stat application
    # Add value to character[stat_name]
    # If stat is health, ensure it doesn't exceed max_health


def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way

    Args:
        character: Character dictionary
        item_data_dict: Dictionary of all item data

    Shows item names, types, and quantities
    """

    inventory = character["inventory"]

    if not inventory:
        print("\nInventory is empty.")
        return

    print("\n=== INVENTORY ===")

    # Count items
    item_counts = {}
    for item_id in inventory:
        item_counts[item_id] = item_counts.get(item_id, 0) + 1

    # Display items
    for item_id, count in item_counts.items():
        item_info = item_data_dict[item_id]
        name = item_info["name"]
        item_type = item_info["type"]

        print(f"{name} ({item_type}) x{count}")

    print("=================\n")

    # TODO: Implement inventory display
    # Count items (some may appear multiple times)
    # Display with item names from item_data_dict


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")

    # Test adding items
    # test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    # 
    # try:
    #     add_item_to_inventory(test_char, "health_potion")
    #     print(f"Inventory: {test_char['inventory']}")
    # except InventoryFullError:
    #     print("Inventory is full!")

    # Test using items
    # test_item = {
    #     'item_id': 'health_potion',
    #     'type': 'consumable',
    #     'effect': 'health:20'
    # }
    # 
    # try:
    #     result = use_item(test_char, "health_potion", test_item)
    #     print(result)
    # except ItemNotFoundError:
    #     print("Item not found")