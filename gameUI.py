import os
import time

from termcolor import colored
import numpy as np

SIZE = (120, 30)
SYMBOLS = [' ', '_', '|', '/', '\\', 'O', '^', '>', 'v', '<', '*', '+', '-', '@', 'o', 'O', '0', 'I']
SHIFT = 5


def main(data, size_x, size_y, TEMP):
        #rows, columns = os.popen('stty size', 'r').read().split()
        columns, rows = SIZE
        if int(rows) == SIZE[1] and int(columns) == SIZE[0]:
                arr = np.zeros((size_y+SHIFT*2, size_x+SHIFT*2)) # clear

                for elem in data:
                        elem_y = elem[2]
                        elem_x = elem[1]
                        if elem[0] == 'YOU':
                                myY = elem[2]
                                myX = elem[1]
                                if arr[elem_y, elem_x] != 0:
                                        if arr[elem.y, elem.x] == 17:
                                                return 'LANDED'
                                        else:
                                                return 'CRASHED'
                                YOU(arr, elem_y, elem_x, elem[3])
                        if elem[0] == 'AST':
                                AST(arr, elem_y, elem_x)
                        if elem[0] == 'PLA':
                                PLA(arr, elem_y, elem_x)
                        if elem[0] == 'PIR':
                                PIR(arr, elem_y, elem_x)
                        if elem[0] == 'BUL':
                                BUL(arr, elem_y, elem_x)
                
                print(symbols_update(arr, TEMP, myX, myY, size_x, size_y)) #print
                return 'SHOW_MUST_GO_ON'
        else:
                raise Exception(f'The terminal size must be at least {SIZE[0]}x{SIZE[1]}')

def YOU(arr, y, x, angl):
        arr[y+SHIFT, x+SHIFT] = 6 + angl
        return arr

def AST(arr, y, x):
        ast = [' _____ ', '/ o   \\', '|   O |', '\_0___/']
        ans = []
        for line in ast:
                l = []
                for elem in line:
                        l.append(SYMBOLS.index(elem))
                ans.append(l)
        arr[y-2+SHIFT:y+2+SHIFT, x-4+SHIFT:x+3+SHIFT] = ans
        return arr

def PLA(arr, y, x):
        arr[y-1+SHIFT, x+SHIFT] = 1
        arr[y+SHIFT, x+SHIFT] = 1
        arr[y+SHIFT, x-1+SHIFT] = 2
        arr[y+SHIFT, x+1+SHIFT] = 2
        return arr

def PIR(arr, y, x):
        arr[y+SHIFT, x+SHIFT] = 10
        return arr

def BUL(arr, y, x):
        arr[y+SHIFT, x+SHIFT] = 13
        return arr

def symbols_update(arr, temp, myX, myY, w, h):
        txt_image = ''
        cropped = arr[SHIFT:h+SHIFT, SHIFT:w+SHIFT]
        if myX >= SIZE[0]/2 and myX <= w-SIZE[0]:
                cropped = cropped[:, myX-SIZE[0]//2:myX+SIZE[0]//2]
        else:
                if myX >= SIZE[0]/2:
                        cropped = cropped[:, w-SIZE[0]:w]
                else:
                        cropped = cropped[:, 0:SIZE[0]]

        for y in range(int(SIZE[1])-3):
                for x in range(int(SIZE[0])):
                        if 2+2 == 5:
                                txt_image += colored(SYMBOLS[int(cropped[y, x])], color='red')
                        else:
                                txt_image += SYMBOLS[int(cropped[y, x])]
                txt_image += '\n'
        txt_image += f'Temperature inside: {str(temp)}' 
        txt_image +=  ' ' * (x-len(str(temp)))
        return txt_image

if __name__ == "__main__":
        while True:
                for i in range(250):
                        test_data = [['YOU', i*4, 5, 1], ['AST', 40, 5], ['PLA', 6, 11], ['PIR', 8, 15], ['BUL', 9, 9]]
                        main(test_data, 1000, 30, 1001)
                        time.sleep(1)
