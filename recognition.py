import cv2
from keras.models import load_model
import numpy as np

model = load_model('digits.h5')


def find_digit(img):
    copy = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
    height, width = copy.shape
    # copy = cv2.resize(copy, (height * 5, width * 5), interpolation=cv2.INTER_AREA)
    blur = cv2.medianBlur(copy, 3)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 3)
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    if not len(cnts):
        return None

    cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

    x, y, w, h = cv2.boundingRect(cnt)

    if w < width / 3 and h < height / 3:
        return None

    copy = copy[y:y + h, x:x + w]

    return cv2.threshold(copy, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


def make_square(img):
    h, w = img.shape

    size_max = max(w, h)
    digit_square = 255 * np.ones(shape=[size_max, size_max], dtype=np.uint8)
    if w > h:
        y_pos = size_max // 2 - h // 2
        digit_square[y_pos:y_pos + h, 0:w] = img

    elif w < h:
        x_pos = size_max // 2 - w // 2
        digit_square[0:h, x_pos:x_pos + w] = img

    else:
        digit_square = img

    return digit_square


def add_boarders(img):
    img_arr = cv2.resize(img, (20, 20))
    sq = 255 * np.ones(shape=[28, 28], dtype=np.uint8)
    sq[4:24, 4:24] = img_arr
    return sq


def predict(img):
    img = find_digit(img)

    if img is None:
        return 0

    img = make_square(img)
    img = add_boarders(img)
    img_arr = img.reshape((1, 28, 28, 1))
    predict = model.predict([img_arr])
    prob = np.amax(predict)
    if prob < 0.85:
        return None

    result = int(np.argmax(predict, axis=1))

    return result
