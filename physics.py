import serial
import json
from random import randint
from random import choice as random_choice
from time import time

from gameUI import main as ui_main


MAP_SIZE = (1000, 200)


class UI_object:
    direcs = {(0, -1): 0, (1, 0): 1, (0, 1): 2, (-1, 0): 3, (1, -1): 1, (1, 1): 1, (-1, 1): 3, (-1, -1): 3}
    def __init__(self):
        self.x = None
        self.y = None
        self.velocity = 0
        self.direction = (1, 0)

    def get_uiable(self):
        raise Exception("UI_object must be inheritanced, it doesn't have it's own type")

class Spaceship(UI_object):
    def __init__(self, x, y):
        UI_object.__init__(self)
        self.x = 0
        self.y = 0
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y

    def get_uiable(self):
        return ("YOU", self.x, self.y, self.direcs[self.direction])

class Asteroid(UI_object):
    def __init__(self, x=None, y=None):
        UI_object.__init__(self)
        self.x, self.y = (randint(0, i) for i in MAP_SIZE)
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        self.direction = random_choice(self.direcs.keys())
        self.velocity = 1 # TO BE TESTED

    def get_uiable(self):
        return ("AST", self.x, self.y)

class Planet(UI_object):
    def __init__(self, x=None, y=None):
        UI_object.__init__(self)
        self.x = MAP_SIZE[0] - 5 # TO BE TESTED
        self.y = MAP_SIZE[1] - 5 # TO BE TESTED
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y

    def get_uiable(self):
        return ("PLA", self.x)

class Pirate(UI_object):
    def __init__(self, x=None, y=None):
        UI_object.__init__(self)
        self.x, self.y = (randint(0, i) for i in MAP_SIZE)
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        self.direction = None

    def get_uiable(self):
        return ("PIR", self.x, self.y)

class Bullet(UI_object):
    def __init__(self, x, y, direction):
        UI_object.__init__(self)
        self.x = x
        self.y = y
        self.velocity = 9 # TO BE TESTED
        self.direction = direction

    def get_uiable(self):
        return ("BUL", self.x, self.y)

class Map(UI_object):
    def __init__(self, gamer):
        # DO NOT CALL UI_object.__init__(self) HERE!!!
        self.x, self.y = (i // 2 for i in MAP_SIZE)
        self.scale = 0
        self.gamer = gamer

    def get_uiable(self):
        return ("MAP", self.gamer, self.x, self.y, self.scale)

def move(ui_object):
    direction = ui_object.direction
    velocity = ui_object.velocity
    ui_object.x += direction[0] * velocity
    ui_object.y += direction[1] * velocity


def com_read_line(com):
    previous = None
    while True:
        ans = ""
        while not ans.endswith("\r\n"):
            try:
                ans += com.read().decode('utf-8')
            except serial.SerialTimeoutException:
                if previous is not None:
                    return previous
        previous = ans


ui_objects = {'YOU': None, 'AST': [], 'PLA': None, 'PIR': [], 'BUL': [], 'MAP': {}}

def init():
    com = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.01) # TO BE TESTED?
    ui_objects['YOU'] = Spaceship()
    for i in range(MAP_SIZE[0] * MAP_SIZE[1] // 2000): # TO BE TESTED
        ui_objects['AST'].append(Asteroid())
    for i in range(MAP_SIZE[0] * MAP_SIZE[1] // 2000): # TO BE TESTED
        ui_objects['PIR'].append(Pirate())
    ui_objects['PLA'] = Planet()
    for gamer in ['pilot', 'shooter', 'navigator']:
        ui_objects['MAP'][gamer] = Map()
    return com

def main(com):
    last_shoot = time() # shoots are allowed not more often than one time per second

    while True:
        for pirate in ui_objects['PIR']:
            sign = lambda x: -1 if x < 0 else (0 if x == 0 else 1)
            direction = []
            direction.append(sign(ui_objects['YOU'].x - pirate.x))
            direction.append(sign(ui_objects['YOU'].y - pirate.y))
            pirate.direction = tuple(direction)

        for obj in ui_objects['AST'] + ui_objects['BUL'] + ui_objects['PIR']:
            move(obj)


        line = com_read_line()
        data = json.loads(line)
        for key, value in data.items():
            if key == 'pilot_joys_1':
                ui_objects['YOU'].direction = tuple(value)
            elif key == 'pilot_potent_1':
                ui_objects['YOU'].velocity = value // 100

            elif key == 'navigator_joys_1':
                ui_objects['MAP']['navigator'].x, ui_objects['MAP'].y = value
            elif key == 'navigator_potent_1':
                ui_objects['MAP']['navigator'].scale = value

            elif key == 'shooter_potent_1':
                ui_objects['MAP']['shooter'].x = value
            elif key == 'shooter_potent_2':
                ui_objects['MAP']['shooter'].y = value
            elif key == 'shooter_button_1':
                coordinates = (ui_objects['YOU'].x, ui_objects['YOU'].y)
                coordinates = tuple(i + 1 for i in coordinates)
                bullet = Bullet(*coordinates, ui_objects['YOU'].direction)

            else:
                raise ValueError("Unknown JSON key got from hardware")

if __name__ == "__main__":
    com = init()
    main(com)
    com.close()