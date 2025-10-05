

from labyrinth_game.constants import COMMANDS, ROOMS
from labyrinth_game.player_actions import (
    attempt_open_treasure,
    get_input,
    move_player,
    show_help,
    show_inventory,
    solve_puzzle,
    take_item,
    use_item,
)
from labyrinth_game.utils import describe_current_room, pseudo_random, trigger_trap

game_state = {
    'player_inventory': [],
    'current_room': 'entrance',
    'game_over': False,
    'steps_taken': 0
}

def process_command(game_state, command, commands):
    """Обрабатывает команды игрока"""
    parts = command.split()
    if not parts:
        return
    
    main_command = parts[0]
    argument = parts[1] if len(parts) > 1 else None
    
    match main_command:
        case "look" | "осмотреться":
            describe_current_room(game_state)
        case "inventory" | "инвентарь":
            show_inventory(game_state)
        case "help" | "помощь":
            show_help(commands)
        case "check" | "проверить":
            current_room = game_state['current_room']
            room_data = ROOMS[current_room]
            if room_data.get('has_trap', False):
                trap_chance = pseudo_random(game_state['steps_taken'], 100)
                if trap_chance < 60:
                    trigger_trap(game_state)
                else:
                    msg = "🔍 Вы аккуратно проверяете комнату и обезвреживаете ловушку!"
                    print(msg)
                    room_data['has_trap'] = False
            else:
                print("В этой комнате нет ловушек.")
        
        # Обработка движения по односложным командам
        case "go" | "иди" if argument:
            if argument in ["north", "south", "east", "west", 
                            "север", "юг", "восток", "запад"]:
                direction_map = {
                    "север": "north", "юг": "south",
                    "восток": "east", "запад": "west"
                }
                direction = direction_map.get(argument, argument)
                if move_player(direction, game_state):
                    describe_current_room(game_state)
            else:
                print("Неверное направление. Используйте: north, south, east, west")
        
        # Односложные команды движения
        case "north" | "south" | "east" | "west" | "север" | "юг" | "восток" | "запад":
            direction_map = {
                "север": "north", "юг": "south",
                "восток": "east", "запад": "west"
            }
            direction = direction_map.get(main_command, main_command)
            if move_player(direction, game_state):
                describe_current_room(game_state)
        
        case "take" | "взять" if argument:
            take_item(game_state, argument)
        case "use" | "использовать" if argument:
            use_item(game_state, argument)
        case "solve" | "решить":
            if game_state['current_room'] == 'treasure_room':
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case "quit" | "выход":
            print("Спасибо за игру! До свидания!")
            game_state['game_over'] = True
        case _:
            print("Неизвестная команда. Введите 'help' для списка команд.")


def main():
    
    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)
    
    while not game_state['game_over']:
        command = get_input("\nВведите команду: ")
        process_command(game_state, command, COMMANDS)  

if __name__ == "__main__":
    main()