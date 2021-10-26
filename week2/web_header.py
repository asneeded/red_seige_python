import requests
import argparse
import sys
import socket
import re
from os import path

app_parser = argparse.ArgumentParser(description="Parse URL headers to check if the Strict-Transport-Security flag is set")
app_parser.add_argument('--url', '-u', help="url to parse")
app_parser.add_argument('--file', '-f', help="file location to read urls from")


def get_url_ip_address(url):
    hostname = re.sub(r'^http[s]://', '', url)
    hostname = re.sub(r'/$', '', hostname)
    if '/' in hostname:
        hostname = hostname.split('/')[0]
    hostname = hostname.strip()
    print(hostname)
    ip_addr = socket.gethostbyname(hostname)
    return ip_addr

def get_url_headers(url):
    req = requests.get(url)
    return req.headers

def check_sts(response_headers):
    if 'Strict-Transport-Security' in response_headers:
        return True
    
def get_urls_from_file(file) -> list:

    if path.exists(file):
        try:
            with open(file, 'r') as f:
                urls = f.readlines()
                            
            return urls
        except:
            print(f"Can't open {file}")
            sys.exit(1)
    else:
        print(f"{file} doesn't exists")    

def main():
    args = app_parser.parse_args()
    if args.url:
        urls = [args.url]
    elif args.file:
        urls = get_urls_from_file(args.file)
        
    missing_sts = []
    for url in urls:

        # url = 'https://www.redsiege.com/'
        headers = get_url_headers(url)
        if not check_sts(headers):
            ip_addr = get_url_ip_address(url)
            missing_sts.append({'url':url.strip(), 'ip_addr':ip_addr})
        else:
            print(f"The Strict-Transport-Security header for {url} is set to {headers['Strict-Transport-Security']}")

    print(missing_sts)

if __name__ == '__main__':
    main()