"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: DeAundre Black

AI Usage: [Syntax errors, structure, and careless errors]


This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)


# AI Usage: Used AI (ChatGPT) to help structure/finish functions if I had errors or if I didn't have the correct formatting

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest

    Args:
        character: Character dictionary
        quest_id: Quest to accept
        quest_data_dict: Dictionary of all quest data

    Requirements to accept quest:
    - Character level >= quest required_level
    - Prerequisite quest completed (if any)
    - Quest not already completed
    - Quest not already active

    Returns: True if quest accepted
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        InsufficientLevelError if character level too low
        QuestRequirementsNotMetError if prerequisite not completed
        QuestAlreadyCompletedError if quest already done
    """

    # 1. Quest exists
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' does not exist.")

    quest = quest_data_dict[quest_id]

    # 2. Level requirement
    required_level = quest.get("required_level", 1)
    if character.get("level", 1) < required_level:
        raise InsufficientLevelError(
            f"Level {required_level} required to accept this quest."
        )

    # 3. Prerequisite requirement
    prereq = quest.get("prerequisite", "NONE")
    if prereq != "NONE" and prereq not in character["completed_quests"]:
        raise QuestRequirementsNotMetError(
            f"Prerequisite quest '{prereq}' not completed."
        )

    # 4. Not already completed
    if quest_id in character["completed_quests"]:
        raise QuestAlreadyCompletedError(
            f"Quest '{quest_id}' already completed."
        )

    # 5. Not already active
    if quest_id in character["active_quests"]:
        raise QuestRequirementsNotMetError(
            f"Quest '{quest_id}' is already active."
        )

    # 6. Accept quest
    character["active_quests"].append(quest_id)
    return True

    # TODO: Implement quest acceptance
    # Check quest exists
    # Check level requirement
    # Check prerequisite (if not "NONE")
    # Check not already completed
    # Check not already active
    # Add to character['active_quests']


def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards

    Args:
        character: Character dictionary
        quest_id: Quest to complete
        quest_data_dict: Dictionary of all quest data

    Rewards:
    - Experience points (reward_xp)
    - Gold (reward_gold)

    Returns: Dictionary with reward information
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        QuestNotActiveError if quest not in active_quests
    """

    # 1. Quest exists
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' does not exist.")

    quest = quest_data_dict[quest_id]

    # 2. Must be active to complete
    if quest_id not in character["active_quests"]:
        raise QuestNotActiveError(
            f"Quest '{quest_id}' is not currently active."
        )

    # Remove from active, move to completed
    character["active_quests"].remove(quest_id)
    character["completed_quests"].append(quest_id)

    # Grant rewards
    xp = quest.get("reward_xp", 0)
    gold = quest.get("reward_gold", 0)

    # Use character manager systems
    from character_manager import gain_experience, add_gold
    gain_experience(character, xp)
    add_gold(character, gold)

    # Return what was awarded
    return {
        "quest_id": quest_id,
        "reward_xp": xp,
        "reward_gold": gold
    }

    # TODO: Implement quest completion
    # Check quest exists
    # Check quest is active
    # Remove from active_quests
    # Add to completed_quests
    # Grant rewards (use character_manager.gain_experience and add_gold)
    # Return reward summary


def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it

    Returns: True if abandoned
    Raises: QuestNotActiveError if quest not active
    """

    if quest_id not in character["active_quests"]:
        raise QuestNotActiveError(
            f"Cannot abandon '{quest_id}' because it is not active."
        )

    character["active_quests"].remove(quest_id)
    return True

    # TODO: Implement quest abandonment


def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests

    Returns: List of quest dictionaries for active quests
    """

    active_list = []

    for quest_id in character.get("active_quests", []):
        if quest_id in quest_data_dict:
            active_list.append(quest_data_dict[quest_id])

    return active_list

    # TODO: Implement active quest retrieval
    # Look up each quest_id in character['active_quests']
    # Return list of full quest data dictionaries


