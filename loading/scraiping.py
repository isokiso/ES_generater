import csv
import requests
from bs4 import BeautifulSoup
import yaml
import os

#login
yaml_dict = yaml.load(open('secret.yaml').read())
payload = {
    'utf8': '✓',
    'user[email]': yaml_dict['id'],
    'user[password]': yaml_dict['password'],
    'user[remember_me]':'1'
}
s = requests.Session()
r = s.get('https://www.onecareer.jp/users/sign_in?store_return_to=%2Farticles')
print(r)
soup = BeautifulSoup(r.text, features="lxml")
auth_token = soup.find(attrs={'name': 'authenticity_token'}).get('value')
payload['authenticity_token'] = auth_token
r = s.post('https://www.onecareer.jp/users/sign_in', data=payload)
print(str(r.status_code))


out_file = '../data/gs.csv'
if os.path.isfile(out_file):
    os.remove(out_file)

url_base = 'https://www.onecareer.jp/companies/9/experiences?middle_categories%5B%5D=entry_sheet&order=latest&page='
for n in range(100):
    r = s.get(url_base + str(n))
    soup = BeautifulSoup(r.content, "html.parser")
    src = soup.find_all(class_='v2-experience')
    for i in src:
        a = i.find('a')
        link = a.get('href')
        url = 'https://www.onecareer.jp' + link
        print(url)
        r = s.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        subj = soup.find(class_="v2-curriculum-item-body__content")
        q = subj.find_all('h3')
        a = subj.find_all('p')
        for q_i, a_i in zip(q,a):
            with open(out_file, 'a') as f:
                writer = csv.writer(f)
                writer.writerow([q_i, a_i])