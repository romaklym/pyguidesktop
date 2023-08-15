from .pyguidesktop import PyGUIDesktop
from time import sleep
import os, logging
from datetime import datetime
from .logger import log_debug, log_error

def main():
    
    try:
        log_debug("Script started")
        
        pgd = PyGUIDesktop()
        pgd.make_screenshot("basic_screenshot")
        # TODO: fix location since it clicks on small screenshot
        pgd.find_text_and_click(text="Run Terminal")

        log_debug("Script completed successfully")
        
    except Exception as e:
        log_error(e)

if __name__ == "__main__":
    main()
