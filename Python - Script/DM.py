from dotenv import load_dotenv
import os
import requests
import time
import random

load_dotenv()

Navigation = os.path.dirname(os.path.realpath(__file__))

NodeApi = os.environ.get('api_url')

class Script():
    def __init__(self,proxy=None, headers='', target='', userId='', dm_text='', dm_link='', cookies=''):
        self.proxy = proxy
        self.target = target
        self.userId = userId
        self.dm_text = dm_text
        self.dm_link = dm_link
        self.headers = headers
        self.cookies = cookies
    def sendDm(self, userId):
        proxyDict = {
            'http': f'http://{self.proxy}',
            'https': f'http://{self.proxy}',
        }
        createThread = requests.post('https://i.instagram.com/api/v1/direct_v2/create_group_thread/', headers=self.headers, cookies=self.cookies, proxies=proxyDict, data={"recipient_users": f"[\"{userId}\"]"})
        response = createThread.json()
        if createThread.status_code == 200:
            thread_id = response['thread_id']
            DMSent = requests.post('https://i.instagram.com/api/v1/direct_v2/threads/broadcast/link/', headers=self.headers, cookies=self.cookies, proxies=proxyDict, data={"action": "send_item", "link_text": self.dm_text, "link_urls": f"[\"{self.dm_link}\"]", "thread_id": thread_id})
            print(DMSent.status_code)
        return createThread

while 1 > 0:
    Accounts = requests.get(NodeApi + '/ListAccounts')
    Accounts = Accounts.json()
    AccountsToBot = len(Accounts)
    for y in range(5):
        for x in range(AccountsToBot):
            try:
                ActualAccount = Script(proxy=Accounts[x]['proxy'].replace(' ', '')   , target=Accounts[x]['target'], dm_link=Accounts[x]['dm_link'], dm_text=Accounts[x]['dm_text'], headers=Accounts[x]['creds'][0], cookies=Accounts[x]['creds'][1])
                with open(Navigation + f'\\Scrap\\{ActualAccount.target}.txt', 'r') as f1:
                    ListIds = f1.read().splitlines()
                    Chosen = random.sample(ListIds, 1)
                # print(Accounts[x]['username'])
                # print(y)
                # if len(ActualAccount.cookies['sessionid']) < 1:
                #     requests.post(NodeApi + '/DeleteAccount', json={'username': Accounts[x]['username']})
                #     raise Exception
                response = ActualAccount.sendDm(Chosen[0])
                if response.status_code == 400:
                    text = response.json()['message']
                    if text == 'challenge_required':
                        print(Accounts[x]['username'])
            except Exception as e:
                print(e)
                continue
    time.sleep(89628)
