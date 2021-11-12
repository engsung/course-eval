from bs4 import BeautifulSoup
import requests
from decouple import config

# Start the session
session = requests.Session()

# Create the payload
payload = {'txtUsername': 'sdf',
          'txtPassword': 'sfdsd'
         }

# Post the payload to the site to log in
s = session.post("https://www.chess.com/login_check", data=payload)

# Navigate to the next page and scrape the data
s = session.get('https://www.chess.com/today')

soup = BeautifulSoup(s.text, 'html.parser')
soup.find('img')['src']


if __name__ == '__main__':
    pass

