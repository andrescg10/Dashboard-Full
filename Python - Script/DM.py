from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import requests
import time
import random

load_dotenv()

# Create Directories

Navigation = os.path.dirname(os.path.realpath(__file__))
path_ua = Navigation + '\\Main\\ListUA.Txt'
path_gecko = Navigation + '\\Main\\geckodriver.exe'
path_extension1 = Navigation + '\\Main\\matteblack.xpi'
path_extension2 = Navigation + '\\Main\\webrtc.xpi'
path_targets = Navigation + '\\Targets.txt'
path_scrapped = Navigation + '\\Scrapped.txt'


# Open UserAgents List

with open(path_ua, 'r') as f1:
    userAgents = f1.read().splitlines()

# Capabilities browser

options = Options()
# options.add_argument('--headless')
profile = webdriver.FirefoxProfile()

# Spoof Browser

ua = random.choice(userAgents)
profile.set_preference("general.useragent.override",  ua)
profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
profile.set_preference("media.peerconnection.enabled", False)
profile.set_preference("javascript.enabled", False)
profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference("useAutomationExtension", False)
profile.set_preference("general.platform.override", "iPhone")
profile.set_preference("intl.accept_languages", "en")

# Env 

NodeApi = os.environ.get('api_url')


class Script():
    def __init__(self, username, password, proxy=None, creds=[], target='', driver=None, userId='', dm_text='', dm_link=''):
        self.username = username
        self.password = password
        self.proxy = proxy
        self.creds = creds
        self.target = target
        self.driver = driver
        self.userId = userId
        self.dm_text = dm_text
        self.dm_link = dm_link

    def getCreds(self):
        PROXY = self.proxy
        PROXY = self.proxy
        webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
            "httpProxy": self.proxy,
            "ftpProxy": self.proxy,
            "sslProxy": self.proxy,
            "proxyType": "MANUAL",
        }
        driver = webdriver.Firefox(
            profile, executable_path=path_gecko, options=options)
        driver.set_window_size(414, 896)
        driver.install_addon(path_extension1, temporary=True)
        driver.install_addon(path_extension2, temporary=True)
        driver.get('https://www.instagram.com/accounts/login/')
        FieldUsername = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, "username")))
        FieldUsername.send_keys(self.username)
        FieldPassword = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, "password")))
        FieldPassword.send_keys(self.password)
        Buttons = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "Igw0E.IwRSH.eGOV_._4EzTm")))
        Buttons[4].click()
        time.sleep(random.randint(4, 8))
        cookiesRaw = driver.get_cookies()
        Final_List = {
            'ig_did': '',
            'csrftoken': '',
            'mid': '',
            'rur': '',
            'ds_user_id': '',
            'sessionid': ''
        }
        for x in cookiesRaw:
            name = x['name']
            value = x['value']
            Final_List[name] = value
        ig_did = f"ig_did={Final_List['ig_did']}"
        csrftoken = f"csrftoken={Final_List['csrftoken']}"
        mid = f"mid={Final_List['mid']}"
        rur = f"rur={Final_List['rur']}"
        ds_user_id = f"ds_user_id={Final_List['ds_user_id']}"
        sessionid = f"sessionid={Final_List['sessionid']}"
        cookieheaders = f'{ig_did}; {csrftoken}; {mid}; {rur}; {ds_user_id}; {sessionid}'
        cookies = {
            'ig_did': Final_List['ig_did'],
            'csrftoken': Final_List['csrftoken'],
            'mid': Final_List['mid'],
            'rur': Final_List['rur'],
            'ds_user_id': Final_List['ds_user_id'],
            'sessionid': Final_List['sessionid']
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'i.instagram.com',
            'User-Agent': ua,
            'Accept': '*/*',
            'Accept-Language': 'en-US;q=1',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cookie': cookieheaders,
            'X-IG-Capabilities': '3wo=',
            'X-IG-Connection-Type': 'WiFi',
            'X-CSRFToken': Final_List['csrftoken'],
        }
        credsUpdated = [headers, cookies]
        self.creds = credsUpdated
        self.driver = driver
        return credsUpdated
    def sendDm(self, userId):
        proxyDict = {
            'http': f'http://{self.proxy}',
            'https': f'http://{self.proxy}',
        }
        createThread = requests.post('https://i.instagram.com/api/v1/direct_v2/create_group_thread/', headers=self.creds[0], cookies=self.creds[1], proxies=proxyDict, data={"recipient_users": f"[\"{userId}\"]"})
        response = createThread.json()
        if createThread.status_code == 200:
            thread_id = response['thread_id']
            sendDM = requests.post('https://i.instagram.com/api/v1/direct_v2/threads/broadcast/link/', headers=self.creds[0], cookies=self.creds[1], proxies=proxyDict, data={"action": "send_item", "link_text": self.dm_text, "link_urls": f"[\"{self.dm_link}\"]", "thread_id": thread_id})
        return createThread.status_code




while 1 > 0:
    Accounts = requests.get(NodeApi + '/ListAccounts')
    Accounts = Accounts.json()
    AccountsToBot = len(Accounts)
    for x in range(AccountsToBot):
        try:
            ActualAccount = Script(username=Accounts[x]['username'], password=Accounts[x]['password'], proxy=Accounts[x]['proxy']   , target=Accounts[x]['target'], dm_link=Accounts[x]['dm_link'], dm_text=Accounts[x]['dm_text'])
            ActualAccount.getCreds()
            with open(Navigation + f'\\Scrap\\{ActualAccount.target}.txt', 'r') as f1:
                ListIds = f1.read().splitlines()
                # Amount of users to send a DM
                Chosen = random.sample(ListIds, 10)
            for x in range(len(Chosen)):
                status_code = ActualAccount.sendDm(Chosen[x])
                if status_code == 400:
                    raise Exception
        except Exception as e:
            print(e)
            try:
                ActualAccount.driver.close()
            except:
                pass
            continue
        finally:
            try:
                ActualAccount.driver.close()
            except:
                pass
    print('DMS Sent, time to sleep...')
    time.sleep(89628)
            