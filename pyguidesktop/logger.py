import os
import logging
import traceback
from datetime import datetime


log_folder = os.path.join(os.getcwd(), "logs")
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

log_file = os.path.join(log_folder, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=log_file,
    filemode='w'
)

def log_debug(message):
    logging.debug(message)
    
def log_error(exception):
    exception_info = traceback.format_exc()
    logging.error(f"An error occurred:\n{exception_info}")
