from django.test import LiveServerTestCase, SimpleTestCase
from selenium.webdriver.chrome.webdriver import WebDriver


class MainPageTests(SimpleTestCase):
    def test_main_page_status(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)

    def test_main_page_content(self):
        response = self.client.get("")
        self.assertContains(response, "textarea")
        self.assertContains(response, "user_code")
        self.assertContains(response, "std_io")
        self.assertContains(response, "button")


CODE = """def f(word):
    return word
print(f(input()))
print(f(input()))
"""


class FunctionalTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = WebDriver()
        cls.browser.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_hello_world(self):
        self.browser.get("%s%s" % (self.live_server_url, ""))
        user_code = self.browser.find_element_by_id("id_user_code")
        user_code.send_keys("print('Hello world')")
        self.browser.find_element_by_id("id_launch").click()
        std_io = self.browser.find_element_by_id("id_std_io")
        self.assertMultiLineEqual(std_io.text, ">>>\nHello world")

    def test_user_input(self):
        self.browser.get("%s%s" % (self.live_server_url, ""))
        user_code = self.browser.find_element_by_id("id_user_code")
        user_code.send_keys(CODE)
        std_io = self.browser.find_element_by_id("id_std_io")
        std_io.send_keys("Test\nTest2")
        self.browser.find_element_by_id("id_launch").click()
        std_io = self.browser.find_element_by_id("id_std_io")
        self.assertMultiLineEqual(std_io.text, ">>> Test\nTest2\n>>> Test\nTest2")

    def test_erroneous_code(self):
        self.browser.get("%s%s" % (self.live_server_url, ""))
        user_code = self.browser.find_element_by_id("id_user_code")
        user_code.send_keys("print(")
        self.browser.find_element_by_id("id_launch").click()
        std_io = self.browser.find_element_by_id("id_std_io")
        self.assertIn("SyntaxError", std_io.text)
