from dotenv import load_dotenv
import os
import requests
import time

load_dotenv()

# Create Directories

Navigation = os.path.dirname(os.path.realpath(__file__))
path_targets = Navigation + '\\Targets.txt'

# Env 

NodeApi = os.environ.get('api_url')

# Script Class

class Script():
    def __init__(self,proxy=None, headers='', target='', userId='', cookies=''):
        self.proxy = proxy
        self.target = target
        self.userId = userId
        self.headers = headers
        self.cookies = cookies
    def getUserID(self):
        proxyDict = {
            'http': f'http://{self.proxy}',
            'https': f'http://{self.proxy}',
        }
        endpoint = f'https://www.instagram.com/{self.target}/?__a=1'
        CallApi = requests.get(endpoint, headers=self.headers, cookies=self.cookies, proxies=proxyDict)
        response = CallApi.json()
        IdTarget = response['graphql']['user']['id']
        self.userId = IdTarget 
    def getNodeFollowers(self):
        proxyDict = {
            'http': f'http://{self.proxy}',
            'https': f'http://{self.proxy}',
        }
        Node = None
        main_endpoint = 'https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={'
        variable = f'"id":"{self.userId}","include_reel":true,"fetch_mutual":true,"first":' + "50}"
        CallApi = requests.get(f'{main_endpoint}{variable}', headers=self.headers, cookies=self.cookies, proxies=proxyDict)
        response = CallApi.json()
        NodeFollowers = response['data']['user']['edge_followed_by']['page_info']['end_cursor']
        if len(NodeFollowers) > 20:
            Node = NodeFollowers
        return Node
    def getFollowers(self, node, userList):
        proxyDict ={
            'http': f'http://{self.proxy}',
            'https': f'http://{self.proxy}'
        }
        node = node
        main_endpoint = 'https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={"id":'
        variable = f'"{self.userId}","include_reel":true,"fetch_mutual":true,"first":50,"after":"{node}"' + '}'
        CallApi = requests.get(f'{main_endpoint}{variable}', headers=self.headers, cookies=self.cookies, proxies=proxyDict)
        response = CallApi.json()
        NewNode = response['data']['user']['edge_followed_by']['page_info']['end_cursor']
        edges = response["data"]["user"]["edge_followed_by"]["edges"]
        if len(NewNode) > 20:
            node = NewNode
            for x in range(len(edges)):
                userList.append(edges[x]['node']['id'])
        return node

while 1 > 0:
    Accounts = requests.get(NodeApi + '/ListAccounts')
    Accounts = Accounts.json()
    AccountsToBot = len(Accounts)
    Targets = requests.get(NodeApi + '/ListTargetFollowers')
    Targets = Targets.json()
    userList = []
    Node = None
    if len(Targets) > 0:
        TargetAccount = Targets[0]['target']
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
                    requests.post(NodeApi + '/DeleteTargetFollowers', json={'targetName': TargetAccount})
            for x in range(AccountsToBot):
                try:
                    ActualAccount = Script(proxy=Accounts[x]['proxy'].replace(' ', ''), target=TargetAccount, headers=Accounts[x]['creds'][2], cookies=Accounts[x]['creds'][1])
                    ActualAccount.getUserID()
                except Exception as e:
                    print(e)
                    continue
                if len(userList) >= Amount_Scrape:
                    break

                try:
                    while Node == None:
                        Node = ActualAccount.getNodeFollowers()
                    while Node != None and len(userList) < Amount_Scrape:
                        Node = ActualAccount.getFollowers(Node, userList)
                        print(len(userList))
                except Exception as e:
                    print(e)
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
    time.sleep(60)