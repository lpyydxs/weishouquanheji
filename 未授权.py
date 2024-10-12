import argparse
import requests
import threading

class check:
    def __init__(self,url):
        self.url=url

    def checkUnraid(self):
        try:
            attck_url=self.url.strip("\n")+"/webterminal/ttyd/"
            reponse = requests.get(attck_url)
            if reponse.status_code == 200:
                print(f"[+]目标网站{attck_url}存在Unraid未授权漏洞....")
            else:
                print("[-]目标网站不存在Unraid未授权漏洞!")
        except:
            print(f"[-] 连接到{self.url}发生了问题!")


    def checkDocker(self):
        try:
            attck_url = self.url.strip("\n") + "/version"
            attck_url1 = self.url.strip("\n") + "/info"
            reponse = requests.get(attck_url)
            reponse1 = requests.get(attck_url1)
            if reponse.status_code == 200:
                print(f"[+]目标网站{attck_url}存在Docker未授权漏洞....")
            elif reponse1.status_code == 200:
                print(f"[+]目标网站{attck_url1}存在Docker未授权漏洞....")
            else:
                print("[-]该网站不存在Docker未授权漏洞!")
        except:
            print(f"[-] 连接到{self.url}发生了问题!")


    def checkElasticsearch(self):
        try:
            attck_url=self.url.strip("\n")+"/_nodes"
            reponse = requests.get(attck_url)
            if reponse.status_code == 200:
                print(f"[+]目标网站{attck_url}存在Elasticsearch未授权漏洞....")
            else:
                print("[-]目标网站不存在Elasticsearch未授权漏洞!")
        except:
            print(f"[-] 连接到{self.url}发生了问题!")



def checkFile(url,check_method):    #check_method 用来指定类型
    with open(url,"r") as f:
        for readline in f.readlines():
            readline_url = check(readline)
            t = threading.Thread(target=getattr(readline_url,check_method))   # getattr(对象,对象中的方法)
            t.start()
            t.join()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='这是一个未授权访问漏洞检测合集')
    parser.add_argument('-u','--url',type=str,help='需要检测的URL')
    parser.add_argument('-f','--file',type=str,help='需要检测的URL文件')
    parser.add_argument('-U','--use',type=str,help='需要检测的漏洞类型(docker/unraid/Elasticsearch未授权)')
    parser.add_argument('-a','--all',action='store_true',help='检测全部漏洞')

    arg = parser.parse_args()
    if arg.url and arg.use:
        usevuln = arg.use
        if usevuln == 'docker':
            check_docker = check(arg.url)
            check_docker.checkDocker()
        elif usevuln == 'unraid':
            check_unraid = check(arg.url)
            check_unraid.checkUnraid()
        else:
            check_unraid = check(arg.url)
            check_unraid.checkElasticsearch()

    elif arg.file and arg.use:
        usevuln = arg.use
        if usevuln == 'docker':
            checkFile(arg.file,'checkDocker')
        elif usevuln == 'unraid':
            checkFile(arg.file,'checkUnraid')
        else:
            checkFile(arg.file,'checkElasticsearch')
    elif arg.url and arg.all:
            check_docker = check(arg.url)
            check_docker.checkDocker()
            check_unraid = check(arg.url)
            check_unraid.checkUnraid()
            check_unraid = check(arg.url)
            check_unraid.checkElasticsearch()
    elif arg.file and arg.all:
        t = threading.Thread(target=checkFile, args=(arg.file,'checkDocker',))
        t.start()
        t.join()
        t = threading.Thread(target=checkFile, args=(arg.file, 'checkUnraid',))
        t.start()
        t.join()
        t = threading.Thread(target=checkFile, args=(arg.file, 'checkElasticsearch',))
        t.start()
        t.join()
    else:
        print("参数错误请查看帮助信息")


