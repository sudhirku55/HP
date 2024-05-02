from Pages_HPX.email_page import *
from Pages_HPX.password_page import *
from Pages_HPX.home_page import *


class CommonUtils(BasicActions):
    """
     This is a class where we can use the general keywords for all work streams
    """
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.alert_handler = (By.ID, "onetrust-accept-btn-handler")
        self.error_msg_1 = (By.XPATH, "//*[text()='Something went wrong']")
        self.error_msg_2 = (By.XPATH, "//*[text()='timeout exceeded']")
        self.error_msg_3 = (By.XPATH, "//*[text()='Something unexpected happened']")
        self.citizen_pay_link = "https://pay.citizensbank.com/auth/login"

    def alert_clear(self):
        self.wait_for_object(self.alert_handler, 45)
        self.click_me(self.alert_handler)

    def signin_to_portal_using_mail_id(self, mail_id, password, avatar_initials):
        """
         This keyword will help you to log in to application
            1. mail_id : Mail ID of the user's
            2. password : Password to type
            3. avatar_initials : Avatar Initial to verify its availability
        """
        email_page = EmailPage(self.driver)
        email_page.enter_username(mail_id)
        email_page.click_next_button()
        password_page = PasswordPage(self.driver)
        password_page.verify_entered_mail_id(mail_id)
        password_page.enter_password(password)
        password_page.click_signin_button()
        self.alert_clear()
        password_page.validate_avatar(avatar_initials)

    def fetch_access_token(self):
        datas = self.get_value_from_cookie()
        print(datas)
        for data in datas:
            if data['name'] == 'stratus-access-token':
                print(data['value'])
                token_value = data['value']
        self.my_logger.info(f"Received token value is: {token_value}")
        return token_value

    @staticmethod
    def collect_credentials(sheet_name="ECOMMERCE", type_of_data="pc", fetch_fields=["Username", "Password", "Avatar"]):
        data = fetch_credentials(sheet_name, type_of_data, fetch_fields=fetch_fields)
        return data

    def error_should_not_appear(self):
        self.wait_for_object_disappear(self.error_msg_1, 2)
        self.wait_for_object_disappear(self.error_msg_2, 2)
        self.wait_for_object_disappear(self.error_msg_3, 2)

    def click_on_citizen_pay_validate(self, citizen_pay_locator):
        self.click_me(citizen_pay_locator)
        self.select_tab_by_index(2)
        status = self.is_current_url(self.citizen_pay_link)
        assert True == status
        self.close_current_opened_tab()
        self.select_tab_by_index(1)
