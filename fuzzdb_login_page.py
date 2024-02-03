import requests
logins = []
with open('Logins.txt', 'r') as filehandle:
    for line in filehandle:
        login = line[:-1]
        logins.append(login)
#domain = "http://testphp.vulnweb.com"
domain = "http://10.1.1.1"
for login in logins:
    print("Checking... "+ domain + login)
    response = requests.get(domain + login, timeout = 5)
    if response.status_code == 200:
        print("Login resource detected: " +login)
