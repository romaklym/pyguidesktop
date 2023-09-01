import pyautogui as gui
import numpy as np
import sys, os
from datetime import datetime
import win32gui
from time import sleep
import time
import cv2
from logger import log_debug, is_same_folder
import subprocess
import winreg
import pytesseract as pyt
from pytesseract import Output
import input as inp

class PyGUIDesktop:
    def __init__(self):
            
        package_dir = os.path.dirname(os.path.abspath(__file__))
        main_folder = os.path.dirname(package_dir)
        now = datetime.now()
        self.timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        self.folder_path = os.path.join(main_folder, "logs", self.timestamp)

        if not is_same_folder(self.timestamp):
            os.makedirs(self.folder_path, exist_ok=True)
        self.BINARY_THRESHOLD = 120
    
    default_screenshot = "screenshot"
    region = (0, 0, gui.size()[0], gui.size()[1])
    timeout = 0.5
    screen_resolution = list(gui.size())
    resize = 2
    
    script_path = os.path.dirname(os.path.abspath(__file__))
    project_folder = os.path.dirname(script_path)
    tesseract_folder = os.path.join(project_folder, 'Tesseract-OCR')
    
    pyt.pytesseract.tesseract_cmd = os.path.join(tesseract_folder, 'tesseract.exe')
    log_debug(f"TESSERACT_PATH: {tesseract_folder}")
    
    def get_app_path(self, app_name):
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths") as key:
                app_key_path = winreg.QueryValue(key, app_name)
                return app_key_path
        except FileNotFoundError:
            print(f"Application '{app_name}' not found in the registry.")
            return None

    def launch_app(self, app_path):
        if not app_path:
            raise ValueError("App path is empty or None.")
        
        try:
            subprocess.Popen(app_path)
            print(f"Launched app: {app_path}")
        except Exception as e:
            print(f"Error launching app: {e}")

    def screen_resolution(self):
        """
            Returns Resolution of the screen as a Tuple.
            Format: x, y, width, height
            x & y by default both 0
        """
        screen_resolution = gui.size()
        log_debug(f"Screen resolution is: {screen_resolution}")
        screen_resolution = list(screen_resolution)

        region = (0, 0, screen_resolution[0], screen_resolution[1])
        log_debug(f"Region is: {region}")

        return region

    def mouse_position(self, input=False):
        """
            Returns Position of the cursor on the screen as Tuple.
            Format: x, y
        """
        if not input:
            position = gui.position()
            log_debug(f"Mouse position at: {position}")
        else:
            position = inp.position()
            log_debug(f"Mouse position at: {position}")

        return position
    
    def coordinates_on_screen(self, x=0, y=0):
        """
            Returns Boolean if coordinates located on the screen.
            Format: True, False
        """

        coordinates_on_screen = gui.onScreen(x=x, y=y)
        log_debug(f"Coordinates present on screen: {coordinates_on_screen}")

        return coordinates_on_screen
    
    def move_to(self, x=0, y=0, timeout=None, input=False, duration=0.1, tween=gui.linear, pause=True):
        """
            Moves cursor to location on the screen specified as arguments.
            Format: True, False
        """
        if not input:
            gui.moveTo(x=x, y=y, duration=duration, tween=tween, pause=pause)
            sleep(timeout)
            success = gui.position() == (x, y)
        else:
            inp.moveTo(x=x, y=y, duration=duration, tween=tween, pause=pause)
            sleep(timeout)
            success = inp.position() == (x, y)
        
        log_debug(f"{'Successfully' if success else 'Failed to'} move to {x}, {y}")
        return success

    def move_mouse(self, x=None, y=None, duration=0):
        """
            Moves mouse by specified set of pixels provided by an arguments.
            Format: None
        """

        gui.move(x=x, y=y, duration=duration)
        log_debug(f"Moved mouse by x pixels: {x}, and y pixels: {y}")

        return None
    
    def drag_to(self, x=0, y=0, duration=0, button=gui.PRIMARY, pause=True):
        """
            Drags mouse to specified location on the screen.
            Format: None
        """
        
        gui.dragTo(x=x, y=y, duration=duration, button=button, pause=pause)
        log_debug(f"Drags mouse to location: x: {x}, y: {y}")

        return None
    
    def drag_mouse(self, x=None, y=None, duration=0.1, button=gui.PRIMARY):
        """
            Drags mouse by specified numbers of pixels provided by arguments.
            Format: None
        """

        gui.drag(x=x, y=y, duration=duration, button=button)
        log_debug(f"Drags mouse by x pixels: {x}, and y pixels: {y}")

        return None
    
    def key_down(self, key, input=False, pause=True):
        """
        Presses key down.

        """
        if key is None:
            raise ValueError("Cannot leave key argument empty")
        
        if not input:
            gui.keyDown(key=key, pause=pause)
            log_debug(f"Pressed this button: {key}")
        else:
            inp.keyDown(key=key, pause=pause)
            log_debug(f"Pressed this button: {key}")
            
        return True
    
    def key_up(self, key, input=False, pause=True):
        """
        Presses key up.

        """
        if key is None:
            raise ValueError("Cannot leave key argument empty")
        
        if not input:
            gui.keyUp(key=key, pause=pause)
            log_debug(f"Pressed this button: {key}")
        else:
            inp.keyUp(key=key, pause=pause)
            log_debug(f"Pressed this button: {key}")
            
        return True
    
    def press(self, key, input=False, pause=True):
        """
        Presses key down and releases.

        """
        if key is None:
            raise ValueError("Cannot leave key argument empty")
        
        if not input:
            gui.press(key=key, pause=pause)
            log_debug(f"Pressed this button: {key}")
        else:
            inp.press(key=key, pause=pause)
            log_debug(f"Pressed this button: {key}")
            
        return True
    
    def click(self, clicks=1, interval=0, input=False, button=gui.PRIMARY, duration=0, tween=gui.linear, pause=True):
        """
            Mouse click.
            Format: None
        """
        if not input:
            gui.click(clicks=clicks, interval=interval, button=button,
                    duration=duration, tween=tween, pause=pause)
            log_debug(f"Clicks this many times: {clicks}, with this button: {button}")
        else:
            inp.click(clicks=clicks, interval=interval, button=button,
                    duration=duration, tween=tween, pause=pause)
            log_debug(f"Clicks this many times: {clicks}, with this button: {button}")
            
        return None
    
    def double_click(self, x=None, y=None, interval=0, input=False, button=gui.LEFT, duration=0, tween=gui.linear, pause=True):
        """
            Double Mouse click.
            Format: None
        """

        if not input:
            gui.doubleClick(x=x, y=y, interval=interval, button=button,
                        duration=duration, tween=tween, pause=pause)
            log_debug(f"Double clicks at x: {x}, y: {y} with this button: {button}")
        else:
            inp.doubleClick(x=x, y=y, interval=interval, button=button,
                        duration=duration, tween=tween, pause=pause)
            log_debug(f"Double clicks at x: {x}, y: {y} with this button: {button}")

        return None
    
    def mouse_down(self, x=None, y=None, button=gui.PRIMARY, duration=0, tween=gui.linear, pause=True):
        """
            Presses specified mouse button down, without releasing it.
            Format: None
        """

        gui.mouseDown(x=x, y=y, button=button, duration=duration,
                      tween=tween, pause=pause)
        log_debug(f"Pressed mouse down at x: {x}, y: {y} with this button: {button}")

        return None
    
    def mouse_up(self, x=None, y=None, button=gui.PRIMARY, duration=0, tween=gui.linear, pause=True):
        """
            Releases specified button up, if it was previously pressed down by mouse_down() function.
            Format: None
        """

        gui.mouseUp(x=x, y=y, button=button, duration=duration,
                    tween=tween, pause=pause)
        log_debug(f"Released mouse at x: {x}, y: {y} with this button: {button}")

        return None

    def mouse_scroll(self, clicks=0, x=None, y=None, pause=True):
        """
            Scrolls mouse wheel down by set amount of clicks, at the specified location.
            Format: None
        """

        gui.scroll(clicks=clicks, x=x, y=y, pause=pause)
        log_debug(f"Scrolled mouse this many clicks: {clicks}")

        return None

    def make_screenshot(self, screenshot_name=default_screenshot, region=region, resize=resize):
        """
        Creates a screenshot and saves it in a new folder with the current date and time as the name.

        :param screenshot_name: Name of the screenshot file (without extension).
        :param region: The region of the screen to capture (left, top, width, height).
        :return: The captured screenshot object.
        """

        if region is None:
            screen_resolution = gui.size()
            region = (0, 0, int(screen_resolution[0]), int(screen_resolution[1]))

        screenshot_path = os.path.join(self.folder_path, f"{screenshot_name}.png")
        log_debug(f"Screenshot path : {screenshot_path}")
        screenshot = gui.screenshot(region=region)
        
        sleep(self.timeout)
        screenshot.save(screenshot_path)

        log_debug(f"Screenshots saved in folder: {self.folder_path}, with size: {list(screenshot.size)}")

        return screenshot
    
    def save_screenshot(self, screenshot_name=default_screenshot, region=region, resize=resize):
        """
        Creates a screenshot and saves it in a new folder with the current date and time as the name, but 
        returns a path to that folder with a name of the image.

        :param screenshot_name: Name of the screenshot file (without extension).
        :param region: The region of the screen to capture (left, top, width, height).
        :return: The captured screenshot object.
        """

        if region is None:
            screen_resolution = gui.size()
            region = (0, 0, int(screen_resolution[0]), int(screen_resolution[1]))

        screenshot_path = os.path.join(self.folder_path, f"{screenshot_name}.png")
        log_debug(f"Screenshot path : {screenshot_path}")
        screenshot = gui.screenshot(region=region)
        
        sleep(self.timeout)
        screenshot.save(screenshot_path)

        log_debug(f"Screenshots saved in folder: {self.folder_path}, with size: {list(screenshot.size)}")

        return screenshot_path
    
    def upload_image(self, image, screenshot_name=default_screenshot):
        """
        Saves images that already exist to runs images folder with the current date and time as the name.
        """
        
        screenshot_path = os.path.join(self.folder_path, f"{screenshot_name}.png")
        log_debug(f"Screenshot path : {screenshot_path}")
        
        uploaded_image = cv2.imwrite(screenshot_path, image)

        if uploaded_image:
            log_debug(f"Image saved in: '{screenshot_path}'")
            return True
        else:
            log_debug("Image save failed")
            return False
    
    def save_gray_image(self, screenshot, screenshot_name=default_screenshot):
        """
        Creates a gray screenshot and saves it into folder with the current date and time as the name.

        :param screenshot_name: Name of the screenshot file (without extension).
        :param screenshot: A file it performs graying out effect on.
        :return: The captured screenshot object.
        """
        gray_image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
        gray_image_path = os.path.join(self.folder_path, f"{screenshot_name}_gray.png")
        
        cv2.imwrite(gray_image_path, gray_image)
        log_debug(f"Screenshots saved in folder: {gray_image_path}")
        
        return gray_image
    
    def process_image(self, image=None, resize_factor=2, screenshot_name=default_screenshot):
        """
        Resizes an image and saves it in a new folder with the current date and time as the name.

        Args:
            image (str): path to the image to be processed.
            screenshot_name (str, optional): Name of the new processed image. Defaults to default_screenshot.
        """
        if image is None:
            image_path = self.save_screenshot(screenshot_name=screenshot_name)
            image = cv2.imread(image_path)
            resized_image = cv2.resize(image, None, fx=resize_factor, fy=resize_factor)
            
        else:
            image = cv2.imread(image)
            resized_image = cv2.resize(image, None, fx=resize_factor, fy=resize_factor)
            
        return resized_image

    def write(self, message, interval=0.25):
        """
            Type words
        """

        message_typed = gui.write(message=message, interval=interval)
        log_debug(f"Message written: {message_typed}")

        return message_typed
    
    def pixel_color(self, x, y):
        """
            Returns a list of RGB value of a given pixel on the screen.
        """
        pixel_color = gui.pixel(x, y)
        
        red = pixel_color[0]
        green = pixel_color[1]
        blue = pixel_color[2]
        log_debug(f"RGB value of given pixel: {red}, {green}, {blue}")

        return [red, green, blue]
    
    def pixel_matching(self, x, y, rgb_value=list):
        """
            Checks if a given pixel RGB values match with the pixel in x, y coordinates
        """
        pixel_color = gui.pixel(x, y)
        
        red = pixel_color[0]
        green = pixel_color[1]
        blue = pixel_color[2]
        log_debug(f"RGB value of given pixel: {red}, {green}, {blue}")
        
        if [red, green, blue] == [rgb_value[0], rgb_value[1], rgb_value[2]]:
            log_debug(f"RGB value target: {rgb_value[0]}, {rgb_value[1]}, {rgb_value[2]}")
            return True
        else:
            return False
        
    def _is_hex_color(self, color):
        return isinstance(color, str) and len(color) == 7 and color[0] == '#' and all(c in '0123456789abcdefABCDEF' for c in color[1:])

    def _is_rgb_color(self, color):
        return isinstance(color, tuple) and len(color) == 3 and all(isinstance(c, int) and 0 <= c <= 255 for c in color)
        
    def color_present_on_screen(self, color, image=None, hex=True, rgb=False):
        """
            Checks if a given color is present on the screen.
            :param image: Path to image to check.
            :param color: Color to check. Checks HEX by default, so value has to be given in HEX style format: #FFF000.
            If you want to check RGB values, you have to give it as a tuple of 3 integers
            :param hex: If True, checks if the color is in HEX format.
            :param rgb: If True, checks if the color is in RGB format.
        """
        if hex and rgb:
            raise ValueError("Cannot have both rgb and hex values at the same time.")
        
        if hex and not self._is_hex_color(color):
            raise ValueError("Hex color should be in the format '#FFF000'")

        if rgb and not self._is_rgb_color(color):
            raise ValueError("RGB color should be a tuple of 3 integers between 0 and 255")
        
        if image is None:
            image_path = self.save_screenshot()
        
            image = cv2.imread(image_path)
            image_array = np.array(image)
        else:
            image = cv2.imread(image)
            image_array = np.array(image)
        
        if hex:
            color_values = []

            for row in image_array:
                for pixel in row:
                    hex_color = '#{0:02x}{1:02x}{2:02x}'.format(pixel[2], pixel[1], pixel[0])
                    color_values.append(hex_color.upper())

            log_debug(f"Color present: {color.upper() in color_values}")
            return color.upper() in color_values

        if rgb:
            color_values = []

            for row in image_array:
                for pixel in row:
                    rgb_color = tuple(pixel[::-1])
                    color_values.append(rgb_color.upper())

            log_debug(f"Color present: {color.upper() in color_values}")
            return color.upper() in color_values
        
        log_debug("Color not present on screen")
        return False
    
    def get_active_window(self):
        """
            Getting Active Window
        """

        active_window_name = None
        
        window = win32gui.GetForegroundWindow()
        active_window_name = win32gui.GetWindowText(window)
        log_debug(f"Active window name: {active_window_name}")

        return active_window_name
    
    def is_window_active(self, desired_window):
        """
        Check if a specific window is currently active.
        """
        active_window_name = self.get_active_window()
        return active_window_name == desired_window
    
    def wait_for_app_activation(self, window_title, timeout=300):
        """
        Wait for a specific application window to become active within a timeout.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.is_window_active(window_title):
                return True
            time.sleep(1)
        return False
    
    def image_processing(self, screenshot, screenshot_name=default_screenshot):
        """
            Image Processing
        """
        ret1, th1 = cv2.threshold(screenshot, self.BINARY_THRESHOLD, 255, cv2.THRESH_BINARY_INV)
        ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        blur = cv2.GaussianBlur(th2, (1, 1), 0)
        ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        processed_image_path = os.path.join(self.folder_path, f"{screenshot_name}_processed.png")
        
        cv2.imwrite(processed_image_path, th3)
        log_debug(f"Screenshots saved in folder: {processed_image_path}")
        
        return th3
    
    def remove_noise(self, screenshot, screenshot_name=default_screenshot):
        """
            Removing noise in image
        """
        removed_noise = cv2.medianBlur(screenshot, 5)
        
        removed_noise_path = os.path.join(self.folder_path, f"{screenshot_name}_removed_noise.png")
        cv2.imwrite(removed_noise_path, removed_noise)
        log_debug(f"Screenshots saved in folder: {removed_noise_path}")
        
        return removed_noise

    def thresholding(self, screenshot, screenshot_name=default_screenshot):
        """
            Using thresholding on image
        """
        
        threshold_image = cv2.threshold(screenshot, self.BINARY_THRESHOLD, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        
        threshold_path = os.path.join(self.folder_path, f"{screenshot_name}_thresholded.png")
        cv2.imwrite(threshold_path, threshold_image)
        log_debug(f"Screenshots saved in folder: {threshold_path}")
        
        return threshold_image

    def dilate(self, screenshot, screenshot_name=default_screenshot):
        """
            Image Dilation
        """
        kernel = np.ones((5, 5), np.uint8)
        dilated = cv2.dilate(screenshot, kernel, iterations = 1)
        
        dilated_path = os.path.join(self.folder_path, f"{screenshot_name}_dilated.png")
        cv2.imwrite(dilated_path, dilated)
        log_debug(f"Screenshots saved in folder: {dilated_path}")
        
        return dilated
    
    def erode(self, screenshot, screenshot_name=default_screenshot):
        """
            Image Erosion
        """
        kernel = np.ones((5,5), np.uint8)
        eroded = cv2.erode(screenshot, kernel, iterations = 1)
        
        eroded_path = os.path.join(self.folder_path, f"{screenshot_name}_eroded.png")
        cv2.imwrite(eroded_path, eroded)
        log_debug(f"Screenshots saved in folder: {eroded_path}")
        
        return eroded

    def opening(self, screenshot, screenshot_name=default_screenshot):
        """
            Performing Morphology on image
        """
        kernel = np.ones((5,5),np.uint8)
        morphology = cv2.morphologyEx(screenshot, cv2.MORPH_OPEN, kernel)
        
        morphology_path = os.path.join(self.folder_path, f"{screenshot_name}_morphology.png")
        cv2.imwrite(morphology_path, morphology)
        log_debug(f"Screenshots saved in folder: {morphology_path}")
        
        return morphology

    def canny(self, screenshot, screenshot_name=default_screenshot):
        """
            Performing canny on image
        """
        canny = cv2.Canny(screenshot, 100, 200)
        
        canny_path = os.path.join(self.folder_path, f"{screenshot_name}_canny.png")
        cv2.imwrite(canny_path, canny)
        log_debug(f"Screenshots saved in folder: {canny_path}")
        
        return canny
    
    def hex_to_rgb(self, hex_color):
        """
            Changing hex color value to rgb color
        """
        hex_color = hex_color.lstrip("#")
        log_debug(f"hex color: {hex_color}, to rgb: {tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))}")
        
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def hough_lines(self, image=None, threshold=90, min_line_length=20, max_line_gap=40, canny_thres_1=100, canny_thres_2=150):
        """
        Detects lines in an image using Hough transform.

        Args:
            image (str): image path
            threshold (int): threshold value
            min_line_length (int): min line length value
            max_line_gap (int): max line gap value
        """
        if image is None:
            new_screenshot = self.save_screenshot(screenshot_name="hough_lines_on_image")
        
            image = cv2.imread(new_screenshot)
            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            image = cv2.imread(image)
            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        lines = cv2.Canny(image_gray, canny_thres_1, canny_thres_2)
        
        lines = cv2.HoughLinesP(lines, 1, np.pi/180, threshold=threshold, minLineLength=min_line_length, maxLineGap=max_line_gap)
        
        all_lines_coords = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            all_lines_coords.append((x1, y1, x2, y2))
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        log_debug(f"All lines coordinates: {all_lines_coords}")
        self.upload_image(image=image, screenshot_name="all_lines_on_image")
        
        return all_lines_coords
    
    def find_color_coordinates(self, color: list, image=None):
        
        if image is None:
            new_screenshot = self.save_screenshot(screenshot_name="find_color_coordinates_on_image")
        
            target_image = cv2.imread(new_screenshot)
        else:
            target_image = cv2.imread(image)

        if color is not None and len(color) == 3:
            target_color = color
            log_debug(f"Target color is: {target_color}")
        elif color is not None:
            target_color = self.hex_to_rgb(color)
            log_debug(f"From hex to rgb, rgb color is: {target_color}")
        else:    
            raise ValueError("Please provide a color value")
        
        target_color_bgr = target_color[::-1]

        lower_bound = (target_color_bgr[0] - 10, target_color_bgr[1] - 10, target_color_bgr[2] - 10)
        upper_bound = (target_color_bgr[0] + 10, target_color_bgr[1] + 10, target_color_bgr[2] + 10)
        mask = cv2.inRange(target_image, lower_bound, upper_bound)
        coordinates = cv2.findNonZero(mask)
        
        log_debug(f"All coordinates: {coordinates}")

        return coordinates
    
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
    
    # def find_text_and_click_easyocr(self, text, image=None, click_type=gui.PRIMARY, click_duration=0.1):
    #     reader = easyocr.Reader(['en'])
        
    #     if image is None:
    #         screenshot = self.save_screenshot()
    #     else:
    #         screenshot = cv2.imread(image)
            
    #     result = reader.readtext(screenshot)
    #     log_debug(f"Found image at these coords: ({result}")
        
    #     return result