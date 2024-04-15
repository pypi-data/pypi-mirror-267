import json
from requests import post,get

class MayuriClient():
    def __init__(self):
        self.url = 'https://mayuri-iyd0.onrender.com'
    def check(self, user_id):
        try:
            url = f"{self.url}/check/"
            resp = post(url,json={'user_id':user_id})
            if not resp:
                return {'status': 400 , 'report': 'user not scanned'}
            else:
                resp = resp.json()
                result = {
                'user_id': resp[0],
                'reason': resp[1],
                'proof': resp[2]}
                return result
        except Exception as e:
            return e
    def revert(self, user_id):
        try:
            url = f"{self.url}/revert/"
            resp = post(url,json={'user_id':user_id})
            return True
        except:
            pass
    def scanlist(self):
        try:
            url = f"{self.url}/scanlist"
            scanlist = get(url).json()['result']
            return scanlist
        except:
            pass
    def scan(self, user_id, reason, proof):
        try:
            url = f"{self.url}/scan/"
            msg = post(url,json={'user_id':user_id,'reason':reason,'proof':proof})
            return True
        except:
            pass




