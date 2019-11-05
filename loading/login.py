from bs4 import BeautifulSoup
import requests

payload = {
    'utf8': '✓',
    'identity': 'tyukyubya12215@gmail.com',
    'password': 'happybaseball'
}

s = requests.Session()
r = s.get('https://www.onecareer.jp/users/sign_in?store_return_to=%2Farticles')
soup = BeautifulSoup(r.text, features="lxml")
auth_token = soup.find(attrs={'name': 'authenticity_token'}).get('value')
payload['authenticity_token'] = auth_token

s.post('https://www.onecareer.jp/users/sign_in?store_return_to=%2Farticles', data=payload)
