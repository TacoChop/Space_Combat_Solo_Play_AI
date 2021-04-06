import PySimpleGUI as sg
import ai_functions as ai


# Tooltip Text
individual_orders_tip = 'If this box is left unchecked one set of orders will be issued that applies to all ships.'
command_profile_tip = 'Generate a personality profile for the enemy commander. Negative \n' \
                      'modifiers are more defensive while positive modifiers are more aggressive. \n' \
                      'Can be rerolled as many times as desired. The "Standard" mission type with \n' \
                      '"None" selected for enemy role presents the widest range of personality \n' \
                      'types while the other missions and roles narrow down the available \n' \
                      'personalities to better fit with the given mission and role.'
add_ship_tip = 'Type the identifier of any ship that you want to issue individual orders to.'
add_button_tip = 'Click to add above ship to list of ships in the enemy fleet.'
remove_button_tip = 'Click to remove above ship from list of ships in the enemy fleet, e.g., \n' \
                    'when a ship is destroyed or for some reason no longer requires orders.'
fleet_strength_tip = 'Selecting "Routed" will result in all ships being ordered \n' \
                     'to cease firing and attempt to flee the battle.'

# Drop Down Text
mission_type = ('Standard', 'Blockade', 'Ambush', 'Pursuit', 'Hit and Run')
enemy_role = ('None', 'Attacker', 'Defender')
ship_names = []
engagement_level = ('No Contact', 'Enemy Sighted', 'Engaging Enemy', 'Under Fire', 'Under Heavy Fire')
fleet_strength = ('Full Strength', 'Minimal Damage', 'Suffering Minor Losses', 'Suffering Heavy Losses', 'Routed')

# Order value variables
command_mod = 0
turn_mod = 0
turn_count = 1

sg.theme('DarkAmber')

column_layout = [[sg.Combo(mission_type, default_value='Standard', size=(12, 1), readonly=True, key='-Mission Type-'),
                 sg.Combo(enemy_role, default_value='None', size=(12, 1), readonly=True, key='-Mission Role-')],
                 [sg.Text('Enemy Command Profile')],
                 [sg.Button('Generate Profile', tooltip=command_profile_tip)],
                 [sg.HorizontalSeparator()],
                 [sg.Checkbox('Issue Individual Orders', enable_events=True, key='-Individual Orders-', default=True,
                              tooltip=individual_orders_tip)],
                 [sg.Input(size=(22, 1), key='-Ship Name-', do_not_clear=False, tooltip=add_ship_tip)],
                 [sg.Button('Add Ship', tooltip=add_button_tip), sg.Button('Remove Ship', tooltip=remove_button_tip)],
                 [sg.HorizontalSeparator()],
                 [sg.Text(f'Turn: {turn_count}', key='-Turn-')],
                 [sg.Text('Enemy Engagement Level')],
                 [sg.Combo(engagement_level, default_value='No Contact', size=(20, 1),
                           readonly=True, key='-Engagement-')],
                 [sg.Text('Enemy Fleet Strength')],
                 [sg.Combo(fleet_strength, default_value='Full Strength', size=(20, 1),
                           tooltip=fleet_strength_tip, readonly=True, key='-Strength-')],
                 [sg.Button('Generate Orders')]]

layout = [[sg.Text('Mission Type', pad=((16, 30), (0, 0))), sg.Text('Enemy Role'),
           sg.Text('Issued Orders Log', pad=((150, 0), (0, 0)))],
          [sg.Column(column_layout, expand_y=True), sg.Output(size=(50, 25), key='-Output-')],
          [sg.Button('Exit', pad=((575, 0), (0, 0)))]]

window = sg.Window('Space Fleet Combat Solo AI', layout)

while True:
    event, value = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break

    if event == 'Generate Profile':
        print('Enemy Command Profile')
        print('------------------------------------')
        command_mod = ai.generate_command_profile(value['-Mission Type-'], value['-Mission Role-'])
        print('')

    if event == 'Add Ship':
        if value['-Ship Name-'] == '':
            sg.popup_error('Please enter a ship identifier.')
        elif value['-Ship Name-'] in ship_names:
            sg.popup_error('This ship identifier has already been added.')
        else:
            ship_names.append(value['-Ship Name-'])
            print(f'Ship added to fleet: {ship_names[-1]}')
            print('')

    if event == 'Remove Ship':
        if value['-Ship Name-'] == '':
            sg.popup_error('Please enter a ship identifier.')
        elif value['-Ship Name-'] not in ship_names:
            sg.popup_error('This ship identifier has not been previously added.')
        else:
            ship_names.remove(value['-Ship Name-'])
            print(f'Ship removed from fleet: {value["-Ship Name-"]}')
            print('')

    if event == 'Generate Orders':
        turn_mod = ai.determine_turn_modifiers(command_mod, value['-Strength-'], value['-Engagement-'])
        print(f'Turn {turn_count} Orders')
        print('--------------------')

        if value['-Individual Orders-']:
            for ship in ship_names:
                ai.determine_ship_orders(turn_mod, value['-Strength-'], ship)
                print('')
        else:
            ai.determine_ship_orders(turn_mod, value['-Strength-'])
            print('')

        turn_count += 1
        window['-Turn-'].update(f'Turn: {turn_count}')

window.close()
