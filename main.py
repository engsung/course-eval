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

        # An authorised request
        p = s.get('https://sqct.uwo.ca/results/search.cfm')
        option_payload = {
            'InsFirstName': '',
            'InsLastName': '',
            'teachingFaculty': '',
            'teachingDept': '',
            'courseSubject': '',
            'courseNumber': '',
            'classSec': '',
            'acadYear': '2019 Fall/Winter',
            'acadTerm': None
        }
        p = s.post("https://sqct.uwo.ca/results/results.cfm", data=option_payload)

        print(p.text)

        soup = BeautifulSoup(p.content, 'html.parser')
        print(soup.title.text)
        print(soup.find('h4').text)


if __name__ == '__main__':
    main()
