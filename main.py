from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv


def main():
    # Create the payload
    load_dotenv()
    payload = {'txtUsername': os.getenv('USERNAME'),
               'txtPassword': os.getenv('PASSWORD'),
               'command': 'authenticate'
               }

    with requests.Session() as s:
        # Post the payload to the site to log in
        p = s.post("https://sqct.uwo.ca/results/login.cfm", data=payload)
        # Navigate to the next page and scrape the data

        # An authorised request.
        r = s.get('https://sqct.uwo.ca/results/search.cfm')
        soup = BeautifulSoup(r.content, 'html.parser')
        print(soup.title.text)


if __name__ == '__main__':
    main()
