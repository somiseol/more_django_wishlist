from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase

class TitleTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_title_on_homepage(self):
        self.selenium.get(self.live_server_url)
        self.assertIn('TRAVEL WISHLIST', self.selenium.title)


class AddPlacesTest(LiveServerTestCase):

    fixtures = ['test_places']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


    def test_add_new_place(self):
        self.selenium.get(self.live_server_url)
        inupt_name = self.selenium.find_element(By.ID, 'id_name')  # find textbox
        inupt_name.send_keys('Denver')  # type in text box

        add_button = self.selenium.find_element(By.ID, 'add-new-place')  # find add new place button
        add_button.click()  # click button

        new_place = self.selenium.find_element(By.ID, 'place-name-5')  # find and assign to variable next Place model object after the 4 added fixtures

        self.assertEqual('Denver', new_place.text)

        self.assertIn('Denver', self.selenium.page_source)  # if 'Denver' is in the text
        self.assertIn('New York', self.selenium.page_source)
        self.assertIn('Tokyo', self.selenium.page_source)
