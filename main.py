"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module

Name: De'Aundre Black

AI Usage:
- Used ChatGPT to help with import issues between modules and to fix
  several syntax/structural problems in the starter code.
"""

# ============================================================================
# IMPORTS
# ============================================================================

import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data

from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    MissingDataFileError,
    InvalidDataFormatError,
    CharacterDeadError,
    CombatError,
)

# ============================================================================
# GAME STATE
# ============================================================================

current_character = None
all_quests = {}
all_items = {}
game_running = False


# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display the main menu and get the player's choice.

    Options:
        1. New Game
        2. Load Game
        3. Exit

    Returns:
        int: The selected menu option (1–3).
    """
    while True:
        print("=== MAIN MENU ===")
        print("1. New Game")
        print("2. Load Game")
        print("3. Exit")

        try:
            menu_choice = int(input("Choose an option (1-3): "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 3.")
            continue

        if 1 <= menu_choice <= 3:
            return menu_choice
        else:
            print("Invalid choice. Please choose a number between 1 and 3.")


# ============================================================================
# NEW GAME / LOAD GAME
# ============================================================================

def new_game():
    """
    Start a new game.

    Prompts the user for:
        - Character name
        - Character class

    Creates the character using character_manager.create_character()
    and then starts the main game loop.
    """
    global current_character

    print("\n=== NEW GAME ===")

    # Get character name
    name = input("Enter your character's name: ").strip()
    while not name:
        name = input("Name cannot be empty. Enter your character's name: ").strip()

    # Get character class and create character
    while True:
        print("Choose a class: Warrior, Mage, Rogue, Cleric")
        char_class = input("Enter class name: ").strip()

        try:
            current_character = character_manager.create_character(name, char_class)
            break
        except InvalidCharacterClassError as e:
            print(f"Error: {e}")
            print("Please enter a valid class.\n")

    print(f"\nCharacter created: {current_character['name']} the {current_character['class']}")
    game_loop()


def load_game():
    """
    Load an existing saved game.

    Shows list of saved characters and prompts user to select one.
    """
    global current_character

    print("\n=== LOAD GAME ===")

    # 1. Get list of saved characters
    saved_characters = character_manager.list_saved_characters()

    if not saved_characters:
        print("No saved characters found.")
        return

    # 2. Display characters
    print("Saved Characters:")
    for idx, name in enumerate(saved_characters, 1):
        print(f"{idx}. {name}")

    # 3. Prompt user to select
    while True:
        try:
            choice = int(input(f"Select a character (1-{len(saved_characters)}): "))
        except ValueError:
            print("Please enter a number.")
            continue

        if 1 <= choice <= len(saved_characters):
            character_name = saved_characters[choice - 1]
            break
        else:
            print("Invalid choice, try again.")

    # 4. Attempt to load character
    try:
        current_character = character_manager.load_character(character_name)
        print(f"Loaded character: {current_character['name']}")
    except CharacterNotFoundError:
        print("Error: Character not found.")
        return
    except SaveFileCorruptedError:
        print("Error: Save file is corrupted.")
        return

    # 5. Start game loop
    game_loop()


# ============================================================================
# SIMPLE DISPLAY HELPERS USED BY GAME LOOP
# ============================================================================

def display_stats(character):
    """Display basic character stats (used by game_loop)."""
    if not character:
        print("No character loaded.")
        return

    print(f"\n=== {character['name']} STATS ===")
    print(f"Class: {character.get('class', 'Unknown')}")
    print(f"Level: {character.get('level', 1)}")
    print(f"HP: {character.get('health', 0)}/{character.get('max_health', 0)}")
    print(f"Strength: {character.get('strength', 0)}")
    print(f"Magic: {character.get('magic', 0)}")
    print(f"Gold: {character.get('gold', 0)}")


def display_inventory_simple(character, item_data_dict):
    """Display inventory in a simple list (used by game_loop)."""
    if not character or not character.get("inventory"):
        print("\nInventory empty.")
        return

    print("\n=== INVENTORY ===")
    for i, item_id in enumerate(character["inventory"], 1):
        info = item_data_dict.get(item_id, {"name": "Unknown", "type": "?"})
        print(f"{i}. {info.get('name', 'Unknown')} ({info.get('type', '?')})")


# ============================================================================
# GAME LOOP & IN-GAME MENU
# ============================================================================

def game_loop():
    """
    Main game loop.

    Repeatedly shows the in-game menu and processes actions
    until the player chooses to save and quit.
    """
    global game_running, current_character

    if current_character is None:
        print("No character is active. Cannot start game loop.")
        return

    game_running = True

    while game_running:
        choice = game_menu()

        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Returning to main menu...")
            game_running = False


def game_menu():
    """
    Display the in-game menu and get the player's choice.

    Options:
        1. View Character Stats
        2. View Inventory
        3. Quest Menu
        4. Explore (Find Battles)
        5. Shop
        6. Save and Quit

    Returns:
        int: The selected option (1–6).
    """
    while True:
        print("\n=== IN-GAME MENU ===")
        print("1. View Character Stats")
        print("2. View Inventory")
        print("3. Quest Menu")
        print("4. Explore (Find Battles)")
        print("5. Shop")
        print("6. Save and Quit")

        try:
            choice = int(input("Select an option (1-6): "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if 1 <= choice <= 6:
            return choice
        else:
            print("Invalid choice. Select between 1 and 6.")


# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """
    Display detailed character information, including quest progress.
    """
    global current_character

    if not current_character:
        print("No character loaded.")
        return

    print("\n=== CHARACTER STATS ===")
    print(f"Name: {current_character['name']}")
    print(f"Class: {current_character.get('class', 'Unknown')}")
    print(f"Level: {current_character.get('level', 1)}")
    print(f"XP: {current_character.get('experience', 0)}")
    print(f"Gold: {current_character.get('gold', 0)}")
    print(f"Health: {current_character.get('health', 0)}/{current_character.get('max_health', 0)}")
    print(f"Strength: {current_character.get('strength', 0)}")
    print(f"Magic: {current_character.get('magic', 0)}")

    # Quest progress
    active = current_character.get("active_quests", [])
    completed = current_character.get("completed_quests", [])

    print("\nActive Quests:")
    if active:
        for q in active:
            print(f" - {q}")
    else:
        print(" (None)")

    print("\nCompleted Quests:")
    if completed:
        for q in completed:
            print(f" - {q}")
    else:
        print(" (None)")


def view_inventory():
    """
    Display and manage the player's inventory.
    """
    global current_character, all_items

    if not current_character:
        print("No character loaded.")
        return

    inv = current_character.get("inventory", [])

    print("\n=== INVENTORY ===")
    if not inv:
        print("Inventory is empty.")
        return

    # Show inventory with item names
    for idx, item_id in enumerate(inv, 1):
        item_info = all_items.get(item_id, {"name": "UNKNOWN"})
        print(f"{idx}. {item_info['name']} ({item_info.get('type', 'unknown')})")

    print("\nOptions:")
    print("1. Use Item")
    print("2. Equip Item")
    print("3. Drop Item")
    print("4. Back")

    try:
        choice = int(input("Select an option: "))
    except ValueError:
        print("Invalid input.")
        return

    if choice == 4:
        return

    try:
        item_choice = int(input("Which item number? ")) - 1
        item_id = inv[item_choice]
        item_data = all_items[item_id]
    except (ValueError, IndexError, KeyError):
        print("Invalid item selection.")
        return

    # Use item
    if choice == 1:
        try:
            result = inventory_system.use_item(current_character, item_id, item_data)
            print(result)
        except Exception as e:
            print(f"Error: {e}")

    # Equip item
    elif choice == 2:
        try:
            t = item_data.get("type", "")
            if t == "weapon":
                print(inventory_system.equip_weapon(current_character, item_id, item_data))
            elif t == "armor":
                print(inventory_system.equip_armor(current_character, item_id, item_data))
            else:
                print("This item cannot be equipped.")
        except Exception as e:
            print(f"Error: {e}")

    # Drop item
    elif choice == 3:
        try:
            inventory_system.remove_item_from_inventory(current_character, item_id)
            print(f"Dropped {item_data['name']}.")
        except Exception as e:
            print(f"Error: {e}")


def quest_menu():
    """
    Quest management menu.
    """
    global current_character, all_quests

    if not current_character:
        print("No character loaded.")
        return

    print("\n=== QUEST MENU ===")
    print("1. View Active Quests")
    print("2. View Available Quests")
    print("3. View Completed Quests")
    print("4. Accept Quest")
    print("5. Abandon Quest")
    print("6. Complete Quest (TEST ONLY)")
    print("7. Back")

    try:
        choice = int(input("Select an option: "))
    except ValueError:
        print("Invalid input.")
        return

    if choice == 7:
        return

    if choice == 1:
        quest_handler.display_active_quests(current_character, all_quests)

    elif choice == 2:
        quest_handler.display_available_quests(current_character, all_quests)

    elif choice == 3:
        quest_handler.display_completed_quests(current_character, all_quests)

    elif choice == 4:
        quest_id = input("Enter quest ID to accept: ").strip()
        try:
            quest_handler.accept_quest(current_character, quest_id, all_quests)
            print("Quest accepted!")
        except Exception as e:
            print(f"Error: {e}")

    elif choice == 5:
        quest_id = input("Enter quest ID to abandon: ").strip()
        try:
            quest_handler.abandon_quest(current_character, quest_id)
            print("Quest abandoned.")
        except Exception as e:
            print(f"Error: {e}")

    elif choice == 6:
        # For testing only
        quest_id = input("Enter quest ID to force-complete: ").strip()
        try:
            quest_handler.complete_quest(current_character, quest_id, all_quests)
            print("Quest completed! (test mode)")
        except Exception as e:
            print(f"Error: {e}")


def explore():
    """
    Find and fight random enemies.
    """
    global current_character

    if not current_character:
        print("No character loaded.")
        return

    print("\n=== EXPLORING... ===")

    try:
        # Generate a level-appropriate enemy
        enemy = combat_system.get_random_enemy_for_level(current_character.get("level", 1))
        print(f"You encountered a {enemy['name']}!")

        # Start combat using combat_system.SimpleBattle
        battle = combat_system.SimpleBattle(current_character, enemy)
        result = battle.start_battle()

        winner = result.get("winner")

        if winner == "player":
            rewards = combat_system.get_victory_rewards(enemy)
            xp = rewards.get("xp", 0)
            gold = rewards.get("gold", 0)

            current_character["experience"] = current_character.get("experience", 0) + xp
            current_character["gold"] = current_character.get("gold", 0) + gold

            print(f"You defeated the {enemy['name']}!")
            print(f"Rewards: +{xp} XP, +{gold} gold")

        elif winner == "enemy":
            print("You were defeated in battle...")
            raise CharacterDeadError("Your character has died.")

        else:
            print("Combat ended without a clear winner.")

    except CombatError as e:
        print(f"Combat error: {e}")

    except CharacterDeadError as e:
        print(f"\n*** GAME OVER ***\n{e}")
        print("Load a saved game to continue.")
        handle_character_death()

    except Exception as e:
        print(f"Unexpected error during exploration: {e}")


def shop():
    """
    Shop menu for buying / selling items.
    """
    global current_character, all_items

    if not current_character:
        print("No character loaded.")
        return

    while True:
        print("\n=== SHOP MENU ===")
        print(f"Your Gold: {current_character.get('gold', 0)}")
        print("Items for Sale:")

        item_list = list(all_items.items())
        for index, (item_id, item) in enumerate(item_list, 1):
            cost = item.get("cost", 0)
            print(f"{index}. {item.get('name', 'Unknown')} ({item.get('type', 'unknown')}), Cost: {cost} gold")

        print("\nOptions:")
        print("1. Buy Item")
        print("2. Sell Item")
        print("3. Back")

        try:
            choice = int(input("Choose an option: "))
        except ValueError:
            print("Invalid input. Enter a number.")
            continue

        # Return to previous menu
        if choice == 3:
            return

        # BUY ITEM
        if choice == 1:
            try:
                num = int(input("Enter item number to buy: ")) - 1
                item_id, item_data = item_list[num]

                inventory_system.purchase_item(current_character, item_id, item_data)
                print(f"Purchased {item_data.get('name', 'Unknown')}!")
            except (ValueError, IndexError):
                print("Invalid item number.")
            except Exception as e:
                print(f"Error: {e}")

        # SELL ITEM
        elif choice == 2:
            inv = current_character.get("inventory", [])

            if not inv:
                print("Your inventory is empty.")
                continue

            print("\nYour Items:")
            for idx, item_id in enumerate(inv, 1):
                item = all_items.get(item_id, {"name": "Unknown", "type": "unknown"})
                print(f"{idx}. {item['name']} ({item['type']})")

            try:
                num = int(input("Enter item number to sell: ")) - 1
                item_id = inv[num]
                item_data = all_items[item_id]

                gold_received = inventory_system.sell_item(current_character, item_id, item_data)
                print(f"Sold {item_data['name']} for {gold_received} gold.")
            except (ValueError, IndexError):
                print("Invalid item number.")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Invalid choice. Pick 1, 2, or 3.")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state."""
    global current_character

    if not current_character:
        print("No character loaded.")
        return

    try:
        character_manager.save_character(current_character)
        print("\nGame saved successfully!\n")
    except Exception as e:
        print(f"[ERROR] Failed to save game: {e}")


def load_game_data():
    """Load all quest and item data from files."""
    global all_quests, all_items

    try:
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()

    except MissingDataFileError:
        print("[WARNING] Data files missing. Creating default files...")
        game_data.create_default_data_files()

        # Try loading again
        try:
            all_quests = game_data.load_quests()
            all_items = game_data.load_items()
        except Exception as e:
            print(f"[ERROR] Failed to load data even after creating defaults: {e}")
            all_quests = {}
            all_items = {}

    except InvalidDataFormatError as e:
        print(f"[ERROR] Data file format invalid: {e}")
        all_quests = {}
        all_items = {}

    except Exception as e:
        print(f"[ERROR] Unexpected error loading data: {e}")
        all_quests = {}
        all_items = {}


def handle_character_death():
    """Handle character death (simple implementation)."""
    global current_character, game_running

    if not current_character:
        return

    print("\n===== YOU HAVE DIED =====")
    print("Want to revive? Choose an option:\n")

    while True:
        print("1. Revive (cost: 50 gold)")
        print("2. Quit to Main Menu")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            gold = current_character.get("gold", 0)
            if gold >= 50:
                current_character["gold"] = gold - 50
                character_manager.revive_character(current_character)
                print("\nYou have been revived!\n")
                return
            else:
                print("Not enough gold to revive!")
        elif choice == "2":
            print("Returning to main menu…")
            game_running = False
            return
        else:
            print("Invalid choice.")


def display_welcome():
    """Display welcome message."""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function."""
    # Display welcome message
    display_welcome()

    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return

    # Main menu loop
    while True:
        choice = main_menu()

        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break


if __name__ == "__main__":
    main()
