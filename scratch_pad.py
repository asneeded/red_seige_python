import socket
url = 'www.redsiege.com/'
url = url.rstrip('/')
print(url)
ip = socket.gethostbyname(url)

print(ip)