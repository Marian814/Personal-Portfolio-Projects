from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
from selenium.webdriver.common.by import By

GOOGLE_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSf9fDXXuaDOEKadIGWNjWIMfylYNsNZ71f0MpUW6QAeEeCAng/viewform?usp=dialog"
ZILLOW = "https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-122.63417331103516%2C%22east%22%3A-122.23248568896484%2C%22south%22%3A37.66992586293845%2C%22north%22%3A37.8805080917795%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22priorityscore%22%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A601844%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22baths%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%2C%22usersSearchTerm%22%3A%22San%20Francisco%20CA%22%7D"

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Accept-Language": "ro-RO,ro;q=0.9,en-US;q=0.8,en;q=0.7"
}

response = requests.get(ZILLOW, headers=header)

data = response.text
soup = BeautifulSoup(data, "html.parser")

link_elements = soup.select(".StyledPropertyCardDataWrapper-c11n-8-109-3__sc-hfbvv9-0.gpfUSu.property-card-data a")
links = [link["href"] for link in link_elements]
print(f"There are {len(links)} rents:\n")
print(links)

address_elements = soup.select(".StyledPropertyCardDataWrapper-c11n-8-109-3__sc-hfbvv9-0.gpfUSu.property-card-data address")
addresses = [address.get_text().replace(" | ", " ").strip() for address in address_elements]
print(addresses)

price_elements = soup.select(".PropertyCardWrapper__StyledPriceGridContainer-srp-8-109-3__sc-16e8gqd-0.bcrfLm span")
prices = [price.get_text().replace("/mo", "").split("+")[0] for price in price_elements if "$" in price.text]
print(prices)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

for n in range(len(links)):
    driver.get(GOOGLE_FORM)
    time.sleep(5)

    address = driver.find_element(by=By.XPATH,
                                  value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(by=By.XPATH,
                                value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(by=By.XPATH,
                               value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(by=By.XPATH,
                                        value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')

    address.send_keys(addresses[n])
    price.send_keys(prices[n])
    link.send_keys(links[n])
    submit_button.click()
