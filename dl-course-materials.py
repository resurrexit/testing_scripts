#!/usr/bin/env python
import urllib.request, getpass, sys, re
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
    if it is an absolute or relative link. Filetype should be a RE object indicating
    the kind of link the user wants downloaded """
def parse_for_links(url, response, filetype):
    links = []
    soup = BeautifulSoup(response, parse_only=SoupStrainer('a'), from_encoding="utf-8")
    # to do: return links ending file types user asked for. start with pdfs.
    for link in soup.find_all('href'):
        match=filetype.match(link.get('href'))
        # CAN DO WITH STRING SLICING INSTEAD (maybe). Although maybe not because not all filetypes
        # are three chars long
        if match:
            # if link begins with / then it is a relative link
            if match.group()[0] == '/':
                links.push(urljoin(url, match.group()))
            else:
                links.push(match.group())
    return links



def main():
    info = info_request()

    response = pull_site(info)

    filetype = re.compile(".+\.pdf")
    parse_for_links(info.url, response, filetype)


if __name__=='__main__':
   main()