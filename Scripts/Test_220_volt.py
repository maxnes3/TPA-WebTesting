import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class TestWebsite:

    @pytest.fixture
    def edgeDriver(self):
        driver = webdriver.Edge()
        yield driver
        driver.quit()

    def login(self, edgeDriver):
        edgeDriver.get('https://ulyanovsk.220-volt.ru/login/')
        login_input = edgeDriver.find_element(By.CSS_SELECTOR, 'input[id="user_email"]')
        login_input.send_keys('linkor2003@mail.ru')
        password_input = edgeDriver.find_element(By.CSS_SELECTOR, 'input[id="user_password"]')
        password_input.send_keys('wasd123654')
        account_submit = edgeDriver.find_element(By.CSS_SELECTOR, 'button[id="link_login"]')
        account_submit.click()
        wait = WebDriverWait(edgeDriver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/profile/"]')))

    def test_login_success(self, edgeDriver):
        self.login(edgeDriver)
        profile_element = edgeDriver.find_element(By.CSS_SELECTOR, 'a[href="/profile/"]')
        assert profile_element is not None, "Ошибка: Вход не выполнен успешно."

    def test_add_to_favorites(self, edgeDriver):
        self.login(edgeDriver)
        edgeDriver.get('https://ulyanovsk.220-volt.ru/catalog-290586/')
        favorite_add = edgeDriver.find_element(By.CSS_SELECTOR, 'a[href="/favorites/add-290586"]')
        favorite_add.click()
        wait = WebDriverWait(edgeDriver, 10)
        favorite = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'table')))
        assert favorite is not None, "Ошибка: Товар не добавлен в избранное."

    def test_remove_from_favorites(self, edgeDriver):
        self.login(edgeDriver)
        edgeDriver.get('https://ulyanovsk.220-volt.ru/profile/favorites/')
        favorite_remove = edgeDriver.find_element(By.CSS_SELECTOR, 'a[class="del-favorite"]')
        favorite_remove.click()
        wait = WebDriverWait(edgeDriver, 10)
        favorite = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//p[contains(text(), "Избранных товаров нет")]')))
        assert favorite is not None, "Ошибка: Товар не удалён из избранного."

    def test_add_to_basket(self, edgeDriver):
        self.login(edgeDriver)
        edgeDriver.get('https://ulyanovsk.220-volt.ru/catalog-409017/')
        wait = WebDriverWait(edgeDriver, 10)
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'a.ecommerce-tracked-product.in-cart.box-inline.bg-yellow-gradient')))
        basket_add = edgeDriver.find_element(By.CSS_SELECTOR,
                                             'a.ecommerce-tracked-product.in-cart.box-inline.bg-yellow-gradient')
        basket_add.click()
        order = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//p[contains(text(), "Товар добавлен в корзину")]')))
        assert order is not None, "Ошибка: Товар не добавлен в корзину."

    def test_remove_to_basket(self, edgeDriver):
        self.login(edgeDriver)
        edgeDriver.get('https://ulyanovsk.220-volt.ru/order/')
        wait = WebDriverWait(edgeDriver, 10)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a[class="btn-del"]')))
        basket_remove = edgeDriver.find_element(By.CSS_SELECTOR, 'a[class="btn-del"]')
        time.sleep(5)
        basket_remove.click()
        order = wait.until(
            EC.visibility_of_element_located((By.XPATH,
                                              '//p[contains(text(), "В вашей корзине пока нет товаров, но специально для Вас мы подобрали товары, которые могут Вас заинтересовать:")]')))
        assert order is not None, "Ошибка: Товар не удалён из избранного."

    def test_displayed_products_count(self, edgeDriver):
        edgeDriver.get('https://ulyanovsk.220-volt.ru/catalog/akkumulyatornye-dreli-shurupoverty/')
        wait = WebDriverWait(edgeDriver, 10)
        select_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "listing-select")))
        select = Select(select_element)
        select.select_by_visible_text("60")
        products = edgeDriver.find_elements(By.CSS_SELECTOR, 'li[class="box-inline v-top"]')
        assert len(products) == 60, "Ошибка: Неправильный вывод кол-во продуктов"

    def test_products_filter(self, edgeDriver):
        edgeDriver.get('https://ulyanovsk.220-volt.ru/catalog/akkumulyatornye-dreli-shurupoverty/')
        wait = WebDriverWait(edgeDriver, 10)

        # Ожидание и клик по фильтру
        filter_element = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'a[href="/catalog/dreli-shurupoverty-akkumulyatornye-18-v/"]')))
        filter_element.click()

        products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.box-inline.v-top')))

        informations = []
        for product in products:
            try:
                # Ищем элемент p внутри каждого li
                info_element = product.find_element(By.CSS_SELECTOR,
                                                    'div.new-item-list-info-small.mvlspace-10 > p.text-small.text-lh-base')
                informations.append(info_element.text)
            except:
                continue

        assert sum('18 В' in info for info in informations) == len(informations), "Ошибка фильтрации"
