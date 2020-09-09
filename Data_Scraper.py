import bs4
import re
from urllib import request as uReq
from bs4 import BeautifulSoup as soup
import os
import json
import time

# Print iterations progress


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


# This is to print the total operation time
start_time = time.time()

# Locate the file directory of this python file
# change the working directory to this location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Manully Input Job Name or title you want
job_name = input("Please enter the job name you want to search ")
# Manully Input number of job ads you want to include in the database
sample_number = int(input(
    "Please enter how many job ads do you want to include in this database "))

# The number of webpage need to load
# Please notice for seek each search page contains 22 results
page_number = int((sample_number - (sample_number % 22))/22 + 1)

# Reformatting the Job name to html link
if job_name[-1] == " ":
    job_name = job_name[:-1]
    job_name = job_name.replace(" ", "-")
else:
    job_name = job_name.replace(" ", "-")

# define database
data = []
counter = 0

for x in range(page_number):
    my_url = 'https://www.seek.com.au/' + job_name + \
        '-jobs/in-All-Sydney-NSW?page=' + str(x+1)
    # Connect to the defined wesbite
    uClient = uReq.urlopen(my_url)
    # Read the website
    page_html = uClient.read()
    # Html parsing
    page_soup = soup(page_html, 'html.parser')

    # save job_id, job_name and weblink into database
    for link in page_soup.findAll('a', attrs={'class': "_2iNL7wI"}):
        counter = counter + 1
        if counter > sample_number:
            break
        a = link.get('href')
        data.append({
            'job id': int(a[5:13]),
            'job name': str(link.string),
            'web link': a
        })

l = len(data)
printProgressBar(0, l, prefix='Progress:', suffix='Complete', length=50)
# This is section is to identify job type from the job title e.g. whether its BI, data analyst
# or data scientist
for i, item in enumerate(data):
    if all(x in item["job name"].lower() for x in ["analyst"]):
        item["job type"] = "data analyst"
    elif all(x in item["job name"].lower() for x in ["analytics"]):
        item["job type"] = "data analyst"
    elif all(x in item["job name"].lower() for x in ["data", "engineer"]):
        item["job type"] = "data engineer"
    elif all(x in item["job name"].lower() for x in ["data", "scientist"]):
        item["job type"] = "data scientist"
    else:
        item["job type"] = "unrelated"
        continue

# This is section is to identify the industry data analyst are in
# Connect to the defined wesbite
    uClient = uReq.urlopen("https://www.seek.com.au" + item["web link"])
    # Read the website
    page_html = uClient.read()
    # Html parsing
    page_soup = soup(page_html, 'html.parser')
# This is to find out which sector is the jobs in
    job_section = page_soup.find("div", class_="K1Fdmkw JyFVSRZ").find_all(
        "strong", class_="lwHBT6d")
    item["job sector"] = job_section[1].get_text()
# This is to find out more detailed job sector is the jobs in
    job_section_2 = page_soup.find("div", class_="K1Fdmkw JyFVSRZ").find_all(
        "span", class_="eBOHjGN")
    item["detailed job description"] = job_section_2[-1].get_text()[2:]
# This is to put a list of key skills to look for in a job application
    keyskills = ["python", "excel", "tableau", "degree", "bachelor", "master",
                 "phd", "power bi", "spark", "hadoop", "hive", "kafka", "java", "matlab", "sas", "mongodb", "postgresql", "mysql", "oracle", "sql", "nosql", "aws", "azure", "gcp"]
# This is to find out more detailed job sector is the jobs in
    if page_soup.find("div", class_="templatetext") == None:
        content = page_soup.find("div", class_="_2e4Pi2B").get_text()
        for skills in keyskills:
            if content.lower().find(skills) > 0:
                item[skills] = int(1)
            else:
                item[skills] = int(0)
        r_skill = "R" in content.split()
        # Find R
        if r_skill == True:
            item["R"] = int(1)
        else:
            item["R"] = int(0)
    else:
        content = page_soup.find(
            "div", class_="templatetext").get_text()
        for skills in keyskills:
            if content.lower().find(skills) > 0:
                item[skills] = int(1)
            else:
                item[skills] = int(0)
        # Find R
        if r_skill == True:
            item["R"] = int(1)
        else:
            item["R"] = int(0)
# # Update Progress Bar
    printProgressBar(i + 1, l, prefix='Progress:',
                     suffix='Complete', length=50)


with open('job_info.json', 'w') as outfile:
    json.dump(data, outfile)

# # This is to print the total operation time
print("--- %s seconds ---" % (time.time() - start_time))