def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests

    Returns: List of quest dictionaries for completed quests
    """

    completed_list = []

    for quest_id in character.get("completed_quests", []):
        if quest_id in quest_data_dict:
            completed_list.append(quest_data_dict[quest_id])

    return completed_list

    # TODO: Implement completed quest retrieval


def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept

    Available = meets level req + prerequisite done + not completed + not active

    Returns: List of quest dictionaries
    """

    available = []
    level = character.get("level", 1)

    for quest_id, quest in quest_data_dict.items():
        required_level = quest.get("required_level", 1)
        prereq = quest.get("prerequisite", "NONE")

        # Skip if completed
        if quest_id in character["completed_quests"]:
            continue

        # Skip if already active
        if quest_id in character["active_quests"]:
            continue

        # Level requirement
        if level < required_level:
            continue

        # Prerequisite check
        if prereq != "NONE" and prereq not in character["completed_quests"]:
            continue

        # If all requirements met, it's available
        available.append(quest)

    return available

    # TODO: Implement available quest search
    # Filter all quests by requirements


# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed

    Returns: True if completed, False otherwise
    """

    return quest_id in character.get("completed_quests", [])

    # TODO: Implement completion check


def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active

    Returns: True if active, False otherwise
    """

    return quest_id in character.get("active_quests", [])

    # TODO: Implement active check


def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest

    Returns: True if can accept, False otherwise
    Does NOT raise exceptions - just returns boolean
    """

    # Quest must exist
    if quest_id not in quest_data_dict:
        return False

    quest = quest_data_dict[quest_id]

    # Must not already be completed
    if quest_id in character.get("completed_quests", []):
        return False

    # Must not be already active
    if quest_id in character.get("active_quests", []):
        return False

    # Level requirement
    required_level = quest.get("required_level", 1)
    if character.get("level", 1) < required_level:
        return False

    # Prerequisite requirement
    prereq = quest.get("prerequisite", "NONE")
    if prereq != "NONE" and prereq not in character.get("completed_quests", []):
        return False

    return True

    # TODO: Implement requirement checking
    # Check all requirements without raising exceptions


def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest

    Returns: List of quest IDs in order [earliest_prereq, ..., quest_id]
    Example: If Quest C requires Quest B, which requires Quest A:
             Returns ["quest_a", "quest_b", "quest_c"]

    Raises: QuestNotFoundError if quest doesn't exist
    """

    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")

    chain = []
    current = quest_id

    while True:
        if current not in quest_data_dict:
            raise QuestNotFoundError(f"Quest '{current}' not found in chain tracing.")

        chain.append(current)
        prereq = quest_data_dict[current].get("prerequisite", "NONE")

        if prereq == "NONE":
            break  # No more prerequisites

        current = prereq  # Move to next prereq in chain

    chain.reverse()  # Put in correct chronological order
    return chain

    # TODO: Implement prerequisite chain tracing
    # Follow prerequisite links backwards
    # Build list in reverse order


# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """
    Calculate what percentage of all quests have been completed

    Returns: Float between 0 and 100
    """

    total_quests = len(quest_data_dict)
    if total_quests == 0:
        return 0.0  # avoid division by zero

    completed = len(character.get("completed_quests", []))
    percentage = (completed / total_quests) * 100
    return percentage

    # TODO: Implement percentage calculation
    # total_quests = len(quest_data_dict)
    # completed_quests = len(character['completed_quests'])
    # percentage = (completed / total) * 100


def get_total_quest_rewards_earned(character, quest_data_dict):
    """
    Calculate total XP and gold earned from completed quests

    Returns: Dictionary with 'total_xp' and 'total_gold'
    """

    total_xp = 0
    total_gold = 0

    for quest_id in character.get("completed_quests", []):
        if quest_id in quest_data_dict:
            quest = quest_data_dict[quest_id]
            total_xp += quest.get("reward_xp", 0)
            total_gold += quest.get("reward_gold", 0)

    return {
        "total_xp": total_xp,
        "total_gold": total_gold
    }

    # TODO: Implement reward calculation
    # Sum up reward_xp and reward_gold for all completed quests


def get_quests_by_level(quest_data_dict, min_level, max_level):
    """
    Get all quests within a level range

    Returns: List of quest dictionaries
    """

    results = []

    for quest_id, quest in quest_data_dict.items():
        lvl = quest.get("required_level", 1)
        if min_level <= lvl <= max_level:
            results.append(quest)

    return results

    # TODO: Implement level filtering


# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information

    Shows: Title, Description, Rewards, Requirements
    """

    print("\n" + "=" * 40)
    print(f"\n=== {quest_data['title']} ===")
    print("=" * 40)

    print(f"Description: {quest_data['description']}")

    print(f"Required Level: {quest_data.get('required_level', 1)}")

    prereq = quest_data.get("prerequisite", "NONE")
    if prereq == "NONE":
        prereq = "None"
    print(f"Prerequisite: {prereq}")

    print(f"Reward XP: {quest_data.get('reward_xp', 0)}")
    print(f"Reward Gold: {quest_data.get('reward_gold', 0)}")
    print()

    # TODO: Implement quest display
    print(f"Description: {quest_data['description']}")
    # ... etc


def display_quest_list(quest_list):
    """
    Display a list of quests in summary format

    Shows: Title, Required Level, Rewards
    """

    if not quest_list:
        print("\n(No quests found.)")
        return

    print("\n=== QUEST LIST ===")
    for quest in quest_list:
        print(f"- {quest['title']} (Level {quest['required_level']})")
        print(f"  Rewards: {quest['reward_xp']} XP, {quest['reward_gold']} Gold")
        print()

    # TODO: Implement quest list display


def display_character_quest_progress(character, quest_data_dict):
    """
    Display character's quest statistics and progress

    Shows:
    - Active quests count
    - Completed quests count
    - Completion percentage
    - Total rewards earned
    """

    print("\n=== QUEST PROGRESS ===")

    active = len(character.get("active_quests", []))
    completed = len(character.get("completed_quests", []))
    total = len(quest_data_dict)

    print(f"Active Quests: {active}")
    print(f"Completed Quests: {completed} / {total}")

    percentage = get_quest_completion_percentage(character, quest_data_dict)
    print(f"Completion: {percentage:.2f}%")

    rewards = get_total_quest_rewards_earned(character, quest_data_dict)
    print(f"Total XP Earned: {rewards['total_xp']}")
    print(f"Total Gold Earned: {rewards['total_gold']}")

    # TODO: Implement progress display


# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist

    Checks that every prerequisite (that's not "NONE") refers to a real quest

    Returns: True if all valid
    Raises: QuestNotFoundError if invalid prerequisite found
    """

    for quest_id, quest in quest_data_dict.items():
        prereq = quest.get("prerequisite", "NONE")

        if prereq != "NONE" and prereq not in quest_data_dict:
            raise QuestNotFoundError(
                f"Quest '{quest_id}' has invalid prerequisite '{prereq}'."
            )

    return True

    # TODO: Implement prerequisite validation
    # Check each quest's prerequisite
    # Ensure prerequisite exists in quest_data_dict


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")

    # Test data
    # test_char = {
    #     'level': 1,
    #     'active_quests': [],
    #     'completed_quests': [],
    #     'experience': 0,
    #     'gold': 100
    # }
    #
    # test_quests = {
    #     'first_quest': {
    #         'quest_id': 'first_quest',
    #         'title': 'First Steps',
    #         'description': 'Complete your first quest',
    #         'reward_xp': 50,
    #         'reward_gold': 25,
    #         'required_level': 1,
    #         'prerequisite': 'NONE'
    #     }
    # }
    #
    # try:
    #     accept_quest(test_char, 'first_quest', test_quests)
    #     print("Quest accepted!")
    # except QuestRequirementsNotMetError as e:
    #     print(f"Cannot accept: {e}")
