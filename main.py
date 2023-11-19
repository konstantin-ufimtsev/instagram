import os
import zipfile
from auth_data import *
from selenium.webdriver.chrome.service import Service
import time
from selenium import webdriver

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


def get_chromedriver(use_proxy=False, user_agent=None):
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        plugin_file = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(plugin_file, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(plugin_file)
    if user_agent:
        chrome_options.add_argument(f'--user-agent={user_agent}')
    
    driver = webdriver.Chrome(options=chrome_options)

    return driver
           
   

def main():
    driver = get_chromedriver(use_proxy=True)
    driver.get('https://whoer.net/')
    #driver.get('https://www.instagram.com/')
    time.sleep(10)
    driver.close()
    driver.quit()

if __name__ == '__main__':
    main()


