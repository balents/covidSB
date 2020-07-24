print("starting script")
import sys
print(sys.version)
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from datetime import datetime, date
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

url = 'https://publichealthsbc.org/status-reports/'
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0"
response = requests.get(url,headers = headers)
soup = BeautifulSoup(response.text, "html.parser")

allits=soup.find_all("div",class_="elementor-accordion-item")
datetimes = []
totalcases = []
totaldaily = []
daybeforestart = datetime(2020, 5, 11)
for item in allits:
    phrase = item.find("a",class_="elementor-accordion-title").text
    date = phrase.split(" as of ")[0]
    date_object = datetime.strptime(date, "%B %d, %Y")
    if date_object < daybeforestart: break
    rows = item.find_all("tr")
    if len(rows)>0:
        for (rnum,row) in enumerate(rows):
            first = row.find("strong")
            coltot=999
            colday=999
            if first != None: 
                if "Geographic Area" in first.text: 
                    headers = row.find_all("td")
                    for (ii,ss) in enumerate(headers):
                        name = ss.find("strong").text               
                        if ("Cases" in name) and ("Confirmed" in name):
                            coltot=ii
                        if ("Cases" in name) and ("Daily" in name):
                            colday=ii
                if coltot<999 and colday<999:
                    lastrow = rnum
                    break
        for rr in range(lastrow+1,len(rows)):
            row = rows[rr]
            place = row.find("td").find("strong").text
            if place == 'CITY OF SANTA BARBARA':
                tds = row.find_all("td")
                ntot=int(tds[coltot].find("strong").text)
                nday=int(tds[colday].find("strong").text)
                break
        datetimes.append(date_object)
        totalcases.append(ntot)
        totaldaily.append(nday)
dates = matplotlib.dates.date2num(datetimes)
formatter = DateFormatter('%m/%d/%y')
matplotlib.style.use('seaborn')
fig, (ax1,ax2) = plt.subplots(1,2)
ax1.plot_date(datetimes, totalcases,linestyle='solid')
ax1.set_ylabel('Cases')
ax1.xaxis.set_major_formatter(formatter)
ax1.xaxis.set_tick_params(rotation=30, labelsize=10)


avg = []
max = len(totaldaily)-7
for i in range(0,max):
    diff = sum(totaldaily[i:i+7])
    average = diff/7.0
    avg.append(average)
truncateddates = matplotlib.dates.date2num(datetimes[:-7])
formatter = DateFormatter('%m/%d/%y')
matplotlib.style.use('seaborn')
ax2.plot_date(truncateddates, avg,linestyle='solid')
ax2.set_ylabel('Daily cases 7 sample average')
ax2.xaxis.set_major_formatter(formatter)
ax2.xaxis.set_tick_params(rotation=30, labelsize=10)
now=datetime.now().strftime('%H:%M on %A, %d %b %Y')
fig.suptitle('City of Santa Barbara data as of '+datetimes[0].strftime("%A, %d %b %Y")+'\n data extracted as of '+now)
fig.savefig('./graphs.png',bbox_inches='tight')

