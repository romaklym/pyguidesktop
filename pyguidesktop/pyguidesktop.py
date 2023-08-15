from .guidesktop import GUIDesktop
import pyautogui as gui
import numpy as np
import sys, os, re
from datetime import datetime
import win32gui
import pytesseract as pyt
from pytesseract import Output
import cv2
from time import sleep
from PIL import Image
from .logger import log_debug


class PyGUIDesktop(GUIDesktop):
    def __init__(self):
        super().__init__()
        
    pyt.pytesseract.tesseract_cmd = 'C:/Users/klyms/Python_Projects/pyguidesktop/Tesseract-OCR/tesseract.exe'
    config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=qwertyuiopasdfghjklzxcvbnm QWERTYUIOPASDFGHJKLZXCVBNM'

    def find_text_and_click(self, text, click_type=gui.PRIMARY, click_duration=0.1, region=None, config=config):
        """
        Find the specified text on the screen using pytesseract and click in the middle of the found text.

        :param text: The text to search for.
        :param click_type: The type of mouse click to perform (PRIMARY or SECONDARY).
        :param click_duration: The duration of the mouse click.
        :param region: The region of the screen to search for the text (left, top, width, height).
        :return: True if text is found and clicked, False otherwise.
        """
        
        if region is None:
            screen_resolution = gui.size()
            region = (0, 0, screen_resolution[0], screen_resolution[1])
            
        sleep(self.timeout)

        screenshot = self.make_screenshot(region=region)
        gray_image = self.save_gray_image(screenshot=screenshot)
        thresh = self.thresholding(gray_image)
        
        sleep(self.timeout)
        
        found_text = pyt.image_to_string(thresh, config=config).lower()
        target_text = text.lower().replace(" ", "")
        log_debug(f"Found text '{found_text}' target text ({target_text})")
        
        sleep(self.timeout)

        if target_text in found_text:
            
            text_location = pyt.image_to_data(thresh, output_type=Output.DICT)
            log_debug(f"Text location '{text_location}')")
            
            for i, word in enumerate(text_location['text']):
                if word.lower() == target_text:
                    x_center = text_location['left'][i] + text_location['width'][i] // 2
                    y_center = text_location['top'][i] + text_location['height'][i] // 2
                    log_debug(f"Found '{target_text}' at center coordinates (x={x_center}, y={y_center})")
                    
                    screenshot_size = gui.screenshot(region=region)
                    screenshot_size = list(screenshot_size.size)
                    
                    if region is not None:
                        x_scale = screenshot_size[0] / region[2]
                        y_scale = screenshot_size[1] / region[3]

                        original_x = region[0] + x_center * x_scale
                        original_y = region[1] + y_center * y_scale
                        
                        log_debug(f"Coordinates '{original_x}', '{original_y}'")
                        gui.click(x=original_x, y=original_y, clicks=1, button=click_type, duration=click_duration)
                        
                    else:
                        log_debug(f"Coordinates '{x_center}', '{y_center}'")
                        gui.click(x=x_center, y=y_center, clicks=1, button=click_type, duration=click_duration)
        
        else:
            return False


        

