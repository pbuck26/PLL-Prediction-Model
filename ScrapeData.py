import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import datetime
from datetime import time, timedelta
import bs4
from bs4 import BeautifulSoup as bs
import time
import queue

# build queue for days to be scraped
q = queue.Queue(maxsize=0)

# I want to grab all of the 2019 season data
# season starting on march 20
# and ended September 29

# TODO MAKE THIS CONFIGURABLE ON GUI?
start = datetime.datetime(2019, 3, 20)
stop = datetime.datetime(2019, 3, 23)
index = pd.date_range(start, stop)
ts = pd.Series()
#q.put(index)

#while loop for scraping    
for dayIdx in range(len(index)):
    days = index[dayIdx].strftime("%Y") + "-" + \
        index[dayIdx].strftime("%m")+ "-" + index[dayIdx].strftime("%d")
    # Configure webdriver
    browser = webdriver.Safari()
    browser.implicitly_wait(6)
    url = f'https://www.covers.com/sports/mlb/matchups?selectedDate={days}'
    browser.get(url)
    # give the browser time to wait
    time.sleep(3)
    html = browser.page_source.encode("utf-8")
    # convert to beautiful soup object
    soup = bs(html, 'html.parser')
    currdate = soup.find('a', {'class':'cmg_active_navigation_item'})
        # print the current day
    if currdate['data-date'] == days:
        # temporary data structure is gonna be a list of dicts
        runTotals = soup.find_all('td', {'class':'cmg_matchup_line_score_total'})
        teamNames = soup.find_all('div', {'class':'cmg_team_name'})
        count = 0
        # find number of scores to associate with this day
        teamRuns = [None] * len(runTotals)
        for scores in range(len(runTotals)):
            count += 1
            if count ==1:
                # temporary data structure is gonna be a list of dicts
                teamRuns[scores] = [{teamNames[scores].text.strip()[-3:]: int(runTotals[scores].text)}]
            elif count == 2:
                teamRuns[scores] = [{teamNames[scores].text.strip()[-3:]: int(runTotals[scores].text)}]
                count = 0
        print(currdate['data-date'])
    else:
        print(f"{days}: no games")
    browser.quit()
    

