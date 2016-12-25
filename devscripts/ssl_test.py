import urllib.request

req = urllib.request.urlopen('https://httpbin.org/ip')
print(req.read().decode('ascii'))
