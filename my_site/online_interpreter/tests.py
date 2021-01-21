import tempfile

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
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


class FunctionalTests(StaticLiveServerTestCase):
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
        self.assertMultiLineEqual(std_io.text, "Hello world")

    def test_user_input(self):
        self.browser.get("%s%s" % (self.live_server_url, ""))
        user_code = self.browser.find_element_by_id("id_user_code")
        user_code.send_keys(CODE)
        std_io = self.browser.find_element_by_id("id_std_io")
        std_io.send_keys("Line_1\nLine_2")
        self.browser.find_element_by_id("id_launch").click()
        std_io = self.browser.find_element_by_id("id_std_io")
        self.assertMultiLineEqual(std_io.text, "Line_1\nLine_2\nLine_1\nLine_2")

    def test_erroneous_code(self):
        self.browser.get("%s%s" % (self.live_server_url, ""))
        user_code = self.browser.find_element_by_id("id_user_code")
        user_code.send_keys("print(")
        self.browser.find_element_by_id("id_launch").click()
        std_io = self.browser.find_element_by_id("id_std_io")
        self.assertIn("SyntaxError", std_io.text)

    def test_validator_open(self):
        self.browser.get("%s%s" % (self.live_server_url, ""))
        user_code = self.browser.find_element_by_id("id_user_code")
        user_code.send_keys("open('script.py')")
        self.browser.find_element_by_id("id_launch").click()
        errorlist = self.browser.find_element_by_class_name("errorlist")
        self.assertIn("You can't use open function", errorlist.text)

    def test_validator_eval(self):
        self.browser.get("%s%s" % (self.live_server_url, ""))
        user_code = self.browser.find_element_by_id("id_user_code")
        user_code.send_keys("eval('1 + 1')")
        self.browser.find_element_by_id("id_launch").click()
        errorlist = self.browser.find_element_by_class_name("errorlist")
        self.assertIn("You can't use eval function", errorlist.text)

    def test_validator_exec(self):
        self.browser.get("%s%s" % (self.live_server_url, ""))
        user_code = self.browser.find_element_by_id("id_user_code")
        user_code.send_keys("exec('print(999)')")
        self.browser.find_element_by_id("id_launch").click()
        errorlist = self.browser.find_element_by_class_name("errorlist")
        self.assertIn("You can't use exec function", errorlist.text)

    def test_validator_os(self):
        self.browser.get("%s%s" % (self.live_server_url, ""))
        user_code = self.browser.find_element_by_id("id_user_code")
        user_code.send_keys("__import__('os').popen('COMMAND').read()")
        self.browser.find_element_by_id("id_launch").click()
        errorlist = self.browser.find_element_by_class_name("errorlist")
        self.assertIn("You can't use os module", errorlist.text)

    def test_validator_subprocess(self):
        self.browser.get("%s%s" % (self.live_server_url, ""))
        user_code = self.browser.find_element_by_id("id_user_code")
        user_code.send_keys("eval(compile(\"__import__('subprocess')\",'','single'))")
        self.browser.find_element_by_id("id_launch").click()
        errorlist = self.browser.find_element_by_class_name("errorlist")
        self.assertIn("You can't use subprocess module", errorlist.text)

    def test_validator_pathlib(self):
        self.browser.get("%s%s" % (self.live_server_url, ""))
        user_code = self.browser.find_element_by_id("id_user_code")
        user_code.send_keys("eval(compile(\"__import__('pathlib')\",'','single'))")
        self.browser.find_element_by_id("id_launch").click()
        errorlist = self.browser.find_element_by_class_name("errorlist")
        self.assertIn("You can't use pathlib module", errorlist.text)

    def test_validator_fileinput(self):
        self.browser.get("%s%s" % (self.live_server_url, ""))
        user_code = self.browser.find_element_by_id("id_user_code")
        user_code.send_keys("eval(compile(\"__import__('fileinput')\",'','single'))")
        self.browser.find_element_by_id("id_launch").click()
        errorlist = self.browser.find_element_by_class_name("errorlist")
        self.assertIn("You can't use fileinput module", errorlist.text)

    def test_validator_shutil(self):
        self.browser.get("%s%s" % (self.live_server_url, ""))
        user_code = self.browser.find_element_by_id("id_user_code")
        user_code.send_keys("eval(compile(\"__import__('shutil')\",'','single'))")
        self.browser.find_element_by_id("id_launch").click()
        errorlist = self.browser.find_element_by_class_name("errorlist")
        self.assertIn("You can't use shutil module", errorlist.text)

    def test_validator_parent_path(self):
        self.browser.get("%s%s" % (self.live_server_url, ""))
        user_code = self.browser.find_element_by_id("id_user_code")
        user_code.send_keys("cd ../../")
        self.browser.find_element_by_id("id_launch").click()
        errorlist = self.browser.find_element_by_class_name("errorlist")
        self.assertIn("You can't go to the parent path", errorlist.text)

    def test_validator_ftp(self):
        self.browser.get("%s%s" % (self.live_server_url, ""))
        user_code = self.browser.find_element_by_id("id_user_code")
        user_code.send_keys("sftp://example.com")
        self.browser.find_element_by_id("id_launch").click()
        errorlist = self.browser.find_element_by_class_name("errorlist")
        self.assertIn("You can't use ftp protocol", errorlist.text)


# >>> with tempfile.NamedTemporaryFile(mode='w+') as fp:
# ...     fp.write('Hello world!')
# ...     fp.name
# ...     fp.seek(0)
# ...     fp.read()
# ...
# FileNotFoundError: [Errno 2] No such file or directory: '/tmp/tmpf33e7l33'
