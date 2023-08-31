import os
import logging
import traceback
from datetime import datetime

package_dir = os.path.dirname(os.path.abspath(__file__))
main_folder = os.path.dirname(package_dir)

screenshots_dir = os.path.join(main_folder, "logs")

os.makedirs(screenshots_dir, exist_ok=True)

now = datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
folder_path = os.path.join(screenshots_dir, timestamp)
os.makedirs(folder_path, exist_ok=True)

log_file = os.path.join(folder_path, f"{timestamp}.log")

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
    
TIME_DIFF_SECONDS = 10

def is_same_folder(timestamp_folder):
    now = datetime.now()
    folder_time = datetime.strptime(timestamp_folder, "%Y-%m-%d_%H-%M-%S")
    time_difference = now - folder_time
    return abs(time_difference.total_seconds()) <= TIME_DIFF_SECONDS
