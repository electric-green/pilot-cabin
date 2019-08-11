import os
import time

import numpy as np

SIZE = (120, 30)
SYMBOLS = [' ', '_', '|', '/', '\\', 'O', '^', '>', 'v', '<', '*', '+', '-', '@']


def main(data, x, y):
        # rows, columns = os.popen('stty size', 'r').read().split()
        columns, rows = SIZE
        if int(rows) == SIZE[1] and int(columns) == SIZE[0]:
                arr = np.zeros((y, y)) #clear

                for elem in data:
                        elem_y = elem[2]
                        elem_x = elem[1]
                        if elem[0] == 'YOU':
                                if arr[elem_y, elem_x] != 0:
                                        if arr[elem.y, elem.x] == 10 or arr[elem_y, elem_x] == 5:
                                                return 'CRASHED'
                                        else:
                                                return 'LANDED'
                                YOU(arr, elem_y, elem_x, elem[3])
                        if elem[0] == 'AST':
                                AST(arr, elem_y, elem_x)
                        if elem[0] == 'PLA':
                                PLA(arr, elem_y, elem_x)
                        if elem[0] == 'PIR':
                                PIR(arr, elem_y, elem_x)
                        if elem[0] == 'BUL':
                                BUL(arr, elem_y, elem_x)
                
                print(symbols_update(arr)) #print
                return 'SHOW_MUST_GO_ON'
        else:
                raise Exception(f'The terminal size must be at least {SIZE[0]}x{SIZE[1]}')

def YOU(arr, y, x, angl):
        arr[y, x] = 6 + angl
        return arr

def AST(arr, y, x):
        ast = [' _____ ', '/ o   \\', '|   O |', '\_0___/']

        arr[y-2:y+2, x-4:x+3] = ast
        # arr[y, x] = 5
        return arr

def PLA(arr, y, x):
        arr[y-1, x] = 1
        arr[y, x] = 1
        arr[y, x-1] = 2
        arr[y, x+1] = 2
        return arr

def PIR(arr, y, x):
        arr[y, x] = 10
        return arr

def BUL(arr, y, x):
        arr[y, x] = 13
        return arr

def symbols_update(arr):
        txt_image = ''
        for y in range(int(SIZE[1])-2):
                for x in range(int(SIZE[0])):
                        txt_image += SYMBOLS[int(arr[y, x])]
                txt_image += '\n'
        return txt_image

if __name__ == "__main__":
        while True:
                for i in range(3):
                        test_data = [['YOU', 5, 6, i], ['AST', 5, 5], ['PLA', 6, 11], ['PIR', 8, 15], ['BUL', 9, 9]]
                        main(test_data)
                        time.sleep(4)