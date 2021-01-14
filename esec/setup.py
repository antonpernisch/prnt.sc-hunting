from distutils.core import setup
import py2exe
import urllib.request
from bs4 import BeautifulSoup
import threading
import time
import re
from colorama import init, Fore, Style

setup(options = {'py2exe': {'bundle_files': 3, 'compressed': True}}, console=['Hunter.py'], zipfile = None,)