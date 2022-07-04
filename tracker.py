import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import smtplib
from email.message import EmailMessage

Max_price = 66000
EMAIL_ADDRESS = "sender's email address"
EMAIL_ADDRESS2 = "recipient's email address"
EMAIL_PASSWORD = '16 digit password generated from gmail' "check if 2 step verification is on, go to app password and create 16 digit id"


def get_product_info(driver):
    product_id = "title_feature_div"
    price_id = "corePriceDisplay_desktop_feature_div"

    product_title = driver.find_element(By.ID, product_id).text
    product_price = driver.find_element(By.ID, price_id).text[5:12].replace(',', '')
    return {
        "title": product_title,
        "price": product_price,
    }


def send_email(product):
    msg = EmailMessage()
    msg['Subject'] = "Amazon Price Tracker Notification"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS2
    msg.add_alternative("""
        <!DOCTYPE html>
        <html>
            <body>
                <h2>Your featured product is under ₹""" + str(Max_price) + """. Don't miss it out!</h2>
                <ul>
                  <li><b>Name:</b> """ + product["title"] + """</li>
                  <li><b>Price:</b> ₹""" + product["price"] + """</li>
                  <li><b>URL:</b> """ + URL + """</li>
                </ul>
            </body>
        </html>
        """, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


if __name__ == '__main__':
    options = Options()
    options.add_argument("--headless")
    s = Service('chromedriver.exe')
    driver = webdriver.Chrome(service=s, options=options)

    URL = "https://www.amazon.in/Apple-iPhone-13-Mini-128GB/dp/B09G9FNN4X"
    driver.get(URL)

while (True):

    product_info = get_product_info(driver)

    if float(product_info["price"]) <= float(Max_price):
        send_email(product_info)
    time.sleep(60 * 60 * 24)