import os

from dotenv import load_dotenv

load_dotenv()

SUDOKU_URL = 'https://sudoku.com'
CHROME_DRIVER_PATH = os.environ.get('CHROME_DRIVER_PATH')
