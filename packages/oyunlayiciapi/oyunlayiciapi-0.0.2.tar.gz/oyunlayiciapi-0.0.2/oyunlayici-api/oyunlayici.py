import requests, json
import socket

class Oyunlayici:
    
    def isOnline(serverIp: str):
        api = "https://api.oyunlayici.com/json/?ip="
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'none',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive'}
        req = requests.get(api+serverIp, headers=hdr)
        return json.loads(req.text)['sunucudurumu']
    
    def serverIp(hostname: str):
        return socket.gethostbyname(hostname)
    
    def playersMax(serverIp: str):
        api = "https://api.oyunlayici.com/json/?ip="
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'none',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive'}
        req = requests.get(api+serverIp, headers=hdr)
        return json.loads(req.text)['oyuncular']['max']
    
    def playersOnline(serverIp: str):
        api = "https://api.oyunlayici.com/json/?ip="
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'none',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive'}
        req = requests.get(api+serverIp, headers=hdr)
        return json.loads(req.text)['oyuncular']['online']
    
    def serverVersion(serverIp: str):
        api = "https://api.oyunlayici.com/json/?ip="
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'none',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive'}
        req = requests.get(api+serverIp, headers=hdr)
        return json.loads(req.text)['versiyon']['versiyon']
    
    def serverProtocol(serverIp: str):
        api = "https://api.oyunlayici.com/json/?ip="
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'none',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive'}
        req = requests.get(api+serverIp, headers=hdr)
        return json.loads(req.text)['versiyon']['protocol']
    
    def queryPing(serverIp: str):
        api = "https://api.oyunlayici.com/json/?ip="
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'none',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive'}
        req = requests.get(api+serverIp, headers=hdr)
        return json.loads(req.text)['querybilgi']['ping']

#print(json.loads(req.text)['sunucudurumu'])
