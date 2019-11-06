import logging
import os

LOG_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.path.pardir,
    'src',
    'geocoder.log'
))
logging.basicConfig(file=LOG_PATH, level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s")
