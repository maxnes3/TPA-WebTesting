import pytest
from selenium import webdriver
from Volt220Pages import LoginPage
from Volt220Pages import FavoritePage
from Volt220Pages import BasketPage
from Volt220Pages import CatalogPage


class TestWebsite:

    @pytest.fixture
    def edgeDriver(self):
        driver = webdriver.Edge()
        yield driver
        driver.quit()

    def login(self, edgeDriver):
        page = LoginPage()
        page.get_login_screen(edgeDriver)
        page.enter_login(edgeDriver)
        page.enter_password(edgeDriver)
        page.submit_login(edgeDriver)
        page.assert_profile(edgeDriver)

    def test_login_success(self, edgeDriver):
        self.login(edgeDriver)
        page = LoginPage()
        assert page.assert_profile(edgeDriver) is not None, "Ошибка: Вход не выполнен успешно."

    def test_add_to_favorites(self, edgeDriver):
        self.login(edgeDriver)
        page = FavoritePage()
        page.get_product_screen(edgeDriver)
        page.submit_add_to_favorites(edgeDriver)
        assert page.assert_add_to_favorites(edgeDriver) is not None, "Ошибка: Товар не добавлен в избранное."

    def test_remove_from_favorites(self, edgeDriver):
        self.login(edgeDriver)
        page = FavoritePage()
        page.get_favorites_screen(edgeDriver)
        page.submit_remove_from_favorites(edgeDriver)
        assert page.assert_remove_from_favorites(edgeDriver) is not None, "Ошибка: Товар не удалён из избранного."

    def test_add_to_basket(self, edgeDriver):
        self.login(edgeDriver)
        page = BasketPage()
        page.get_product_screen(edgeDriver)
        page.submit_add_to_basket(edgeDriver)
        assert page.assert_add_to_basket(edgeDriver) is not None, "Ошибка: Товар не добавлен в корзину."

    def test_remove_to_basket(self, edgeDriver):
        self.login(edgeDriver)
        page = BasketPage()
        page.get_basket_screen(edgeDriver)
        page.submit_remove_from_basket(edgeDriver)
        assert page.assert_remove_from_basket(edgeDriver) is not None, "Ошибка: Товар не удалён из избранного."

    def test_displayed_products_count(self, edgeDriver):
        page = CatalogPage()
        page.get_catalog_screen(edgeDriver)
        page.select_products_count(edgeDriver)
        products = page.assert_products_count(edgeDriver)
        assert len(products) == 60, "Ошибка: Неправильный вывод кол-во продуктов"

    def test_products_filter(self, edgeDriver):
        page = CatalogPage()
        page.get_catalog_screen(edgeDriver)
        page.submit_products_filter(edgeDriver)
        information = page.assert_products_filter(edgeDriver)
        assert sum('18 В' in info for info in information) == len(information), "Ошибка фильтрации"
