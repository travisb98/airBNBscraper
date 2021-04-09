import csv
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import datetime
import pandas as pd


#open the csv containing the hyper links and save each link to a  list
with open('links.csv') as links:
    linkReader = csv.reader(links)
    links = [x[0] for x in linkReader]



# define executable path using location of chrome drive
executable_path = {'executable_path': "C:/Program Files (x86)/Chrome Driver/chromedriver.exe"}

## defining the browser by using the executable path
browser = Browser('chrome', executable_path, headless=False)

## create a list to save the html for each page
HTMLlist =[]


### for each link
for link in links:
    # opend the browser to the link
    browser.visit(link)
    time.sleep(10)
    # add the html to the html list
    HTMLlist.append(browser.html)
    time.sleep(2)
browser.quit()

# create an empty list for each feature

totalList=[]

basePerNightList=[]

startDateList = []

endDateList = []

nightsList = []

extraFeesList=[]

starList = []

titleList = []

ratingList =[]

roomList=[]

bedList=[]

bathList=[]

guestsList=[]

locationList = []


# for each saved HTML page
for airHTML in HTMLlist:
    # parse the html into soup
    airSoup=bs(airHTML,'html.parser')

    try:
        ### get the total from the html
        total = airSoup.find(class_='_1d3ext9m').text
        ### convert total into an integer
        total = int(total[1:].replace(',',''))
    except:
        total = 'null'

    totalList.append(total)


    try:
        #get the base price per night
        basePerNight=airSoup.find(class_='_pgfqnw').text
        #convert to integer
        basePerNight= int(basePerNight[1:].replace(',',''))
    except:
        basePerNight='null'
    basePerNightList.append(basePerNight)

    try:
        # get the dates 
        dates= airSoup.findAll(class_='_1g8031c')
        ##get the start date and the end date from the list of items with the """date""" class
        startDate= dates[0].text
        endDate=dates[1].text
    except:
        startDate='null'
        endDate='null'

    startDateList.append(startDate)
    endDateList.append(endDate)


    try:
        ###calculate the numbert of nights use the end and start dates. uses datetime, I could use an alias for date time to make the prettier
        nights = int((datetime.datetime.strptime(endDate,'%m/%d/%Y')-datetime.datetime.strptime(startDate,'%m/%d/%Y')).days)
    except:
        nights='null'
    nightsList.append(nights)


    try:

        #use the base fee per night, number of nights, and total to calculate the 'other fees'
        extraFees = total - basePerNight*nights
    except:
        extraFees='null'
    extraFeesList.append(extraFees)

    try:
        ### get average review 
        star = float(airSoup.find(class_='_12si43g').text)
    except:
        star='null'

    starList.append(star)

    try:
        # get the title
        title =airSoup.find(class_='_14i3z6h').text
    except:
        title='null'

    titleList.append(title)


    try:
        # get the number of ratings
        rating = int(airSoup.find(class_='_bq6krt').text[1:-1])
    except:
        rating='null'

    ratingList.append(rating)

    # get the number of  bedrooms, beds, and baths
    try:
        bbb= airSoup.find(class_='_tqmy57').text.split('·')

        room = int(bbb[1][1])
        bed = int(bbb[2][1])
        bath =int(bbb[3][1])
    except:
        room = 'null'
        bed = 'null'
        bath ='null'


    roomList.append(room)
    bedList.append(bed)
    bathList.append(bath)



    try:
        # get number of guests
        guests= int((airSoup.find(class_='_1ir6ymk').text).split(' ')[0])
    except:
        guests ='null'

    guestsList.append(guests)

    try:
        location = airSoup.find(class_='_169len4r').text
    except:
        location = 'null'
    locationList.append(location)
    

## save results to dataframe
df=pd.DataFrame({
    'total':totalList,
    'nightlyFee':basePerNightList,
    'startDate':startDateList,
    'endDate':endDateList,
    'nights':nightsList,
    'extraFees':extraFeesList,
    'averageRating':starList,
    'title':titleList,
    'numOfRatings':ratingList,
    'rooms':roomList,
    'beds':bedList,
    'baths':bathList,
    'guests':guestsList,
    'location':locationList
})

print(df)


# save results as a csv
df.to_csv('results.csv')

