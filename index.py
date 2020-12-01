# app.py
from flask import Flask, request, json, jsonify
import requests
from lxml import html
import csv
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
from sys import platform

app = Flask(__name__)


# Read CSV File
def read_CSV(file, json_file):
    csv_rows = []
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        field = reader.fieldnames
        for row in reader:
            csv_rows.extend([{field[i]: row[field[i]] for i in range(len(field))}])
        convert_write_json(csv_rows, json_file)


# Convert csv data into json
def convert_write_json(data, json_file):
    with open(json_file, "w") as f:
        f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')))  # for pretty


# function to take care of downloading file
def enable_download_headless(browser, download_dir):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)


def initChromeDriver():
    # instantiate a chrome options object so you can set the size and headless preference
    # some of these chrome options might be uncessary but I just used a boilerplate
    # change the <path_to_download_default_directory> to whatever your default download folder is located
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--verbose')
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": "<path_to_download_default_directory>",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
    })
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')

    chromedriver = "chromedriver"
    # initialize driver object and change the <path_to_chrome_driver> depending on your directory where your chromedriver should be
    #driver = webdriver.Chrome(ChromeDriverManager().install())
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="E:/chromedriver.exe")

    # change the <path_to_place_downloaded_file> to your directory where you would like to place the downloaded file
    # file = os.environ['USERPROFILE'] + '\Downloads'
    # file = os.environ['HOME'] + "/Downloads"
    # download_dir = file

    # function to handle setting up headless download
    # enable_download_headless(driver, download_dir)
    return driver


# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"



@app.route('/postmates/scores', methods=['GET'])
def postmate_scores():
    #driver = initChromeDriver()
    itemlist =[]
    #driver = webdriver.Chrome("chromedriver.exe")
    url = "https://www.cbssports.com/college-football/rankings/index/"
    try:
        page = requests.get(url)
        tree = html.fromstring(page.content)

        pagetitles = tree.xpath('.//*[@id="TableBase"]/h4/text()')
        print(len(pagetitles))
        index = 0
        for title in pagetitles:
            print(title.strip())
            index += 1
            print(index)
            print(title.strip().find("CBS Sports Ranking"))
            if title.strip().find("CBS Sports Ranking") != -1 and index == 5:
                # hrefs = tree.xpath('//*[@id="TableBase"]/div[1]/div/table/tbody/tr[1]/td[2]/span/div/div[2]/div/span/a/text()')
                # hrefs = tree.xpath('.//div[contains(@id, "TableBase") and 3]//span[@class="TeamName"]/a/text()')
                hrefs = tree.xpath(
                    './/div[contains(@class, "TableBaseWrapper") and position()=3]//span[@class="TeamName"]/a/text()')
                print(len(hrefs))
                for href in hrefs:
                    print(href)
                    itemlist.append(href)
            else:
                print("Not found!")

    except NoSuchElementException:
        print('No found Element')
        #driver.quit()
    json_numbers = json.dumps(itemlist)
    print(json_numbers)

    return json_numbers


if __name__ == '__main__':

    app.run()

