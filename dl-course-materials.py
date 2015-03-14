#!/usr/bin/env python
import urllib.request, getpass, sys
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urljoin

class HTTPAUTH:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

def info_request():
    url = input('Enter the URL: ')
    username = input('Enter username: ')
    password = getpass.getpass('Enter password: ')

    info = HTTPAUTH(url, username, password)
    return info

def pull_site(info):
    # password manager time woohoo!
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, info.url, info.username, info.password)

    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)

    # create opener that uses handler
    opener = urllib.request.build_opener(handler)
    urllib.request.install_opener(opener)

    try:
        return urllib.request.urlopen(info.url)
    except urllib.error.HTTPError as ue:
        print(ue.reason, file=sys.stderr)


""" Keep in mind that url may not needed to be appended to the link. Depends on
    if it is an absolute or relative link. """
def parse_for_pdf(url, response):
     soup = BeautifulSoup(response, parse_only=SoupStrainer('a'), from_encoding="utf-8")
     # to do: return links ending file types user asked for. start with pdfs.
     # if link begins with / then it is a relative link

def main():
    info = info_request()

    response = pull_site(info)
    parse_for_pdf(response)


if __name__=='__main__':
   main()