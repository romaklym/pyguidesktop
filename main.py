# main.py
from pyguidesktop.pyguidesktop import PyGUIDesktop
from time import sleep
from pyguidesktop.logger import log_debug, log_error

def main():
    
    try:
        log_debug("Script started")
        
        pgd = PyGUIDesktop()
        
        desired_window = "main.py - pyguidesktop - Visual Studio Code"
        timeout = 60
        
        # Checks if the desired window becomes active within a timeout
        if not pgd.wait_for_app_activation(desired_window, timeout=timeout):
            log_error(f"{desired_window} did not become active within the timeout. Stopping the script.")
            log_debug(f"Actual active window: {pgd.get_active_window()}")
            return
        
        if pgd.is_window_active(desired_window):
            # Perform actions while the window is active
            
            # MAIN CODE
            play(pgd)

        else:
            log_error(f"{desired_window} is no longer active. Stopping the script.")

        log_debug("Script completed successfully")
            
        
    except Exception as e:
        log_error(e)
        
# Main code logic to perform actions
def play(pgd):
    
    app_path = r"APP_PATH"
    sleep(2)
    # pgd.hough_lines()
    # pgd.launch_app(APP_PATH)
    pgd.find_text_and_click("Run")
    # pgd.find_text_coordinates("YOUR_TEXT")
    # pgd.get_active_window()
    # pgd.find_image_on_screen_and_click()
    # pgd.color_present_on_screen("#YOUR_HEX_COLOR")
    # mouse_position = pgd.mouse_position()
    # pgd.pixel_color(mouse_position.x, mouse_position.y)
    
    
if __name__ == "__main__":
    main()
