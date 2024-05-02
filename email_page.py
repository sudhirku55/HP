import time

from selenium.webdriver.common.by import By
from Pages_HPX.basic_actions import BasicActions


class EmailPage(BasicActions):
    """
        This class is used to store the email page locator and actions
        Note: BasicActions class has imported to access the web actions with exception handling
    """
    user_entry = (By.ID, "username")
    next_btn = (By.ID, "user-name-form-submit")
    use_mobile_number_instead = (By.ID, "switch-username")
    remember_me_checkbox = (By.ID, "remember-me")
    forget_username = (By.ID, "forgot-cred")
    sign_up_btn = (By.ID, "sign-up")
    privacy_btn = (By.ID, "privacy")
    no_user_name_alert = (By.XPATH, "//span[text()='Enter your username or email address']")
    window_title = "HPID Login"

    """ Mobile number entries """
    mobile_number_entry = (By.ID, "phoneNumber")
    iso_code_drop_down = (By.ID, "isoCode")
    search_box_iso_code = (By.XPATH, '//input[@placeholder="Search"]')
    selected_iso_code = (By.XPATH, "//li[@aria-selected='true']/div/span/div")
    no_mobile_number_alert = (By.ID, "isoCode-helper-text")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def enter_username(self, username):
        self.log_my_keyword_name_and_arguments()
        self.wait_for_object(self.user_entry, self.basic_wait_time)
        self.type_words(self.user_entry, username)

    def clear_mail_id_entry(self):
        self.log_my_keyword_name_and_arguments()
        self.clear_field(self.user_entry)

    def click_next_button(self):
        self.log_my_keyword_name_and_arguments()
        self.click_me(self.next_btn)

    def get_remember_me_checkbox_status(self):
        self.log_my_keyword_name_and_arguments()
        status = self.get_checkbox_value(self.remember_me_checkbox)
        return status

    def select_remember_me_checkbox(self):
        self.log_my_keyword_name_and_arguments()
        self.set_checkbox_value(self.remember_me_checkbox, True)

    def un_select_remember_me_checkbox(self):
        self.log_my_keyword_name_and_arguments()
        self.set_checkbox_value(self.remember_me_checkbox, False)

    def click_on_forget_username(self):
        self.log_my_keyword_name_and_arguments()
        self.click_me(self.forget_username)

    def click_on_sign_up_button(self):
        self.log_my_keyword_name_and_arguments()
        self.click_me(self.sign_up_btn)

    def click_on_privacy(self):
        self.log_my_keyword_name_and_arguments()
        self.click_me(self.privacy_btn)

    def click_on_privacy_button_validate_url(self):
        self.click_me(self.privacy_btn)
        self.select_tab_by_index(2)
        status = self.is_current_url(self.privacy_link_url)
        assert True == status
        self.select_tab_by_index(1)

    def check_email_page_element_visibilities(self):
        self.log_my_keyword_name_and_arguments()
        variables = {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("__") and not callable(value) and isinstance(value, tuple)
        }
        for variable in variables:
            appeared_status = self.element_displayed(variable)
            assert True == appeared_status

    def click_on_use_mobile_number_instead(self):
        self.log_my_keyword_name_and_arguments()
        self.click_me(self.use_mobile_number_instead)

    def enter_mobile_number(self, number):
        self.log_my_keyword_name_and_arguments()
        self.type_words(self.mobile_number_entry, number)

    def set_iso_code(self, iso_code):
        self.log_my_keyword_name_and_arguments()
        self.click_me(self.iso_code_drop_down)
        self.type_words(self.search_box_iso_code, iso_code)
        self.click_me((By.XPATH, f"//div[@title='{iso_code}']"))

    def get_current_selected_iso_code(self):
        self.log_my_keyword_name_and_arguments()
        return self.get_attribute_value(self.selected_iso_code, "title")

    def no_username_alert_should_appear(self):
        self.log_my_keyword_name_and_arguments()
        assert True == self.element_displayed(self.no_user_name_alert)

    def no_mobile_number_alert_should_appear(self):
        self.log_my_keyword_name_and_arguments()
        assert True == self.element_displayed(self.no_mobile_number_alert)

    def click_signup_button(self):
        self.click_me(self.sign_up_btn)

class ForgetUsernamePage(BasicActions):

    recovery_email_address_entry = (By.ID, "recoveryInput")
    recovery_next_btn_after_email = (By.ID, "username-recovery")
    recovery_back_button = (By.ID, "back-link")
    recovery_privacy_button = (By.ID, "privacy")
    recovery_page_url = "https://login3.stg.cd.id.hp.com/login3/username-recovery"

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def enter_recovery_email_address(self, email_id):
        self.type_words(self.recovery_email_address_entry, email_id)

    def clear_recovery_email_address(self):
        self.clear_field(self.recovery_email_address_entry)

    def click_back_button_recovery_email_address(self):
        self.click_me(self.recovery_back_button)

    def validate_recovery_email_address_url(self):
        assert True == self.is_current_url(ForgetUsernamePage.recovery_page_url)

    def validate_privacy_button_on_username_recovery(self):
        self.click_me(self.recovery_privacy_button)
        self.select_tab_by_index(2)
        status = self.is_current_url(self.privacy_link_url)
        assert True == status
        self.select_tab_by_index(1)

