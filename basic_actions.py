import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from PIL import ImageGrab
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from utilities.database_operations import *
import os
from datetime import datetime
import inspect
import re
from utilities.pytest_logger import SingletonLogger
from utilities.exception_handling import *
from selenium.webdriver.chrome.service import Service


class BasicActions:
    basic_wait_time = 45

    def __init__(self, driver=None):
        self.logger = SingletonLogger()
        self.logger.logger.info("Basic actions class is initiated with browser driver value")
        self.driver = driver
        self.wait_for_45_seconds = 45

        """  HP ONE ELEMENTS """
        self.toggle_button = (By.XPATH, '//button[@aria-label="Toggle Menu"]')
        self.privacy_link_url = "https://www.hp.com/us-en/privacy/privacy.html"

    def type_words(self, locator, text):
        self.log_my_keyword_name_and_arguments()
        element = self.driver.find_element(locator[0], locator[1])
        element.clear()
        element.send_keys(text)

    def element_displayed(self, locator, timeout=None):
        self.log_my_keyword_name_and_arguments()
        if timeout is None:
            timeout = self.basic_wait_time
        try:
            self.wait_for_object(locator, timeout)
            return self.driver.find_element(locator[0], locator[1]).is_displayed()
        except Exception as err:
            try:
                self.scroll_element_into_view(locator)
                return self.driver.find_element(locator[0], locator[1]).is_displayed()
            except Exception as err:
                self.logger.logger.info(str(err))
                print(str(err))
                self.logger.logger.debug(
                    f"element_displayed called \n locator: {locator} > locator not available in the web page")
                return False

    def click_me(self, locator):
        self.log_my_keyword_name_and_arguments()
        element = self.get_web_element(locator)
        clicked = False
        try:
            element.click()
            clicked = True
            self.logger.logger.info(f"element clicked using selenium")
        except Exception as err:
            self.logger.logger.info(f"Click using WebDriver is failed: {str(err)}")
        if not clicked:
            try:
                actions = ActionChains(self.driver)
                actions.move_to_element(element).click().perform()
                clicked = True
                self.logger.logger.info(f"element clicked using action chains")
            except Exception as e:
                self.logger.logger.info(f"Click using ActionChains failed: {str(e)}")
        if not clicked:
            try:
                javascript_code = """
                function clickElement(element) {
                        if (element) {
                            element.click();
                            return true;
                        } else {
                            return false;
                        }
                    }
                return clickElement(arguments[0]);
                """
                clicked = self.driver.execute_script(javascript_code, element)
                self.logger.logger.info(f"element clicked using java script query")
                self.logger.logger.info(clicked)
            except Exception as e:
                self.logger.logger.info(f"Click using JavaScript failed: {str(e)}")
        if not clicked:
            message = f"Element is not clicked ==> {str(locator)}"
            self.logger.logger.info(message)
            raise ElementNotClicked(message)

    def get_attribute_value(self, locator, attribute):
        self.log_my_keyword_name_and_arguments()
        self.wait_for_object(locator)
        if attribute == "text":
            return self.driver.find_element(locator[0], locator[1]).text
        return self.driver.find_element(locator[0], locator[1]).get_attribute(attribute)

    def append_text(self, locator, text):
        self.log_my_keyword_name_and_arguments()
        self.wait_for_object(locator)
        self.driver.find_element(locator[0], locator[1]).send_keys(Keys.END)
        self.driver.find_element(locator[0], locator[1]).send_keys(text)

    def capture_screenshot(self, filename=None):
        self.log_my_keyword_name_and_arguments()
        my_framework_dir = os.path.dirname(os.getcwd())
        destination_directory = os.path.join(my_framework_dir, "reports\\screenshots")
        if not os.path.exists(destination_directory):
            os.makedir(destination_directory)
        screenshot = ImageGrab.grab()
        filename = re.sub(".png", "", filename)
        if filename is not None:
            screenshot.save(os.path.join(destination_directory, f"{filename}.png"))
        else:
            filename = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            screenshot.save(os.path.join(destination_directory, f"{filename}.png"))
        self.logger.logger.info(f"screen shot is captured and saved in the name of {filename}")

    def check_text_of_object(self, locator, text_to_compare):
        self.log_my_keyword_name_and_arguments()
        received_text = self.get_attribute_value(locator, "text")
        if received_text == "" or received_text is None:
            received_text = self.get_attribute_value(locator, "value")
        return received_text == text_to_compare

    def clear_field(self, locator):
        self.log_my_keyword_name_and_arguments()
        element = self.driver.find_element(locator[0], locator[1])
        element.clear()

    def click_me_with_index(self, locator, pos):
        self.log_my_keyword_name_and_arguments()
        self.wait_for_object(locator)
        my_elements = self.driver.find_elements(locator[0], locator[1])
        if len(my_elements) >= pos:
            my_elements[pos - 1].click()
        else:
            self.logger.logger.debug("position input is greater than available elements")
            print("XPATH Position is more than available elements")

    def click_using_text(self, text):
        self.log_my_keyword_name_and_arguments()
        if self.element_displayed((By.XPATH, "//*[text()='{}']".format(text))):
            self.logger.logger.info("Element clicked using text value presents in the object")
            locator = (By.XPATH, "//*[text()='{}']".format(text))
        else:
            self.logger.logger.info("Element clicked using value attribute presents in the object")
            locator = (By.XPATH, "//*[@value='{}']".format(text))
        self.click_me(locator)

    def click_using_text_by_index(self, text, pos):
        self.log_my_keyword_name_and_arguments()
        status = False
        if self.element_displayed((By.XPATH, "//*[text()='{}']".format(text))):
            self.logger.logger.info("Element clicked using text value presents in the object")
            try:
                locator = (By.XPATH, "//*[text()='{}']".format(text))
                self.click_me_with_index(locator, pos)
                status = True
            except:
                self.logger.logger.debug("position input is greater than available elements")
        if status is not True:
            self.logger.logger.info("Element clicked using value attribute presents in the object")
            locator = (By.XPATH, "//*[@value='{}']".format(text))
            try:
                self.click_me_with_index(locator, pos)
            except:
                self.logger.logger.debug("position input is greater than available elements")

    def close_browser(self):
        self.log_my_keyword_name_and_arguments()
        self.driver.close()

    def double_click(self, locator):
        self.log_my_keyword_name_and_arguments()
        actions = ActionChains(self.driver)
        actions.double_click(locator).perform()

    def execute_java_script(self, script_data):
        self.log_my_keyword_name_and_arguments()
        self.driver.execute_script(script_data)

    def get_css_property(self, locator, property_name):
        self.log_my_keyword_name_and_arguments()
        self.wait_for_object(locator)
        self.driver.find_element(locator[0], locator[1]).value_of_css_property(property_name)

    def get_current_url(self):
        self.log_my_keyword_name_and_arguments()
        return self.driver.current_url

    def get_value_from_cookie(self):
        self.log_my_keyword_name_and_arguments()
        data = self.driver.get_cookies()
        return data

    def go_to_url(self, url):
        self.log_my_keyword_name_and_arguments()
        self.driver.get(url)

    def is_clickable_object(self, locator):
        self.log_my_keyword_name_and_arguments()
        try:
            WebDriverWait(self.driver, self.basic_wait_time).until(EC.element_to_be_clickable(locator))
            return True
        except:
            self.logger.logger.info(f"Un-clickable object")
            return False

    def is_current_url(self, url):
        self.log_my_keyword_name_and_arguments()
        if self.get_current_url() == url:
            self.logger.logger.info("current URL is same")
            return True
        self.logger.logger.info("Not a current URL")
        return False

    def press_home_key(self, input_field_id=None):
        self.log_my_keyword_name_and_arguments()
        if input_field_id is not None:
            self.wait_for_object(input_field_id)
            self.driver.find_element(input_field_id[0], input_field_id[1]).send_keys(Keys.HOME)
            self.logger.logger.info("Cursor moved to the Home object")
            return True
        else:
            self.logger.logger.debug("Press home key button is not clicked")
            return False

    def press_page_down_key(self):
        self.log_my_keyword_name_and_arguments()
        locator = (By.TAG_NAME, "body")
        self.driver.find_element(locator[0], locator[1]).send_keys(Keys.PAGE_DOWN)

    def press_page_up_key(self):
        self.log_my_keyword_name_and_arguments()
        locator = (By.TAG_NAME, "body")
        self.driver.find_element(locator[0], locator[1]).send_keys(Keys.PAGE_UP)

    def refresh_page(self):
        self.log_my_keyword_name_and_arguments()
        self.driver.refresh()

    def scroll_element_into_view(self, locator):
        self.log_my_keyword_name_and_arguments()
        self.driver.execute_script("arguments[0].scrollIntoView(true);", self.get_web_element(locator))

    def select_default_frame(self):
        self.log_my_keyword_name_and_arguments()
        self.driver.switch_to.default_content()

    def select_frame(self, locator):
        self.log_my_keyword_name_and_arguments()
        frame_element = self.get_web_element(locator)
        self.driver.switch_to.frame(frame_element)

    def back_to_body_from_frame(self):
        self.driver.switch_to.default_content()

    def select_tab_by_index(self, position):
        self.log_my_keyword_name_and_arguments()
        self.driver.switch_to.window(self.driver.window_handles[position - 1])

    def set_default_timeout(self, timeout):
        self.log_my_keyword_name_and_arguments()
        self.basic_wait_time = timeout

    def submit_element(self, locator):
        self.log_my_keyword_name_and_arguments()
        self.driver.find_element(locator[0], locator[1]).submit()

    def wait_for_object(self, locator, timeout=None):
        self.log_my_keyword_name_and_arguments()
        if timeout is None:
            timeout = self.basic_wait_time
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    def wait_for_object_disappear(self, locator, timeout):
        self.log_my_keyword_name_and_arguments()
        WebDriverWait(self.driver, timeout).until_not(EC.presence_of_element_located(locator))

    def is_alert_appear(self):
        self.log_my_keyword_name_and_arguments()
        try:
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            self.logger.logger.info(f"Alert appear")
            return True
        except:
            self.logger.logger.info(f"Alert not appear")
            return False

    def get_alert_text(self):
        self.log_my_keyword_name_and_arguments()
        if self.is_alert_appear():
            alert = self.driver.switch_to.alert
            self.logger.logger.info(f"collected alert text value:  {alert.text}")
            return alert.text
        else:
            self.logger.logger.info("Alert is not appear to get the text")
            raise AssertionError

    def accept_the_alert(self):
        self.log_my_keyword_name_and_arguments()
        if self.is_alert_appear():
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            self.logger.logger.info(f"collected alert text value:  {alert_text}")
            return alert_text
        else:
            self.logger.logger.info("Alert is not appear to get the text")
            raise AssertionError

    def dismiss_the_alert(self):
        self.log_my_keyword_name_and_arguments()
        if self.is_alert_appear():
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.dismiss()
            self.logger.logger.info(f"collected alert text value:  {alert_text}")
            return alert_text
        else:
            self.logger.logger.info("Alert is not appear to get the text")
            raise AssertionError

    def alert_text_should_be(self, comparision_text):
        self.log_my_keyword_name_and_arguments()
        alert = self.driver.switch_to.alert
        alert_text = alert.text
        self.logger.logger.info(f"compared output: {alert_text == comparision_text} ")
        return alert_text == comparision_text

    def set_checkbox_value(self, locator, value=True):
        self.log_my_keyword_name_and_arguments()
        check_box = self.driver.find_element(locator[0], locator[1])
        check_box.set_checked(value)

    def get_checkbox_value(self, locator):
        self.log_my_keyword_name_and_arguments()
        check_box = self.driver.find_element(locator[0], locator[1])
        self.logger.logger.info(f"check box selected status is : {check_box.is_selected()}")
        return check_box.is_selected()

    def close_current_opened_tab(self):
        self.log_my_keyword_name_and_arguments()
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def close_tab_by_index(self, index_number):
        self.log_my_keyword_name_and_arguments()
        self.select_tab_by_index(index_number)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def drag_and_drop(self, source_element, target_element):
        self.log_my_keyword_name_and_arguments()
        action = ActionChains(self.driver)
        source_element = self.driver.find_element(source_element[0], source_element[1])
        target_element = self.driver.find_element(target_element[0], target_element[1])
        action.drag_and_drop(source_element, target_element).perform()

    def get_window_title(self):
        self.log_my_keyword_name_and_arguments()
        self.logger.logger.info(f"Window title is: {self.driver.title} ")
        return self.driver.title

    def click_browser_back_button(self):
        self.log_my_keyword_name_and_arguments()
        self.driver.back()

    def maximize_browser_window(self):
        self.log_my_keyword_name_and_arguments()
        self.driver.maximize_window()

    def mouse_hover_on_element(self, locator):
        self.log_my_keyword_name_and_arguments()
        my_element = self.driver.find_element(locator[0], locator[1])
        actions = ActionChains(self.driver)
        actions.move_to_element(my_element).perform()

    def get_radio_button_value(self, locator):
        self.log_my_keyword_name_and_arguments()
        my_element = self.driver.find_element(locator[0], locator[1])
        return my_element.is_selected()

    def set_radio_button_value(self, locator, value=True):
        self.log_my_keyword_name_and_arguments()
        my_element = self.driver.find_element(locator[0], locator[1])
        if value != my_element.is_selected():
            my_element.click()

    def select_from_list_by_index(self, locator, index_value):
        self.log_my_keyword_name_and_arguments()
        my_element = self.driver.find_element(locator[0], locator[1])
        select_obj = Select(my_element)
        select_obj.select_by_index(index_value)

    def select_from_list_by_value(self, locator, value):
        self.log_my_keyword_name_and_arguments()
        my_element = self.driver.find_element(locator[0], locator[1])
        select_obj = Select(my_element)
        select_obj.select_by_value(value)

    def select_from_list_by_visible_text(self, locator, value):
        self.log_my_keyword_name_and_arguments()
        my_element = self.driver.find_element(locator[0], locator[1])
        select_obj = Select(my_element)
        select_obj.select_by_visible_text(value)

    def quit_browser(self):
        self.log_my_keyword_name_and_arguments()
        self.driver.quit()

    def open_chrome(self):
        self.log_my_keyword_name_and_arguments()
        driver_path = get_parent_framework_path() + "\\drivers\\chromedriver.exe"
        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service)
        return self.driver

    def open_firefox(self):
        self.log_my_keyword_name_and_arguments()
        driver_path = get_parent_framework_path() + "\\drivers\\geckodriver.exe"
        service = Service(driver_path)
        self.driver = webdriver.Firefox(service=service)
        return self.driver

    def open_edge(self):
        self.log_my_keyword_name_and_arguments()
        driver_path = get_parent_framework_path() + "\\drivers\\msedgedriver.exe"
        service = Service(driver_path)
        self.driver = webdriver.Edge(service=service)
        return self.driver

    def open_my_browser(self):
        self.log_my_keyword_name_and_arguments()
        try:
            my_browser_name = get_browser_name()
            browsers = {"chrome": self.open_chrome, "edge": self.open_edge, "firefox": self.open_firefox}
            self.driver = browsers[my_browser_name]()
            self.logger.logger.info(f"{my_browser_name} opened for testing")
        except:
            self.logger.logger.info(f"chrome browser is  opened for testing")
            self.driver = self.open_chrome()
        return self.driver

    def log_and_requirement_covered(self, requirement_number):
        self.log_my_keyword_name_and_arguments()
        self.logger.logger.info(f"log_and_requirement_covered: {requirement_number}")

    def get_text_of_the_object(self, locator):
        self.log_my_keyword_name_and_arguments()
        received_text = self.get_attribute_value(locator, "text")
        if received_text == "" or received_text is None:
            received_text = self.get_attribute_value(locator, "value")
        return received_text

    def get_element_by_index(self, locator, pos):
        self.log_my_keyword_name_and_arguments()
        self.wait_for_object(locator)
        my_elements = self.driver.find_elements(locator[0], locator[1])
        if len(my_elements) >= pos:
            return my_elements[pos - 1]
        else:
            self.logger.logger.debug("position input is greater than available elements")
            print("locator position is more than available elements")

    def element_displayed_by_index(self, locator, pos):
        self.log_my_keyword_name_and_arguments()
        self.wait_for_object(locator)
        my_elements = self.driver.find_elements(locator[0], locator[1])
        if len(my_elements) >= pos:
            elem = my_elements[pos - 1]
            return elem.is_displayed()
        else:
            self.logger.logger.debug("position input is greater than available elements")
            print("locator position is more than available elements")
            return False

    def get_web_element(self, locator):
        self.log_my_keyword_name_and_arguments()
        element = self.driver.find_element(locator[0], locator[1])
        return element

    def click_me_using_action_chains(self, locator):
        self.log_my_keyword_name_and_arguments()
        action_chains = ActionChains(self.driver)
        elem = self.get_web_element(locator)
        action_chains.move_to_element(elem).click().perform()

    # HP ONE WEB SITE BASIC ACTIONS
    def click_menu_button(self, menu_btn):
        self.log_my_keyword_name_and_arguments()
        if self.element_displayed(menu_btn, 3):
            self.click_me(menu_btn)
        elif self.element_displayed(self.toggle_button, 3):
            self.click_me(self.toggle_button)
            self.click_me(menu_btn)
        else:
            self.wait_for_object(menu_btn)
            self.click_me(menu_btn)

    def log_my_keyword_name_and_arguments(self):
        """ This function is used to collect the variable name and arguments to log in logging """
        """ To get function name """
        current_frame = inspect.currentframe()
        calling_frame = current_frame.f_back
        function_name = calling_frame.f_code.co_name
        """ To get variables in dict format """
        frame = inspect.currentframe().f_back
        format_args = ""
        for key, value in frame.f_locals.items():
            if key != "self":
                format_args += str(key) + "=" + str(value) + " "
        format_args = "No arguments" if format_args == "" else format_args
        self.logger.logger.info(f"{function_name} called   Arguments=====>: {format_args}")

    def click_sub_menu_button(self, parent_menu, submenu):
        self.log_my_keyword_name_and_arguments()
        try:
            if self.element_displayed(submenu, 3):
                pass
            elif self.element_displayed(parent_menu):
                self.click_me(parent_menu)
            elif self.element_displayed(self.toggle_button):
                self.click_me(self.toggle_button)
                self.click_me(parent_menu)
            time.sleep(1)  # This sleep is helping to click exact sub-menu (Must needed-due to app slowness)
            self.click_me(submenu)
        except Exception as err:
            self.click_me_using_action_chains(submenu)

    def scroll_specific_div(self, parent_id, pixel_data=900):
        self.log_my_keyword_name_and_arguments()
        parent_element = self.driver.find_element(parent_id[0], parent_id[1])
        script = f"arguments[0].scrollTop = arguments[0].scrollTop + {pixel_data};"
        self.driver.execute_script(script, parent_element)

    def change_screen_size(self, size):
        self.log_my_keyword_name_and_arguments()
        self.driver.execute_script(f"document.body.style.zoom='{size}%'")

    def element_should_be_displayed(self, locator, timeout):
        if not self.element_displayed(locator, timeout=timeout):
            raise ElementNotDisplayed("Element is not displayed")

    def element_should_be_clickable(self, locator, timeout=1):
        if not self.is_clickable_object(locator):
            raise ElementNotClickable("Element is not clickable")

    def element_should_be_disappeared(self, locator, timeout=3):
        if self.element_displayed(locator, timeout=timeout):
            raise ElementDisplayed("Element is not disappeared")
