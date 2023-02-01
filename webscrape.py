import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from csv import writer
from array import *
import requests
from flask import *
import time
import json
from threading import Thread

app = Flask(__name__)
@app.route('/', methods=['GET'])
def scrape():
    urljson = ("https://api.npoint.io/a859025834f060b13545")
    r = requests.get(urljson)
    jsonData = json.dumps(r.json(), separators=(',', ':'))
    print(r.json())


    timeStamp = time.time() * 1000
    item = str(request.args.get('item')).replace("%20", " ")
    driver = webdriver.Chrome()
    #Amazon
    print("Amazon Catalog: ")

    url = "https://www.amazon.com"

    driver.get(url)

    def get_url(search_term):
        template = "https://www.amazon.com/s?k={}&ref=nb_sb_noss_1"
        search_term = search_term.replace(' ', '+')
        return template.format(search_term)


    url = get_url(item)

    def Convert(lst):
        res_dct = map(lambda i: (lst[i], lst[i+1]), range(len(lst)-1)[::2])
        return dict(res_dct)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #results_products=soup.find_all("div",{"class":"a-section a-spacing-small puis-padding-left-small puis-padding-right-small"}, partial=False)
    #results_product = soup.find_all("span",{"class":"a-size-base-plus a-color-base a-text-normal"}, partial=False)
    cnt = 0
    title1 = ""
    price1 = 0
    link1 = ""
    tempLink = ""
    tempCnt = 0
    image1 = ""
    breakCheck = False
    product_price = soup.findAll('span', {'class':['a-size-base-plus a-color-base a-text-normal', 'a-offscreen']})
    product_title = soup.findAll("span", class_="a-size-base-plus a-color-base a-text-normal")
    product_link = soup.findAll("a",{"class":"a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"}, href=True)
    prodcut_img = soup.findAll("img", class_="s-image")
    productTitle = []
    productPrice = []
    productLink = []
    productImage = []

    for each1 in product_title:
        productTitle.append(str(each1.get_text()))
        

    for each2 in product_price:
        productPrice.append(str(each2.get_text()))


    for each3 in product_link:
        tempLink = each3['href']
        productLink.append("https://www.amazon.com" + str(tempLink))


    for each4 in prodcut_img:
        productImage.append(str(each4['src']))
        


    for each in product_price:
        try:
            title1 = productTitle[cnt]
            price1 =  productPrice[cnt]
            link1 = productLink[cnt]
            image1 = productImage[cnt]
            if image1.__contains__("jpg"):
                driver.get(link1)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                price = 0
                priceTemp = ""
                productPrice = []
                if(url.__contains__("amazon.com")):
                    price = soup.findAll("span", {'class':['a-offscreen']})
                    for each2 in price:
                        productPrice.append(str(each2.get_text()))
                    price1 = productPrice[0]

                if(url.__contains__("ebay.com")):
                    price = soup.findAll("div", class_="x-price-primary")
                    for each2 in price:
                        productPrice.append(str(each2.get_text()))
                    price1 = productPrice[0]

                if(url.__contains__("bjs.com")):
                    price = soup.findAll("div", class_="normal-price")
                    for each2 in price:
                        productPrice.append(str(each2.get_text()))
                    price1 = productPrice[0]
                    
                if(url.__contains__("costco.com")):
                    price = soup.findAll("div", class_="pull-right")
                    for each2 in price:
                        priceTemp = str(each2.get_text())
                        priceTemp = priceTemp.replace('\n', '')
                        priceTemp = priceTemp.replace('\t', '')
                        productPrice.append(priceTemp[0:len(priceTemp)-1])
                    price1 = productPrice[1]

                if(url.__contains__("officedepot.com")):
                    price = soup.findAll("div", class_="od-graphql-price")
                    for each2 in price:
                        productPrice.append(str(each2.get_text()))
                    price1 = productPrice[0]
                    
                if(url.__contains__("staples.com")):
                    price = soup.findAll("div", class_="price-info__final_price_sku")
                    for each2 in price:
                        productPrice.append(str(each2.get_text()))
                    price1 = productPrice[0]
                if(cnt==3):
                    break
                if price1.__contains__("$") and price1.__contains__("."):
                    cnt = cnt + 1
                else:
                    for x in productPrice:
                        if(x.__contains__("$") and x.__contains__(".")):
                            price1 = x
                            cnt = tempCnt + 1
                            break
                        else:
                            tempCnt = tempCnt + 1
                            continue
                        
                info1 = [title1, price1, link1, image1]
                r = requests.get(urljson)
                jsonData = json.dumps(r.json(), separators=(',', ':'))
                jsonData = "[" + jsonData[1:len(jsonData)-1] + "," + json.dumps({'item': title1, 'cost': float(price1.replace("$","")[0:price1.index(".")+2]), 'link': link1, 'image': image1, 'comapny': 'Amazon', 'shortItem': 'TBA', 'count': 1, 'history':{0:{'time': timeStamp, 'cost': float(price1.replace("$","")[0:price1.index(".")+2])}}}, separators=(',', ':')) + "]"
                data = json.loads(jsonData)
                x = requests.post(urljson, json = data)
                print(info1)#thewriter.writerow(info)
        except:
            continue
    #Costco
    print("Costco Catalog: ")

    url = "https://www.costco.com"

    driver.get(url)

    def get_url1(search_term):
        template = "https://www.costco.com/CatalogSearch?dept=All&keyword={}"
        search_term = search_term.replace(' ', '+')
        return template.format(search_term)


    url = get_url1(item)


    #missing

    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #results_products=soup.find_all("div",{"class":"a-section a-spacing-small puis-padding-left-small puis-padding-right-small"}, partial=False)
    #results_product = soup.find_all("span",{"class":"a-size-base-plus a-color-base a-text-normal"}, partial=False)
    cnt = 0
    title1 = ""
    tempTitle = ""
    tempPrice = ""
    price1 = 0
    link1 = ""
    tempLink = ""
    image1 = ""
    product_price = soup.findAll('div', class_="price")
    product_title = soup.findAll("span", class_="description")
    product_link = soup.findAll("a",{"class":"product-image-url"}, href=True)
    product_image = soup.findAll("img", class_="img-responsive", src=True)
    productTitle = []
    productPrice = []
    productLink = []
    productImage = []

    for each1 in product_title:
        tempTitle = str(each1.get_text())
        tempTitle = tempTitle.replace('\n', '')
        tempTitle = tempTitle.replace('\t', '')
        productTitle.append(str(tempTitle))
        

    for each2 in product_price:
        tempPrice = str(each2.get_text())
        tempPrice = tempPrice.replace('\n', '')
        tempPrice = tempPrice.replace('\t', '')
        productPrice.append(str(tempPrice))


    for each3 in product_link:
        tempLink = each3['href']
        productLink.append(str(tempLink))
        

    for each4 in product_image:
        if(str(each4['src']).__contains__("images.costco-static.com")):
            productImage.append(str(each4['src']))
        else:
            continue



    for each in product_price:
        try:
            title1 = productTitle[cnt]
            price1 =  productPrice[cnt]
            link1 = productLink[cnt]
            image1 = productImage[cnt]
            info1 = [title1, price1, link1, image1]
            if(cnt == 2):
                break
            if price1.__contains__("$") and price1.__contains__("."):
                print(info1)
                r = requests.get(urljson)
                jsonData = json.dumps(r.json(), separators=(',', ':'))
                jsonData = "[" + jsonData[1:len(jsonData)-1] + "," + json.dumps({'item': title1, 'cost': float(price1.replace("$","")[0:price1.index(".")+2]), 'link': link1, 'image': image1, 'comapny': 'Costco', 'shortItem': 'TBA', 'count': 1, 'history':{0:{'time': timeStamp, 'cost': float(price1.replace("$","")[0:price1.index(".")+2])}}}, separators=(',', ':')) + "]"
                data = json.loads(jsonData)
                x = requests.post(urljson, json = data)
            else:
                continue
                        #thewriter.writerow(info)
            cnt = cnt + 1
        except:
            continue
        
    #Ebay
    print("Ebay Catalog: ")    

    url = "https://www.ebay.com"

    driver.get(url)

    def get_url2(search_term):
        template = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1312&_nkw={}&_sacat=0"
        search_term = search_term.replace(' ', '+')
        return template.format(search_term)


    url = get_url2(item)


    #missing


    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #results_products=soup.find_all("div",{"class":"a-section a-spacing-small puis-padding-left-small puis-padding-right-small"}, partial=False)
    #results_product = soup.find_all("span",{"class":"a-size-base-plus a-color-base a-text-normal"}, partial=False)
    cnt = 1
    title1 = ""
    price1 = 0
    link1 = ""
    tempLink = ""
    image1 = ""
    product_price = soup.findAll('span', class_="s-item__price")
    product_title = soup.findAll("div", class_="s-item__title")
    product_link = soup.findAll("a",{"class":"s-item__link"}, href=True)
    product_image = soup.findAll("img", class_="s-item__image-img", src=True)
    productTitle = []
    productPrice = []
    productLink = []
    productImage = []

    for each1 in product_title:
        productTitle.append(str(each1.get_text()))
        
    for each2 in product_price:
        productPrice.append(str(each2.get_text()))


    for each3 in product_link:
        tempLink = each3['href']
        productLink.append(str(tempLink))
        

    for each4 in product_image:
        productImage.append(str(each4['src']))




    for each in product_price:
        try:
            title1 = productTitle[cnt]
            price1 =  productPrice[cnt]
            link1 = productLink[cnt]
            image1 = productImage[cnt]
            info1 = [title1, price1, link1, image1]
            if(cnt==2):
                break
            if price1.__contains__("$") and price1.__contains__("."):
                cnt = cnt + 1
                print(info1)
                r = requests.get(urljson)
                jsonData = json.dumps(r.json(), separators=(',', ':'))
                jsonData = "[" + jsonData[1:len(jsonData)-1] + "," + json.dumps({'item': title1, 'cost': float(price1.replace("$","")[0:price1.index(".")+2]), 'link': link1, 'image': image1, 'comapny': 'Ebay', 'shortItem': 'TBA', 'count': 1, 'history':{0:{'time': timeStamp, 'cost': float(price1.replace("$","")[0:price1.index(".")+2])}}}, separators=(',', ':')) + "]"
                data = json.loads(jsonData)
                x = requests.post(urljson, json = data)
            else:
                continue
                    #thewriter.writerow(info)
        except:
            continue
        
        

    #Staples
    print("Staples Catalog: ")
        
    url = "https://www.staples.com"

    driver.get(url)

    def get_url4(search_term):
        template = "https://www.staples.com/banana/directory_{}"
        search_term = search_term.replace(' ', '+')
        return template.format(search_term)


    url = get_url4(item)


    #missing

    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #results_products=soup.find_all("div",{"class":"a-section a-spacing-small puis-padding-left-small puis-padding-right-small"}, partial=False)
    #results_product = soup.find_all("span",{"class":"a-size-base-plus a-color-base a-text-normal"}, partial=False)
    cnt = 0
    title1 = ""
    price1 = 0
    link1 = ""
    tempLink = ""
    tempPrice = ""
    image1 = ""
    product_price = soup.findAll('span', class_="standard-tile__final_price false")
    product_title = soup.findAll("div", class_="standard-tile__title")
    product_link = soup.findAll("a",{"class":"standard-tile__image_wrapper"}, href=True)
    product_image = soup.findAll("img", class_="standard-tile__image", src=True)
    productTitle = []
    productPrice = []
    productLink = []
    productImage = []
    for each1 in product_title:
        productTitle.append(str(each1.get_text()))
        

    for each2 in product_price:
        tempPrice = str(each2.get_text())
        tempPrice = tempPrice.replace('Final price ', '')
        productPrice.append(str(tempPrice))


    for each3 in product_link:
        tempLink = each3['href']
        productLink.append("https://www.staples.com" + str(tempLink))
        
    for each4 in product_image:
        productImage.append(str(each4['src']))



    for each in product_price:
        try:
            title1 = productTitle[cnt]
            price1 =  productPrice[cnt]
            link1 = productLink[cnt]
            image1 = productImage[cnt]
            info1 = [title1, price1, link1, image1]
            if(cnt == 2):
                break
            if price1.__contains__("$") and price1.__contains__("."):
                print(info1)
                r = requests.get(urljson)
                jsonData = json.dumps(r.json(), separators=(',', ':'))
                jsonData = "[" + jsonData[1:len(jsonData)-1] + "," + json.dumps({'item': title1, 'cost': float(price1.replace("$","")[0:price1.index(".")+2]), 'link': link1, 'image': image1, 'comapny': 'Staples', 'shortItem': 'TBA', 'count': 1, 'history':{0:{'time': timeStamp, 'cost': float(price1.replace("$","")[0:price1.index(".")+2])}}}, separators=(',', ':')) + "]"
                data = json.loads(jsonData)
                x = requests.post(urljson, json = data)
            else:
                continue
                        #thewriter.writerow(info)
            cnt = cnt + 1
        except:
            continue
    #Office Depot
    print("Office Depot Catalog: ")

    url = "https://www.officedepot.com"

    driver.get(url)

    def get_url3(search_term):
        template = "https://www.officedepot.com/a/search/?q={}"
        search_term = search_term.replace(' ', '+')
        return template.format(search_term)


    url = get_url3(item)


    #missing


    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #results_products=soup.find_all("div",{"class":"a-section a-spacing-small puis-padding-left-small puis-padding-right-small"}, partial=False)
    #results_product = soup.find_all("span",{"class":"a-size-base-plus a-color-base a-text-normal"}, partial=False)
    cnt = 0
    title1 = ""
    price1 = 0
    link1 = ""
    tempLink = ""
    image1 = ""
        
    product_price = soup.findAll('span', class_="od-graphql-price-big-price-group")
    product_title = soup.findAll("a", class_="od-product-card-description")
    product_link = soup.findAll("a",{"class":"od-product-card-description"}, href=True)
    product_image = soup.findAll("img", class_="od-sku-image", src=True)
    productTitle = []
    productPrice = []
    productLink = []
    productImage = []
    for each1 in product_title:
        productTitle.append(str(each1.get_text()))
        

    for each2 in product_price:
        productPrice.append(str(each2.get_text()))


    for each3 in product_link:
        tempLink = "https://www.officedepot.com/" + each3['href']
        productLink.append(str(tempLink))
        


    for each4 in product_image:
        productImage.append(str(each4['src']))


    for each in product_price:
        try:
            title1 = productTitle[cnt]
            price1 =  productPrice[cnt]
            link1 = productLink[cnt]
            image1 = productImage[cnt]
            info1 = [title1, price1, link1, image1]
            if(cnt == 2):
                break
            if price1.__contains__("$") and price1.__contains__("."):
                print(info1)
                r = requests.get(urljson)
                jsonData = json.dumps(r.json(), separators=(',', ':'))
                jsonData = "[" + jsonData[1:len(jsonData)-1] + "," + json.dumps({'item': title1, 'cost': float(price1.replace("$","")[0:price1.index(".")+2]), 'link': link1, 'image': image1, 'comapny': 'Office Depot', 'shortItem': 'TBA', 'count': 1, 'history':{0:{'time': timeStamp, 'cost': float(price1.replace("$","")[0:price1.index(".")+2])}}}, separators=(',', ':')) + "]"
                data = json.loads(jsonData)
                x = requests.post(urljson, json = data)
            else:
                continue
                        #thewriter.writerow(info)
        except:
            continue
        cnt = cnt + 1
        
    data = json.loads(jsonData)
    print("*********")
    print(data)
    print("*********")
    x = requests.post(urljson, json = data)
    print(x)
    print("**********")
    return(data)
def run():
	app.run(host='0.0.0.0',port=8080)

t = Thread(target=run)
t.start()
