import requests
import datetime
import argparse
import json
import csv

from bs4 import BeautifulSoup

def get_url(item_to_search, number_of_page):
    """Returns the URL concatenated with the search term and number of the page
    
    Args:
        item_to_search (str): The term to search on Amazon search bar
        number_of_page (int): The number of the page to request

    Returns:
        conv_url (str): string, following URL convention, that is a concatenation of the template amazon URL with the search term and number of the page
    """

    template = f"https://www.amazon.com/s?k={item_to_search}"
    conv_url = template.replace(' ', '+') + "&page=" #replace every space with '+' to follow URL convention
    conv_url += str(number_of_page)

    return conv_url

def write_to_csv(data):
    """This function writes to a csv named amazon_web_scrapper_dataset.
    The argument newline='' enables the iteration between lines; 
    The parameter "w" specifies that it will be writted over the file.
    The encoding parameter is Unicode Transformation Format 8-bit 
    The csv will contain the following headers: Description, Price, Number of Reviews, Scraping Date, URL
    and the respective data
    """

    with open("amazon_web_scrapper_dataset.csv", "w", newline='', encoding="UTF-8") as file:
        writer=csv.writer(file)
        writer.writerow(["Description", "Price", "Rating", "Number of Reviews", "Scrapping Date", "URL"])
        writer.writerows(data)

def extract_record_info(item):
    """Extract and returns data from a record

    Args:
        item (str): each item that appears in the results page

    Returns:
        result (tuple): Tuple containing the description, price, rating, number_of_reviews, scrapping_date, and url)
    """

    # Description and URL
    description = item.h2.a.text.strip()

    url = "https://www.amazon.com" + item.h2.a.get("href")

    # Grab Price Attribute
    try:
        price = item.find("span", {"class": "a-offscreen"}).text.strip()[1:] #grabs a cleaner price
    except AttributeError:
        return

    # Rating Attribute
    try:
        rating = item.i.text.strip()
    except AttributeError:
        return

    # No of Reviews Attribute
    try:
        number_of_reviews = item.find("span", {"class":"a-size-base s-underline-text"}).text.strip().replace("(", "").replace(")", "")
    except AttributeError:
        return

    #today's datetime
    scrapping_date = datetime.date.today()

    result_record = (description,price,rating,number_of_reviews,scrapping_date,url)

    return result_record


def parse_record_info(url, headers, data):
    """Makes use of the request module to make a request to the web page stated on the URL
        and stores it on the data variable
    
    Args:
        url (str): string returned from get_url function
        headers (dict): dictionary that contain the agent user
        data (list): list of tuples that collects the result_record entries
    """
    
    response_page = requests.get(url, headers=headers, cookies={'__hs_opt_out': 'no'})
    soup_1 = BeautifulSoup(response_page.content, "html.parser") # Parsing the HTML content
    soup_2 = BeautifulSoup(soup_1.prettify(), "html.parser") #Parses the soup1 into a nicely formatted Unicode string
    results = soup_2.find_all("div", {"data-component-type": "s-search-result"}) #results per page

    for item in results:
        record_info = extract_record_info(item)
        if record_info:
            data.append(record_info)

def parse_arguments():
    """This function parses the argument(s) of this WebScrapper
        The text to display before the argument help will be "Process all the arguments for this WebScrapper"

        Args:
            item_to_search : name of the command line field to insert on the runtime

        Return:
            args: Stores the extracted data from the parser run
    """

    parser = argparse.ArgumentParser(description='Process all the arguments for this WebScrapper')
    parser.add_argument('item_to_search', help='The item to search on Amazon Search Bar')
    args = parser.parse_args()
    return args

def main():
    """This is the main function of this WebScrapper"""
    args = parse_arguments()

    paginator = range(1, 10)
    data = [] # list of tupples [(), (), ()]

    with open("headers.json") as f:
        headers = json.load(f)

    for page in paginator:
        url = get_url(args.item_to_search, page)

        print(f"Requesting data from Page {page}", "\n")
        parse_record_info(url, headers, data)

    print("Writing data to a CSV...")
    write_to_csv(data)

if __name__ == '__main__':
    main()