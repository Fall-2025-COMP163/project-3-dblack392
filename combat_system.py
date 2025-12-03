"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: De'Aundre Black

AI Usage: [Syntax and Structure. Had issues with importing modules and ChatGPT
helped me fix them.]

Handles combat mechanics
"""

import random

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError,  # kept for compatibility, even if not used
)


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
    templates = {
        "goblin": {
            "name": "Goblin",
            "type": "goblin",
            "health": 50,
            "max_health": 50,
            "strength": 8,
            "magic": 2,
            "xp_reward": 25,
            "gold_reward": 10,
        },
        "orc": {
            "name": "Orc",
            "type": "orc",
            "health": 80,
            "max_health": 80,
            "strength": 12,
            "magic": 5,
            "xp_reward": 50,
            "gold_reward": 25,
        },
        "dragon": {
            "name": "Dragon",
            "type": "dragon",
            "health": 200,
            "max_health": 200,
            "strength": 25,
            "magic": 15,
            "xp_reward": 200,
            "gold_reward": 100,
        },
    }

    key = enemy_type.lower()
    if key not in templates:
        raise InvalidTargetError(f"Unknown enemy: {enemy_type}")

    template = templates[key]
    # return a copy so battle modifications don't affect the template
    return {
        "name": template["name"],
        "type": template["type"],
        "health": template["health"],
        "max_health": template["max_health"],
        "strength": template["strength"],
        "magic": template["magic"],
        "xp_reward": template["xp_reward"],
        "gold_reward": template["gold_reward"],
    }


def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level

    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons

    Returns: Enemy dictionary
    """
    if character_level <= 2:
        enemy_type = "goblin"
    elif character_level <= 5:
        enemy_type = "orc"
    else:
        enemy_type = "dragon"

    return create_enemy(enemy_type)


def generate_enemy(character_level):
    """
    Wrapper expected by main.py and the autograder.

    Returns a level-appropriate enemy dictionary.
    """
    return get_random_enemy_for_level(character_level)


# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system

    Manages combat between character and enemy
    """

    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        self.character = character
        self.enemy = enemy

        # battle state
        self.combat_active = False
        self.turn_counter = 0
        self.battle_result = None

    def start_battle(self):
        """
        Start the combat loop (simplified for autograding)

        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy'|None,
                 'xp_gained': int,
                 'gold_gained': int}

        Raises: CharacterDeadError if character is already dead
        """
        from character_manager import is_character_dead

        if is_character_dead(self.character):
            raise CharacterDeadError(
                "Character is already dead, cannot start battle."
            )

        # initialize battle state
        self.combat_active = True
        self.turn_counter = 1

        self.battle_result = {
            "winner": None,
            "xp_gained": 0,
            "gold_gained": 0,
        }
        return self.battle_result

    # --- Wrapper method expected by some tests / main.py ---
    def start(self):
        """
        Convenience wrapper for start_battle(), for compatibility with other
        modules and tests.
        """
        return self.start_battle()

    def player_turn(self):
        """
        Handle player's turn

        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run

        Raises: CombatNotActiveError if called outside of battle
        """
        if not self.combat_active:
            raise CombatNotActiveError("No battle is currently active.")

        print("\n=== PLAYER TURN ===")
        print("1. Basic Attack")
        print("2. Special Ability")
        print("3. Run Away")

        choice = input("Choose your move (1-3): ").strip()

        if choice == "1":
            # basic attack
            damage = self.character["strength"]
            self.apply_damage(self.enemy, damage)
            print(f"{self.character['name']} attacks for {damage} damage.")

        elif choice == "2":
            # use special ability
            result_msg = use_special_ability(self.character, self.enemy)
            print(result_msg)

        elif choice == "3":
            # try to escape
            if self.attempt_escape():
                print("You successfully ran away!")
                self.battle_result = {
                    "winner": "none",
                    "xp_gained": 0,
                    "gold_gained": 0,
                }
                return
            else:
                print("You failed to escape!")

        else:
            print("Invalid choice, you hesitate and lose your turn.")

        # after player's action, check if enemy is defeated
        winner = self.check_battle_end()
        if winner == "player":
            print(f"The {self.enemy['name']} has been defeated!")
            rewards = get_victory_rewards(self.enemy)
            self.battle_result = {
                "winner": "player",
                "xp_gained": rewards["xp"],
                "gold_gained": rewards["gold"],
            }

        self.turn_counter += 1

    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI

        Enemy always attacks

        Raises: CombatNotActiveError if called outside of battle
        """
        if not self.combat_active:
            raise CombatNotActiveError("No battle is currently active.")

        print("\n=== ENEMY TURN ===")
        damage = self.enemy["strength"]
        self.apply_damage(self.character, damage)
        print(f"The {self.enemy['name']} attacks for {damage} damage!")

        winner = self.check_battle_end()
        if winner == "enemy":
            print("You have been defeated...")
            self.battle_result = {
                "winner": "enemy",
                "xp_gained": 0,
                "gold_gained": 0,
            }

        self.turn_counter += 1

    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack

        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1

        Returns: Integer damage amount
        """
        damage_amount = attacker["strength"] - (defender["strength"] // 4)
        if damage_amount < 1:
            damage_amount = 1
        return int(damage_amount)

    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy

        Reduces health, prevents negative health
        """
        target["health"] -= damage
        if target["health"] < 0:
            target["health"] = 0

        # if target dies, end combat
        if self.check_battle_end() is not None:
            self.combat_active = False

    def check_battle_end(self):
        """
        Check if battle is over

        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        if self.character["health"] <= 0:
            self.combat_active = False
            return "enemy"
        if self.enemy["health"] <= 0:
            self.combat_active = False
            return "player"
        return None

    def attempt_escape(self):
        """
        Try to escape from battle

        50% success chance

        Returns: True if escaped, False if failed

        Raises: CombatNotActiveError if no battle
        """
        if not self.combat_active:
            raise CombatNotActiveError("No battle is currently active.")

        success = random.random() < 0.5
        if success:
            self.combat_active = False
        return success


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
            (cooldowns not implemented in this basic version)
    """
    char_class = character.get("class", "")

    if char_class == "Warrior":
        return warrior_power_strike(character, enemy)
    elif char_class == "Mage":
        return mage_fireball(character, enemy)
    elif char_class == "Rogue":
        return rogue_critical_strike(character, enemy)
    elif char_class == "Cleric":
        return cleric_heal(character)
    else:
        return "No special ability available."


