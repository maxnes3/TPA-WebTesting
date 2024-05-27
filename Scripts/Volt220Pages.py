import SeleniumController as sc


class LoginPage:

    def get_login_screen(self, driver):
        sc.get_URL(driver, 'https://ulyanovsk.220-volt.ru/login/')

    def enter_login(self, driver):
        sc.input_value(driver, 'input[id="user_email"]', 'linkor2003@mail.ru')

    def enter_password(self, driver):
        sc.input_value(driver, 'input[id="user_password"]', 'wasd123654')

    def submit_login(self, driver):
        sc.submit_element(driver, 'button[id="link_login"]')

    def assert_profile(self, driver):
        return sc.wait_css_selector_presence(driver, 'a[href="/profile/"]')


class FavoritePage:

    def get_product_screen(self, driver):
        sc.get_URL(driver, 'https://ulyanovsk.220-volt.ru/catalog-290586/')

    def get_favorites_screen(self, driver):
        sc.get_URL(driver, 'https://ulyanovsk.220-volt.ru/profile/favorites/')

    def submit_add_to_favorites(self, driver):
        sc.submit_element(driver, 'a[href="/favorites/add-290586"]')

    def submit_remove_from_favorites(self, driver):
        sc.submit_element(driver, 'a[class="del-favorite"]')

    def assert_add_to_favorites(self, driver):
        return sc.wait_css_selector_visibility(driver, 'table')

    def assert_remove_from_favorites(self, driver):
        return sc.wait_xpath_visibility(driver, '//p[contains(text(), "Избранных товаров нет")]')


class BasketPage:

    def get_product_screen(self, driver):
        sc.get_URL(driver, 'https://ulyanovsk.220-volt.ru/catalog-409017/')

    def get_basket_screen(self, driver):
        sc.get_URL(driver, 'https://ulyanovsk.220-volt.ru/order/')

    def submit_add_to_basket(self, driver):
        sc.wait_css_selector_visibility(driver, 'a.ecommerce-tracked-product.in-cart.box-inline.bg-yellow-gradient')
        sc.submit_element(driver, 'a.ecommerce-tracked-product.in-cart.box-inline.bg-yellow-gradient')

    def submit_remove_from_basket(self, driver):
        sc.wait_css_selector_visibility(driver, 'a[class="btn-del"]')
        sc.submit_element_with_sleep(driver, 'a[class="btn-del"]')

    def assert_add_to_basket(self, driver):
        return sc.wait_xpath_visibility(driver, '//p[contains(text(), "Товар добавлен в корзину")]')

    def assert_remove_from_basket(self, driver):
        return sc.wait_xpath_visibility(driver,
                                 '//p[contains(text(), "В вашей корзине пока нет товаров, но специально для Вас мы подобрали товары, которые могут Вас заинтересовать:")]')


class CatalogPage:

    def get_catalog_screen(self, driver):
        sc.get_URL(driver, 'https://ulyanovsk.220-volt.ru/catalog/akkumulyatornye-dreli-shurupoverty/')

    def select_products_count(self, driver):
        sc.select_option(driver, "listing-select", "60")

    def submit_products_filter(self, driver):
        sc.submit_element(driver, 'a[href="/catalog/dreli-shurupoverty-akkumulyatornye-18-v/"]')

    def assert_products_count(self, driver):
        return sc.find_css_selector_list(driver, 'li[class="box-inline v-top"]')

    def assert_products_filter(self, driver):
        products = sc.wait_css_selector_list(driver, 'li.box-inline.v-top')
        return sc.foreach_css_selector(products,
                                               'div.new-item-list-info-small.mvlspace-10 > p.text-small.text-lh-base')
