# -*- coding: utf-8 -*-
from robot.api.deco import keyword
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from appium_flutter_finder import FlutterFinder
from AppiumFlutterLibrary import AppiumFlutterLibrary
from .module2 import XDrint
import time

class XPrint(AppiumFlutterLibrary):
    def __init__(self):
        super().__init__()
        self._ne = XDrint()
        self._bi = BuiltIn()
        self.finder = FlutterFinder()

    @keyword("XPrint Log")
    def XPrint_log(self):
        print("Hello, world! เทสภาษาไทย111")

    def TestModule2(self):
        instance = XDrint()  # You might consider renaming the variable to something meaningful
        instance.CDCDCD()    # Assuming CDCDCD is a valid method
        self._ne.CDCDCD()    # Ensure that _ne has the method CDCDCD

    def XQuit_App(self):
        """ปิดแอพปัจจุบันและปิดเซสชัน"""
        driver = self._current_application()
        driver.quit()

    @keyword('Switch Mode')
    def Switch_Mode(self, mode):
        """Switch Mode to NATIVE_APP OR FLUTTER."""
        driver = self._current_application()
        if mode == 'NATIVE_APP':
            driver.switch_to.context('NATIVE_APP')
        elif mode == 'FLUTTER':  # Changed from 'if' to 'elif' for logical correctness
            driver.switch_to.context('FLUTTER')

    def _current_application(self):
        """คืนค่าอินสแตนซ์ของแอปพลิเคชันปัจจุบัน"""
        return self._bi.get_library_instance('AppiumFlutterLibrary')._current_application()

    @keyword('Is Button Active')
    def is_button_active(self, key):
        """Check if the button with the given key is active in a Flutter application."""
        try:
            driver = self._current_application() #มีการเพิ่มเข้ามา
            button = self.finder.by_value_key(key)
            element = driver.find_element(button)   #ลบ self
            is_visible = element.is_displayed()
            is_enabled = element.is_enabled()

            if is_visible and is_enabled:
                logger.info(f"Button with key '{key}' is active and visible.")
                return True
            else:
                if not is_visible:
                    logger.warn(f"Button with key '{key}' is not visible.")
                if not is_enabled:
                    logger.warn(f"Button with key '{key}' is not enabled.")
                return False
        except Exception as e:
            logger.error(f"Error checking if button is active: {e}")
            return False

    @keyword('Wait Until Button Is Active')
    def wait_until_button_is_active(self, key, timeout=10):
        """Wait until the button with the given key is active in a Flutter application."""
        end_time = time.time() + timeout
        while time.time() < end_time:
            if self.is_button_active(key):
                return True
            time.sleep(1)

        logger.warn(f"Button with key '{key}' did not become active within {timeout} seconds.")
        return False
