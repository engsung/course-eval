import csv
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv


def main():
    f = open(f"prof_mean.csv", 'w')
    f.write("Instructor,Faculty,Mean Displays Enthusiasm,Mean Well Organized,Mean Presents Concepts Clearly,"
            "Mean Encourages Participation,Mean Responds To Questions Clearly,Mean Encourages Reflection,"
            "Mean Provides Fair Evaluation,Mean Provides Helpful Feedback,Mean Good Motivator,Mean Average 1 to 9,"
            "Mean Effective As A University Teacher,Mean Course As Learning Experience\n")

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

        soup = BeautifulSoup(p.content, 'html.parser')
        tables = soup.findAll("table")
        for table in tables:
            # TODO: ERASE THE 10
            for tr in table.findAll("tr")[1:10]:
                for td in tr.findAll("td"):
                    for a in td.findAll("a"):
                        prof_url = 'https://sqct.uwo.ca/results/'+a["href"]
                        prof = s.get(prof_url)
                        prof_soup = BeautifulSoup(prof.content, 'html.parser')
                        tables = prof_soup.findAll("table")

                        table1_tr = tables[0].findAll("tr")[1]
                        table1_td = table1_tr.findAll("td")
                        f.write(table1_td[0].text+','+table1_td[1].text+',')

                        table2_tr = tables[1].findAll("tr")[1:]
                        for tr in table2_tr:
                            inside_table2_td = tr.findAll("td")
                            f.write(inside_table2_td[9].text.strip()+',')
                        f.write('\n')

        print("Finished extracting data")


if __name__ == '__main__':
    main()
