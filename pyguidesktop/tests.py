from .pyguidesktop import PyGUIDesktop
from time import sleep
from .logger import log_debug, log_error

def main():
    
    try:
        log_debug("Script started")
        
        pgd = PyGUIDesktop()
        # pgd.make_screenshot("basic_screenshot")
        # # TODO: make it work for multiple words
        # pgd.find_text_and_click(text="Run")
        pgd.get_active_window()
        pgd.find_image_on_screen_and_click()

        log_debug("Script completed successfully")
        
    except Exception as e:
        log_error(e)

if __name__ == "__main__":
    main()
