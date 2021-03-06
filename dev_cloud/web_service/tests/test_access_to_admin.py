# -*- coding: utf-8 -*-
# @COPYRIGHT_begin
#
# Copyright [2015] Michał Szczygieł, M4GiK Software
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# @COPYRIGHT_end


from django.test import LiveServerTestCase
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys


class AdminTest(LiveServerTestCase):
    fixtures = ['admin_user.json']
    BROWSER_IS_WORKING = False

    def setUp(self):
        try:
            self.display = Display(visible=0, size=(800, 600))
            self.display.start()

            self.browser = webdriver.Firefox()
            self.browser.implicitly_wait(3)
            self.BROWSER_IS_WORKING = True
        except WebDriverException:
            print 'Selenium have problem to run test'



    def tearDown(self):
        if self.BROWSER_IS_WORKING:
            self.browser.quit()
            self.display.stop()



    def test_can_create_new_poll_via_admin_site(self):
        if self.BROWSER_IS_WORKING:
            # Solenium opens her web browser, and goes to the admin page
            self.browser.get(self.live_server_url + '/admin/')

            # She sees the familiar 'Django administration' heading
            body = self.browser.find_element_by_tag_name('body')
            self.assertIn('Django administration', body.text)

            # She types in her username and passwords and hits return
            username_field = self.browser.find_element_by_name('username')
            username_field.send_keys('m4gik')

            password_field = self.browser.find_element_by_name('password')
            password_field.send_keys('qetuo1357')
            password_field.send_keys(Keys.RETURN)

            # her username and password are accepted, and she is taken to
            # the Site Administration page
            body = self.browser.find_element_by_tag_name('body')
            self.assertIn('Django administration', body.text)

            # She now sees a couple of hyperlink that says "Web_Service"
            web_service_links = self.browser.find_elements_by_link_text('Models')
            self.assertEquals(len(web_service_links), 1)

