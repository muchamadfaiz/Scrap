import os
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_page():
    base_url = "https://www.pararius.com/apartments/" + location + f"/page-{page}"
    response = requests.get(base_url)
    if response.status_code != 200:
        raise Exception (f"Unable to download the page {base_url}")
    page_content = response.text
    soup = BeautifulSoup(page_content, 'html.parser')

    return soup

def get_total_pages(location, page):

    get_page()
    total_pages = []
    pagination = soup.find("ul", class_="pagination__list")
    pages = pagination.find_all("li", limit=5)
    for page in pages:
        total_pages.append(page.text.strip())

    total = int(max(total_pages))
    return total

def extract_data(soup):
    tags =soup.find_all("section")

    data_list = []
    for tag in tags:
        name = tag.find("a",class_= "listing-search-item__link listing-search-item__link--title").text.strip()
        address = tag.find("div",class_= "listing-search-item__sub-title").text.strip()
        price = tag.find("div",class_= "listing-search-item__price").text.strip()
        area = tag.find("li",class_= "illustrated-features__item illustrated-features__item--surface-area").text.strip()
    
        # sorting data
        data_dict = {
            "name" : name,
            "address" : address,
            "price" : price,
            "area" : area
        }
        data_list.append(data_dict)

    return data_list

def get_json_data(data_list):
    try:
        os.mkdir("json_result")
    except FileExistsError:
        pass
    with open ("json_result/job_list.json","w+") as json_data:
        json.dump(data_list, json_data)

    print("data json created")

def create_csv(data_list):
    df = pd.DataFrame(data_list)
    df.to_csv("pararius_data.csv", index=False)
    df.to_excel("pararius_data.xlsx", index=False)

    print("data csv created")


def run ():
    location = "groningen"
    p = get_page(location, 1)
    # data_page = get_total_pages(p)
    # print(data_page)
    data = extract_data(p)
    get_json_data(data)
    create_csv(data)
    print(f'jumlah data adalah {len(data)}')
    # print(data)

if __name__ == "__main__":
    run()   