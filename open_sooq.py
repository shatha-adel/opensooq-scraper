import requests
from bs4 import BeautifulSoup
import csv
import os.path
data=[] 
dir_path = os.path.dirname(os.path.realpath(__file__))
# print(dir_path)
completeName = os.path.join(dir_path, "opensooq.csv") 
# print(completeName)
page_num = 0
while True:
    # use requests to fetch url
    results = requests.get(f"https://jo.opensooq.com/en/cars/cars-for-sale?page={page_num}")
    # save page content/markup
    src = results.content

    # create soup object to parse content
    soup = BeautifulSoup(src, "lxml")

    # page limit = 46362
    page_limit = 46362
    # page_limit = 3


    if (page_num > page_limit // 30):
        print("page ended")
        break

    sections=soup.find_all("div", {"class":"mb-32 relative"})
    for section in sections:
        title=''
        price=''
        location=''
        link=''
        car_spec=''
        img_name=''
        img=''
        try:
            title=section.find('h2').text
        except:
            pass
        try:
            price = section.find("div", {"class":"postPrice"}).text
        except:
            pass
        try:    
            location = section.select_one('.category .bold').text
        except:
            pass
        try:
            car_spec = section.select_one('.flexSpaceBetween+ div').text
        except:
            pass
        try:
            link = "https://jo.opensooq.com"+section.select_one('a')['href']
        except:
            pass
        
        try:

            img= section.select_one('img')['src']
            img_name=img.split('/')[-1]
            response = requests.get(img)
            if response.status_code == 200:
                with open(os.path.join(dir_path, img_name) , "wb") as f:
                    f.write(response.content)
            
        except:
            pass
        row = {}
        row['title'] = title
        row['price'] = price
        row['car_spec'] = car_spec
        row['location'] = location
        row['link'] = link
        row['image'] = img_name
       
        data.append(row)
        # print(data)
    
    page_num += 1
    print("page switched")

# creat csv file



with open(completeName, "w", newline='', encoding="utf-8-sig") as myfile:
   
    w = csv.DictWriter(myfile,["title", "price", "car_spec", "location", "link",'image'])
    w.writeheader()
    for row in data:
        w.writerow(row)

