# Python 3 Web Scraper

# Ensure both beautifulsoup and requests are installed:
#   Windows
#   pip install beautifulsoup4
#   pip install requests

import requests
from bs4 import BeautifulSoup

map_page = requests.get("https://www.sustainablejersey.com/certification/search-participating-municipalities-approved-actions/")
map_data = map_page.content
soup = BeautifulSoup(map_data, "html.parser")

# lists all municipalities, listing them in the order of:
# Municipality, County, Certification
all = []

# finds all the tr tags in soup (the webpage) containing community=row as its class
for tr_tags in soup.find_all(attrs={"class": "community-row"}):
    #  finds all the td values in a given tr tag (there should be 3)
    for td_tags in tr_tags.find_all("td"):
        # Appends the values to all and removes whitespace
        all.append(" ".join(td_tags.text.split()))
# print(all)
# total number should come out to 1365 with 455 municipalities
# print(len(all))

municipalities = []
counties = []
certifications = []
i = 0
for item in all:
    if i % 3 == 0:
        municipalities.append(item)
    if i % 3 == 1:
        counties.append(item)
    if i % 3 == 2:
        certifications.append(item)
    i = i + 1

# print(municipalities)
# print(len(municipalities))

# Converts counties to a dictionary to remove duplicates
counties = list(dict.fromkeys(counties))
# print(counties)
# print(len(counties))

# Removes duplicates from certifications to show all certification values
certifications = list(dict.fromkeys(certifications))
# print(certifications)
# print(len(certifications))




# Start of Actions page

actions_page = requests.get("https://www.sustainablejersey.com/actions/")
actions_data = actions_page.content
soup2 = BeautifulSoup(actions_data, "html.parser")

# lists all categories
categories = []
# Lists all actions under each category. New categories are specified to make it easier to seperate categories from actions
actions = []
# finds all the tr tags in soup2 (the webpage) containing community=row as its class
for li_tags in soup2.find_all(attrs={"class": "action-category"}):
    #  finds all the td values in a given tr tag (there should be 3)
    i = 0
    for h3_tags in li_tags.find_all("h3"):
        # Appends the values to all and removes whitespace
        categories.append(" ".join(h3_tags.text.split()))
        actions.append("NEW_CATEGORY")
        actions.append(" ".join(h3_tags.text.split()))
        # for sub_cat in li_tags.find_all(attrs={"class": "action-subcategory--header"}):
            # actions.append("NEW_SUB_CAT")
            # actions.append(" ".join(sub_cat.text.split()))
        # Actions are all printed in order
        for h4_tags in li_tags.find_all("h4"):
            actions.append(" ".join(h4_tags.text.split()))
        # Points are all printed in order
        # for div_tags in li_tags.find_all(attrs={"class": "action--points"}):
        #     actions.append(" ".join(div_tags.text.split()))
        for req_tags in li_tags.find_all(attrs={"class": "action--req"}):
            actions.append(" ".join(req_tags.text.split()))

# print(categories)

# The category is first in the list, followed by a sub category (specified by NEW_SUB_CAT),
# followed by all of the actions, followed by their corresponding point values, followed by
# the items that are priority or required.
# print(actions)


# code to print out the insertion queries for Categories
# for category in sorted(categories):
#     print("INSERT INTO Categories (Cname)")
#     print("VALUES(\'" + category + "\');")
#     print("")

# for county in sorted(counties):
#     print("INSERT INTO Counties (CTYname)")
#     print("VALUES(\'" + county + "\');")
#     print("")

# for municipality in sorted(municipalities):
#     print("INSERT INTO Municipalities (Mname, CTYcode)")
#     print("VALUES(\'" + municipality + "\', (INSERT_CTYcode_HERE));")
#     print("")
