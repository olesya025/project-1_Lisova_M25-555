import math

from labyrinth_game.constants import DAMAGE_CHANCE, EVENT_PROBABILITY, ROOMS


def pseudo_random(seed, modulo):
    """Генерирует псевдослучайное число в диапазоне [0, modulo]"""
    value = math.sin(seed * 12.9898) * 43758.5453
    fractional = value - math.floor(value)
    return int(fractional * modulo)

def describe_current_room(game_state):
    """Выводит описание текущей комнаты."""
    current_room_id = game_state['current_room']
    room_data = ROOMS[current_room_id]
    room_name = current_room_id.replace('_', ' ').title()
    
    print(f"\n== {room_name.upper()} ==")
    print(room_data['description'])
    
    if room_data['items']:
        print("Заметные предметы:", ", ".join(room_data['items']))
    
    exits = list(room_data['exits'].keys())
    print("Выходы:", ", ".join(exits))
    
    if room_data['puzzle']:
        print("Кажется, здесь есть загадка (используйте команду solve).")
    
    if room_data.get('has_trap', False):
        print("⚠️ Вы чувствуете, что здесь может быть ловушка!")

def trigger_trap(game_state):
    """Активирует ловушку с негативными последствиями для игрока"""
    print("💥 Ловушка активирована! Пол стал дрожать...")
    
    inventory = game_state['player_inventory']
    if inventory:
        items_count = len(inventory)
        random_index = pseudo_random(game_state['steps_taken'], items_count)
        lost_item = inventory.pop(random_index)
        print(f"😱 В суматохе вы потеряли: {lost_item}!")
        return True
    else:
        damage_chance = pseudo_random(game_state['steps_taken'], 10)
        if damage_chance < DAMAGE_CHANCE:
            print("💀 Вы не смогли избежать ловушки и погибли... Игра окончена!")
            game_state['game_over'] = True
            return True
        else:
            print("🎯 Вам удалось увернуться от ловушки! "
                  "Вы уцелели, но это было близко.")
            return False

def random_event(game_state):
    """Обрабатывает случайные события при перемещении игрока"""
    event_occurrence = pseudo_random(game_state['steps_taken'], EVENT_PROBABILITY)
    if event_occurrence != 0:
        return False
    
    event_type = pseudo_random(game_state['steps_taken'] + 1, 3)
    
    if event_type == 0:
        current_room = game_state['current_room']
        room_data = ROOMS[current_room]
        print("💰 Вы заметили что-то блестящее на полу...")
        room_data['items'].append('coin')
        print("На полу лежит монетка! Она добавлена в комнату.")
        return True
    elif event_type == 1:
        print("👂 Вы слышите странный шорох из темноты...")
        if 'sword' in game_state['player_inventory']:
            print("⚔️ Вы достаёте меч, и шорох мгновенно стихает!")
        else:
            print("Вы замираете от страха, но шорох вскоре прекращается.")
        return True
    elif event_type == 2:
        current_room = game_state['current_room']
        if (current_room == 'trap_room' and 
            'torch' not in game_state['player_inventory']):
            print("🌑 В темноте вы не заметили ловушку под ногами!")
            return trigger_trap(game_state)
        else:
            print("🌀 Вы почувствовали лёгкий ветерок, но ничего не произошло.")
            return True
    
    return False