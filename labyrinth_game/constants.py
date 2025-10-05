"""Константы игры Лабиринт."""

ROOMS = {
    'entrance': {
        'description': 'Вы в темном входе лабиринта...',
        'exits': {'north': 'hall', 'east': 'trap_room'},
        'items': ['torch'],
        'puzzle': None,
        'has_trap': False
    },
    'hall': {
        'description': 'Большой зал с эхом. По центру стоит '
                       'пьедестал с запечатанным сундуком.',
        'exits': {'south': 'entrance', 'west': 'library', 'north': 'treasure_room'},
        'items': [],
        'puzzle': ('На пьедестале надпись: "Назовите число, которое идет '
                   'после девяти". Введите ответ цифрой или словом.', '10'),
        'has_trap': True
    },
    'trap_room': {
        'description': 'Комната с хитрой плиточной поломкой. '
                       'На стене видна надпись: "Осторожно --- ловушка".',
        'exits': {'west': 'entrance'},
        'items': ['rusty_key'],
        'puzzle': ('Чтобы пройти, назовите слово "шаг" три раза подряд '
                   '(введите "шаг шаг шаг")', 'шаг шаг шаг'),
        'has_trap': True
    },
    'library': {
        'description': 'Пыльная библиотека. На полках старые свитки. '
                       'Где-то здесь может быть ключ от сокровищницы.',
        'exits': {'east': 'hall', 'north': 'armory'},
        'items': [],
        'puzzle': ('В одном свитке загадка: "Что растет, когда его съедают?" '
                   '(ответ одно слово)', 'аппетит'),
        'has_trap': False
    },
    'armory': {
        'description': 'Старая оружейная комната. На стене висит меч, '
                       'рядом --- небольшая бронзовая шкатулка.',
        'exits': {'south': 'library'},
        'items': ['sword', 'bronze_box'],
        'puzzle': None,
        'has_trap': True
    },
    'treasure_room': {
        'description': 'Комната, на стене большой сундук. '
                       'Дверь заперта --- нужен особый ключ.',
        'exits': {'south': 'hall'},
        'items': ['treasure_chest'],
        'puzzle': ('Дверь защищена кодом. Введите код '
                   '(подсказка: это число пятикратного шага, 2*5= ? )', '10'),
        'has_trap': False
    }
}

COMMANDS = {
    "go <direction>": "перейти в направлении (north/south/east/west)",
    "look": "осмотреть текущую комнату", 
    "take <item>": "поднять предмет",
    "use <item>": "использовать предмет из инвентаря",
    "inventory": "показать инвентарь",
    "solve": "попытаться решить загадку в комнате",
    "check": "проверить комнату на ловушки", 
    "quit": "выйти из игры",
    "help": "показать это сообщение"
}

# Константы для замены "магических чисел"
TRAP_CHANCE = 40
EVENT_PROBABILITY = 10  
DAMAGE_CHANCE = 3
CHECK_TRAP_CHANCE = 60
RANDOM_MODULO = 100