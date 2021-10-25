import os
import argparse
import requests
import json
import ipaddress
import re
from colorama import Fore, Style, Back



def get_ip_geolocation(ip):
    try:
        API_KEY = os.environ['API_KEY']
        response = requests.get(f"https://api.ipgeolocation.io/ipgeo?apiKey={API_KEY}&ip={ip}")
        
        
        return response.text
    except:
        print(f"Could not get geolocation for {ip}")
        
        
        
def get_ips_from_file(file):
    try:
        with open(file) as ip_file:
            ip_addrs = []
            for line in ip_file.readlines():
                if '/' in line:
                    network = ipaddress.ip_network(line)
                    hosts = network.hosts() 
                    for host in hosts:
                        ip_addrs.append(host)
                else:
                    ip_addrs.append(line)
            return ip_addrs
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
    
    if args.ip :
        hosts = [ args.ip ]
    elif args.file:
        hosts = get_ips_from_file(args.file)

    api_method(hosts)

def get_content(url):
    resp = requests.get(url, allow_redirects=True)
    return resp.text

def api_method(hosts):
    print(Fore.YELLOW + f'\n[INFO:] using API')
    for host in hosts:
        try:
            print(Fore.GREEN + f"\nLocating {host}: ")
            API_KEY = os.environ['API_KEY']
            req_resp = get_content(f"https://api.ipgeolocation.io/ipgeo?apiKey={API_KEY}&ip={host}")
            json_dict = json.loads(req_resp)
            ip = json_dict['ip']
            contient_name = json_dict['continent_name']
            country_name = json_dict['country_name']
            state_prov = json_dict['state_prov']
            city = json_dict['city']
            organization = json_dict['organization']
            isp = json_dict['isp']
            longitude = json_dict['longitude']
            latitude = json_dict['latitude']

            data = Fore.GREEN + f"""
                {Fore.GREEN}Organization: \t{Fore.LIGHTBLUE_EX}
                {Fore.GREEN}Contient: \t{Fore.LIGHTBLUE_EX}{contient_name}
                {Fore.GREEN}Country: \t{Fore.LIGHTBLUE_EX}{country_name}
                {Fore.GREEN}State/Prov: \t{Fore.LIGHTBLUE_EX}{state_prov}
                {Fore.GREEN}City: \t\t{Fore.LIGHTBLUE_EX}{city}
                
                {Fore.GREEN}Longitude: \t{Fore.LIGHTBLUE_EX}{longitude}
                {Fore.GREEN}Latitde: \t{Fore.LIGHTBLUE_EX}{latitude}
                """
            print(data)

        except:
            print("Error occured")


def non_api_method(hosts):
    print(Fore.GREEN + f'\n[INFO:] Not using API')
    for host in hosts:
        try:
            print(f"\nLocating {host}: ")
            req_resp = get_content(f'https://www.ipligence.com/ip-address?ip={host}')
            reverse_dns = re.findall(r"Reverse dns:(.*?)", req_resp)
            country_name = re.findall(r"Country:(.*?)", req_resp)
            continent = re.findall(r"Contient:(.*)", req_resp)
            city = re.findall(r"City:(.*?)<", req_resp)
            time_zone = re.findall(r"Time Zone:(.?)<", req_resp)
            data = f'''
            Target-IP: {host}
            Reverse-DNS: {reverse_dns[0]}
            Country: {country_name[0]}
            Continent: {continent[0]}
            City: {city[0]}
            Time Zone: {time_zone[0]}

            '''
        except:
            pass

if __name__ == '__main__':
    main()
    
    