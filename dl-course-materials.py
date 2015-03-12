#!/usr/bin/env python
import urllib.request

class HTTPAUTH:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

def info_request():
    url = input('Enter the URL: ')
    username = input('Enter username: ')
    password = input('Enter password: ')

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
    except urllib.error.URLError as ue:
        print(ue.reason)

def main():
    info = info_request()

    response = pull_site(info)

if __name__=='__main__':
   main()