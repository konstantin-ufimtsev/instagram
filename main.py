import os
import zipfile
from auth_data import *
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
import logg
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pickle

class Instagram_Liker:
    def __init__(self, url:str, hashtag: list):
        self.url = url
        self.hashtag = hashtag
        logg.logging.info('Инициализация прошла')


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


    def __get_url(self):

        self.driver.get(self.url)
        for cookie in pickle.load(open('session', "rb")):
            self.driver.add_cookie(cookie)
        logg.logging.info('Куки загружены')
        #time.sleep(100)
        #pickle.dump(self.driver.get_cookies(), open('session', 'wb'))
        logg.logging.info(f'URL {self.url} загружен')
        self.driver.refresh()
        
        time.sleep(20)
        
        try:
            WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='_a9-- _ap36 _a9_1']"))).click()
            logg.logging.info('Кнопка отказа от уведомлений нажата')
        except Exception as ex:
            logg.logging.info('Кнопка отказа от уведомлений НЕ НАЖАТА')
        time.sleep(50)

    #функция заологинивания, не нужна пока работют кукис
    def __login(self, login = INSTAGRAM_LOGIN, password = INSTAGRAM_PASSWORD):
            try:
                self.login = login
                self.password = password
                
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))) #ожидаем появления поля ввода

                username_input = self.driver.find_element(By.NAME, "username")
                username_input.clear()
                username_input.send_keys(login)
                time.sleep(2)
                username_password = self.driver.find_element(By.NAME, "password")
                username_password.clear()
                username_password.send_keys(password) 
                
                username_password.send_keys(Keys.ENTER)
                
                
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.frame_to_be_available_and_switch_to_it((By.ID, "recaptcha-iframe")))
                    logg.logging.info('Фрэйм найден')
                except Exception as ex:
                    logg.logging.info('Фрэйм не найден')
                
                #клик по чекбоксу капчи внутри iframe
                time.sleep(10)
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.ID, 'recaptcha-anchor'))).click()
                    logg.logging.info('Капча найдена')
                except Exception as ex:
                    logg.logging.info('Капча не найдена')
               

                logg.logging.info('Аутентификация осуществлена')
                time.sleep(20)
            except Exception as ex:
                logg.logging.info(f'Аутенификация НЕ ОСУЩЕСТВЛЕНА - ошибка: {ex}')

    def __close_driver(self):
        self.driver.close()
        self.driver.quit()
        logg.logging.info('Драйвер закрыт')
        

   
    def parse(self):
        self.__get_chromedriver(use_proxy=True, user_agent=None)
        self.__get_url()
        #self.__login()
        self.__close_driver()
        
     


if __name__ == '__main__':
    
    Instagram_Liker(url='https://www.instagram.com/', hashtag=['калиниинград',]).parse()


