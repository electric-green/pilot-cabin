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
        self.direction = (1, 0)

    def get_uiable(self):
        raise Exception("UI_object must be inheritanced, it doesn't have it's own type")

class Spaceship(UI_object):
    def __init__(self, x=None, y=None):
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
        self.direction = random_choice(list(self.direcs.keys()))

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
        return ("PLA", self.x, self.y)

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
    ui_object.x += direction[0] * 1 #velocity
    ui_object.y += direction[1] * 1 #velocity
    if(ui_object.x < 0):
        ui_object.x = 0
    if(ui_object.y < 0):
        ui_object.y = 0
    if(ui_object.x > MAP_SIZE[0]):
        ui_object.x = MAP_SIZE[0]
    if(ui_object.y > MAP_SIZE[1]):
        ui_object.y


def com_read_line(com):
    print("CRL called")
    ans = ""
    while not ans.endswith("\r\n"):
        try:
            ans += com.read().decode('utf-8')
        except:
            pass
    return ans

def read_from_coms(coms):
    ans = []
    for com in coms:
        local = com_read_line(com)
        ans += list(json.loads(local).items())
    return dict(ans)


ui_objects = {'YOU': None, 'AST': [], 'PLA': None, 'PIR': [], 'BUL': [], 'MAP': {}}

def get_uiable_info(objects):
    ans = []
    for obj in ui_objects.values():
        if type(obj) is list:
            for ui_object in obj:
                ans.append(ui_object.get_uiable())
        elif type(obj) is dict:
            for ui_object in obj.values():
                ans.append(ui_object.get_uiable())
        else:
            ans.append(obj.get_uiable())
    return ans

def init():
    ans = []
    i = 0
    while True:
        try:
            ans.append(serial.Serial(f"/dev/ttyUSB{i}", 115200)) # TO BE TESTED?
        except:
            break
        i += 1
    if not len(ans):
        raise Exception("Couldn't load any ttyUSBs")

    ui_objects['YOU'] = Spaceship()
    for i in range(MAP_SIZE[0] * MAP_SIZE[1] // 20000): # TO BE TESTED
        ui_objects['AST'].append(Asteroid())
    for i in range(MAP_SIZE[0] * MAP_SIZE[1] // 20000): # TO BE TESTED
        ui_objects['PIR'].append(Pirate())
    ui_objects['PLA'] = Planet()
    for gamer in ['pilot', 'shooter', 'navigator']:
        ui_objects['MAP'][gamer] = Map(gamer)
    return ans

def main(coms):
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
        move(ui_objects['YOU'])

        removable_pirates = []
        removable_bullets = []
        for pidx, pirate in enumerate(ui_objects['PIR']):
            for bidx, bullet in enumerate(ui_objects['BUL']):
                if(pirate.x == bullet.x) and (pirate.y == bullet.y):
                    removable_pirates.append(pidx)
                    removable_bullets.append(bidx)
        removable_pirates = sorted(removable_pirates, reverse=True)
        removable_bullets = sorted(removable_bullets, reverse=True)
        for idx in removable_pirates:
            del ui_objects['PIR'][idx]
        for idx in removable_bullets:
            del ui_objects['BUL'][idx]


        temp = None
        data = read_from_coms(coms)
        for key, value in data.items():
            if key == 'pilot_joys_1':
                ui_objects['YOU'].direction = tuple(value)
            elif key == 'pilot_potent_1':
                temp = value

            elif key == 'navigator_joys_1':
                ui_objects['MAP']['navigator'].x, ui_objects['MAP'].y = value
            elif key == 'navigator_potent_1':
                ui_objects['MAP']['navigator'].scale = value

            elif key == 'shooter_potent_1':
                ui_objects['MAP']['shooter'].x = value
            elif key == 'shooter_potent_2':
                ui_objects['MAP']['shooter'].y = value
            elif key == 'shooter_butt_1':
                if(time() - last_shoot < 1):
                    continue
                coordinates = (ui_objects['YOU'].x, ui_objects['YOU'].y)
                coordinates = tuple(i + 1 for i in coordinates)
                shooter_map = ui_objects['MAP']['shooter']
                bullet = Bullet(*coordinates, (shooter_map.x, shooter_map.y))

            else:
                raise ValueError(f"Unknown JSON key {key} got from hardware")

        result = ui_main(get_uiable_info(ui_objects), *MAP_SIZE, temp)
        if(result == "SHOW_MUST_GO_ON"):
            continue
        elif(result == "CRASHED"):
            print("Game over. You losed!")
        else:
            print("Game over. You win!")
        return 0

if __name__ == "__main__":
    coms = init()
    main(coms)
    for com in coms:
        com.close()