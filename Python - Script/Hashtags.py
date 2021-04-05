from dotenv import load_dotenv
import os
import requests
import time
import random

load_dotenv()

# Create Directories

Navigation = os.path.dirname(os.path.realpath(__file__))
path_targets = Navigation + '\\Targets.txt'

NodeApi = os.environ.get('api_url')

# Script Class

class Script():
    def __init__(self,proxy=None, headers='', target='', userId='', cookies=''):
        self.proxy = proxy
        self.target = target
        self.userId = userId
        self.headers = headers
        self.cookies = cookies
    def getNodeFollowers(self):
        proxyDict = {
            'http': f'http://{self.proxy}',
            'https': f'http://{self.proxy}',
        }
        Node = None
        main_endpoint = 'https://www.instagram.com/graphql/query/?variables={"tag_name":'
        variable = f'"{self.target}","first":50,"after":""' + '}' + '&query_hash=9b498c08113f1e09617a1703c22b2f32'
        CallApi = requests.get(f'{main_endpoint}{variable}', headers=self.headers, cookies=self.cookies, proxies=proxyDict)
        response = CallApi.json()
        NodeFollowers = response['data']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
        if len(NodeFollowers) > 20:
            Node = NodeFollowers
        return Node
    def getFollowers(self, node, userList):
        proxyDict ={
            'http': f'http://{self.proxy}',
            'https': f'http://{self.proxy}'
        }
        node = node
        main_endpoint = 'https://www.instagram.com/graphql/query/?variables={"tag_name":'
        variable = f'"{self.target}","first":15,"after":"{node}"' + '}' + '&query_hash=9b498c08113f1e09617a1703c22b2f32'
        CallApi = requests.get(f'{main_endpoint}{variable}', headers=self.headers, cookies=self.cookies, proxies=proxyDict)
        response = CallApi.json()
        NewNode = response['data']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
        edges = response["data"]["hashtag"]["edge_hashtag_to_media"]["edges"]
        if len(NewNode) > 20:
            node = NewNode
            for x in range(len(edges)):
                userList.append(edges[x]['node']['owner']['id'])
        return node



while 1 > 0:
    Accounts = requests.get(NodeApi + '/ListAccounts')
    Accounts = Accounts.json()
    AccountsToBot = len(Accounts)
    Targets = requests.get(NodeApi + '/ListHashtags')
    Targets = Targets.json()
    userList = []
    Node = None
    if len(Targets) > 0:
        TargetAccount = Targets[0]['target']
        ApiTarget = TargetAccount[1:]
        Amount_Scrape = Targets[0]['amount']
        while len(userList) < Amount_Scrape:
            with open(path_targets, 'r') as f1:
                ListNodes = f1.read().splitlines()
                try: 
                    Index = ListNodes.index(TargetAccount)
                    if ListNodes[Index + 1] != '0':
                        Node = ListNodes[Index + 1]
                except:
                    with open(path_targets, 'a+') as f1:
                        f1.write("%s\n" % TargetAccount)
                        f1.write("%s\n" % 0)
                finally:
                    requests.post(NodeApi + '/DeleteHashtag', json={'targetName': TargetAccount})
            for x in range(AccountsToBot):
                try:
                    ActualAccount = Script(proxy=Accounts[x]['proxy'].replace(' ', ''), target=TargetAccount, headers=Accounts[x]['creds'][2], cookies=Accounts[x]['creds'][1])
                except Exception as e:
                    print(e)
                    continue
                try:
                    while Node == None:
                        Node = ActualAccount.getNodeFollowers()
                    while Node != None and len(userList) < Amount_Scrape:
                        Node = ActualAccount.getFollowers(Node, userList)
                except Exception as e:
                    continue
            
            with open(path_targets, 'r') as f1:
                ListNodes = f1.read().splitlines()
            Index = ListNodes.index(TargetAccount)
            ListNodes[Index + 1] = Node
            with open(path_targets, 'w') as f1:
                for x in ListNodes:
                    f1.write("%s\n" % x)
            with open(Navigation + f'\\Scrap\\{TargetAccount}.txt', 'a+') as f1:
                for x in userList:
                    f1.write("%s\n" % x)
    time.sleep(600)
