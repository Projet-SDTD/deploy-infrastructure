import requests
import time
import datetime

session = requests.Session()

def url_ok(url):
    r = session.head(url)
    return r.status_code

with open('out.csv', 'w') as f:
    f.write("time;requesttime;status\n")
    for i in range(200):
        time.sleep(0.5)
        try:
            t = time.time()
            rcode = url_ok("https://phase1.sdtd.marche.ovh/ping")
            print(rcode)
            f.write(str(datetime.datetime.now())+";"+str(time.time()-t)+";"+str(rcode)+"\n")
        except Exception as e:
            print(e)
            f.write(str(datetime.datetime.now())+";ERR;ERR\n")