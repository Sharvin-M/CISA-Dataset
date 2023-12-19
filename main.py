import requests
from csv import writer
from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer as strainer

# initialized lists for standard fields
advisoryTitles = []
advisoryIDs = []
advisoryDates = []
advisorySolutions = []
advisoryLinks = []


def main():
    # iterate through each page, parse only necessary parts
    for page in range(0, 15):
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

    for j in range(len(advisoryIDs)):
        urls = (
            "https://www.cisa.gov/news-events/cybersecurity-advisories/"
            + (advisoryIDs[j])
        )

        # advisory link
        advisoryLinks.append(urls)

    # write data to a csv file
    with open("csvFiles/test.csv", "w") as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(advisoryTitles)
        writer_object.writerow(advisoryIDs)
        writer_object.writerow(advisoryLinks)
        writer_object.writerow(advisoryDates)
        f_object.close()


if __name__ == "__main__":
    main()
