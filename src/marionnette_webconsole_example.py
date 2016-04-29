import sys
import time
from marionette import Marionette
from marionette_driver import By
from marionette_driver import Wait
from marionette_driver import expected


class TestConsoleLogCapture():
    def setup(self):
        try:
            self.client = Marionette(host='localhost', port=2828)
            self.client.start_session()
            self.client.set_pref('general.warnOnAboutConfig', False)
        except:
            sys.exit("Could not find Firefox browser running")

    def test_push_notification_received(self):
        self.client.navigate("https://people.mozilla.org/~ewong2/push-notification-test/")

        unregister_button = self.client.find_element(By.ID, "unreg_btn")
        if unregister_button.is_displayed() == True:
            unregister_button.click()
            Wait(self.client, timeout=5, interval=1).until(expected.element_not_displayed(By.ID, "unreg_btn"))

        Wait(self.client).until(expected.element_displayed(By.ID, "reg_btn"))
        self.client.find_element(By.ID, "reg_btn").click()
        Wait(self.client).until(expected.element_displayed(By.ID, "subscribe_btn"))
        self.client.find_element(By.ID, "subscribe_btn").click()
        Wait(self.client).until(expected.element_displayed(By.ID, "doXhr_btn"))
        self.client.find_element(By.ID, "doXhr_btn").click()

        result = self.web_console_filter_for_string("Received a push message")
        assert result == 1

    def web_console_filter_for_string(self, console_string=None):
        self.client.set_context(self.client.CONTEXT_CHROME)

        handles = self.client.window_handles
        chrome_handles = self.client.chrome_window_handles
        browser_handle = self.client.current_chrome_window_handle
        notifications = 0
        for handle in chrome_handles:
            if handle != browser_handle:
                console_handle = handle
                self.client.switch_to_window(console_handle)
                time.sleep(1)
                results = self.client.find_elements(By.CLASS_NAME, "console-string")
                for result in results:
                    if console_string in result.text:
                        notifications = notifications + 1
        self.client.find_element(By.CLASS_NAME, "webconsole-clear-console-button").click()
        return notifications


    def tear_down(self):
        self.client.close()
