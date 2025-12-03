""""
COMP
163 - Project
3: Quest
Chronicles
Main
Game
Module - Starter
Code

Name:
DeAundre Black

AI
Usage:
I did need a lot of help in terms of making my imports work, chatGPT helped me fix those along with small syntax and structural errors
*ALSO
SEE
LINE
184
AND
LINE
185, IMPORTS
BELOW
APPARENTLY
WERE
NOT
WORKING.

This is the
main
game
file
that
ties
all
modules
together.
Demonstrates
module
integration and complete
game
flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# AI Usage: Used AI (ChatGPT) to help structure/finish functions if I had errors or if I didn't have the correct formatting

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():

    """
Display
main
menu and get
player
choice

Options:
1.
New
Game
2.
Load
Game
3.
Exit

Returns: Integer
choice(1 - 3)
"""
while True:
    print("=== MAIN MENU - Choose an option: ===")
    print("1: New Game")
    print("2: Load Game")
    print("3: Exit")

    try:
        menu_choice = int(input("Mode Selection (1-3): "))
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 3.")
        continue

    if menu_choice in range(1, 4):
        return menu_choice
    else:
        print("Invalid Mode Choice. Please choose a number between 1 and 3.")

# TODO: Implement main menu display
# Show options
# Get user input
# Validate input (1-3)
# Return choice


def new_game():
"""
Start
a
new
game

Prompts
for:
    - Character
    name
- Character


class


Creates
character and starts
game
loop
"""
global current_character

# TODO: Implement new game creation
# Get character name from user
# Get character class from user
# Try to create character with character_manager.create_character()
# Handle InvalidCharacterClassError
# Save character
# Start game loop


def load_game():
"""
Load
an
existing
saved
game

Shows
list
of
saved
characters
Prompts
user
to
select
one
"""
global current_character

from character_manager import list_saved_characters, load_character # The imports at the top are apparently not working

# 1. Get list of saved characters
saved_characters = list_saved_characters()  # from character_manager

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
        if 1 <= choice <= len(saved_characters):
            character_name = saved_characters[choice - 1]
            break
        else:
            print("Invalid choice, try again.")
    except ValueError:
        print("Please enter a number.")

# 4. Attempt to load character
try:
    current_character = load_character(character_name)
    print(f"Loaded character: {current_character['name']}")
except CharacterNotFoundError:
    print("Error: Character not found.")
    return
except SaveFileCorruptedError:
    print("Error: Save file is corrupted.")
    return

# 5. Start game loop
game_loop()

# TODO: Implement game loading
# Get list of saved characters
# Display them to user
# Get user choice
# Try to load character with character_manager.load_character()
# Handle CharacterNotFoundError and SaveFileCorruptedError
# Start game loop


# AI USAGE: Since display_stats/display_inventory weren't working, I had ChatGPT explain was was wrong
# It suggested me to add these functions below to test if the code would work after.

# temporary/simple implementations if missing
def display_stats(character, class_name=None, level=None): # Function to display character's stats
if not character:
    print("No character loaded.")
    return
print(f"{character['name']} - {class_name} (Level {level})")
print(f"HP: {character['health']}/{character['max_health']}  STR:{character['strength']}  MAG:{character['magic']}  Gold:{character['gold']}")

def display_inventory(character, item_data_dict): # Function to display character's inventory
if not character or not character.get("inventory"):
    print("Inventory empty.")
    return
for i, item_id in enumerate(character["inventory"], 1):
    info = item_data_dict.get(item_id, {"name":"Unknown"})
    print(f"{i}. {info.get('name','Unknown')} ({info.get('type','?')})")


# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
"""
Main
game
loop - shows
game
menu and processes
actions
"""

global game_running, current_character

from character_manager import save_character # Imports at the top aren't working apparently

game_running = True

while game_running:
    print("\n=== GAME MENU ===")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Go on Quest / Battle")
    print("4. Save Game")
    print("5. Exit to Main Menu")

    try:
        choice = int(input("Select an option: "))
    except ValueError:
        print("Please enter a number.")
        continue

    if choice == 1:
        display_stats(current_character, current_character.get("class", "Unknown"), current_character.get("level", 1))
    elif choice == 2:
        display_inventory(current_character, all_items)  # assuming all_items is loaded
    elif choice == 3:
        print("Starting quest or battle... (placeholder)")
        # You can integrate quest_handler / combat_system here
    elif choice == 4:
        try:
            save_character(current_character)
            print("Game saved successfully.")
        except Exception as e:
            print(f"Error saving game: {e}")
    elif choice == 5:
        print("Exiting to main menu...")
        game_running = False
    else:
        print("Invalid choice. Please select a number from 1-5.")

# TODO: Implement game loop
# While game_running:
#   Display game menu
#   Get player choice
#   Execute chosen action
#   Save game after each action


def game_menu():
"""
Display
game
menu and get
player
choice

Options:
1.
View
Character
Stats
2.
View
Inventory
3.
Quest
Menu
4.
Explore(Find
Battles)
5.
Shop
6.
Save and Quit

Returns: Integer
choice(1 - 6)
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

# TODO: Implement game menu


# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
"""
Display
character
information
"""
    global current_character

    if not current_character:
        print("No character loaded.")
        return

    print("\n=== CHARACTER STATS ===")
    print(f"Name: {current_character['name']}")
    print(f"Class: {current_character['class']}")
    print(f"Level: {current_character['level']}")
    print(f"XP: {current_character['experience']}")
    print(f"Gold: {current_character['gold']}")
    print(f"Health: {current_character['health']}/{current_character['max_health']}")
    print(f"Strength: {current_character['strength']}")
    print(f"Magic: {current_character['magic']}")

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

    # TODO: Implement stats display
    # Show: name, class, level, health, stats, gold, etc.
    # Use character_manager functions
    # Show quest progress using quest_handler


def view_inventory():
    """
Display and manage
inventory
"""
    global current_character, all_items

    inv = current_character["inventory"]

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
    except:
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
            t = item_data["type"]
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

    # TODO: Implement inventory menu
    # Show current inventory
    # Options: Use item, Equip weapon/armor, Drop item
    # Handle exceptions from inventory_system


def quest_menu():
    """
Quest
management
menu
"""
    global current_character, all_quests

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

    # TODO: Implement quest menu
    # Show:
    #   1. View Active Quests
    #   2. View Available Quests
    #   3. View Completed Quests
    #   4. Accept Quest
    #   5. Abandon Quest
    #   6. Complete Quest (for testing)
    #   7. Back
    # Handle exceptions from quest_handler


def explore():
    """
Find and fight
random
enemies
"""
    global current_character

    print("\n=== EXPLORING... ===")

    try:
        # Generate a level-appropriate enemy
        enemy = combat_system.generate_enemy(current_character["level"])
        print(f"You encountered a {enemy['name']}!")

        # Start combat
        battle = combat_system.SimpleBattle(current_character, enemy)
        result = battle.start()

        if result == "victory":
            rewards = combat_system.get_victory_rewards(enemy)
            xp = rewards["xp"]
            gold = rewards["gold"]

            current_character["experience"] += xp
            current_character["gold"] += gold

            print(f"You defeated the {enemy['name']}!")
            print(f"Rewards: +{xp} XP, +{gold} gold")

        elif result == "defeat":
            print("You were defeated in battle...")
            raise CharacterDeadError("Your character has died.")

        else:
            print("Combat ended unexpectedly.")

    except CombatError as e:
        print(f"Combat error: {e}")

    except CharacterDeadError as e:
        print(f"\n*** GAME OVER ***\n{e}")
        print("Load a saved game to continue.")
        return

    except Exception as e:
        print(f"Unexpected error during exploration: {e}")

    # TODO: Implement exploration
    # Generate random enemy based on character level
    # Start combat with combat_system.SimpleBattle
    # Handle combat results (XP, gold, death)
    # Handle exceptions


def shop():
    """
Shop
menu
for buying / selling items"""
    global current_character, all_items

    while True:
        print("\n=== SHOP MENU ===")
        print(f"Your Gold: {current_character['gold']}")
        print("Items for Sale:")

        item_list = list(all_items.items())
        for index, (item_id, item) in enumerate(item_list, 1):
            print(f"{index}. {item['name']} ({item['type']}), Cost: {item['cost']} gold")

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
                print(f"Purchased {item_data['name']}!")

            except IndexError:
                print("Invalid item number.")
            except Exception as e:
                print(f"Error: {e}")

        # SELL ITEM
        elif choice == 2:
            inv = current_character["inventory"]

            if not inv:
                print("Your inventory is empty.")
                continue

            print("\nYour Items:")
            for idx, item_id in enumerate(inv, 1):
                item = all_items[item_id]
                print(f"{idx}. {item['name']} ({item['type']})")

            try:
                num = int(input("Enter item number to sell: ")) - 1
                item_id = inv[num]
                item_data = all_items[item_id]

                gold_received = inventory_system.sell_item(current_character, item_id, item_data)
                print(f"Sold {item_data['name']} for {gold_received} gold.")

            except IndexError:
                print("Invalid item number.")
            except Exception as e:
                print(f"Error: {e}")

        else:
            print("Invalid choice. Pick 1, 2, or 3.")

    # TODO: Implement shop
    # Show available items for purchase
    # Show current gold
    # Options: Buy item, Sell item, Back
    # Handle exceptions from inventory_system


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character

    try:
        character_manager.save_character(current_character)
        print("\nGame saved successfully!\n")
    except Exception as e:
        print(f"[ERROR] Failed to save game: {e}")


    # TODO: Implement save
    # Use character_manager.save_character()
    # Handle any file I/O exceptions


def load_game_data():
    """Load all quest and item data from files"""
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

    # TODO: Implement data loading
    # Try to load quests with game_data.load_quests()
    # Try to load items with game_data.load_items()
    # Handle MissingDataFileError, InvalidDataFormatError
    # If files missing, create defaults with game_data.create_default_data_files()


def handle_character_death():
    """Handle character death"""
    global current_character, game_running

    print("\n===== YOU HAVE DIED =====")
    print("Want to revive? Choose an option:\n")

    while True:
        print("1. Revive (cost: 50 gold)")
        print("2. Quit to Main Menu")

        choice = input("Choose an option: ")

        if choice == "1":
            if current_character.gold >= 50:
                current_character.gold -= 50
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


    # TODO: Implement death handling
    # Display death message
    # Offer: Revive (costs gold) or Quit
    # If revive: use character_manager.revive_character()
    # If quit: set game_running = False


def display_welcome():
    """Display welcome message"""
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
    """Main game execution function"""

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
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()