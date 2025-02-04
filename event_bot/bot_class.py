from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException


def generate_dates():
    today = datetime.now()
    available_dates = []
    for i in range(7):
        new_date = today + timedelta(i)
        available_dates.append(f'{new_date.day}/{new_date.month}')
    return available_dates


# converts a date string from 'dd/mm' to a list of integers [day, month]
def convert_date(date):
    res_date = [int(i) for i in date.split('/')]
    return res_date


class EventBot:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.restart_driver()

    # method restarts or creates a new driver to start a new session
    def restart_driver(self):
        options = Options()
        options.add_argument("user-agent=Mozilla/5.0")
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        if self.driver:
            self.driver.quit()
            self.driver = None
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 20)

    def open_main_page(self):
        self.restart_driver()
        url = 'https://afisha.relax.by/'
        self.driver.get(url)
        try:
            self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '.cookiesNotificationBy__control--button.--disable'))).click()
        except {WebDriverException, TimeoutException}:
            self.restart_driver()

    # method extracts available categories from the main page
    def get_categories_list(self):
        event_types = self.driver.find_elements(By.CLASS_NAME, 'b-where-to_heading')
        event_types_list = [i.find_element(By.CSS_SELECTOR, 'a').text.strip() for i in event_types]
        return event_types_list

    def open_selected_category(self, event):
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f'//*[@id="append-shcedule"]/section/div/h2/a[contains(text(),"{event}")]'))).click()

    # method generates dates for the next 7 days
    def get_available_dates(self):
        return generate_dates()

    # method opens the calendar and selects the desired date
    def select_date(self, date):
        date = convert_date(date)
        selected_day = date[0]
        selected_month = date[1]
        calendar_tab = self.driver.find_element(By.ID, 'datepicker')
        calendar_tab.click()

        # switches to the next month if necessary
        if selected_month != int(datetime.now().month):
            next_month_button = self.driver.find_element(By.CSS_SELECTOR, '.ui-datepicker-next.ui-corner-all')
            next_month_button.click()

        # checks if the date is available
        try:
            selected_day_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, f"//*[@class='ui-datepicker-calendar']//td/a[text()='{selected_day}']")))
            selected_day_button.click()
            return True
        except TimeoutException:
            return False

    def get_locations_list(self):
        location_btn = self.driver.find_element(By.ID, 'title_places')
        location_btn.click()
        locations_list = [i.find_element(By.XPATH, ".//*").text.strip() for i in
                          self.driver.find_elements(By.CLASS_NAME, 'b-playbill_options_item_cinemas_item') if
                          i.text != '']
        del locations_list[0]
        return locations_list

    def select_location(self, location):
        # waiting until the selected location is available for clicking
        xpath = f'//*[@class="b-playbill_options_item_cinemas"]//li//a[contains(text(),"{location}")]'
        self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

        # wating for unnecessary events to disappear in order to collect only the necessary ones
        try:
            old_count = len(self.driver.find_elements(By.CSS_SELECTOR, '.schedule__item.table_by_place'))
            self.wait.until(lambda driver: len(
                driver.find_elements(By.CSS_SELECTOR, '.schedule__item.table_by_place')) != old_count)
        # for cases when there are events only at the selected location on the chosen day
        except TimeoutException:
            pass

    def get_result_events(self):
        result = []
        events_on_location = self.driver.find_elements(By.CSS_SELECTOR, '.schedule__item.table_by_place')

        if len(events_on_location) == 0:
            return False

        for event in events_on_location:
            try:
                name = event.find_element(By.CSS_SELECTOR, 'a').text
                # there are two types of event displays on the site
                try:
                    time_options = [i.text for i in event.find_elements(By.CSS_SELECTOR,
                                                                        '.schedule__seance-time.schedule__seance--buy.js-buy-ticket')]
                    time = ' '.join(el for el in time_options)
                    price = event.find_element(By.CSS_SELECTOR, '.seance-price').text
                except:
                    time_options = [i.text for i in event.find_elements(By.CSS_SELECTOR, '.schedule__seance-time')]
                    time = ' '.join(el for el in time_options)
                    price = 'уточняйте на сайте'

                result.append(f'Название: {name}\nВремя: {time}\nЦена: {price}\n\n')
            # skip broken data
            except WebDriverException:
                continue
        return result
