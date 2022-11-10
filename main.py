import math

import cv2
from recognition import predict

from solver import solveSudoku


def extract_board_img(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 3)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 3)
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
    x, y, w, h = cv2.boundingRect(cnt)
    return image[y:y + h, x:x + w]


def extract_cells(img):
    width = math.floor(img.shape[1] / 9)
    delta = math.floor(width/7)
    matrix_board = list()

    for i in range(9):
        row = list()
        for j in range(9):
            cell = img[i*width+delta: i*width + width-delta, j*width+delta: j*width + width-delta]
            # cv2.imwrite(f'tests/cropped/test{i}_{j}.jpg', cell)
            row.append(predict(cell))
        matrix_board.append(row)
    return matrix_board


def print_board(board):
    for i in range(9):
        if i in (3, 6):
            print(14 * '—— ')
        for j in range(9):
            if j in (3, 6):
                print('|', end='\t')
            print(board[i][j], end='\t')
        print()



