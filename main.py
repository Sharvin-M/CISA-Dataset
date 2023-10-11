import requests, csv
from csv import writer
from bs4 import BeautifulSoup as bs
import pandas as pd
from bs4 import SoupStrainer as strainer
import urllib

# initialized lists for standard fields 
advisoryTitles = []
advisoryIDs = []
advisoryDates = []
advisorySummaries = []
advisorySolutions = []
advisoryReferences = []
advisoryLinks = []


def main():
    # iterate through each page, parse only necessary parts
    for page in range(0, 12):
        url = "https://www.cisa.gov/news-events/cybersecurity-advisories?f%5B0%5D=advisory_type%3A94&page={page}".format(
            page=page
        )
        page = requests.get(url)
        only_c_row = strainer("div", attrs={"class": "c-view__row"})
        soup = bs(page.content, "html.parser", parse_only=only_c_row)

        # advisory title
        advisoryTitle = soup.find_all("h3", attrs={"class": "c-teaser__title"})
        for tag in advisoryTitle:
            advisoryTitles.append(
                str(tag.text.strip())
            )  # reduce every tag to a simple string and append to approriate list

        # advisory ID
        advisoryID = soup.find_all(attrs={"class": "c-teaser__meta"})
        for tag in advisoryID:
            advisoryIDs.append(
                tag.text.strip().replace("Cybersecurity Advisory | ", "")
            )  # remove unnecessary part of string

        # advisory date
        advisoryDate = soup.find_all(attrs={"class": "c-teaser__date"})
        for tag in advisoryDate:
            advisoryDates.append(tag.text.strip())

    # iterate through each individual page
    length = len(advisoryIDs)
    for j in range(length):
        urls = "https://www.cisa.gov/news-events/cybersecurity-advisories/" + (
            advisoryIDs[j]
        )  # for every id create a new link
        advisories = requests.get(urls)
        only_section_content = strainer(
            "div", attrs={"class": "l-page-section__content"}
        )  # specify class to parse
        soups = bs(advisories.content, "html.parser", parse_only=only_section_content)

        # advisory link
        advisoryLinks.append(urls)

        # advisory summary
        advisorySummary = soups.find("p", string=True)
        if "summary" or "note:" in str(advisorySummarytext).lower():
                advisorySummaries.append(advisorySummary.text)
        else:
            advisorySummaries.append("summary not found")


        # # advisory solution
        # advisorySolution = soups.find_all("h3", string=True)
        # for tag in advisorySolution:
        #     if tag.text == "Mitigations":
        #         texts = tag.findNext("p").findNext().findChildren()
        #         for t in texts:
        #                 advisorySolutions.append(str(t.text))

        # # advisory reference
        # advisoryReference = soups.find_all("h3", string=True)
        # for tag in advisoryReference:
        #     if tag.text == "References":
        #         p_child = tag.findNext("p").findChildren("a")
        #         for child in p_child:
        #             if child.text == "None":
        #                 advisoryReferences.append("None")
        #             else:
        #                 advisoryReferences.append(child.get("href"))

    # write data to a csv file
    with open("test.csv", "a") as f_object:
        writer_object = writer(f_object)
        # writer_object.writerow(advisoryTitles)
        # writer_object.writerow(advisoryIDs)
        # writer_object.writerow(advisoryLinks)
        # writer_object.writerow(advisoryDates)
        writer_object.writerow(advisorySummaries)
        # writer_object.writerow(advisorySolutions)
        # writer_object.writerow(advisoryReferences)
        f_object.close()


main()
