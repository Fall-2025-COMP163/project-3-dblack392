"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module

Name: De'Aundre Black

AI Usage: Syntax, structure, and fixing careless errors.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError,
)


# ======================================================================
# HELPER PARSERS
# ======================================================================

def parse_quest_block(lines):
    """
    Parse a block of quest lines into a dict with UPPERCASE keys.

    Raises InvalidDataFormatError on problems.
    """
    quest = {}
    try:
        for line in lines:
            if not line.strip():
                continue
            key, value = line.strip().split(": ", 1)
            if key in ["REWARD_XP", "REWARD_GOLD", "REQUIRED_LEVEL"]:
                value = int(value)
            quest[key] = value
    except Exception as e:
        raise InvalidDataFormatError(f"Failed to parse quest block: {e}")
    return quest


def parse_item_block(lines):
    """
    Parse a block of item lines into a dict with UPPERCASE keys.

    Raises InvalidDataFormatError on problems.
    """
    item = {}
    try:
        for line in lines:
            if not line.strip():
                continue
            key, value = line.strip().split(": ", 1)
            if key == "COST":
                value = int(value)
            item[key] = value
    except Exception as e:
        raise InvalidDataFormatError(f"Failed to parse item block: {e}")
    return item


# ======================================================================
# VALIDATION
# ======================================================================

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields and types.

    Required (lowercase) keys:
      quest_id, title, description, reward_xp,
      reward_gold, required_level, prerequisite

    Raises InvalidDataFormatError on problems.
    """
    required_fields = {
        "quest_id": str,
        "title": str,
        "description": str,
        "reward_xp": int,
        "reward_gold": int,
        "required_level": int,
        "prerequisite": str,
    }

    for key, expected_type in required_fields.items():
        if key not in quest_dict:
            raise InvalidDataFormatError(f"Missing required field: {key}")
        if not isinstance(quest_dict[key], expected_type):
            raise InvalidDataFormatError(
                f"Field {key} should be of type {expected_type.__name__}"
            )

    return True


def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields and types.

    Required (lowercase) keys:
      item_id, name, type, effect, cost, description

    Valid types: weapon, armor, consumable
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
        if not isinstance(item_dict[field], expected_type):
            raise InvalidDataFormatError(
                f"Field '{field}' must be of type {expected_type.__name__}"
            )

    if item_dict["type"] not in valid_types:
        raise InvalidDataFormatError(
            f"Invalid item type: {item_dict['type']}. Must be one of {valid_types}"
        )

    return True


# ======================================================================
# DATA LOADING
# ======================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file.

    Raises:
      - MissingDataFileError if file doesn't exist
      - InvalidDataFormatError for bad structure
      - CorruptedDataError for other I/O problems
    """
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Quest file not found: {filename}")

    quests = {}

    try:
        with open(filename, "r") as f:
            lines = f.read().splitlines()

        block = []
        for line in lines + [""]:
            if line.strip() == "":
                if block:
                    raw = parse_quest_block(block)           # UPPERCASE keys
                    quest = {k.lower(): v for k, v in raw.items()}  # lowercase
                    validate_quest_data(quest)
                    quest_id = quest["quest_id"]
                    quests[quest_id] = quest
                    block = []
                continue

            block.append(line)

    except InvalidDataFormatError:
        # Let the specific format error propagate
        raise
    except Exception as e:
        # Any other problem considered corrupted data
        raise CorruptedDataError(f"Could not read quest file: {e}")

    return quests


def load_items(filename="data/items.txt"):
    """
    Load item data from file.

    Same exception behavior as load_quests.
    """
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Item file not found: {filename}")

    items = {}

    try:
        with open(filename, "r") as f:
            lines = f.read().splitlines()

        block = []
        for line in lines + [""]:
            if line.strip() == "":
                if block:
                    raw = parse_item_block(block)
                    item = {k.lower(): v for k, v in raw.items()}
                    validate_item_data(item)
                    item_id = item["item_id"]
                    items[item_id] = item
                    block = []
                continue

            block.append(line)

    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise CorruptedDataError(f"Could not read item file: {e}")

    return items


def create_default_data_files():
    """
    Create default data/quests.txt and data/items.txt if missing.
    """
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)

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
