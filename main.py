import requests
import os
from dotenv import load_dotenv
import argparse

def shorten_link(token, url):
  bitlinks_url = 'https://api-ssl.bitly.com/v4/bitlinks'
  auth_api = {"Authorization": token}
  long_url = {'long_url': args.url}
  response = requests.post(bitlinks_url, headers=auth_api, json=long_url)
  response.raise_for_status()
  bitlink = response.json()['id']
  return bitlink

def count_clicks(token, link):
  clicks_url = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks'.format(link)
  auth_api = {"Authorization": token}
  info = {'bitlink': args.url,
          'unit ':'ISO-8601'
  }
  response = requests.get(clicks_url, headers=auth_api, params=info)
  response.raise_for_status()
  return response.json()

if __name__ == '__main__':
  load_dotenv()
  BITLY_TOKEN = os.getenv('BITLY_API')
  parser = argparse.ArgumentParser(description='converts url to bitly-url')
  parser.add_argument('url', type=str, help='url to be converted to bitly-url')
  args = parser.parse_args()
  if args.url.startswith('bitly.is/') or args.url.startswith('bit.ly/'):
    try:
      print('Короткая ссылка :',args.url)
      print('По вашей ссылки прошли :',count_clicks(BITLY_TOKEN, args.url)['link_clicks'][0]['clicks'],'раз(а)')
    except requests.exceptions.HTTPError:
      print('INCORRECT URL')
  else:
    shorted = shorten_link(BITLY_TOKEN, args.url)
    try:
      print('Короткая ссылка :',shorted)
      print('По вашей ссылки прошли :',count_clicks(BITLY_TOKEN, shorted)['link_clicks'][0]['clicks'],'раз(а)') 
    except requests.exceptions.HTTPError:
      print('INCORRECT URL')


