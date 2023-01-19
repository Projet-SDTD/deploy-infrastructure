import requests
headers = {'User-Agent': 'Mozilla/5.0'}
payload = {'URL':'https://www.twitch.tv/linca','QUALITY':'720p60', 'FPS': '5'}

session = requests.Session()
session.post('https://phase1.sdtd.marche.ovh/stop',headers=headers,data=payload)