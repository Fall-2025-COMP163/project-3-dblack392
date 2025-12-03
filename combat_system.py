"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: De'Aundre Black

AI Usage: [Syntax and Structure. Had issues with importing modules and chatGPT helped me fix them.]


Handles combat mechanics
"""

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)


# AI Usage (1): Couldn't figure out why my start_battle function was giving me an error, ChatGPT told me to import the is_character_dead function from character_manager.py

# AI Usage (2): Used AI (ChatGPT) to help structure/finish functions if I had errors or if I didn't have the correct formatting
# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type

    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100

    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    # TODO: Implement enemy creation
    # Return dictionary with: name, health, max_health, strength, magic, xp_reward, gold_reward

    enemies = {
        "goblin": {
            "name": "Goblin",
            "type": "Goblin",
            "health": 30,
            "max_health": 30,
            "strength": 5,
            "magic": 0,
            "xp_reward": 10,
            "gold_reward": 5
        },
        "orc": {
            "name": "Orc",
            "type": "Orc",
            "health": 50,
            "max_health": 50,
            "strength": 12,
            "magic": 2,
            "xp_reward": 20,
            "gold_reward": 12
        }
    }

    enemy_type = enemy_type.lower()  # normalize input

    if enemy_type not in enemies:
        raise InvalidTargetError(f"Unknown enemy: {enemy_type}")

    # Return a new dictionary so modifications in battle don't affect template
    e = enemies[enemy_type]
    return {
        "name": e["name"],
        "type": e["type"],
        "health": e["health"],
        "max_health": e["max_health"],
        "strength": e["strength"],
        "magic": e["magic"],
        "xp_reward": e["xp_reward"],
        "gold_reward": e["gold_reward"]
    }


def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level

    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons

    Returns: Enemy dictionary
    """
    # TODO: Implement level-appropriate enemy selection
    # Use if/elif/else to select enemy type
    # Call create_enemy with appropriate type

    if character_level in range(1, 3):  # Level 1/Level 2 characters start off by fight Goblins
        return create_enemy(enemy_type="goblin")

    elif character_level in range(3, 6):  # Then, characters with levels 3-5 fight Orcs
        return create_enemy(enemy_type="orc")

    elif character_level >= 6:  # Characters level 6 and above fight Dragons.
        return create_enemy(enemy_type="dragon")


# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system

    Manages combat between character and enemy
    """

    def __init__(self, character, enemy):

        # BELOW: Intitializing Characters and Enemies for battle
        self.character = character
        self.enemy = enemy

        # BELOW: combat_active flag
        self.combat_active = True

        # BELOW: turn counter starts at 0 at beginning of the battle
        self.turn_counter = 0

        """Initialize battle with character and enemy"""
        # TODO: Implement initialization
        # Store character and enemy
        # Set combat_active flag
        # Initialize turn counter

    def start_battle(self):

        """
        Start the combat loop

        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}

        Raises: CharacterDeadError if character is already dead
        """
        # Imported is_character_dead function from character_manager since it was needed to run this function.
        from character_manager import is_character_dead

        # Make sure character is alive
        if is_character_dead(self.character):
            raise CharacterDeadError("Character is already dead, cannot start battle.")

        # Initialize battle results
        battle_results = {
            "winner": None,
            "xp_gained": 0,
            "gold_gained": 0
        }

        # Example: turn counter starts at 1
        self.turn_counter = 1

        # TODO: Implement actual battle loop here
        # while self.combat_active:
        #     self.player_turn()
        #     self.enemy_turn()
        #     check for death/winner

        return battle_results

    def player_turn(self):

        """
        Handle player's turn

        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run

        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement player turn
        # Check combat is active
        # Display options
        # Get player choice
        # Execute chosen action

        if not self.combat_active:
            raise CombatNotActiveError(
                "No battles active.")  # Special exception to handle function calls while battle is inactive

        self.turn_counter += 1  # Adds a turn every time one is taken

        print("\n=== PLAYER TURN ===")
        print("1. Basic Attack")
        print("2. Special Ability")
        print("3. Run Away")

        player_choice = input("Choose your move!:" \
                              "1: Basic Attack" \
                              "2: Heavy Attack (Special Ability) " \
                              "3: Run Away")

        if player_choice == "1":  # Basic Attack
            damage = self.character["strength"]
            self.enemy["health"] -= damage  # Enemy takes damage based off of Character strength
            print(f"{self.character["
            Name
            "]} chose Basic attack: Dealt {damage} damage.")

            elif player_choice == "2":  # Heavy Attack/Special
            damage = self.character["strength"]
            self.enemy["health"] -= damage + 5  # Enemy takes extra damage (heavy attack)
            print(f"{self.character["
            Name
            "]} chose Basic attack: Dealt {damage} damage.")

            elif player_choice == "3":  # Run Away (Chance)
            escape_chance = self.enemy["strength"] // 5  # Equation for how your character can escape

            if self.character["level"] >= escape_chance:
                print("You successfully ran away!")
            self.combat_active = False
            self.battle_result = {"winner": "none", "xp_gained": 0, "gold_gained": 0}
            return
        else:
            print("You were not strong enough to escape!")

        # CHECK FOR ENEMY DEATH
        if self.enemy["health"] <= 0:
            print(f"The {self.enemy['type']} has been defeated!")

            self.combat_active = False  # Fight ended, combat returns false
            self.battle_result = {
                "winner": "player",
                "xp_gained": self.enemy.get("xp_reward", 20),
                "gold_gained": self.enemy.get("gold_reward", 10)
            }

        self.turn_counter += 1

    def enemy_turn(self):

        """
        Handle enemy's turn - simple AI

        Enemy always attacks

        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement enemy turn
        # Check combat is active
        # Calculate damage
        # Apply to character

        if not self.combat_active:
            raise CombatNotActiveError("No battles active.")

        print("\n=== ENEMY TURN ===")

        # 2. Enemy always attacks
        damage = self.enemy["strength"]
        self.character["health"] -= damage

        print(f"The {self.enemy['type']} attacks you for {damage} damage!")

        # 3. Check player death
        if self.character["health"] <= 0:
            print("You have been defeated...")  # Character receives defeat message

            self.combat_active = False  # Battle is over, combat_active = false

            # Prints the battle result
            self.battle_result = {
                "winner": "enemy",
                "xp_gained": 0,
                "gold_gained": 0
            }

    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack

        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1

        Returns: Integer damage amount
        """
        damage_amount = attacker["strength"] - (defender["strength"] // 4)  # Used Damage Formula

        if damage_amount < 1:
            damage_amount = 1  # Minimum amount of damage that can be done

        return int(damage_amount)  # Returns integer amount

    def apply_damage(self, target, damage):

        """
        Apply damage to a character or enemy

        Reduces health, prevents negative health
        """
        # TODO: Implement damage application

        target["health"] -= damage

        if target["health"] <= 0:
            target["health"] = 0  # Prevents negative health

    def check_battle_end(self):
        """
        Check if battle is over

        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        # TODO: Implement battle end check

        if self.character["health"] <= 0:
            return "enemy"

        if self.enemy["health"] <= 0:
            return "player"

        else:
            return None  # If both characters are still alive

    def attempt_escape(self):
        """
        Try to escape from battle

        50% success chance

        Returns: True if escaped, False if failed
        """
        if self.character["magic"] > self.enemy[
            "strength"]:  # Escapes are based on if character magic is greater than enemy strength
            self.combat_active = False
            return True

        return False

        # TODO: Implement escape attempt
        # Use random number or simple calculation
        # If successful, set combat_active to False


# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability

    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)

    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    # TODO: Implement special abilities
    # Check character class
    # Execute appropriate ability
    # Track cooldowns (optional advanced feature)

    if character["class"] == "Warrior":
        return warrior_power_strike(character, enemy)

    elif character["class"] == "Mage":
        return mage_fireball(character, enemy)

    elif character["class"] == "Rogue":
        return rogue_critical_strike(character, enemy)

    elif character["class"] == "Cleric":
        return cleric_heal(character)

    else:
        return "No special ability available."


def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    # TODO: Implement power strike
    # Double strength damage

    damage = character["strength"] * 2
    enemy["health"] -= damage
    return f'{character["name"]} used Power Strike for {damage} damage!'


def mage_fireball(character, enemy):
    """Mage special ability"""
    # TODO: Implement fireball
    # Double magic damage

    damage = character["magic"] * 2
    enemy["health"] -= damage
    return f'{character["name"]} cast Fireball for {damage} damage!'


def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    # TODO: Implement critical strike
    # 50% chance for triple damage

    # 50% chance – determined by even enemy health
    crit = (enemy["health"] % 2 == 0)

    if crit:
        damage = character["strength"] * 3
        enemy["health"] -= damage
        return f'{character["name"]} landed a CRITICAL STRIKE for {damage} damage!'
    else:
        damage = character["strength"]  # normal damage
        enemy["health"] -= damage
        return f'{character["name"]} attacked for {damage} damage.'


def cleric_heal(character):
    """Cleric special ability"""
    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)


# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character, combat_active):
    """
    Check if character is in condition to fight

    Returns: True if health > 0 and not in battle
    """
    # TODO: Implement fight check

    if character["health"] > 0 and combat_active == False:
        print("Character is available for battle")
        return True

    else:
        return False


def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy

    Returns: Dictionary with 'xp' and 'gold'
    """
    # TODO: Implement reward calculation

    # xp/gold dictionary, used .get() to prevent any key errors
    return {
        "xp": enemy.get("xp_reward", 0),
        "gold": enemy.get("gold_reward", 0)
    }


def display_combat_stats(character, enemy):
    """
    Display current combat status

    Shows both character and enemy health/stats
    """
    # TODO: Implement status display

    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")


def display_battle_log(message):
    message = "=== DUEL TIME!! ==="
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f">>> {message}")


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")

    # Test enemy creation
    # try:
    #     goblin = create_enemy("goblin")
    #     print(f"Created {goblin['name']}")
    # except InvalidTargetError as e:
    #     print(f"Invalid enemy: {e}")

    # Test battle
    # test_char = {
    #     'name': 'Hero',
    #     'class': 'Warrior',
    #     'health': 120,
    #     'max_health': 120,
    #     'strength': 15,
    #     'magic': 5
    # }
    #
    # battle = SimpleBattle(test_char, goblin)
    # try:
    #     result = battle.start_battle()
    #     print(f"Battle result: {result}")
    # except CharacterDeadError:
    #     print("Character is dead!")