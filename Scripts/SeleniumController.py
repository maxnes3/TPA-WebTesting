from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time


def get_URL(driver, url):
    driver.get(url)


def find_css_selector(driver, element):
    return driver.find_element(By.CSS_SELECTOR, element)


def find_css_selector_list(driver, element):
    return driver.find_elements(By.CSS_SELECTOR, element)


def foreach_css_selector(list, value):
    elements = []
    for li in list:
        try:
            element = li.find_element(By.CSS_SELECTOR, value)
            elements.append(element.text)
        except:
            continue
    return elements


def input_value(driver, element, value):
    input_element = find_css_selector(driver, element)
    input_element.send_keys(value)


def submit_element(driver, element):
    submit = wait_css_selector_clickable(driver, element)
    submit.click()


def submit_element_with_sleep(driver, element):
    submit = wait_css_selector_clickable(driver, element)
    time.sleep(5)
    submit.click()


def wait_css_selector_presence(driver, element):
    wait = WebDriverWait(driver, 10)
    return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, element)))


def wait_css_selector_visibility(driver, element):
    wait = WebDriverWait(driver, 10)
    return wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, element)))


def wait_css_selector_clickable(driver, element):
    wait = WebDriverWait(driver, 10)
    return wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, element)))


def wait_xpath_visibility(driver, element):
    wait = WebDriverWait(driver, 10)
    return wait.until(
        EC.visibility_of_element_located((By.XPATH, element)))


def wait_css_selector_list(driver, element):
    wait = WebDriverWait(driver, 10)
    return wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, element)))


def select_option(driver, element, value):
    wait = WebDriverWait(driver, 10)
    select_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, element)))
    select = Select(select_element)
    select.select_by_visible_text(value)
