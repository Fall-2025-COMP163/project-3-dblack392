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
    InvalidItemTypeError,
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20


def _ensure_inventory(character):
    """Internal helper to make sure character has an inventory list."""
    if "inventory" not in character or character["inventory"] is None:
        character["inventory"] = []


# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================


def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory

    Args:
        character: Character dictionary
        item_id: Unique item identifier

    Returns: True if added successfully
    Raises: InventoryFullError if inventory is at max capacity
    """
    _ensure_inventory(character)
    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError(
            "Character inventory at maximum capacity. Unable to add more items"
        )
    character["inventory"].append(item_id)
    return True


def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory

    Args:
        character: Character dictionary
        item_id: Item to remove

    Returns: True if removed successfully
    Raises: ItemNotFoundError if item not in inventory
    """
    _ensure_inventory(character)
    if item_id not in character["inventory"]:
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory.")
    character["inventory"].remove(item_id)
    return True


def has_item(character, item_id):
    """
    Check if character has a specific item

    Returns: True if item in inventory, False otherwise
    """
    return item_id in character.get("inventory", [])


def count_item(character, item_id):
    """
    Count how many of a specific item the character has

    Returns: Integer count of item
    """
    return character.get("inventory", []).count(item_id)


def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory

    Returns: Integer representing available slots
    """
    return MAX_INVENTORY_SIZE - len(character.get("inventory", []))


def clear_inventory(character):
    """
    Remove all items from inventory

    Returns: List of removed items
    """
    _ensure_inventory(character)
    removed_items = character["inventory"][:]
    character["inventory"].clear()
    return removed_items


# ============================================================================
# ITEM USAGE
# ============================================================================


def _resolve_item_info(item_id, item_data):
    """
    Helper: item_data may be either a single item dict OR
    a dict of all items {item_id: item_info}. This returns
    the item_info dict for the given item_id.
    """
    if isinstance(item_data, dict) and "type" in item_data:
        # already a single item dict
        return item_data
    # assume dict of all items
    return item_data[item_id]


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
    _ensure_inventory(character)

    if item_id not in character["inventory"]:
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory")

    info = _resolve_item_info(item_id, item_data)

    if info.get("type") != "consumable":
        raise InvalidItemTypeError("Item type cannot be 'used' (only equipped).")

    stat_name, value = parse_item_effect(info["effect"])
    apply_stat_effect(character, stat_name, value)

    character["inventory"].remove(item_id)

    return f"Used {info.get('name', item_id)}, {stat_name} increased by {value}"


def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon

    Args:
        character: Character dictionary
        item_id: Weapon to equip
        item_data: Item information dictionary OR full items dict

    Weapon effect format: "strength:5" (adds 5 to strength)

    If character already has weapon equipped:
    - Unequip current weapon (remove bonus)
    - Add old weapon back to inventory

    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'weapon'
    """
    _ensure_inventory(character)

    if item_id not in character["inventory"]:
        raise ItemNotFoundError(f"Weapon '{item_id}' not found in inventory")

    info = _resolve_item_info(item_id, item_data)

    if info.get("type") != "weapon":
        raise InvalidItemTypeError(f"Item '{item_id}' is not a weapon")

    # Unequip current weapon if any
    old_weapon_id = character.get("equipped_weapon")
    if old_weapon_id:
        # try to get its data if possible
        old_info = None
        if isinstance(item_data, dict) and old_weapon_id in item_data and isinstance(
            item_data[old_weapon_id], dict
        ):
            old_info = item_data[old_weapon_id]

        if old_info and "effect" in old_info:
            stat, val = parse_item_effect(old_info["effect"])
            apply_stat_effect(character, stat, -val)

        # return old weapon to inventory
        character["inventory"].append(old_weapon_id)

    # Equip new weapon
    if "effect" in info:
        stat, val = parse_item_effect(info["effect"])
        apply_stat_effect(character, stat, val)

    character["equipped_weapon"] = item_id
    character["inventory"].remove(item_id)

    return f"{character['name']} has equipped {info.get('name', item_id)}"


