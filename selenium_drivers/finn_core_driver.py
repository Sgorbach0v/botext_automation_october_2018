import time
from config.creds import credentials
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class finn_core_messenger_bot:
    """Data handling class with selenium for finn core in messenger

    sda
    """

    def __init__(self, driver):
        self.driver = driver


    def login_to_messenger(self, args):
        """Login to messenger.

        Arguments:
        args -- list of arguments. Here args[0] is alwasys 'Get Started'
        """
        # get login and password elements
        username_field = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.ID,"email")))
        password_field = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.ID,"pass")))

        # TODO: provide username and password #get variables from the .env
        username_field.send_keys(credentials['finn core']['username'])
        password_field.send_keys(credentials['finn core']['password'])

        # get login button and click
        login_button = self.driver.find_element_by_id("loginbutton")
        login_button.click()

        self.get_started(args)


    def get_started(self, query):
        # get 'Get Started' element and click on it
        try:
            get_started = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT, query[0])))
            get_started.click()
            time.sleep(5)
        except Exception as e:
            print('No Get Started present')
            print(e)



    #find index of the last item on the right
    def last_right_index(self, list_of_items, last_right_item):
        index = [x[0] for x in enumerate(list_of_items) if last_right_item in x]
        return index[-1]

    def verify_text_response(self, query):
        # TODO: check waiting time
        time.sleep(5)

        # get all text responses in a list
        all_selenium_elements = self.driver.find_elements_by_xpath('//span[@class="_3oh- _58nk"]')
        list_of_all_selenium_elements_text = [x.text for x in all_selenium_elements]

        # get index of last text response on the right == last user query
        all_elements_on_the_right = self.driver.find_elements_by_xpath('//div[@class="_3058 _ui9 _hh7 _s1- _52mr _43by _3oh-"][@data-tooltip-position="right"]')
        all_elements_on_the_right_text = [x.text for x in all_elements_on_the_right]

        last_element_on_the_right = all_elements_on_the_right_text[-1]

        #get all bot responses after the user query
        index_of_last_right = self.last_right_index(list_of_all_selenium_elements_text, last_element_on_the_right)
        list_of_bot_responses = list_of_all_selenium_elements_text[index_of_last_right + 1:]

        #self.last_right_index(list_of_all_selenium_elements_text, last_element_on_the_right)
        return list_of_bot_responses


    def verify_qr_text(self, args):

        list_of_QR_items = []

        # read info from the carousel: read -> click forward -> read -> click forward
        while True:
            try:
                # reading QRs and saving them if not present already
                QRs_selenium_objects = self.driver.find_elements_by_xpath('//div[@class="_10-e"]')
                for element in QRs_selenium_objects:
                    if element.text not in list_of_QR_items:
                        list_of_QR_items.append(element.text)

                # forward button click
                self.click_forward()
            except:
                break

        QRs_selenium_no_empty_list = list(filter(None, [x for x in list_of_QR_items]))

        return QRs_selenium_no_empty_list


    def take_screenshot(self,title):
        self.driver.save_screenshot("../reports/screenshots/"+title+".png")


    #send a query
    def send_query(self, args):
        while True:
            try:
                active_element = self.driver.switch_to.active_element
                active_element.send_keys(args[0])
                send_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Send')))
                send_button.click()
                break
            except:
                message_field = self.driver.find_element_by_class_name('_1mf')
                message_field.click()
                continue

        time.sleep(4)

    #go to secure login
    def authenticate(self, args):
        try:
            self.send_query(['login'])
            self.click_go_to_secure_login()
            self.enter_username_and_password_for_secure_login()
        except:
            print('    Already authenticated. Continue...')

    def click_go_to_secure_login(self):
        go_to_secure_login = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT,'🔒Go to secure login')))
        go_to_secure_login.click()

    #enter username and login for bank
    def enter_username_and_password_for_secure_login(self):
        #switch to iframe
        self.driver.switch_to.frame(self.driver.find_element_by_name("messenger_ref"))

        # get login and password elements
        username_field = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "username")))
        password_field = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "password")))

        #provide username and password TODO: get username and password from .env
        username_field.send_keys('123')
        password_field.send_keys('123')
        time.sleep(2)

        #click on login button
        login_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, 'button')))
        login_button.click()
        time.sleep(2)

        #switch back to default frame
        self.driver.switch_to.default_content()
        time.sleep(2)

    #USE THIS AS THE EXAMPLE FOR THE REST OF THE FUNCTIONS
    #click on a QR based on provided text
    def click_on_qr(self, QR_text):
        QR_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="_10-e" and text()="'+QR_text[0]+'"]')))
        QR_button.click()
        time.sleep(10)


    #get account names and their balances from carousels
    def verify_account_names_and_amounts(self, args):
        time.sleep(5)
        list_of_carousel_items = []

        #read info from the carousel: read -> click forward -> read -> click forward
        while True:
            try:

                #reading info from carousel items and saving them if not present already
                account_and_amounts_selenium = self.driver.find_elements_by_class_name('_3cne')
                for element in account_and_amounts_selenium:
                    if element.text not in list_of_carousel_items:
                        list_of_carousel_items.append(element.text)

                # forward button click
                self.click_forward()

            except:
                break


        final_carousel_items = []

        #splitting result into separate lines if it's multiline and deleting empty ones
        for final_element in list_of_carousel_items:
            #if response is multiline
            if '\n' in final_element:
                #split by line and add to the list
                    for z in final_element.split('\n'):
                        final_carousel_items.append(z)
            #if empty
            elif final_element == '':
                continue

            else:
                final_carousel_items.append(final_element)

        return final_carousel_items


    def verify_button_name(self, args):
        button_to_verify = WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable((By.CLASS_NAME, '_3cnp')))
        button_to_verify_text = []
        button_to_verify_text.append(button_to_verify.text)
        return button_to_verify_text


    #click on persistent menu
    def click_on_persistent_menu(self, option):
        #get the hamburger button (three horizontal lines icon) and click on it
        hamburger_button = self.driver.find_element_by_class_name('_3km2')
        hamburger_button.click()

        #click on the option and if it's not there click 'more' and click on the option
        try:
            # get the option to click object and click on it
            option_to_click = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, option[0].replace('select ', ''))))
            option_to_click.click()

        except Exception as e:
            # get 'more' button and click on it
            more_button = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.LINK_TEXT, 'More')))
            more_button.click()

            # get the option to click object and click on it
            option_to_click = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, option[0].replace('select ', ''))))
            option_to_click.click()
            # TODO: add a printer function or handle errors in a different place

        time.sleep(7)


    def click_forward(self):
        # forward button click
        forward_button = self.driver.find_element_by_xpath("//div[@direction='forward']")
        forward_button.click()
        time.sleep(0.5)


    def click_on_view_transactions(self, account_name):

        time.sleep(5)

        #find carousel item for requested account name
        while True:
            try:
                account_name_selenium = WebDriverWait(self.driver, 1).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="_3cni" and text()="' + account_name[0] + '"]')))
            #self.driver.find_element_by_xpath('//div[@class="_3cni" and text()="' + account_name[0] + '"]')
                break
            except:
                self.click_forward()

        #find the button 'View transactions' and click on it
        while True:
            parent_element = account_name_selenium.find_element_by_xpath('..')
            account_name_selenium = parent_element
            if parent_element.get_attribute('class') == '_3cne':
                parent_element_sibling = parent_element.find_element_by_xpath('following-sibling::div')
                parent_element_sibling.click()
                break


        time.sleep(10)


    def get_div_after_last_query(self):
        #1. get the last text sent to bot

        # all elements on the right
        all_elements_on_the_right = self.driver.find_elements_by_xpath('//div[@class="_3058 _ui9 _hh7 _s1- _52mr _43by _3oh-"]')

        # get the last one on the right

        # get all next div siblings or just the next one

        pass



    ### CAROUSELS
    #make it methods
    #click on the action (view transactions or view categories)
    def action_click_1_argument_carousel(self, account_or_transaction_name):
        while True:
            parent_element = account_or_transaction_name.find_element_by_xpath('..')
            account_or_transaction_name = parent_element
            if parent_element.get_attribute('class') == '_3cne':
                parent_element_sibling = parent_element.find_element_by_xpath('following-sibling::div')
                parent_element_sibling.click()
                break


    def action_click_2_arguments_carousel(self, category_or_date, action):
        while True:
            parent_element = category_or_date.find_element_by_xpath('..')
            category_or_date = parent_element
            if parent_element.get_attribute('class') == '_3cne':
                parent_element_sibling = parent_element.find_element_by_xpath('following-sibling::div and text()="'+ action +'"')
                parent_element_sibling.click()
                break


    # check spending - time period - view categories or show weekly/monthly
    def view_categories(self, action):

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "_3cnp")))

        action = self.driver.find_element_by_xpath('//a[@class="_3cnp" and text()="' + action[0] + '"]')
        action.click()
        time.sleep(10)


    # def verify_all_account_names_and_balances(self, account_name):
    #     account_name = self.driver.find_element_by_xpath('//div[@class="_3cni" and text()="' + account_name[0] + '"]')
    #     self.action_click_1_argument_carousel(account_name)
    #     time.sleep(7)

    # get balance - view transactions for an account name - flag as fraud transactions
    def flag_as_fraud(self, transaction_name):
        transaction_name = self.driver.find_element_by_xpath('//div[@class="_3cni" and text()="' + transaction_name[0] + '"]')
        self.action_click_1_argument_carousel(transaction_name)
        time.sleep(5)

    #check spending - time period - view categories - view transactions for a category
    def view_transactions_for_categories(self, category_name):
        category_name = self.driver.find_element_by_xpath('//div[@class="_3cni" and text()="' + category_name[0] + '"]')
        self.action_click_1_argument_carousel(category_name)
        time.sleep(5)

    # check spending - time period (last month) - view categories - show weekly
    def show_weekly(self, args): #date, action arguments
        date = self.driver.find_element_by_xpath('//div[@class="_3cni" and text()="' + args[0] + '"]')
        self.action_click_2_arguments_carousel(date, args[1])
        time.sleep(5)

    # check spending - time period (last year) - view categories - show monthly
    def show_monthly(self, args):
        date = self.driver.find_element_by_xpath('//div[@class="_3cni" and text()="' + args[0] + '"]')
        self.action_click_2_arguments_carousel(date, args[1])
        time.sleep(5)

