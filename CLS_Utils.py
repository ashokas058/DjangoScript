import subprocess
import os
import time
from simple_term_menu import TerminalMenu
class UtilesDjango:
    def __init__(self) -> None:
        pass


    def listFormated(self,items,title):
        count=1
        if(items):
            print(f"---------------List of {title}--------------\n")
            for list in items:
                print(f"\t{count}){list}\n")
                count=count+1
            print(f"---------------List ENDS--------------\n")
            return True
        else:
            return False

    def installSSL(self,domain):
        try:
            subprocess.check_call(['nginx', '-t'])
        except subprocess.CalledProcessError:
            print("nginx configuration test failed. Aborting.")
            return False
        subprocess.call(['nginx', '-s', 'reload'])

        subprocess.call(['certbot', '--nginx', '-d', domain])
        return True

    def nginxSiteLink(self,siteAvailable,siteEnabled):
        enableLink=os.path.join(siteEnabled,os.path.basename(siteAvailable))
        os.symlink(siteAvailable, enableLink)
    def clear(self):
        time.sleep(2)
        os.system('clear')

    def terminalUI(self,list):
        terminal_menu = TerminalMenu(list)
        return  terminal_menu.show()