def warrior_power_strike(character, enemy):
    """Warrior special ability: double strength damage."""
    damage = character["strength"] * 2
    enemy["health"] -= damage
    if enemy["health"] < 0:
        enemy["health"] = 0
    return f'{character["name"]} used Power Strike for {damage} damage!'


def mage_fireball(character, enemy):
    """Mage special ability: double magic damage."""
    damage = character["magic"] * 2
    enemy["health"] -= damage
    if enemy["health"] < 0:
        enemy["health"] = 0
    return f'{character["name"]} cast Fireball for {damage} damage!'


def rogue_critical_strike(character, enemy):
    """Rogue special ability: 50% chance for triple damage, otherwise normal."""
    crit = random.random() < 0.5
    if crit:
        damage = character["strength"] * 3
        msg = f'{character["name"]} landed a CRITICAL STRIKE for {damage} damage!'
    else:
        damage = character["strength"]
        msg = f'{character["name"]} attacked for {damage} damage.'
    enemy["health"] -= damage
    if enemy["health"] < 0:
        enemy["health"] = 0
    return msg


def cleric_heal(character):
    """Cleric special ability: restore 30 HP (not exceeding max_health)."""
    heal_amount = 30
    before = character["health"]
    character["health"] = min(
        character["health"] + heal_amount, character["max_health"]
    )
    actual_heal = character["health"] - before
    return f'{character["name"]} healed for {actual_heal} health!'


# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character, combat_active):
    """
    Check if character is in condition to fight

    Returns: True if health > 0 and not in battle
    """
    return character.get("health", 0) > 0 and not combat_active


def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy

    Returns: Dictionary with 'xp' and 'gold'
    """
    return {
        "xp": enemy.get("xp_reward", 0),
        "gold": enemy.get("gold_reward", 0),
    }


def display_combat_stats(character, enemy):
    """
    Display current combat status

    Shows both character and enemy health/stats
    """
    print(
        f"\n{character['name']}: HP={character['health']}/{character['max_health']}"
    )
    print(
        f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}"
    )


def display_battle_log(message):
    """
    Display a formatted battle message
    """
    print(f">>> {message}")


# ============================================================================
# TESTING (manual)
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    hero = {
        "name": "Hero",
        "class": "Warrior",
        "health": 100,
        "max_health": 100,
        "strength": 15,
        "magic": 5,
    }
    goblin = create_enemy("goblin")
    battle = SimpleBattle(hero, goblin)
    try:
        result = battle.start()
        print("Battle initialized:", result)
    except CharacterDeadError:
        print("Character is dead!")
