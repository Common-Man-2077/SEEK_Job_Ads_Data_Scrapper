import bs4
import re
from urllib import request as uReq
from bs4 import BeautifulSoup as soup
import os
import json

# Locate the file directory of this python file
# change the working directory to this location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Manully Input Job Name you want the criteria of
job_name = "data"

# Reformatting the Job name to html link
if job_name[-1] == " ":
    job_name = job_name[:-1]
    job_name = job_name.replace(" ", "-")
else:
    job_name = job_name.replace(" ", "-")

jobs_list = []
data = []

# Manully input how many page of ads data need to gather
# Each page contains 22 results
for x in range(100):
    my_url = 'https://www.seek.com.au/' + job_name + \
        '-jobs/in-All-Sydney-NSW?page=' + str(x+1)
    # Connect to the defined wesbite
    uClient = uReq.urlopen(my_url)
    # Read the website
    page_html = uClient.read()
    # Html parsing
    page_soup = soup(page_html, 'html.parser')

    for link in page_soup.findAll('a', attrs={'class': "_2iNL7wI"}):
        a = link.get('href')
        data.append({
            'job id': int(a[5:13]),
            'job name': str(link.string),
            'web link': a
        })


with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
