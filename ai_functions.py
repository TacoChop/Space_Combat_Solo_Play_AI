from random import randint


def generate_command_profile(mission_type, mission_role):
    """Generates a random profile for the enemy commander based on the chosen mission type and the enemy's role for the
    mission. Provides the initial modifier used in determine_turn_modifiers() as well as a general outline of how the
    commander should behave in a given situation."""

    command_personalities_dict = {-4: 'Cowardly', -3: 'Overly Cautious', -2: 'Cautious', -1: 'Defensive', 0: 'Average',
                                  1: 'Active', 2: 'Aggressive', 3: 'Overly Aggressive', 4: 'Foolhardy'}
    standing_orders_dict = {-4: 'Avoid All Contact', -3: 'Perform Reconnaissance', -2: 'Probe Enemy Defenses',
                            -1: 'Cautiously Engage Enemy', 0: 'Engage Enemy', 1: 'Press Any Advantage',
                            2: 'Assault Enemy', 3: 'Aggressively Assault Enemy', 4: 'Annihilate Enemy'}
    charisma_levels_dict = {-3: 'Disrespected', -2: 'Overbearing', -1: 'Bothersome', 0: 'Average', 1: 'Liked',
                            2: 'Respected', 3: 'Inspirational'}

    total_command_mod = 0
    personality_mod = randint(-4, 4)
    charisma_mod = randint(-3, 3)
    orders_mod = randint(-4, 4)

    if mission_type == 'Blockade' and mission_role == 'Attacker':
        orders_mod = randint(-1, 4)
        personality_mod = randint(-2, 4)
        total_command_mod += 1
    elif mission_type == 'Blockade' and mission_role == 'Defender':
        orders_mod = randint(-1, 1)
        personality_mod = randint(-2, 2)
        total_command_mod -= 1
    elif mission_type == 'Ambush' and mission_role == 'Attacker':
        orders_mod = randint(2, 4)
        personality_mod = randint(-1, 4)
        total_command_mod += 2
    elif mission_type == 'Ambush' and mission_role == 'Defender':
        orders_mod = randint(-4, 2)
        total_command_mod -= 1
    elif mission_type == 'Pursuit' and mission_role == 'Attacker':
        orders_mod = randint(-1, 4)
        total_command_mod += 2
    elif mission_type == 'Pursuit' and mission_role == 'Defender':
        orders_mod = randint(-4, 1)
    elif mission_type == 'Hit and Run' and mission_role == 'Attacker':
        orders_mod = randint(-1, 3)
        total_command_mod += 1
    elif mission_type == 'Hit an Run' and mission_role == 'Defender':
        orders_mod = randint(-4, 1)
        total_command_mod -= 1

    personality = command_personalities_dict[personality_mod]
    total_command_mod += personality_mod

    charisma = charisma_levels_dict[charisma_mod]
    total_command_mod += charisma_mod

    orders = standing_orders_dict[orders_mod]
    total_command_mod += orders_mod

    if total_command_mod > 5:
        total_command_mod = 5
    elif total_command_mod < -5:
        total_command_mod = -5

    print(f'The enemy commander is {personality} and is')
    print(f'considered {charisma} by their subordinates.')
    print(f'They have standing orders to {orders}.')
    print(f'Command modifier: {total_command_mod}')

    return total_command_mod


def determine_turn_modifiers(command_mod, fleet_strength, engagement_level):
    """Generates an overall modifier based on fleet strength, engagement level, and command modifier to be used
    each turn with determine_ship_orders()."""

    fleet_strength_vals = {'Full Strength': 1, 'Minimal Damage': 0, 'Suffering Minor Losses': -1,
                           'Suffering Heavy Losses': -3, 'Routed': -4}

    engagement_level_vals = {'No Contact': 0, 'Enemy Sighted': 1, 'Engaging Enemy': 0, 'Under Fire': -1,
                             'Under Heavy Fire': -2}

    strength = fleet_strength_vals[fleet_strength]
    engagement = engagement_level_vals[engagement_level]
    turn_mod = command_mod + strength + engagement

    if fleet_strength == 'Full Strength' and turn_mod < 0:
        turn_mod = 0
    elif fleet_strength == 'Minimal Damage' and turn_mod < 0:
        turn_mod += 1
    elif fleet_strength == 'Suffering Heavy Losses' and turn_mod > 0:
        turn_mod -= 1
    elif fleet_strength == 'Routed':
        turn_mod = -15

    if engagement_level == 'No Contact':
        turn_mod = 0
    elif engagement_level == 'Enemy Sighted' and turn_mod < 0:
        turn_mod += 1
    elif engagement_level == 'Under Heavy Fire' and turn_mod > 0:
        turn_mod -= 1

    return turn_mod


def determine_ship_orders(turn_mod, fleet_strength, ship_name='All Ships'):
    """Uses the turn modifier and a small random variance to determine orders for any ship passed to ship_name.
    The value passed to fleet_strength is used to determine whether or not the fleet has been routed and should attempt
    to flee the battle."""

    movement_orders = {-5: 'Charge FTL Drives', -4: 'Move Maximum Distance From Enemy', -3: 'Disengage From Enemy',
                       -2: 'Stay Outside Enemy Optimal Range', -1: 'Maintain Long Range', 0: 'Maintain Optimal Range',
                       1: 'Maintain Medium Range', 2: 'Close Within Short Range'}

    fire_orders = {-4: 'Cease Firing, Charge FTL Drives', -3: 'Cease Firing, Take Evasive Action',
                   -2: 'Defensive Firing Only', -1: 'Fire On Closest Enemy', 0: 'Engage Priority Target',
                   1: 'Fire On Damaged Enemy', 2: 'Fire On Closest Damaged Enemy', 3: 'Engage Multiple Targets'}

    move_mod = turn_mod + randint(-1, 1)
    fire_mod = turn_mod + randint(-1, 1)

    if move_mod > 2:
        move_mod = 2
    elif move_mod < -4:
        move_mod = -4

    if fire_mod > 3:
        fire_mod = 3
    elif fire_mod < -3:
        fire_mod = -3

    if fleet_strength == 'Routed':
        move_mod = -5
        fire_mod = -4

    movement = movement_orders[move_mod]
    fire = fire_orders[fire_mod]

    print(f'Ship: {ship_name}')
    print(f'Movement Order: {movement}')
    print(f'Fire Order: {fire}')
