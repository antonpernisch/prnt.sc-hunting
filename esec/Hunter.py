import urllib.request
from bs4 import BeautifulSoup
import threading
import time
import re
from colorama import init, Fore, Style
init(convert=True, autoreset=True)

class Hunter:

    threads_run = True
    threads_pause = False
    nextCode = 0
    downloading_threads = list()
    threads_num = 6

    # regexes for later checking
    letters_reg = re.compile(r"^[a-z]{2}$")

    def checks(self):
        # this method check for regexes and other checks that need to be done
        if self.letters_reg.match(self.letters):
            # letters are ok - code 200
            if self.amount > self.threads_num:
                # ok
                return 200
            else:
                # more threads then amout
                return 501
        else:
            # invalid letters - code 500
            return 500
        return

    def downloading_thread(self):
        while self.threads_run:
            if self.threads_pause:
                time.sleep(0.2)
                continue
            else:
                currentCode = self.nextCode
                self.nextCode = self.nextCode + 1

                if currentCode == self.amount + self.startingNum:
                    # we are at the end, this is last thread
                    self.threads_run = False

                # format the current code, such that it has four digits
                i = '{0:04}'.format(currentCode)
                
                # build url address according to users prefs
                urlCode = self.letters + str(i)
                url = "https://prnt.sc/" + urlCode + "/"

                page = urllib.request.urlopen(urllib.request.Request(url))
                soup = BeautifulSoup(page, features="html.parser")

                imgCode = soup.body.find('img', attrs={'id' : 'screenshot-image'})
                imgSrc = str(BeautifulSoup(str(imgCode), features="html.parser").img.attrs["src"])

                # check if this img exists - possible because of the diffrent starting of url
                # starting with https = exists, else does not
                if imgSrc.startswith("https"):
                    # this image exists, download it and continue
                    print(Fore.GREEN + "() Found image, downloading")
                    try:
                        urllib.request.urlretrieve(imgSrc, "Images/" + self.letters + str(i) +".png")
                    except:
                        print(Fore.RED + "/\ Downloading failed, is there \"Images\" folder?")
                    continue
                else:
                    # does not exist :( continue
                    print(Fore.YELLOW + "(!) Image not found, proceeding")
                    continue

    # main loop function
    def start(self):
        if self.amount <= 10000 and self.amount >= 0:
            # check was successful
            self.opener = urllib.request.build_opener()
            self.opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'), ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'), ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'), ('Accept-Encoding', 'none'), ('Accept-Language', 'en-US,en;q=0.8'), ('Connection', 'keep-alive')]
            urllib.request.install_opener(self.opener)

            if self.checks(self) == 500:
                # wrong letters
                print(Fore.RED + "(!) You have typed wrong letters. Choose only two letters, for example \"nr\"")
                self.startup(self)
            elif self.checks(self) == 501:
                # more threads then amout
                print(Fore.RED + "(!) You must download at least 7 pictures")
                self.startup(self)

            self.nextCode = self.startingNum

            # start threads and wait till all of them are dead
            self.threads_run = True
            for thread in range(self.threads_num):
                newThread = threading.Thread(target = self.downloading_thread, args = (self, ))
                self.downloading_threads.append(newThread)
                newThread.start()

            while self.threads_run:
                time.sleep(0.2)
                continue

            print(Fore.GREEN + "() Images downloaded in \"Images\" folder")
            print(Fore.CYAN + "() Waiting 5 seconds for threads to ends their job...")
            time.sleep(5)
            print(Fore.CYAN + "() Restarting engine...")
            self.startup(self)
        else:
            # user typed incorrect amount num
            print(Fore.RED +  "(!) You have typed wrong number of pictures to save, choose only from 1 to 1000")
            self.startup(self)

    # after startup
    def startup(self):
        self.threads_pause = False
        self.nextCode = 0
        self.downloading_threads = list()
        self.threads_num = 6

        self.letters = input("> Write two letters at the beggining: ")
        try:
            self.startingNum = int(input("> From where do you want to start? "))
        except ValueError:
            print(Fore.RED +  "(!) You have typed wrong value, please type only numbers")
            self.startup(self)

        try:
            self.amount = int(input("> How many pictures do you want to save? "))
        except ValueError:
            print(Fore.RED +  "(!) You have typed wrong number of pictures to save, choose only from 1 to 1000")
            self.startup(self)

        self.start(self)

print("")
print(Style.BRIGHT + "PRNT.SC SCREENSHOT HUNTING TOOL")
print("")

Hunter.startup(Hunter)