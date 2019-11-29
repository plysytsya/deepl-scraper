import platform
import datetime
import os
import subprocess
import signal

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.action_chains import ActionChains


def kill_process_by_keyword(keyword):
    """
        Use it to kill stuck webdrivers.
        E.g. kill_process_by_keyword(chrome)
    """
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():
        if keyword in str(line).lower():
            pid = int(line.split(None, 1)[0])
            try:
                os.kill(pid, signal.SIGKILL)
            except OSError:
                pass


class Browser:

    def __init__(self, headless=False):
        self.headless = headless
        self.os = self.get_name_operating_system()
        self.THIS_DIR = os.path.dirname(os.path.abspath(__file__))
        self.WEBDRIVERS_DIR = os.path.join(self.THIS_DIR, 'webdrivers')
        self.start()

    def start(self):
        chrome_binary = self.choose_browser_binary()[0]
        geckobrowser_binary = self.choose_browser_binary()[1]
        try:
            self.start_chrome(chrome_binary)
        except Exception as e:
            print(e)
            self.start_firefox(geckobrowser_binary)
        self.driver.maximize_window()

    def start_chrome(self, name_of_driver_binary):
        chrome_options = ChromeOptions()
        if self.headless is True:
            chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(
            options=chrome_options,
            executable_path=os.path.join(self.WEBDRIVERS_DIR, name_of_driver_binary))

    def start_firefox(self, name_of_driver_binary):
        firefox_options = FirefoxOptions()
        firefox_options = self.headless
        self.driver = webdriver.Firefox(
            options=firefox_options,
            executable_path=os.path.join(self.WEBDRIVERS_DIR, name_of_driver_binary))

    def choose_browser_binary(self):
        browser_binaries = {
            'Darwin': ['chromedriver_mac64', 'geckodriver_mac64'],
            'Linux': ['chromedriver_linux64', 'geckodriver_linux64']
        }
        return browser_binaries.get(self.os)

    def restart(self):
        self.quit()
        self.start()

    def quit(self):
        self.driver.quit()

    def wait_until_url_changes(self, expected_url, timeout=30):
        start = datetime.datetime.now()
        timeout = datetime.timedelta(seconds=timeout)
        while True:
            if self.driver.current_url == expected_url:
                break
            if datetime.datetime.now() > start + timeout:
                break

    def wait_for_pageload_until_keywords_in_html(self, keyword_list, timeout=30):
        start = datetime.datetime.now()
        timeout = datetime.timedelta(seconds=timeout)
        while True:
            html = self.find_html_element_by_xpath(xpath='/html').get_attribute('outerHTML')
            if any(keyword in html for keyword in keyword_list):
                break
            if datetime.datetime.now() > start + timeout:
                break

    def get_name_operating_system(self):
        return platform.system()

    def open_website(self, website):
        self.driver.get(website)

    def find_html_element_by_visible_text(self, text):
        xpath = "//*[contains(text(), '%s')]" % text
        return self.driver.find_element_by_xpath(xpath)

    def find_html_element_by_tag_name(self, tag_name):
        return self.driver.find_element_by_tag_name(tag_name)

    def find_html_element_by_class_name(self, class_name):
        return self.driver.find_element_by_class_name(class_name)

    def find_html_element_by_xpath(self, xpath):
        return self.driver.find_element_by_xpath(xpath)

    def find_html_element_by_id(self, _id):
        return self.driver.find_element_by_id(_id)

    def fill_input_field_with_text(self, input_field, text):
        input_field.send_keys(text)

    def scroll_to_bottom_of_page(self):
        self.driver.find_element_by_tag_name('body').send_keys(Keys.END)

    def scroll2element(self, element):
        element.location_once_scrolled_into_view

    def find_html_elements_by_tag_and_outer_html(self, tag_name, keywords):
        tags = self.driver.find_elements_by_tag_name(tag_name)
        elements_found = [
            element for element in tags
            if any(kwd in element.get_attribute('outerHTML') for kwd in keywords)]
        assert len(elements_found) > 0, f"No element found for tag {tag_name} and keyword={keywords}"
        return elements_found

    def double_click(self, element):
        actionChains = ActionChains(element)
        actionChains.double_click(element).perform()


if __name__ == '__main__':
    browser = Browser()
