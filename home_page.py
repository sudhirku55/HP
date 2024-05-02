from selenium.webdriver.common.by import By
from Pages_HPX.basic_actions import BasicActions
from utilities.database_operations import *


class HomePage(BasicActions):
    """ This class is used to store the PC Home Page element locator and its actions """

    hp_smart_header_title = (By.XPATH, "//span[contains(@class, 'subtitle-regular') and text()='HP Smart']")

    """ Left menu contents """
    account_dashboard_menu = (By.XPATH, '//li[@data-testid="home-menu"]/a')
    hp_one_pc_menu = (By.XPATH, '//li[@data-testid="hp-one-pcs-menu"]/a')
    hp_one_print_menu = (By.XPATH, '//li[@data-testid="hp-one-printers-menu"]/a')
    instant_ink_menu = (By.XPATH, '//li[@data-testid="print-plans-menu"]/a')
    printers_menu = (By.XPATH, '//li[@data-testid="my-printers-menu"]/a')
    solutions_menu = (By.XPATH, '//li[@data-testid="services-menu"]/a')
    account_menu = (By.XPATH, '//li[@data-testid="my-account-menu"]/a')
    help_center_menu = (By.XPATH, "//div[text()='Help Center']/parent::a")
    chat_with_virtual_assistant = (By.XPATH, '//li[@data-testid="portal-side-menu-va-button"]/a')

    account_dashboard_menu_load = (By.XPATH, "//h5[text()='Connectivity']")
    hp_one_pc_menu_load = (By.XPATH, "//p[text()='Manage address']/..")
    hp_one_print_menu_load = (By.XPATH, '//li[@data-testid="hp-one-printers-overview-submenu"]/a')
    instant_ink_menu_load = None
    printers_menu_load = (By.CLASS_NAME, "sc-fzqOul jvihTa")
    solutions_menu_load = (By.XPATH, '//li[@data-testid="hp-smart-advance-submenu"]/a')
    account_menu_load = (By.XPATH, '//li[@data-testid="subscriptions-submenu"]/a')
    help_center_menu_load = (By.XPATH, "//div[text()='About HP Smart']/parent::a")
    chat_with_virtual_assistant_load = (By.XPATH, '//button[@aria-label="Cancel"]')

    """ HP One Print Sub menu's """
    hp_one_print_overview = (By.XPATH, '//li[@data-testid="hp-one-printers-overview-submenu"]/a')
    hp_one_print_update_plan = (By.XPATH, '//li[@data-testid="hp-one-printers-update-plan-submenu"]/a')
    hp_one_print_track_shipments = (By.XPATH, '//li[@data-testid="hp-one-printers-shipment-tracking-submenu"]/a')

    hp_one_print_overview_load = (By.XPATH, '//a[@data-testid="citizens-balance-card-link"]')
    hp_one_print_update_plan_load = (By.XPATH, "//span[text()='Current Plan']")
    hp_one_print_track_shipments_load = (By.ID, "#shipment-history-table")

    """ Solution sub menu's """
    solutions_hp_smart_advance = (By.XPATH, '//li[@data-testid="hp-smart-advance-submenu"]/a')

    solutions_hp_smart_advance_load = (By.XPATH, "//span[text()='Install HP Smart']")

    """ account sub menu's """
    account_subscriptions = (By.XPATH, '//li[@data-testid="subscriptions-submenu"]/a')
    account_orders = (By.XPATH, '//li[@data-testid="orders-submenu"]/a')
    account_hp_one_statements = (By.XPATH, '//li[@data-testid="invoices-submenu"]/a')
    account_hp_one_shipping_billing = (By.XPATH, '//li[@data-testid="shipping-billing-submenu"]/a')
    account_profile = (By.XPATH, '//li[@data-testid="profile-submenu"]/a')
    account_users = (By.XPATH, '//li[@data-testid="users-submenu"]/a')
    account_notifications = (By.XPATH, '//li[@data-testid="view-notifications-submenu"]/a')

    account_subscriptions_load = (By.XPATH, "//button[text()='Cancel plan']")
    account_orders_load = (By.XPATH, '//div[@data-testid="orderAccordion"]')
    account_hp_one_statements_load = None
    account_hp_one_shipping_billing_load = (By.XPATH, "//span[text()='Edit']")
    account_profile_load = (By.XPATH, "//p[text()='First name']")
    account_users_load = (By.XPATH, "//h3[text()='Users']")
    account_notifications_load = (By.LINK_TEXT, 'View')

    """ Help Center Sub menu's """
    help_center_about_hp_smart = (By.XPATH, "//div[text()='About HP Smart']/parent::a")
    help_center_about_hp_smart_advance = (By.XPATH, '//a[@href="/us/en/ucde/help/hp-smart-advance"]')
    help_center_hp_instant_ink = (By.XPATH, '//a[@href="/us/en/ucde/help/hp-instant-ink"]')
    help_center_printer_connection_info = (By.XPATH, "//div[text()='Printer and Connection Information']/parent::a")
    help_center_print_scan_share = (By.XPATH, "//div[text()='Print, Scan, and Share']/parent::a")
    help_center_additional_help_support = (By.XPATH, "//div[text()='Additional Help and Support']/parent::a")

    help_center_about_hp_smart_load = (By.XPATH, "//h5[@data-testid='sharing-files']")
    help_center_about_hp_smart_advance_load = (By.XPATH, '//h5[@data-testid="printanywhereadvance"]')
    help_center_hp_instant_ink_load = (By.XPATH, '//a[@data-udl-link-id="section-link"]')
    help_center_printer_connection_info_load = (By.XPATH, '//div[@aria-controls="print-service-plugin"]')
    help_center_print_scan_share_load = (By.XPATH, '//div[@aria-controls="fax"]')
    help_center_additional_help_support_load = (By.XPATH, '//div[@aria-controls="hp-mobile-printing"]')

    """ Header buttons """
    notification_button = (By.XPATH, '//button[@data-testid="portal-notifications-button"]')
    avatar_button = (By.ID, 'menu-avatar-container')

    """ Dashboard labels """
    general_label = (By.XPATH, '//h5[text()="General"]')
    status_label = (By.XPATH, '//h5[text()="Status"]')
    connectivity_label = (By.XPATH, '//h5[text()="Connectivity"]')
    owner_printers_label = (By.XPATH, '//h5[text()="Owned Printers"]')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.page_load_wait = 60

    def check_elements_visibility(self):
        self.my_logger.info("Checking the HOME PAGE ELEMENTS VISIBILITIES ")
        basic_actions = BasicActions(self.driver, self.my_logger)
        variables = {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("__") and not callable(value) and isinstance(value, tuple)
        }
        for variable in variables:
            appeared_status = basic_actions.element_displayed(variable)
            if appeared_status is not True:
                basic_actions.click_menu_button(self.account_menu)
                basic_actions.click_menu_button(self.help_center)
                appeared_status = basic_actions.element_displayed(variable)
            assert appeared_status == True

    def click_account_dashboard_menu(self):
        self.click_menu_button(self.account_dashboard_menu)
        self.wait_for_object(self.account_dashboard_menu_load, self.page_load_wait)

    def check_avatar_initial(self, initial):
        return self.element_displayed((By.XPATH, f'//span[text()="{initial}"]'))

    def click_hp_one_pc_left_menu(self):
        self.click_menu_button(self.hp_one_pc_menu)
        self.wait_for_object(self.hp_one_pc_menu_load, self.page_load_wait)

    def click_hp_one_print_menu(self):
        self.click_menu_button(self.hp_one_print_menu)
        self.wait_for_object(self.hp_one_print_menu_load, self.page_load_wait)

    def click_instant_ink_menu(self):
        self.click_menu_button(self.instant_ink_menu)
        self.wait_for_object(self.instant_ink_menu_load, self.page_load_wait)

    def click_printers_menu(self):
        self.click_menu_button(self.printers_menu)
        self.wait_for_object(self.printers_menu_load, self.page_load_wait)

    def click_solutions_menu(self):
        self.click_menu_button(self.solutions_menu)
        self.wait_for_object(self.solutions_menu_load, self.page_load_wait)

    def click_account_menu(self):
        self.click_menu_button(self.account_menu)
        self.wait_for_object(self.account_menu_load, self.page_load_wait)

    def click_help_center_menu(self):
        self.click_menu_button(self.help_center_menu)
        self.wait_for_object(self.help_center_menu_load, self.page_load_wait)

    def click_chat_with_virtual_assistant_menu(self):
        self.click_menu_button(self.chat_with_virtual_assistant)
        self.wait_for_object(self.chat_with_virtual_assistant_load, self.page_load_wait)

    def validate_pc_left_menu(self):
        self.wait_for_object(self.account_dashboard_menu)
        self.wait_for_object(self.hp_one_pc_menu, 2)
        self.wait_for_object(self.instant_ink_menu, 2)
        self.wait_for_object(self.printers_menu, 2)
        self.wait_for_object(self.solutions_menu, 2)
        self.wait_for_object(self.account_menu, 2)
        self.wait_for_object(self.help_center_menu, 2)
        self.wait_for_object(self.chat_with_virtual_assistant, 2)

    """ HPOne Print sub menu click's"""

    def click_hp_one_print_overview(self):
        self.click_menu_button(self.hp_one_print_overview)
        self.wait_for_object(self.hp_one_print_overview_load, self.page_load_wait)

    def click_hp_one_print_update_plan(self):
        self.click_menu_button(self.hp_one_print_update_plan)
        self.wait_for_object(self.hp_one_print_update_plan_load, self.page_load_wait)

    def click_hp_one_print_track_shipments(self):
        self.click_menu_button(self.hp_one_print_track_shipments)
        self.wait_for_object(self.hp_one_print_track_shipments_load, self.page_load_wait)

    """ Solution sub menu click's """

    def click_solutions_hp_smart_advance(self):
        self.click_menu_button(self.solutions_hp_smart_advance)
        self.wait_for_object(self.solutions_hp_smart_advance_load, self.page_load_wait)

    """ Account sub menu click's """

    def click_account_subscriptions_menu(self):
        self.click_sub_menu_button(self.account_menu, self.account_subscriptions)
        self.wait_for_object(self.account_subscriptions_load, self.page_load_wait)

    def click_account_orders_menu(self):
        self.click_sub_menu_button(self.account_menu, self.account_orders)
        self.wait_for_object(self.account_orders_load, self.page_load_wait)

    def click_account_hp_one_statements(self):
        self.click_sub_menu_button(self.account_menu, self.account_hp_one_statements)
        self.wait_for_object(self.account_hp_one_statements_load, self.page_load_wait)

    def click_account_shipping_billing(self):
        self.click_sub_menu_button(self.account_menu, self.account_hp_one_shipping_billing)
        self.wait_for_object(self.account_hp_one_shipping_billing_load, self.page_load_wait)

    def click_account_profile_menu(self):
        self.click_sub_menu_button(self.account_menu, self.account_profile)
        self.wait_for_object(self.account_profile_load, self.page_load_wait)

    def click_account_users_menu(self):
        self.click_sub_menu_button(self.account_menu, self.account_users)
        self.wait_for_object(self.account_users_load, self.page_load_wait)

    def click_account_notifications_menu(self):
        self.click_sub_menu_button(self.account_menu, self.account_notifications)
        self.wait_for_object(self.account_notifications_load, self.page_load_wait)

    """ Help Center sub menu click's """
    def click_help_center_about_hp_smart(self):
        self.click_sub_menu_button(self.help_center_menu, self.help_center_about_hp_smart)
        self.wait_for_object(self.help_center_about_hp_smart_load, self.page_load_wait)

    def click_help_center_hp_smart_advance(self):
        self.click_sub_menu_button(self.help_center_menu, self.help_center_about_hp_smart_advance)
        self.wait_for_object(self.help_center_about_hp_smart_advance_load, self.page_load_wait)

    def click_help_center_hp_instant_ink(self):
        self.click_sub_menu_button(self.help_center_menu, self.help_center_hp_instant_ink)
        self.wait_for_object(self.help_center_hp_instant_ink_load, self.page_load_wait)

    def click_help_center_printer_connection_info(self):
        self.click_sub_menu_button(self.help_center_menu, self.help_center_printer_connection_info)
        self.wait_for_object(self.help_center_printer_connection_info_load, self.page_load_wait)

    def click_help_center_print_scan_share(self):
        self.click_sub_menu_button(self.help_center_menu, self.help_center_print_scan_share)
        self.wait_for_object(self.help_center_print_scan_share_load, self.page_load_wait)

    def click_help_center_additional_help_and_support(self):
        self.click_sub_menu_button(self.help_center_menu, self.help_center_additional_help_support)
        self.wait_for_object(self.help_center_additional_help_support_load, self.page_load_wait)

    """ Dashboard Verifications """
    def check_dashboard_labels(self):
        self.wait_for_object(self.general_label)
        self.wait_for_object(self.status_label, 2)
        self.wait_for_object(self.connectivity_label, 2)
        self.wait_for_object(self.owner_printers_label, 2)
