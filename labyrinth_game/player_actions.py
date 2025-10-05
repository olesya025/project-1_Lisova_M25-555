from labyrinth_game.constants import RANDOM_MODULO, ROOMS, TRAP_CHANCE
from labyrinth_game.utils import pseudo_random, random_event, trigger_trap


def show_inventory(game_state):
    """Показывает инвентарь игрока."""
    inventory = game_state['player_inventory']
    if inventory:
        print("Ваш инвентарь:", ", ".join(inventory))
    else:
        print("Ваш инвентарь пуст.")

def get_input(prompt="> "):
    """Получает ввод от пользователя с обработкой ошибок."""
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def move_player(direction, game_state):
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]
    
    if direction in room_data['exits']:
        new_room = room_data['exits'][direction]
        
        # Используем временные переменные для коротких условий
        is_treasure = new_room == 'treasure_room'
        has_key = 'rusty_key' in game_state['player_inventory']
        
        if is_treasure and not has_key:
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return False
        elif is_treasure and has_key:
            # Строка 36:
            msg = "Вы используете найденный ключ, чтобы открыть " \
              "путь в комнату сокровищ."
            print(msg)
            game_state['current_room'] = new_room
            game_state['steps_taken'] += 1
            random_event(game_state)
            print(f"Вы переместились {direction}.")
            return True
        else:
            game_state['current_room'] = new_room
            game_state['steps_taken'] += 1
            random_event(game_state)
            print(f"Вы переместились {direction}.")
            return True
    else:
        print(f"Нельзя пойти {direction}.")
        return False

def take_item(game_state, item_name):
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]
    
    if item_name == 'treasure_chest':
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return False
        
    if item_name in room_data['items']:
        if room_data.get('has_trap', False):
            trap_chance = pseudo_random(game_state['steps_taken'], RANDOM_MODULO)
            if trap_chance < TRAP_CHANCE:
                print("🔄 При попытке взять предмет...")
                trigger_trap(game_state)
        
        game_state['player_inventory'].append(item_name)
        room_data['items'].remove(item_name)
        print(f"Вы подняли: {item_name}")
        return True
    else:
        print("Такого предмета здесь нет.")
        return False

def use_item(game_state, item_name):
    """Использует предмет из инвентаря"""
    inventory = game_state['player_inventory']
    
    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return False
        
    match item_name:
        case "torch":
            print("Вы зажигаете факел. Стало светлее!")
            return True
        case "sword":
            print("Вы размахиваете мечом. Чувствуете себя увереннее!")
            return True
        case "bronze box":
            print("Вы открываете бронзовую шкатулку...")
            if "rusty_key" not in inventory:
                inventory.append("rusty_key")
                print("Внутри вы нашли rusty_key!")
            else:
                print("Шкатулка пуста.")
            return True
        case "treasure_chest":
            return attempt_open_treasure(game_state)
        case "mysterious_herb":
            print("Вы съедаете таинственную траву. Чувствуете прилив сил!")
            inventory.remove(item_name)
            return True
        case "coin":
            print("Вы подбрасываете монетку. Она блестит на свету.")
            return True
        case _:
            print("Вы не знаете, как использовать этот предмет.")
            return False

def solve_puzzle(game_state):
    """Решает загадку в текущей комнате"""
    current_room_id = game_state['current_room']
    room_data = ROOMS[current_room_id]
    
    if current_room_id == 'treasure_room':
        return attempt_open_treasure(game_state)
        
    if not room_data['puzzle']:
        print("Загадок здесь нет.")
        return False
        
    question, correct_answer = room_data['puzzle']
    print(f"Загадка: {question}")
    user_answer = input("Ваш ответ: ").strip().lower()

    def check_number_after_nine(answer):
        number_words = {
            'десять': 10, 'ten': 10, '10': 10,
            'одиннадцать': 11, 'eleven': 11, '11': 11,
            'двенадцать': 12, 'twelve': 12, '12': 12,
        }
        if answer in number_words:
            number = number_words[answer]
            return number > 9
        try:
            number = int(answer)
            return number > 9
        except ValueError:
            return False

    is_correct = False
    if current_room_id == 'hall':
        is_correct = check_number_after_nine(user_answer)
    else:
        is_correct = user_answer == correct_answer

    if is_correct:
        print("Правильно! Загадка решена.")
        room_data['puzzle'] = None
        
        if current_room_id == 'hall':
            game_state['player_inventory'].append('treasure_key')
            print("Вы получили treasure_key!")
        elif current_room_id == 'trap_room':
            game_state['player_inventory'].append('health_potion')
            print("Вы получили health_potion!")
        elif current_room_id == 'library':
            game_state['player_inventory'].append('rusty_key')
            print("Вы получили rusty_key!")
        return True
    else:
        print("Неверно. Попробуйте снова.")
        return False

def show_help(commands):
    """Показывает список доступных команд"""
    print("\nДоступные команды:")
    for cmd, desc in commands.items():
        print(f" {cmd:<16} - {desc}")

def attempt_open_treasure(game_state):
    """Пытается открыть сундук с сокровищами"""
    current_room_id = game_state['current_room']
    room_data = ROOMS[current_room_id]
    
    if 'treasure_chest' not in room_data['items']:
        print("Сундук уже открыт или отсутствует.")
        return False
        
    inventory = game_state['player_inventory']
    if 'treasure_key' in inventory or 'rusty_key' in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room_data['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return True
        
    response = input("Сундук заперт. Ввести код? (да/нет): ").strip().lower()
    if response == 'да':
        if room_data['puzzle']:
            question, correct_answer = room_data['puzzle']
            user_code = input(f"{question}: ").strip()
            if user_code == correct_answer:
                print("Замок щёлкает! Сундук открыт!")
                room_data['items'].remove('treasure_chest')
                print("В сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
                return True
            else:
                print("Неверный код.")
                return False
        else:
            print("Здесь нет загадки для ввода кода.")
            return False
    else:
        print("Вы отступаете от сундука.")
        return False