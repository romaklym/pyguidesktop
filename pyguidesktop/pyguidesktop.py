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
from PIL import ImageGrab


class PyGUIDesktop(GUIDesktop):
    
    def __init__(self):
        super().__init__()
        
        if not os.path.exists(self.folder_path):
            print(f"Creating directory: {self.folder_path}")
            os.makedirs(self.folder_path)
        else:
            print(f"Directory already exists: {self.folder_path}")
        
        
    pyt.pytesseract.tesseract_cmd = 'C:/Users/klyms/Python_Projects/pyguidesktop/Tesseract-OCR/tesseract.exe'

    def find_text_and_click(self, text, click_type=gui.PRIMARY, click_duration=0.1, region=None, config=None):
        """
        Find the specified text on the screen using pytesseract and click in the middle of the found text.

        :param text: The text to search for.
        :param click_type: The type of mouse click to perform (PRIMARY or SECONDARY).
        :param click_duration: The duration of the mouse click.
        :param region: The region of the screen to search for the text (left, top, width, height).
        :return: True if text is found and clicked, False otherwise.
        """
        
        if config is None:
            config = config = r'--oem 3 --psm 6 -c tessedit_char_blacklist=$'
        
        if region is None:
            screen_resolution = gui.size()
            region = (0, 0, screen_resolution[0], screen_resolution[1])
            
        sleep(self.timeout)

        screenshot = self.make_screenshot(region=region)
        log_debug(f"Made screenshot: '{screenshot}'")
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
            log_debug(f"Failed to find word '{target_text}'")
            return False
    
    
    def find_image_on_screen_and_click(self, image_path=None, region=None):
        """
        Find the image on the screen using pytesseract and click in the middle of the found image.

        :param image_path: The path to the image to search for.
        :param region: The region of the screen to search for the image (left, top, width,height).
        """
        
        if image_path is None:
            assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')
            image_filename = 'test.png'
            image_path = os.path.join(assets_dir, image_filename)
            
            source_image = cv2.imread(image_path, cv2.COLOR_BGR2GRAY)
            log_debug(f"Source image for template matching {source_image}")
        else:
            source_image = cv2.imread(image_path, cv2.COLOR_BGR2GRAY)
            log_debug(f"Source image for template matching {source_image}")
            
        if region is None:
            screen_resolution = gui.size()
            region = (0, 0, screen_resolution[0], screen_resolution[1])
        
        screenshot = self.save_screenshot(screenshot_name="screenshot_template_matching", region=region)
        log_debug(f"Screenshot for template matching {screenshot}")
        screen_image = cv2.imread(screenshot, cv2.COLOR_BGR2GRAY)
        log_debug(f"Reading screenshot for template matching with cv2: {screen_image}")
        
        result = cv2.matchTemplate(screen_image, source_image, cv2.TM_CCORR_NORMED)
        log_debug(f"Match template function result: {result}")
        
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        h = source_image.shape[0]
        w = source_image.shape[1]
        
        a, b = max_loc
        c, d = max_loc[0] + w, max_loc[1] + h
        
        height = d - b
        width = c - a
        rectangle_size = width, height
        
        final_result = max_loc + rectangle_size
        log_debug(f"Final coordinates for found image at: {final_result}")
        
        x_click = final_result[0] + (rectangle_size[0] // 2)
        y_click = final_result[1] + (rectangle_size[1] // 2)
        
        gui.click(x_click, y_click, clicks=1, button=gui.PRIMARY, duration=0.1)
        
        cv2.rectangle(screen_image, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 255, 255), 2)
        cv2.imwrite(self.folder_path+"\\template_matched.png", screen_image)
        
        return log_debug(f"Found image at: ({x_click}, {y_click})")
    



                        
                    


                

