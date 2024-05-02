from selenium.webdriver.common.by import By
from Pages_HPX.basic_actions import *
import subprocess


class PasswordPage(BasicActions):
    """
        This class is used to store the password page locator and actions
        Note: BasicActions class has imported to access the web actions with exception handling
    """
    password_input_box_id = (By.ID, "password")
    password_toggle_visibility_xpath = (By.XPATH, "//div[@aria-label='Toggle password visibility']")
    sign_in_xpath = (By.XPATH, '//button[@id="sign-in"]/parent::div')
    forget_password_link = (By.ID, 'forgot-cred')
    privacy_link_id = (By.ID, 'privacy')
    back_button_id = (By.ID, 'back-link')
    wrong_password_alert = (By.XPATH, "//span[text()='Invalid username or password']")
    no_password_alert = (By.XPATH, "//span[text()='Enter your password']")
    window_title = "HPID Login"

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def enter_password(self, password):
        self.wait_for_object(self.password_input_box_id, self.basic_wait_time)
        print(password)
        password = convert_password(password)
        print(password)
        self.type_words(self.password_input_box_id, password)

    def click_signin_button(self):
        self.click_me(self.sign_in_xpath)

    def check_element_visibilities(self):
        variables = {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("__") and not callable(value) and isinstance(value, tuple)
        }
        for variable in variables:
            appeared_status = self.element_displayed(variable)
            assert True == appeared_status

    def verify_entered_mail_id(self, mail_id):
        self.wait_for_object((By.XPATH, f"//p[text()='{mail_id}']"))

    def validate_avatar(self, initials):
        self.wait_for_object((By.XPATH, f'//span[text()="{initials}"]'), self.wait_for_45_seconds)

    def no_password_alert_should_appear(self):
        self.wait_for_object(self.no_password_alert, 2)
        assert True == self.element_displayed(self.no_password_alert)

    def wrong_password_alert_should_appear(self):
        self.wait_for_object(self.wrong_password_alert, self.wait_for_45_seconds)
        assert True == self.element_displayed(self.wrong_password_alert)

    def click_on_back_link_button(self):
        self.click_me(self.back_button_id)

    def click_on_privacy_button_validate_url(self):
        self.click_me(self.privacy_link_id)
        self.select_tab_by_index(2)
        status = self.is_current_url(self.privacy_link_url)
        assert True == status
        self.select_tab_by_index(1)


class ForgetPasswordPageMobileNumber(BasicActions):

    forget_password_iso_code_drop_down = (By.ID, "isoCode")
    forget_password_mobile_number_entry = (By.ID, "phoneNumber")
    forget_password_switch_email_address = (By.ID, "switch-username")
    forget_password_next_button = (By.ID, "password-recovery")
    forget_password_back_link = (By.ID, "back-link")
    forget_password_privacy_button = (By.ID, "privacy")
    search_box_iso_code = (By.XPATH, '//input[@placeholder="Search"]')

    def __init__(self, driver, logger, iso_code, mobile_number):
        super().__init__(driver, logger)
        self.driver = driver
        self.logger = logger
        self.iso_code = iso_code
        self.recovery_mobile_number = mobile_number

    def enter_mobile_number(self, mobile_number=None):
        self.log_my_keyword_name_and_arguments()
        if mobile_number is None:
            mobile_number = self.recovery_mobile_number
        self.type_words(self.forget_password_mobile_number_entry, mobile_number)

    def clear_mobile_number(self):
        self.log_my_keyword_name_and_arguments()
        self.clear_field(self.forget_password_mobile_number_entry)

    def click_on_switch_email_address(self):
        self.log_my_keyword_name_and_arguments()
        self.click_me(self.forget_password_switch_email_address)

    def click_on_next_button(self):
        self.log_my_keyword_name_and_arguments()
        self.click_me(self.forget_password_next_button)

    def click_on_back_link(self):
        self.log_my_keyword_name_and_arguments()
        self.click_me(self.forget_password_back_link)

    def set_iso_code(self, iso_code) :
        self.log_my_keyword_name_and_arguments()
        self.click_me(self.forget_password_iso_code_drop_down)
        self.type_words(self.search_box_iso_code, iso_code)
        self.click_me((By.XPATH, f"//div[@title='{iso_code}']"))

    def click_on_privacy_button_validate_url(self):
        self.click_me(self.forget_password_privacy_button)
        self.select_tab_by_index(2)
        status = self.is_current_url(self.privacy_link_url)
        assert True == status
        self.select_tab_by_index(1)


class ForgetPasswordPageEmail(BasicActions):

    recovery_password_entry = (By.ID, "recoveryInput")
    recovery_password_use_mobile_entry = (By.ID, "switch-username")
    recovery_password_next_button = (By.ID, "password-recovery")
    recovery_password_back_button = (By.ID, "back-link")
    recovery_password_url = "https://login3.stg.cd.id.hp.com/login3/password-recovery"
    recovery_password_privacy_button = (By.ID, "privacy")

    def __init__(self, driver, logger, email_id):
        super().__init__(driver, logger)
        self.driver = driver
        self.logger = logger
        self.recovery_email_id = email_id

    def enter_recovery_email_address(self, email_id=None):
        if email_id is None:
            email_id = self.recovery_email_id
        self.type_words(self.recovery_password_entry, email_id)

    def clear_recovery_email(self):
        self.clear_field(self.recovery_password_entry)

    def validate_forget_password_url(self):
        assert True == self.is_current_url(self.recovery_password_url)

    def get_recovery_user_name_entered(self):
        return self.get_attribute_value(self.recovery_password_entry, "value")

    def click_on_next_button(self):
        self.click_me(self.recovery_password_next_button)

    def click_on_back_link(self):
        self.click_me(self.recovery_password_back_button)

    def click_on_use_mobile_number_instead(self):
        self.click_me(self.recovery_password_use_mobile_entry)

    def click_on_privacy_button_validate_url(self):
        self.click_me(self.recovery_password_privacy_button)
        self.select_tab_by_index(2)
        status = self.is_current_url(self.privacy_link_url)
        assert True == status
        self.select_tab_by_index(1)
