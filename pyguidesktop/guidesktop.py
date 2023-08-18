import pyautogui as gui
import numpy as np
import sys, os
from datetime import datetime
import win32gui
from time import sleep
import cv2
from .logger import log_debug


class GUIDesktop:
    def __init__(self):
        package_dir = os.path.dirname(os.path.abspath(__file__))
        main_folder = os.path.dirname(package_dir)
        self.screenshots_dir = os.path.join(main_folder, "images")
        if not os.path.exists(self.screenshots_dir):
            os.makedirs(self.screenshots_dir)

        now = datetime.now()
        self.timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        self.folder_path = os.path.join(self.screenshots_dir, self.timestamp)
        os.makedirs(self.folder_path)
        self.BINARY_THREHOLD = 120
    
    default_screenshot = "screenshot"
    region = (0, 0, gui.size()[0], gui.size()[1])
    timeout = 0.5
    screen_resolution = list(gui.size())
    resize = 2

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

    def mouse_position(self):
        """
            Returns Position of the cursor on the screen as Tuple.
            Format: x, y
        """

        position = gui.position()
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
    
    def move_to(self, x=0, y=0, timeout=None, duration=0.1, tween=gui.linear, pause=True):
        """
            Moves cursor to location on the screen specified as arguments.
            Format: True, False
        """

        gui.moveTo(x=x, y=y, duration=duration, tween=tween, pause=pause)
        log_debug(f"Moves cursor to location: x: {x}, y: {y}")

        sleep(timeout)

        if gui.position() == (x, y):
            log_debug(f"Succesfully moved to {x}, {y}")
            return True

        else:
            log_debug(f"Failed to move cursor to: {x}, {y}")
            return False

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
    
    def click(self, clicks=1, interval=0, button=gui.PRIMARY, duration=0, tween=gui.linear, pause=True):
        """
            Mouse click.
            Format: None
        """

        gui.click(clicks=clicks, interval=interval, button=button,
                  duration=duration, tween=tween, pause=pause)
        log_debug(f"Clicks this many times: {clicks}, with this button: {button}")

        return None
    
    def double_click(self, x=None, y=None, interval=0, button=gui.LEFT, duration=0, tween=gui.linear, pause=True):
        """
            Double Mouse click.
            Format: None
        """

        gui.doubleClick(x=x, y=y, interval=interval, button=button,
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
        log_debug(f"Scrolled mousethis many clicks: {clicks}")

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

    def write(self, message, interval=0.25):
        """
            Type words
        """

        message_typed = gui.write(message=message, interval=interval)

        return message_typed
    
    def get_active_window(self):
        """
            Getting Active Window
        """

        active_window_name = None
        
        window = win32gui.GetForegroundWindow()
        active_window_name = win32gui.GetWindowText(window)
        log_debug(f"Active window name: {active_window_name}")

        return active_window_name
    
    def image_processing(self, screenshot, screenshot_name=default_screenshot):
        """
            Image Processing
        """
        ret1, th1 = cv2.threshold(screenshot, self.BINARY_THREHOLD, 255, cv2.THRESH_BINARY_INV)
        ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        blur = cv2.GaussianBlur(th2, (1, 1), 0)
        ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        processed_image_path = os.path.join(self.folder_path, f"{screenshot_name}_processed.png")
        
        cv2.imwrite(processed_image_path, th3)
        log_debug(f"Screenshots saved in folder: {processed_image_path}")
        
        return th3
    
    def remove_noise(self, screenshot, screenshot_name=default_screenshot):
        removed_noise = cv2.medianBlur(screenshot, 5)
        
        removed_noise_path = os.path.join(self.folder_path, f"{screenshot_name}_removed_noise.png")
        cv2.imwrite(removed_noise_path, removed_noise)
        log_debug(f"Screenshots saved in folder: {removed_noise_path}")
        
        return removed_noise

    def thresholding(self, screenshot, screenshot_name=default_screenshot):
        
        threshold_image = cv2.threshold(screenshot, self.BINARY_THREHOLD, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        
        threshold_path = os.path.join(self.folder_path, f"{screenshot_name}_thresholded.png")
        cv2.imwrite(threshold_path, threshold_image)
        log_debug(f"Screenshots saved in folder: {threshold_path}")
        
        return threshold_image

    def dilate(self, screenshot, screenshot_name=default_screenshot):
        kernel = np.ones((5, 5), np.uint8)
        dilated = cv2.dilate(screenshot, kernel, iterations = 1)
        
        dilated_path = os.path.join(self.folder_path, f"{screenshot_name}_dilated.png")
        cv2.imwrite(dilated_path, dilated)
        log_debug(f"Screenshots saved in folder: {dilated_path}")
        
        return dilated
    
    def erode(self, screenshot, screenshot_name=default_screenshot):
        kernel = np.ones((5,5), np.uint8)
        eroded = cv2.erode(screenshot, kernel, iterations = 1)
        
        eroded_path = os.path.join(self.folder_path, f"{screenshot_name}_eroded.png")
        cv2.imwrite(eroded_path, eroded)
        log_debug(f"Screenshots saved in folder: {eroded_path}")
        
        return eroded

    def opening(self, screenshot, screenshot_name=default_screenshot):
        kernel = np.ones((5,5),np.uint8)
        morphology = cv2.morphologyEx(screenshot, cv2.MORPH_OPEN, kernel)
        
        morphology_path = os.path.join(self.folder_path, f"{screenshot_name}_morphology.png")
        cv2.imwrite(morphology_path, morphology)
        log_debug(f"Screenshots saved in folder: {morphology_path}")
        
        return morphology

    def canny(self, screenshot, screenshot_name=default_screenshot):
        canny = cv2.Canny(screenshot, 100, 200)
        
        canny_path = os.path.join(self.folder_path, f"{screenshot_name}_cannyy.png")
        cv2.imwrite(canny_path, canny)
        log_debug(f"Screenshots saved in folder: {canny_path}")
        
        return canny
    
    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip("#")
        log_debug(f"hex color: {hex_color}, to rgb: {tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))}")
        
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))