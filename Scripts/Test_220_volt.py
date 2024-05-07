import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
        favorite = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'p:contains("Избранных товаров нет")')))
        assert favorite is not None, "Ошибка: Товар не удалён из избранного."
