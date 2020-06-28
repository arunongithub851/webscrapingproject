import requests
from bs4 import BeautifulSoup
import pandas as pd
import argparse
import connect

parser=argparse.ArgumentParser()
parser.add_argument("--page_num_max",help="Enter the number the pages to parse",type=int)
parser.add_argument("--dbname",help="Enter the name of db",type=str)
args=parser.parse_args()

flpkrt_url="https://www.flipkart.com/search?q=laptops&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&as-pos=1&as-type=HISTORY&as-searchtext=l&page="
page_num_MAX=args.page_num_max
scrapped_info = []
connect.connect(args.dbname)

for page in range(1,page_num_MAX):
    url=flpkrt_url+str(page)
    print("Get Request for: "+url)
    req=requests.get(url)
    content=req.content
    soup=BeautifulSoup(content,"html.parser")
    all_laptops=soup.find_all("div",{"class":"_3O0U0u"})

    for laptop in all_laptops:
        laptop_dict={}
        laptop_dict["name"]=laptop.find("div",{"class":"_3wU53n"}).text
        try:
            laptop_dict["rating"]=laptop.find("span",{"class":"_2_KrJI"}).text
        except AttributeError:
           laptop_dict["rating"]=None
        parant_amenities_element=laptop.find("div",{"class":"_3ULzGw"})
        amenities_list=[]
        for amenity in parant_amenities_element.find_all("li",{"class":"tVe95H"}):
            amenities_list.append(amenity.text.strip())

        laptop_dict["amenities"]=', '.join(amenities_list)
        scrapped_info.append(laptop_dict)
        connect.insert_in_to_table(args.dbname,tuple(laptop_dict.values()))
        #try.....except block:-used in a case a particular info is not present for all the elements.


dataFrame=pd.DataFrame(scrapped_info)
print("Creating a csv file...")
dataFrame.to_csv("laptop_list.csv")
connect.get_laptop_info(args.dbname)
