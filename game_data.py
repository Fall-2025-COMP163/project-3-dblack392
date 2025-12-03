"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: De'Aundre Black

AI Usage: [Syntax, Structure, any careless errors in my code.]


This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)


# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

# AI Usage: Used AI (ChatGPT) to help structure/finish functions if I had errors or if I didn't have the correct formatting

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file

    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)

    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """

    import os

    if not os.path.exists(filename):
        raise MissingDataFileError(f"Quest file not found: {filename}")

    quests = {}
    try:
        with open(filename, "r") as f:
            lines = f.read().splitlines()

        current_quest = {}
        for line in lines + [""]:
            line = line.strip()
            if line == "":
                if current_quest:
                    required_fields = ["QUEST_ID", "TITLE", "DESCRIPTION",
                                       "REWARD_XP", "REWARD_GOLD", "REQUIRED_LEVEL", "PREREQUISITE"]
                    for field in required_fields:
                        if field not in current_quest:
                            raise InvalidDataFormatError(f"Missing field '{field}' in quest")
                    quest_id = current_quest["QUEST_ID"]
                    # Normalize keys to lowercase (should match test case calls)
                    normalized_quest = {k.lower(): v for k, v in current_quest.items()}
                    quests[quest_id] = normalized_quest
                    current_quest = {}
                continue

            if ": " not in line:
                raise InvalidDataFormatError(
                    f"Invalid line format: {line}")  # Custom exception for Invalid data formats

            key, value = line.split(": ", 1)
            key = key.strip()
            value = value.strip()
            if key in ["REWARD_XP", "REWARD_GOLD", "REQUIRED_LEVEL"]:
                try:
                    value = int(value)
                except ValueError:
                    raise InvalidDataFormatError(f"Expected integer for {key}, got '{value}'")
            current_quest[key] = value

    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise CorruptedDataError(f"Could not read quest file: {e}")

    return quests

    # TODO: Implement this function
    # Must handle:
    # - FileNotFoundError → raise MissingDataFileError
    # - Invalid format → raise InvalidDataFormatError
    # - Corrupted/unreadable data → raise CorruptedDataError


def load_items(filename="data/items.txt"):
    """
    Load item data from file

    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description

    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle same exceptions as load_quests

    import os

    if not os.path.exists(filename):
        raise MissingDataFileError(f"Item file not found: {filename}")

    items = {}
    try:
        with open(filename, "r") as f:
            lines = f.read().splitlines()

        current_item = {}
        for line in lines + [""]:
            line = line.strip()
            if line == "":
                if current_item:
                    required_fields = ["ITEM_ID", "NAME", "TYPE", "EFFECT", "COST", "DESCRIPTION"]
                    for field in required_fields:
                        if field not in current_item:
                            raise InvalidDataFormatError(f"Missing field '{field}' in item")
                    item_id = current_item["ITEM_ID"]
                    # Normalize keys to lowercase
                    normalized_item = {k.lower(): v for k, v in current_item.items()}
                    items[item_id] = normalized_item
                    current_item = {}
                continue

            if ": " not in line:
                raise InvalidDataFormatError(f"Invalid line format: {line}")

            key, value = line.split(": ", 1)
            key = key.strip()
            value = value.strip()
            if key == "COST":
                try:
                    value = int(value)
                except ValueError:
                    raise InvalidDataFormatError(f"Expected integer for COST, got '{value}'")
            current_item[key] = value

    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise CorruptedDataError(f"Could not read item file: {e}")

    return items


def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields

    Required fields: quest_id, title, description, reward_xp,
                    reward_gold, required_level, prerequisite

    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """

    required_fields = {
        "quest_id": str,
        "title": str,
        "description": str,
        "reward_xp": int,
        "reward_gold": int,
        "required_level": int,
        "prerequisite": str
    }
    # Loops through fields & checks if they're in the quest dictionary
    for key, expected_type in required_fields.items():
        # Raises InvalidDataFormatError if the key is not in the quest dictionary
        if key not in quest_dict:
            raise InvalidDataFormatError(f"Missing required field(s): {key}")
        # Also raises InvalidDataFormatError if the key does not match its expected type
        if not isinstance(quest_dict[key], expected_type):
            raise InvalidDataFormatError(f"Field {key} should be this type: {expected_type.__name__}")

    return True

    # TODO: Implement validation
    # Check that all required keys exist
    # Check that numeric values are actually numbers


def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields

    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable

    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    required_fields = {
        "item_id": str,
        "name": str,
        "type": str,
        "effect": str,
        "cost": int,
        "description": str,
    }

    valid_types = ["weapon", "armor", "consumable"]

    for field, expected_type in required_fields.items():
        if field not in item_dict:
            raise InvalidDataFormatError(f"Missing required field: {field}")

        # Check type
        if not isinstance(item_dict[field], expected_type):
            raise InvalidDataFormatError(f"Field '{field}' must be of type {expected_type.__name__}")

    # Check item type validity
    if item_dict["type"] not in valid_types:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}. Must be one of {valid_types}")

    return True

    # TODO: Implement validation


def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """

    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)  # Create data directory if missing

    # Default quests file
    quests_file = os.path.join(data_dir, "quests.txt")
    if not os.path.exists(quests_file):
        try:
            with open(quests_file, "w") as f:
                f.write(
                    "QUEST_ID:quest_001\n"
                    "TITLE:First Adventure\n"
                    "DESCRIPTION:Begin your journey.\n"
                    "REWARD_XP:100\n"
                    "REWARD_GOLD:50\n"
                    "REQUIRED_LEVEL:1\n"
                    "PREREQUISITE:NONE\n\n"
                )
        except PermissionError:
            print("Permission denied: Cannot create default quests.txt")

    # Default items file
    items_file = os.path.join(data_dir, "items.txt")
    if not os.path.exists(items_file):
        try:
            with open(items_file, "w") as f:
                f.write(
                    "ITEM_ID:item_001\n"
                    "NAME:Health Potion\n"
                    "TYPE:consumable\n"
                    "EFFECT:health:20\n"
                    "COST:10\n"
                    "DESCRIPTION:Restores 20 health.\n\n"
                )

        except PermissionError:
            print("Permission denied: Cannot create default items.txt")

    # TODO: Implement this function
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary

    Args:
        lines: List of strings representing one quest

    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """

    quest = {}
    try:
        for line in lines:
            if not line.strip():
                continue  # skip empty lines
            key, value = line.strip().split(": ", 1)
            if key in ["REWARD_XP", "REWARD_GOLD", "REQUIRED_LEVEL"]:
                value = int(value)
            quest[key] = value
    except Exception as e:
        raise InvalidDataFormatError(f"Failed to parse quest block: {e}")

    return quest

    # TODO: Implement parsing logic
    # Split each line on ": " to get key-value pairs
    # Convert numeric strings to integers
    # Handle parsing errors gracefully


def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary

    Args:
        lines: List of strings representing one item

    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """

    item = {}
    try:
        for line in lines:
            if not line.strip():
                continue  # skip empty lines
            key, value = line.strip().split(": ", 1)
            if key == "COST":
                value = int(value)
            item[key] = value
    except Exception as e:
        raise InvalidDataFormatError(f"Failed to parse item block: {e}")

    return item

    # TODO: Implement parsing logic


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")

    # Test creating default files
    # create_default_data_files()

    # Test loading quests
    # try:
    #     quests = load_quests()
    #     print(f"Loaded {len(quests)} quests")
    # except MissingDataFileError:
    #     print("Quest file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid quest format: {e}")

    # Test loading items
    # try:
    #     items = load_items()
    #     print(f"Loaded {len(items)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")