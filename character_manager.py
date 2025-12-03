"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module

Name: De'Aundre Black

AI Usage: Implemented with ChatGPT assistance, handling formatting, syntax,
and helping correct incorrect code.

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError,
)


# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class.

    Valid classes: Warrior, Mage, Rogue, Cleric

    Returns:
        dict: character data including
          - name, class, level, health, max_health, strength, magic
          - experience, gold, inventory, active_quests, completed_quests

    Raises:
        InvalidCharacterClassError: if `character_class` is not valid.
    """
    valid_classes = {
        "Warrior": {"health": 120, "strength": 15, "magic": 5},
        "Mage": {"health": 80, "strength": 8, "magic": 20},
        "Rogue": {"health": 90, "strength": 12, "magic": 10},
        "Cleric": {"health": 100, "strength": 10, "magic": 15},
    }

    if character_class not in valid_classes:
        # Explicitly raise the custom error when the class is invalid
        raise InvalidCharacterClassError(f"Invalid class: {character_class}")

    base = valid_classes[character_class]

    character = {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": base["health"],
        "max_health": base["health"],
        "strength": base["strength"],
        "magic": base["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": [],
    }

    return character


def save_character(character, save_directory="data/save_games"):
    """
    Save character to a file.

    Filename format: {character_name}_save.txt

    The file is saved as simple key/value pairs.

    Returns:
        bool: True if successful.

    Raises:
        SaveFileCorruptedError: if there is any problem writing the file
        (IOError / PermissionError are wrapped into this custom exception).
    """
    # Basic validation before saving
    try:
        validate_character_data(character)
    except InvalidSaveDataError as e:
        # If character data is already invalid, surface that clearly
        raise InvalidSaveDataError(f"Cannot save invalid character data: {e}")

    if not os.path.exists(save_directory):
        os.makedirs(save_directory, exist_ok=True)

    filename = os.path.join(save_directory, f"{character['name']}_save.txt")

    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"NAME: {character['name']}\n")
            file.write(f"CLASS: {character['class']}\n")
            file.write(f"LEVEL: {character['level']}\n")
            file.write(f"HEALTH: {character['health']}\n")
            file.write(f"MAX_HEALTH: {character['max_health']}\n")
            file.write(f"STRENGTH: {character['strength']}\n")
            file.write(f"MAGIC: {character['magic']}\n")
            file.write(f"EXPERIENCE: {character['experience']}\n")
            file.write(f"GOLD: {character['gold']}\n")

            inventory_str = ",".join(character["inventory"]) if character["inventory"] else ""
            active_str = ",".join(character["active_quests"]) if character["active_quests"] else ""
            completed_str = ",".join(character["completed_quests"]) if character["completed_quests"] else ""

            file.write(f"INVENTORY: {inventory_str}\n")
            file.write(f"ACTIVE_QUESTS: {active_str}\n")
            file.write(f"COMPLETED_QUESTS: {completed_str}\n")

    except (OSError, PermissionError) as e:
        # Wrap any file write problems in the custom error
        raise SaveFileCorruptedError(f"Could not save character data: {e}")

    return True


def load_character(character_name, save_directory="data/save_games"):
    """
    Load a character from a save file.

    Returns:
        dict: character data.

    Raises:
        CharacterNotFoundError: if the save file does not exist.
        SaveFileCorruptedError: if the file cannot be read at all.
        InvalidSaveDataError: if the file contents are malformed or missing
                              required fields.
    """
    filename = os.path.join(save_directory, f"{character_name}_save.txt")

    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"No save file found for {character_name}")

    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except (OSError, PermissionError) as e:
        # File exists but cannot be read
        raise SaveFileCorruptedError(f"Could not read save file for {character_name}: {e}")

    character = {}

    try:
        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                continue

            if ":" not in line:
                # Every line must be KEY: VALUE
                raise InvalidSaveDataError("Missing ':' in save data")

            # Split only on the first colon, allow either 'KEY: value' or 'KEY:value'
            if ": " in line:
                key, value = line.split(": ", 1)
            else:
                key, value = line.split(":", 1)
                value = value.lstrip()

            key = key.strip()
            value = value.strip()

            # Lists
            if key in ("INVENTORY", "ACTIVE_QUESTS", "COMPLETED_QUESTS"):
                items = [v for v in value.split(",") if v] if value else []
                character[key.lower()] = items

            # Integers
            elif key in (
                "LEVEL",
                "HEALTH",
                "MAX_HEALTH",
                "STRENGTH",
                "MAGIC",
                "EXPERIENCE",
                "GOLD",
            ):
                character[key.lower()] = int(value)

            # Strings
            else:
                character[key.lower()] = value

        # Validate structure and types
        validate_character_data(character)

    except InvalidSaveDataError:
        # Re-raise exactly as InvalidSaveDataError so tests can catch it
        raise
    except Exception as e:
        # Any other parsing errors are treated as invalid save data
        raise InvalidSaveDataError(f"Save file format incorrect: {e}")

    return character


def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names.

    Returns:
        list[str]: character names (without the _save.txt extension).
    """
    if not os.path.exists(save_directory):
        return []

    names = []
    for filename in os.listdir(save_directory):
        if filename.endswith("_save.txt"):
            names.append(filename.replace("_save.txt", ""))

    return names


