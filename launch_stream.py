import requests
headers = {'User-Agent': 'Mozilla/5.0'}
payload = {'URL':'https://www.twitch.tv/zerator','QUALITY':'720p60', 'FPS': '5'}

session = requests.Session()
session.post('https://phase1.sdtd.marche.ovh/start',headers=headers,data=payload)