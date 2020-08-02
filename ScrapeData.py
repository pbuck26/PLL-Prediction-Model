import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import datetime
from datetime import time, timedelta
import bs4
from bs4 import BeautifulSoup as bs
import time
import queue

# build queue for days to be scraped
q = queue.Queue(maxsize=0)


# TODO MAKE THIS CONFIGURABLE ON GUI?
#start = datetime.datetime(2019, 3, 20)
#stop = datetime.datetime(2019, 3, 23)
#index = pd.date_range(start, stop)
#ts = pd.Series()
#q.put(index)

#Configure webdriver
browser = webdriver.Safari()
browser.implicitly_wait(6)
url = f'https://stats.premierlacrosseleague.com/games'
browser.get(url)
# give the browser time to wait
time.sleep(3)
html = browser.page_source.encode("utf-8")
# convert to beautiful soup object
soup = bs(html, 'html.parser')
# print the current day
gameLinks = soup.find_all('a', {'class':'jss15'})

# iterate over each link
for link in range(len(gameLinks)):
    try:
        partialLink = gameLinks[link]['href']
        browser.get(url[:-6] + partialLink)
        browser.implicitly_wait(6)
        # grab all of the team data
        # table stats --> <td class="MuiTableCell-root MuiTableCell-body jss2409 MuiTableCell-alignCenter MuiTableCell-sizeSmall">9</td>
        # team name --> <a href="/teams/RED">RED</a>
        # S	1G	2G	A	Sh	Sh%	SOG	TO	CT	GB	FO	FO%	Sv	Sv%	SA	SAA	PEN	PIM	PP%	PP	PPSh	PK%	PK
        html = browser.page_source.encode("utf-8")
        # convert to beautiful soup object
        soup = bs(html, 'html.parser')
        teamStats = soup.find_all('td', class_ = 'MuiTableCell-root MuiTableCell-body jss187 MuiTableCell-alignCenter MuiTableCell-sizeSmall')
        teamNamesTemp = soup.find_all('a', class_ = 'href')
        TeamNameHome = teamNamesTemp[0].text
        TeamNameAway = teamNamesTemp[1].text
    except:
        print("Link Invalid")
        continue
    



browser.quit()