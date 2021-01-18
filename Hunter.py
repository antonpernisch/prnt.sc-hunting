import urllib.request
from bs4 import BeautifulSoup
import threading
import time
import re
import random
import string

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
        if self.letters_reg.match(self.letters) or self.patternCode == 1:
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

                if currentCode == self.amount + self.startingNum - 1:
                    # we are at the end, this is last thread
                    self.threads_run = False

                # format the current code, such that it has four digits
                if self.patternCode == 0:
                    i = '{0:04}'.format(currentCode)
                

                # build url code according to users prefs
                if self.patternCode == 0:
                    # pattern xx0000
                    urlCode = self.letters + str(i)
                elif self.patternCode == 1:
                    # random pattern
                    urlCode = ''.join(random.choice(self.allLetters) for i in range(6))
                url = "https://prnt.sc/" + urlCode + "/"

                page = urllib.request.urlopen(urllib.request.Request(url))
                soup = BeautifulSoup(page, features="html.parser")

                imgCode = soup.body.find('img', attrs={'id' : 'screenshot-image'})
                try:
                    imgSrc = str(BeautifulSoup(str(imgCode), features="html.parser").img.attrs["src"])
                except AttributeError:
                    self.valuesbin.textCtrl__output.SetLabel("[Hunter] Image with code " + urlCode + " wasn't found, proceeding")
                    self.valuesbin.textCtrl__output.SetForegroundColour((255, 153, 0))
                    self.valuesbin.progressBar.SetValue(currentCode - self.startingNum + 1)
                    continue

                # check if this img exists - possible because of the diffrent starting of url
                # starting with https = exists, else does not
                if imgSrc.startswith("https"):
                    # this image exists, download it and continue
                    if self.writePermission:
                        self.valuesbin.textCtrl__output.SetLabel("[Hunter] Downloading image with code " + urlCode)
                        self.valuesbin.textCtrl__output.SetForegroundColour((0, 153, 204))
                    self.valuesbin.progressBar.SetValue(currentCode - self.startingNum + 1)
                    if currentCode == self.amount + self.startingNum - 1:
                        self.threads_run = False
                        self.valuesbin.textCtrl__output.SetLabel("[Hunter] Done, waiting for threads to end their job...")
                        self.valuesbin.textCtrl__output.SetForegroundColour((0, 153, 204))
                        self.writePermission = False
                        time.sleep(2.5)
                        self.valuesbin.textCtrl__output.SetLabel("Downloading complete")
                        self.valuesbin.textCtrl__output.SetForegroundColour((0, 153, 51))
                        self.valuesbin.progressBar.SetValue(0)
                        self.valuesbin.startBtn.Enable(True)
                    try:
                        # build destination path and download
                        urllib.request.urlretrieve(imgSrc, Hunter.downloadPath.replace("/", "\\") + "\\" + urlCode +".png")
                        self.downloadedImgs += 1
                    except:
                        self.writePermission = False
                        self.valuesbin.textCtrl__output.SetLabel("[Hunter] Couldn't download image, try again")
                        self.valuesbin.textCtrl__output.SetForegroundColour((255, 51, 0))
                        self.valuesbin.progressBar.SetValue(0)
                        self.valuesbin.startBtn.Enable(True)
                        self.threads_run = False
                        break
                    continue
                else:
                    # does not exist :( continue
                    self.valuesbin.textCtrl__output.SetLabel("[Hunter] Image with code " + urlCode + " wasn't found, proceeding")
                    self.valuesbin.textCtrl__output.SetForegroundColour((255, 153, 0))
                    self.valuesbin.progressBar.SetValue(currentCode - self.startingNum + 1)
                    if currentCode == self.amount + self.startingNum - 1:
                        self.threads_run = False
                        self.valuesbin.textCtrl__output.SetLabel("[Hunter] Done, waiting for threads to end their job...")
                        self.valuesbin.textCtrl__output.SetForegroundColour((0, 153, 204))
                        self.writePermission = False
                        time.sleep(2.5)
                        self.valuesbin.textCtrl__output.SetLabel("Downloading complete")
                        self.valuesbin.textCtrl__output.SetForegroundColour((0, 153, 51))
                        self.valuesbin.progressBar.SetValue(0)
                        self.valuesbin.startBtn.Enable(True)
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
                self.valuesbin.textCtrl__output.SetLabel("[Hunter] Invalid value for \"Letters\", choose two letters")
                self.valuesbin.textCtrl__output.SetForegroundColour((255, 51, 0))
                self.valuesbin.progressBar.SetValue(0)
                self.valuesbin.startBtn.Enable(True)
                return
            elif self.checks(self) == 501:
                # more threads then amout
                self.valuesbin.textCtrl__output.SetLabel("[Hunter] Invalid value for \"Download amount\", minimum is 7")
                self.valuesbin.textCtrl__output.SetForegroundColour((255, 51, 0))
                self.valuesbin.progressBar.SetValue(0)
                self.valuesbin.startBtn.Enable(True)
                return

            self.valuesbin.textCtrl__output.SetLabel("[Hunter] Checks OK, starting threads and downloading...")
            self.valuesbin.textCtrl__output.SetForegroundColour((0, 153, 51))
            self.valuesbin.progressBar.SetValue(0)
            self.valuesbin.progressBar.SetRange(self.amount)

            self.nextCode = self.startingNum

            # start threads and wait till all of them are dead
            self.threads_run = True
            for thread in range(self.threads_num):
                newThread = threading.Thread(target = self.downloading_thread, args = (self, ))
                self.downloading_threads.append(newThread)
                newThread.start()
        else:
            # user typed incorrect amount num
            self.valuesbin.textCtrl__output.SetLabel("[Hunter] Invalid value for \"Download amount\"")
            self.valuesbin.textCtrl__output.SetForegroundColour((255, 51, 0))
            self.valuesbin.progressBar.SetValue(0)
            self.valuesbin.startBtn.Enable(True)
            return

    # after startup
    def startup(self, valuesbin_var):
        self.valuesbin = valuesbin_var
        self.threads_pause = False
        self.nextCode = 0
        self.downloading_threads = list()
        self.threads_num = 6
        self.writePermission = True
        self.downloadedImgs = 0
        self.patternCode = self.valuesbin.attackPattern.GetSelection()
        self.allLetters = string.ascii_lowercase + string.digits

        try:
            if self.patternCode == 0:
                self.startingNum = int(self.startingNum)
            elif self.patternCode == 1:
                self.startingNum = 0
        except ValueError:
            self.valuesbin.textCtrl__output.SetLabel("[Hunter] Invalid value for \"Start from\"")
            self.valuesbin.textCtrl__output.SetForegroundColour((255, 51, 0))
            self.valuesbin.progressBar.SetValue(0)
            self.valuesbin.startBtn.Enable(True)
            return

        try:
            self.amount = int(self.amount)
        except ValueError:
            self.valuesbin.textCtrl__output.SetLabel("[Hunter] Invalid value for \"Download amount\"")
            self.valuesbin.textCtrl__output.SetForegroundColour((255, 51, 0))
            self.valuesbin.progressBar.SetValue(0)
            self.valuesbin.startBtn.Enable(True)
            return

        self.valuesbin.textCtrl__output.SetLabel("[Hunter] Values imported, preparing download")
        self.valuesbin.textCtrl__output.SetForegroundColour((0, 153, 204))
        self.start(self)