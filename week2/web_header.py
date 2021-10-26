import requests
import argparse

app_parser = argparse.ArgumentParser(description="Parse URL headers to check if the Strict-Transport-Security flag is set")
app_parser.add_argument('--url', '-u', help="url to parse")
app_parser.add_argument('--file', '-f', help="file location to read urls from")


def get_url_headers(url):
    req = requests.get(url)
    return req.headers

def check_sts(response_headers):
    if 'Strict-Transport-Security' in response_headers:
        return True
    

def main():
    url = 'https://www.redsiege.com/'
    headers = get_url_headers(url)
    if not check_sts(headers):
        print(f"{url} is missing Strict-Transport-Security")
    else:
        print(f"The Strict-Transport-Security header for {url} is set to {headers['Strict-Transport-Security']}")

    

if __name__ == '__main__':
    main()