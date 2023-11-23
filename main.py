import os
import zipfile
from auth_data import *
from selenium.webdriver.chrome.service import Service
import time
from selenium import webdriver
import logg

class Instagram_Liker:
    def __init__(self, url:str, hashtag: list):
        self.url = url
        self.hashtag = hashtag
        logg.logging.info('Инициализация прошла')


    def __login(self, login = INSTAGRAM_LOGIN, password = INSTAGRAM_PASSWORD):
        self.login = login
        self.password = password
        

    def __get_url(self):
        self.driver.get(self.url)
        logg.logging.info(f'URL {self.url} загружен')


    def __get_chromedriver(self, use_proxy=False, user_agent=None):
        manifest_json = """
        {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (PROXY_IP, PROXY_PORT, PROXY_LOGIN, PROXY_PASSWORD)
        chrome_options = webdriver.ChromeOptions()
        if use_proxy:
            plugin_file = 'proxy_auth_plugin.zip'
            with zipfile.ZipFile(plugin_file, 'w') as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", background_js)
            chrome_options.add_extension(plugin_file)
        if user_agent:
            chrome_options.add_argument(f'--user-agent={user_agent}')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        logg.logging.info('Драйвер получен')

    def __close_driver(self):
        time.sleep(10)
        self.driver.close()
        self.driver.quit()
        logg.logging.info('Драйвер закрыт')
        

   
    def parse(self):
        self.__get_chromedriver(use_proxy=True, user_agent=None)
        self.__get_url()
        self.__close_driver()
     


if __name__ == '__main__':
    Instagram_Liker(url='https://www.instagram.com/', hashtag=['калиниинград',]).parse()


