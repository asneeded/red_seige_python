'''
Project 1 - The Scope!

Scenario: Congrats, your Penetration testing company Red Planet has landed an external assessment for Microsoft! Your point of contact has give you a few IP addresses for you to test. Like with any test you should always verify the scope given to you to make sure there wasn't a mistake.

Beginner Task: Write a script that will have the user input an IP address and verify the ownership and the geographical location of the IP. The script should output the results in a way that is clean and organized in order to be added to your report.

Intermediate Task:  Have the script read multiple IP addresses from a file and process them all at once.

Expert Task:Have the script read from a file containing both single IP addresses and CIDR notation, having it process it both types.

Here are your IP addresses to check:
131.253.12.5
131.91.4.55
192.224.113.15
199.60.28.111
'''
import os
import argparse
import requests
import json
import ipaddress
from colorama import Fore, Style, Back



def get_ip_geolocation(ip):
    try:
        API_KEY = os.environ['API_KEY']
        response = requests.get(f"https://api.ipgeolocation.io/ipgeo?apiKey={API_KEY}&ip={ip}")
        
        
        return response.text
    except:
        print(f"Could not get geolocation for {ip}")
        
def get_ips_in_cidr(network):
    pass
        
def get_ips_from_file(file):
    try:
        with open(file) as ip_file:
            ip_addrs = []
            for line in ip_file.readlines():
                if '/' in line:
                    get_ips_in_cidr(line)
                else:
                    get_ip_geolocation(line)
    except :
        print(f"{file} not found.")

        
def main():
    app_parser = argparse.ArgumentParser(prog="carman",
                                         usage="%(prog)s [options] IP Adresses",
                                         description="Find geolocation of a given IP address")
    
    app_parser.add_argument('-i',
                            '--ip',
                            type=str,
                            help='List of IP Addresses')
    
    app_parser.add_argument('-f',
                            '--file',
                            type=str,
                            help="File that contains a list of ip addresses")
    args = app_parser.parse_args()
    print(args)
    ip_addrs = [ args.ip ]
    # ip_addrs = ['131.253.12.5', '131.91.4.55','8.8.8.8']
    for ip in ip_addrs:
        print(get_ip_geolocation(ip))





if __name__ == '__main__':
    main()
    
    