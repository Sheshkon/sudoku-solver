import base64
import datetime
from copy import deepcopy
from time import sleep

import cv2
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

from main import extract_board_img, extract_cells, print_board
from settings import CHROME_DRIVER_PATH, SUDOKU_URL
from solver import solveSudoku

chrome_options = webdriver.ChromeOptions()

service = Service(CHROME_DRIVER_PATH)
browser = webdriver.Chrome(service=service, options=chrome_options)


class Difficulty:
    easy = 'easy'
    medium = 'medium'
    hard = 'hard'
    expert = 'expert'
    evil = 'evil'

lvl = Difficulty.evil
browser.get(SUDOKU_URL + '/' + lvl + '/')

def solve():
    canvas = browser.find_element(By.XPATH, '//canvas')
    canvas_base64 = browser.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)
    canvas_png = base64.b64decode(canvas_base64)

    filename = f'canvas{datetime.datetime.now().strftime(("%Y-%m-%d%H%M%S"))}.png'
    with open(filename, 'wb') as f:
        f.write(canvas_png)

    image = cv2.imread(filename)
    # image = extract_board_img(image)
    board = extract_cells(image)

    start_board = deepcopy(board)

    if (solveSudoku(board, 0, 0)):
        print_board(board)
    else:
        print('no solutions')

    main_body = browser.find_element(By.XPATH, "//html")

    x = int(canvas.location['x'])
    y = int(canvas.location['y'])
    width = int(canvas.size['width'])
    height = int(canvas.size['height'])

    ActionChains(browser)\
        .move_to_element_with_offset(canvas,-width/2, -height/2)\
        .click()\
        .release()\
        .perform()

    for i in range(9):
        for j in range(9):
            if i % 2 == 0:
                if start_board[i][j] == 0:
                    main_body.send_keys(eval(f'Keys.NUMPAD{board[i][j]}'))

                if j != 8:
                    main_body.send_keys(Keys.ARROW_RIGHT)

            else:
                if start_board[i][8 - j] == 0:
                    main_body.send_keys(eval(f'Keys.NUMPAD{board[i][8 - j]}'))

                if j != 8:
                    main_body.send_keys(Keys.LEFT)


        # for _ in range(8):
        #     main_body.send_keys(Keys.ARROW_LEFT)
        main_body.send_keys(Keys.ARROW_DOWN)


while True:
    i = input("Enter text (or Enter to quit): ")
    if not i:
        break

    if 'lvl:' in i:
        lvl = i.split(': ')[-1]
        browser.get(SUDOKU_URL + '/' + lvl + '/')

    elif i == 'solve':
        try:
            solve()
        except:
            print('something wrong, refreshing...')
            browser.refresh()
    elif i == "refresh":
        browser.refresh()

    print("Your input:", i)
print("While loop has exited")