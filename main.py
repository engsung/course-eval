import csv
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv


def main():
    # Create the payload
    load_dotenv()
    payload = {'txtUsername': os.getenv('USERNAME'),
               'txtPassword': os.getenv('PASSWORD'),
               'command': 'authenticate'
               }
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

    with requests.Session() as s:
        # Post the payload to the site to log in
        p = s.post("https://sqct.uwo.ca/results/login.cfm", data=payload)

        # Navigate to the next page and scrape the data
        # An authorised request
        p = s.get('https://sqct.uwo.ca/results/search.cfm')
        p = s.post("https://sqct.uwo.ca/results/results.cfm", data=option_payload)

        # go to prof page
        p = s.get('https://sqct.uwo.ca/results/detail.cfm?id=108705')
        soup = BeautifulSoup(p.content, 'html.parser')

        tables = soup.findAll("table")
        for i in range(len(tables)):
            f = open(f"{i+1}.csv", 'a')
            for tr in tables[i].findAll("tr"):
                for th in tr.findAll("th"):
                    f.write(th.text+',')
                for td in tr.findAll("td"):
                    f.write(td.text + ',')
                f.write('\n')


if __name__ == '__main__':
    main()
