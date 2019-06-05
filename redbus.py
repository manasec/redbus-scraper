import bs4
import requests
from selenium import webdriver
from time import sleep
import patterns
import re
from List2xlsx import List2xlsx

def open_url(url):
    driver = webdriver.Chrome(executable_path=r"C:\Users\acer\Desktop\python\chromedriver_win32\chromedriver.exe")
    driver.get(url)
    return driver

def get_validity(driver):
    validity = []
    valid = driver.find_elements_by_css_selector(".OfferValidity")
    for vali in valid:
        validity.append(vali.text)
        
    return validity

def get_text(soup):
    tagobjects = soup.select(".TNCTermsliText")
    text = ""
    for tagobject in tagobjects:
        text = text + tagobject.text + "\n"
    return text

def code_and_details(text):
    coupon_code = patterns.coupon_code_pattern.search(text)
    offer_details = patterns.ods.findall(text)
    details = ""
    if coupon_code:
        if "Referral" not in text:
            coupon_code = coupon_code.group(0)
            for offer_detail in offer_details:
                details += offer_detail
            
        else:
            offer_detail = soup.select("#OfferDiscription")[0]
            coupon_code = "your referral code"
            details += offer_detail.text
        
    else:
        coupon_code = "N/A"
        for offer_detail in offer_details:
            details += offer_detail

    return coupon_code, details

def get_minimum_amount(text):
    mini = patterns.minimum.search(text)
    if mini:
        mini = mini.group(0)
    else:
        mini = "N/A"
        
    return mini

def get_booking_channel(text):
    channel = patterns.chan.search(text)
    if channel:
        channel = channel.group(0)
    else:
        channel = "All channels"

    return channel

def get_offer_type(soup):
    offer_type = soup.select(".offerType")[0]
    offer_type = offer_type.text

    return offer_type

def get_applicable_bank(text):
    applicable_bw = patterns.applicable.search(text)
    if applicable_bw:
        applicable_bw = applicable_bw.group(0)
    else:
        applicable_bw = "N/A"

    return applicable_bw

def get_constraints(text):
    constraint = patterns.constreg.search(text)
    if "Referral" not in text:
        if constraint:
            constraint = constraint.group(0)
        else:
            constraint = "N/A"
    else:
        constraint = "can only earn 1000 from referral program"

    return constraint

def get_offer_link(text, offer_type):
    if "BUS" in offer_type:
        link = "https://www.redbus.in/bus-tickets/"
    if "HOTEL" in offer_type:
        link = "https://www.redbus.in/hotels/"
    link = '=HYPERLINK("{}","{}")'.format(link, "Link")

    return link

platform = "Redbus"
workbook = "data.xlsx"
sheetname = "Sheet1"
url = "https://www.redbus.in/info/OfferTerms"
driver = open_url(url)

validity = get_validity(driver)

tiles = driver.find_elements_by_css_selector(".tiles")
alist = []


for index,tile in enumerate(tiles):
    
    text = ""
    tile.click()
    page_source = driver.page_source
    soup = bs4.BeautifulSoup(page_source, 'html.parser')
    
    text = get_text(soup)
    
    coupon_code, details = code_and_details(text)
    mini = get_minimum_amount(text)
    channel = get_booking_channel(text)
    applicable_bw = get_applicable_bank(text)
    constraint = get_constraints(text)
    offer_type = get_offer_type(soup)
    link = get_offer_link(text, offer_type)
        
    driver.find_element_by_css_selector("#offerClose").click()
    
    alist.append([platform, coupon_code, offer_type, details, mini,
                   channel, applicable_bw,validity[index],constraint, link])
    
List2xlsx.list2xlsx(workbook, sheetname,alist)
List2xlsx.formatting(workbook,sheetname)
sleep(5)
driver.quit()


