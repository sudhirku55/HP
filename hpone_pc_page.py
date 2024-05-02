import time

from selenium.webdriver.common.by import By
from Pages_HPX.basic_actions import BasicActions


class HPOnePCPage(BasicActions):
    """ HPOne PC Page elements locators and its functionalities """
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.pre_arrival_alert_div = (By.XPATH, '//div[@data-testid="preavrrival-laptop"]')
        self.pre_arrival_alert_first_line = (By.XPATH, '//p[text()="You\'ll see information about your device below after you set up your PC."]')
        self.pre_arrival_alert_second_line = (By.XPATH, "")
        self.contact_support_btn = (By.LINK_TEXT, "Contact Support")
        self.support_url = "https://support.hp.com/contact"

    def validate_for_contact_support(self):
        self.click_me(self.contact_support_btn)
        self.select_tab_by_index(2)
        self.is_current_url(self.support_url)
        self.close_current_opened_tab()
        self.select_tab_by_index(1)

    def validate_pre_arrival_message(self):
        self.wait_for_object(self.pre_arrival_alert_div)
