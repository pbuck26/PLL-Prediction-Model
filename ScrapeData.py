import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import bs4
from bs4 import BeautifulSoup as bs
import time
#import matplotlib


#Configure webdriver
browser = webdriver.Safari()
browser.implicitly_wait(6)
url = f'https://stats.premierlacrosseleague.com/pll-team-table'
browser.get(url)
# give the browser time to wait
time.sleep(3)
html = browser.page_source.encode("utf-8")
# convert to beautiful soup object
soup = bs(html, 'html.parser')
# initialize Stats List
Stats = []
teamStats = soup.find_all('td', class_= 'MuiTableCell-root MuiTableCell-body jss351 MuiTableCell-alignCenter MuiTableCell-sizeSmall')
for teams in range(1,8):
    try:
        game = {}
        # Home Team
        # temporary
        if teams == 1:
            game['Team'] = 'Whipsnakes'
        elif teams == 2:
            game['Team'] = 'Chrome'
        elif teams == 3:
            game['Team'] = 'Archers'
        elif teams == 4:
            game['Team'] = 'Redwoods'
        elif teams == 5:
            game['Team'] = 'Waterdogs'
        elif teams == 6:
            game['Team'] = 'Atlas'
        elif teams == 7:
            game['Team'] = 'Chaos'
    
        game['Wins'] = int(teamStats[0].text)
        game['Losses'] = int(teamStats[1].text)
        game['Scores'] = int(teamStats[2].text)
        game['1G'] = int(teamStats[3].text)
        game['2G'] = int(teamStats[4].text)
        game['A'] = int(teamStats[5].text)
        game['Sh'] = int(teamStats[6].text)
        game['Sh%'] = int(teamStats[7].text[:-1])
        game['2-Point Sh%'] = int(teamStats[8].text[:-1])
        game['SOG'] = int(teamStats[9].text)
        game['TO'] = int(teamStats[10].text)
        game['CT'] = int(teamStats[11].text)
        game['GB'] = int(teamStats[12].text)
        game['FO'] = int(teamStats[13].text[0:1]) / int(teamStats[13].text[3:])
        game['FO%'] = int(teamStats[14].text[:-1])
        game['SV'] = int(teamStats[15].text)
        game['SV%'] = int(teamStats[16].text[:-1])
        game['SA'] = int(teamStats[17].text)
        game['SAA'] = float(teamStats[18].text[:-1])
        game['PEN'] = int(teamStats[19].text)
        game['PIM'] = float(teamStats[20].text)
        game['PP%'] = int(teamStats[21].text[:-1])
        game['PP'] = int(teamStats[22].text[0]) / int(teamStats[22].text[2:])
        game['PPSh'] = int(teamStats[23].text)
        game['PK%'] = int(teamStats[24].text[:-1])
        game['PK'] = int(teamStats[25].text[0]) / int(teamStats[25].text[2:])
        Stats.append(game)
        # Delete the info we just used from soup
        teamStats = teamStats[26:]
    except:
        print("Something went wrong!!!")
        continue

stats_df = pd.DataFrame(Stats)
stats_df.to_csv('~/Documents/Code/PLLModel/Stats.csv',)
print(Stats)
browser.quit()