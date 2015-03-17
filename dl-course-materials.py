#!/usr/bin/env python
import urllib.request, getpass, sys, re, urllib.error
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urljoin
from sys import exit

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
        sys.exit(1)


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
                links.append(urljoin(url, match.group()))
            else:
                links.append(match.group())
    return links

def download_file(download_url):
    fn = re.compile("/(.*\.pdf$)")
    m = fn.match(download_url)

    response = urllib.request.urlopen(download_url)

    name = m.group(1)
    file = open(name, 'wb')
    file.write(response.read())
    file.close()

def main():
    info = info_request()

    response = pull_site(info)
    #file_request = input("Enter file type: ")
    filetype = re.compile(".*\.pdf$")
    links = parse_for_links(info.url, response, filetype)

    for l in links:
        download_file(l)


if __name__=='__main__':
   main()