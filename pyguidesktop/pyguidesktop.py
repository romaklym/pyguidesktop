from pyguidesktop.guidesktop import GUIDesktop
import pyautogui as gui
import os
import pytesseract as pyt
from pytesseract import Output
import cv2
from time import sleep
from pyguidesktop.logger import log_debug


class PyGUIDesktop(GUIDesktop):
    
    def __init__(self):
        super().__init__()
        
        if not os.path.exists(self.folder_path):
            print(f"Creating directory: {self.folder_path}")
            os.makedirs(self.folder_path)
        else:
            print(f"Directory already exists: {self.folder_path}")
        
        
    script_path = os.path.dirname(os.path.abspath(__file__))
    project_folder = os.path.dirname(script_path)
    tesseract_folder = os.path.join(project_folder, 'Tesseract-OCR')

    # Set the Tesseract executable path
    pyt.pytesseract.tesseract_cmd = os.path.join(tesseract_folder, 'tesseract.exe')
    log_debug(f"TESSERACT_PATH: {tesseract_folder}")

    def find_text_coordinates(self, text, click_type=gui.PRIMARY, click_duration=0.1, region=None, config=None, preprocess_image=False):
        """
        Finds all coordinates of the text we are looking for, if its one word returns the middle coordinates of that word, if two or 
        more words, calculates the middle of those words and returns it

        :param text: The text to search for.
        :param click_type: The type of mouse click to perform (PRIMARY or SECONDARY).
        :param click_duration: The duration of the mouse click.
        :param region: The region of the screen to search for the text (left, top, width, height).
        :return: True if text is found and clicked, False otherwise.
        """
        resize_factor = 2
        
        if config is None:
            config = config = r'--oem 3 --psm 6 -c tessedit_char_blacklist=$'
        
        if region is None:
            screen_resolution = gui.size()
            region = (0, 0, screen_resolution[0], screen_resolution[1])
            
        sleep(self.timeout)

        if not preprocess_image:
            screenshot = self.make_screenshot(region=region)
            log_debug(f"Made screenshot: '{screenshot}'")
        else:
            screenshot = self.save_screenshot(region=region)
            screenshot = self.process_image(screenshot, resize_factor=resize_factor)
            
        gray_image = self.save_gray_image(screenshot=screenshot)
        thresh = self.thresholding(gray_image)
        
        sleep(self.timeout)
        
        found_text = pyt.image_to_string(thresh, config=config).lower()
        target_text = text.lower()
        log_debug(f"Found text '{found_text}' target text ({target_text}")
        
        sleep(self.timeout)

        if target_text in found_text:
            
            target_text = text.lower().split()
            text_location = pyt.image_to_data(thresh, output_type=Output.DICT)
            log_debug(f"Text location {text_location['text']}")

            matching_sequences = []
            for idx, word in enumerate(text_location['text']):
                
                lower_word = word.lower()

                if lower_word == target_text[0]:
                    matching_indices = [idx]

                    for i in range(1, len(target_text)):
                        next_idx = idx + i
                        if next_idx < len(text_location['text']) and text_location['text'][next_idx].lower() == target_text[i]:
                            matching_indices.append(next_idx)
                        else:
                            break

                    if len(matching_indices) == len(target_text):
                        matching_sequences.append(matching_indices)
                        
            log_debug(f"Whole {matching_sequences} list of a found words")
            coordinates_of_all_found_text = []
            
            for loc in matching_sequences:
                center_of_the_target = []
                for _ in loc:
                    log_debug(f"Location {_} of a found word")
                    log_debug(f"Text location {text_location}")
                    x_center = text_location['left'][_] + text_location['width'][_] // 2
                    y_center = text_location['top'][_] + text_location['height'][_] // 2
                    log_debug(f"Found text at center coordinates (x={x_center}, y={y_center})")
                    
                    screenshot_size = gui.screenshot(region=region)
                    screenshot_size = list(screenshot_size.size)
                    
                    if region is not None:
                        x_scale = screenshot_size[0] / region[2]
                        y_scale = screenshot_size[1] / region[3]

                        original_x = region[0] + x_center * x_scale
                        original_y = region[1] + y_center * y_scale
                        
                        log_debug(f"Coordinates '{original_x}', '{original_y}'")
                        center_of_the_target.append([original_x, original_y])
                        
                    else:
                        log_debug(f"Coordinates '{x_center}', '{y_center}'")
                        center_of_the_target.append([original_x, original_y])
                        
                coordinates_of_all_found_text.append(center_of_the_target)
            
            coordinates = []
            for sublist in coordinates_of_all_found_text:
                middle_x = (sublist[-1][0] - sublist[0][0]) / 2 + sublist[0][0]
                
                middle_y = sublist[0][1]
                coordinates.append([middle_x, middle_y])
                
            log_debug(f"All found coordinates {coordinates}")
            return coordinates
            
        else:
            log_debug(f"Failed to find word/words '{target_text}'")
            return False
    
    def find_text_and_click(self, text, click_type=gui.PRIMARY, click_duration=0.1, region=None, config=None, preprocess_image=False):
        """
        Find the specified text on the screen using pytesseract and click in the middle of the found text.

        :param text: The text to search for.
        :param click_type: The type of mouse click to perform (PRIMARY or SECONDARY).
        :param click_duration: The duration of the mouse click.
        :param region: The region of the screen to search for the text (left, top, width, height).
        :return: True if text is found and clicked, False otherwise.
        """
        resize_factor = 2
        
        if config is None:
            config = config = r'--oem 3 --psm 6 -c tessedit_char_blacklist=$'
        
        if region is None:
            screen_resolution = gui.size()
            region = (0, 0, screen_resolution[0], screen_resolution[1])
            
        sleep(self.timeout)

        if not preprocess_image:
            screenshot = self.make_screenshot(region=region)
            log_debug(f"Made screenshot: '{screenshot}'")
        else:
            screenshot = self.save_screenshot(region=region)
            screenshot = self.process_image(screenshot, resize_factor=resize_factor)
            
        gray_image = self.save_gray_image(screenshot=screenshot)
        thresh = self.thresholding(gray_image)
        
        sleep(self.timeout)
        
        found_text = pyt.image_to_string(thresh, config=config).lower()
        target_text = text.lower()
        log_debug(f"Found text '{found_text}' target text ({target_text}")
        
        sleep(self.timeout)

        if target_text in found_text:
            
            target_text = text.lower().split()
            text_location = pyt.image_to_data(thresh, output_type=Output.DICT)
            log_debug(f"Text location {text_location['text']}")

            matching_sequences = []
            for idx, word in enumerate(text_location['text']):
                
                lower_word = word.lower()

                if lower_word == target_text[0]:
                    matching_indices = [idx]

                    for i in range(1, len(target_text)):
                        next_idx = idx + i
                        if next_idx < len(text_location['text']) and text_location['text'][next_idx].lower() == target_text[i]:
                            matching_indices.append(next_idx)
                        else:
                            break

                    if len(matching_indices) == len(target_text):
                        matching_sequences.append(matching_indices)
                        
            log_debug(f"Whole {matching_sequences} list of a found words")
            center_of_the_target = []
            # Checking only first matched result
            for _ in matching_sequences[0]:
            # for _ in loc:
                log_debug(f"Location {_} of a found word")
                log_debug(f"Text location {text_location}")
                x_center = text_location['left'][_] + text_location['width'][_] // 2
                y_center = text_location['top'][_] + text_location['height'][_] // 2
                log_debug(f"Found text at center coordinates (x={x_center}, y={y_center})")
                
                screenshot_size = gui.screenshot(region=region)
                screenshot_size = list(screenshot_size.size)
                
                if region is not None:
                    x_scale = screenshot_size[0] / region[2]
                    y_scale = screenshot_size[1] / region[3]

                    original_x = region[0] + x_center * x_scale
                    original_y = region[1] + y_center * y_scale
                    
                    log_debug(f"Coordinates '{original_x}', '{original_y}'")
                    center_of_the_target.append([original_x, original_y])
                    
                else:
                    log_debug(f"Coordinates '{x_center}', '{y_center}'")
                    center_of_the_target.append([original_x, original_y])
                
            middle_x = (center_of_the_target[-1][0] - center_of_the_target[0][0]) / 2 + center_of_the_target[0][0]
            middle_y = center_of_the_target[0][1]

            gui.click(x=middle_x, y=middle_y, clicks=1, button=click_type, duration=click_duration)
                
            log_debug(f"Middle coordinates clicked: {middle_x}, {middle_y}")
            return True
            
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


                        
                    


                