def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file.

    Returns:
        bool: True if deleted successfully.

    Raises:
        CharacterNotFoundError: if character doesn't exist.
    """
    filename = os.path.join(save_directory, f"{character_name}_save.txt")

    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"No save file for {character_name}")

    try:
        os.remove(filename)
    except (OSError, PermissionError) as e:
        # Treat failure to delete as corrupted save file
        raise SaveFileCorruptedError(f"Could not delete save file: {e}")

    return True


# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups.

    Level up formula: level_up_xp = current_level * 100

    When leveling:
      - Increase level by 1
      - Increase max_health by 10
      - Increase strength by 2
      - Increase magic by 2
      - Restore health to max_health

    Returns:
        bool: True if the character leveled up at least once.

    Raises:
        CharacterDeadError: if character health is 0 or below.
    """
    if character["health"] <= 0:
        raise CharacterDeadError("Character is dead and cannot gain XP.")

    character["experience"] += xp_amount
    leveled_up = False

    while character["experience"] >= character["level"] * 100:
        character["experience"] -= character["level"] * 100
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]
        leveled_up = True

    return leveled_up


def add_gold(character, amount):
    """
    Add (or subtract) gold from the character.

    Args:
        character (dict): character data.
        amount (int): amount to add. Negative values spend gold.

    Returns:
        int: new gold total.

    Raises:
        ValueError: if the result would be negative.
    """
    new_total = character["gold"] + amount
    if new_total < 0:
        raise ValueError("Gold cannot be negative.")

    character["gold"] = new_total
    return character["gold"]


def heal_character(character, amount):
    """
    Heal the character by a certain amount.

    Returns:
        int: actual amount of health restored.

    Raises:
        ValueError: if `amount` is negative.
    """
    if amount < 0:
        raise ValueError("Heal amount cannot be negative.")

    old_health = character["health"]
    character["health"] = min(character["health"] + amount, character["max_health"])
    return character["health"] - old_health


def is_character_dead(character):
    """
    Check if character's health is 0 or below.

    Returns:
        bool: True if dead, False otherwise.
    """
    return character["health"] <= 0


def revive_character(character):
    """
    Revive a dead character to half of max health.

    Returns:
        bool: True if revived, False if the character was not dead.
    """
    if not is_character_dead(character):
        return False

    character["health"] = character["max_health"] // 2
    return True


# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that a loaded or to-be-saved character dict has all required
    fields and correct types.

    Raises:
        InvalidSaveDataError: if anything is missing or of wrong type.
    """
    required = {
        "name",
        "class",
        "level",
        "health",
        "max_health",
        "strength",
        "magic",
        "experience",
        "gold",
        "inventory",
        "active_quests",
        "completed_quests",
    }

    for field in required:
        if field not in character:
            raise InvalidSaveDataError(f"Missing field: {field}")

    numeric_fields = [
        "level",
        "health",
        "max_health",
        "strength",
        "magic",
        "experience",
        "gold",
    ]
    for field in numeric_fields:
        if not isinstance(character[field], int):
            raise InvalidSaveDataError(f"{field} must be an integer")

    list_fields = ["inventory", "active_quests", "completed_quests"]
    for field in list_fields:
        if not isinstance(character[field], list):
            raise InvalidSaveDataError(f"{field} must be a list")

    return True


# ============================================================================
# TESTING (manual)
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")

    # Simple smoke test when running this file directly
    try:
        char = create_character("TestHero", "Warrior")
        print(f"Created: {char['name']} the {char['class']}")
        print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
        save_character(char)
        print("Character saved successfully.")
        loaded = load_character("TestHero")
        print(f"Loaded: {loaded['name']} (Level {loaded['level']})")
    except Exception as e:
        print(f"Error during manual test: {e}")
