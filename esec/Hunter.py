import urllib.request
from bs4 import BeautifulSoup

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

# main loop function
def start(letters, amount):
    if amount <= 10000 and amount >= 0:
        # check was successful
        for iRaw in range(0, amount):
            # format the current code, such that it has four digits
            i = '{0:04}'.format(iRaw)
            
            # build url address according to users prefs
            urlCode = letters + str(i)
            url = "https://prnt.sc/" + urlCode + "/"

            page = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'none', 'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive'}))
            soup = BeautifulSoup(page, features="html.parser")

            x = soup.body.find('img', attrs={'id' : 'screenshot-image'})

            print(x)
            break
    else:
        # user typed incorrect amount num, die
        print(colors.FAIL + "You have typed wrong number of pictures to save, choose only from 1 to 1000")
        exit(0)

# after startup
def startup():
    print("")
    print(colors.BOLD + colors.UNDERLINE + "prnt.sc screenshot hunting tool" + colors.ENDC)
    print("")

    letters = input("Write two letters at the beggining: ")
    amount = int(input("How many pictures do you want to save? "))

    start(letters, amount)

startup()
