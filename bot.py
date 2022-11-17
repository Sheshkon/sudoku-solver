import base64
import datetime
import os

import cv2
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from extractor import extract_board_img, extract_cells
from settings import CHROME_DRIVER_PATH, SUDOKU_URL
from solver import solveSudoku

lvl = 'evil'
chrome_options = webdriver.ChromeOptions()
service = Service(CHROME_DRIVER_PATH)
browser = webdriver.Chrome(service=service, options=chrome_options)
browser.get(SUDOKU_URL + '/' + lvl + '/')


def print_board(board):
    for i in range(9):
        if i in (3, 6):
            print(14 * '—— ')
        for j in range(9):
            if j in (3, 6):
                print('|', end='\t')
            print(board[i, j], end='\t')
        print()


def solve():
    canvas = browser.find_element(By.XPATH, '//canvas')
    canvas_base64 = browser.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)
    canvas_png = base64.b64decode(canvas_base64)
    main_body = browser.find_element(By.XPATH, "//html")
    width = int(canvas.size['width'])
    height = int(canvas.size['height'])

    if not os.path.isdir(f'logs/{datetime.datetime.now().strftime(("%Y-%m-%d"))}'):
        os.makedirs(f'logs/{datetime.datetime.now().strftime(("%Y-%m-%d"))}')

    filename = f'logs/{datetime.datetime.now().strftime(("%Y-%m-%d/%H-%M-%S"))}.png'
    with open(filename, 'wb') as f:
        f.write(canvas_png)

    image = cv2.imread(filename)
    image = extract_board_img(image)
    board = extract_cells(image)
    start_board = board.copy()

    if (solveSudoku(board, 0, 0)):
        print_board(board)
    else:
        print('no solutions')
        return

    ActionChains(browser)\
        .move_to_element_with_offset(canvas, -width/2, -height/2)\
        .click()\
        .release()\
        .perform()

    for i in range(9):
        for j in range(9):
            if i % 2 == 0:
                if start_board[i, j] == 0:
                    main_body.send_keys(eval(f'Keys.NUMPAD{board[i, j]}'))
                if j != 8:
                    main_body.send_keys(Keys.ARROW_RIGHT)
            else:
                if start_board[i, 8 - j] == 0:
                    main_body.send_keys(eval(f'Keys.NUMPAD{board[i, 8 - j]}'))
                if j != 8:
                    main_body.send_keys(Keys.LEFT)

        main_body.send_keys(Keys.ARROW_DOWN)


while True:
    # lvl: evil [easy, medium, hard, expert] - set sudoku lvl
    # solve - solve sudoku
    # refresh - refresh page
    # Enter - quite
    i = input("Enter command (or Enter to quit): ")
    if not i:
        break

    if 'lvl:' in i:
        lvl = i.split(': ')[-1]
        browser.get(SUDOKU_URL + '/' + lvl + '/')

    elif i == 'solve':
        try:
            solve()
        except Exception as e:
            print(e, '\nsomething wrong, refreshing...')
            browser.refresh()

    elif i == "refresh":
        browser.refresh()

    print("Your input:", i)