def equip_armor(character, item_id, item_data):
    """
    Equip armor

    Args:
        character: Character dictionary
        item_id: Armor to equip
        item_data: Item information dictionary OR full items dict

    Armor effect format: "max_health:10" (adds 10 to max_health)

    If character already has armor equipped:
    - Unequip current armor (remove bonus)
    - Add old armor back to inventory

    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'armor'
    """
    _ensure_inventory(character)

    if item_id not in character["inventory"]:
        raise ItemNotFoundError(f"Armor '{item_id}' not found in inventory")

    info = _resolve_item_info(item_id, item_data)

    if info.get("type") != "armor":
        raise InvalidItemTypeError(f"Item '{item_id}' is not armor")

    # Unequip current armor if any
    old_armor_id = character.get("equipped_armor")
    if old_armor_id:
        old_info = None
        if isinstance(item_data, dict) and old_armor_id in item_data and isinstance(
            item_data[old_armor_id], dict
        ):
            old_info = item_data[old_armor_id]

        if old_info and "effect" in old_info:
            stat, val = parse_item_effect(old_info["effect"])
            apply_stat_effect(character, stat, -val)

        character["inventory"].append(old_armor_id)

    # Equip new armor
    if "effect" in info:
        stat, val = parse_item_effect(info["effect"])
        apply_stat_effect(character, stat, val)

    character["equipped_armor"] = item_id
    character["inventory"].remove(item_id)

    return f"Equipped {info.get('name', item_id)}, {stat} increased by {val}"


def unequip_weapon(character, item_data):
    """
    Remove equipped weapon and return it to inventory

    item_data may be a full items dict OR a single item dict.

    Returns: Item ID that was unequipped, or None if no weapon equipped
    Raises: InventoryFullError if inventory is full
    """
    _ensure_inventory(character)

    equipped = character.get("equipped_weapon")
    if not equipped:
        return None

    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("Inventory is full")

    # find data for the equipped weapon
    if isinstance(item_data, dict) and equipped in item_data and isinstance(
        item_data[equipped], dict
    ):
        info = item_data[equipped]
    else:
        info = item_data  # assume single dict for this weapon

    if "effect" in info:
        stat, val = parse_item_effect(info["effect"])
        apply_stat_effect(character, stat, -val)

    character["inventory"].append(equipped)
    character["equipped_weapon"] = None

    return equipped


def unequip_armor(character, item_data):
    """
    Remove equipped armor and return it to inventory

    Returns: Item ID that was unequipped, or None if no armor equipped
    Raises: InventoryFullError if inventory is full
    """
    _ensure_inventory(character)

    equipped = character.get("equipped_armor")
    if not equipped:
        return None

    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("Inventory is full")

    if isinstance(item_data, dict) and equipped in item_data and isinstance(
        item_data[equipped], dict
    ):
        info = item_data[equipped]
    else:
        info = item_data

    if "effect" in info:
        stat, val = parse_item_effect(info["effect"])
        apply_stat_effect(character, stat, -val)

    character["inventory"].append(equipped)
    character["equipped_armor"] = None

    return equipped


# ============================================================================
# SHOP SYSTEM
# ============================================================================


def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop

    Args:
        character: Character dictionary
        item_id: Item to purchase
        item_data: Item information with 'cost' field OR full items dict

    Returns: True if purchased successfully
    Raises:
        InsufficientResourcesError if not enough gold
        InventoryFullError if inventory is full
    """
    _ensure_inventory(character)

    info = _resolve_item_info(item_id, item_data)
    cost = info["cost"]

    if character.get("gold", 0) < cost:
        raise InsufficientResourcesError(
            f"You do not have enough gold to purchase {item_id} (cost: {cost})"
        )

    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Your inventory is full. Cannot buy any more items")

    character["gold"] = character.get("gold", 0) - cost
    character["inventory"].append(item_id)
    return True


def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost

    Args:
        character: Character dictionary
        item_id: Item to sell
        item_data: Item information with 'cost' field OR full items dict

    Returns: Amount of gold received
    Raises: ItemNotFoundError if item not in inventory
    """
    _ensure_inventory(character)

    if item_id not in character["inventory"]:
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory.")

    info = _resolve_item_info(item_id, item_data)
    cost = info["cost"]
    gold_gained = cost // 2

    character["inventory"].remove(item_id)
    character["gold"] = character.get("gold", 0) + gold_gained

    return gold_gained


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
    stat, value = effect_string.split(":", 1)
    return stat, int(value)


def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character

    Valid stats: health, max_health, strength, magic

    Note: health cannot exceed max_health
    """
    if stat_name not in character:
        character[stat_name] = 0

    character[stat_name] += value

    if stat_name == "health":
        if character["health"] > character.get("max_health", character["health"]):
            character["health"] = character["max_health"]


def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way

    Args:
        character: Character dictionary
        item_data_dict: Dictionary of all item data

    Shows item names, types, and quantities
    """
    _ensure_inventory(character)
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
        info = item_data_dict.get(item_id, {"name": "UNKNOWN", "type": "unknown"})
        name = info["name"]
        item_type = info["type"]
        print(f"{name} ({item_type}) x{count}")

    print("=================\n")


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    # You can put manual tests here if you want to run this file directly.
)