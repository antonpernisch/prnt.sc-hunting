import urllib.request
from bs4 import BeautifulSoup
import threading
import time

# colors in ansi coding
class colors:
    HEADER = '\033[95m'
    WHITE = '\033[0m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DARK_CYAN = '\033[90m'

class Hunter:

    threads_run = True
    threads_pause = False
    nextCode = 0
    downloading_threads = list()

    def checks(self):
        # this method check for regexes and other checks that need to be done
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
                    print(colors.OKGREEN + "Found image, downloading" + colors.ENDC)
                    try:
                        urllib.request.urlretrieve(imgSrc, self.letters + str(i) +".png")
                    except:
                        print(colors.FAIL + "/\ Downloading failed" + colors.ENDC)
                    continue
                else:
                    # does not exist :( continue
                    print(colors.WARNING + "Image not found, proceeding" + colors.ENDC)
                    continue

    # main loop function
    def start(self):
        if self.amount <= 10000 and self.amount >= 0:
            # check was successful
            self.opener = urllib.request.build_opener()
            self.opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'), ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'), ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'), ('Accept-Encoding', 'none'), ('Accept-Language', 'en-US,en;q=0.8'), ('Connection', 'keep-alive')]
            urllib.request.install_opener(self.opener)

            self.nextCode = self.startingNum

            # start threads and wait till all of them are dead
            self.threads_run = True
            for thread in range(6):
                newThread = threading.Thread(target = self.downloading_thread, args = (self, ))
                self.downloading_threads.append(newThread)
                newThread.start()

            while self.threads_run:
                time.sleep(0.2)
                continue
        else:
            # user typed incorrect amount num, die
            print(colors.FAIL + "You have typed wrong number of pictures to save, choose only from 1 to 1000")
            exit(0)

    # after startup
    def startup(self):
        print("")
        print(colors.BOLD + colors.UNDERLINE + "prnt.sc screenshot hunting tool" + colors.ENDC)
        print("")

        self.letters = input("Write two letters at the beggining: ")
        self.startingNum = int(input("From where do you want to start? "))
        self.amount = int(input("How many pictures do you want to save? "))

        self.start(self)

<<<<<<< HEAD
Hunter.startup(Hunter)
=======
Hunter.startup(Hunter)
>>>>>>> 95958f68e0f2b582820fb18b64dd2159f193ea3c
