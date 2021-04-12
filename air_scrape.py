import csv
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import datetime
import pandas as pd


##### basic function to open the links in the csv file and returns the links in a list.
#### i would like to change this to dynamically create the links so we can change the dates and potentially other options
def openLinks():

    #open the csv containing the hyper links and save each link to a  list
    with open('links.csv') as links:
        linkReader = csv.reader(links)
        links = [x[0] for x in linkReader]
    return links





###function that scrapes the page for each link in the list of links saved in the csv file 
def scrapeNsave(links):

    # use the links from the CSV file
    links = openLinks()

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
        time.sleep(6)
        # add the html to the html list
        HTMLlist.append(browser.html)
        time.sleep(1)
    browser.quit()


    ### creating the data structure in dictionary form
    data_dict={
    'title':[],
    'location':[],
    'total':[],
    'costPerPerson':[],
    'basePerNight':[],
    'extraFees':[], 
    'startDate':[],
    'endDate':[],
    'nights':[],
    'averageRating':[],
    'numOfRatings':[],
    'rooms':[],
    'beds':[],
    'baths':[],
    'guests':[]
    } 


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
        # add the total to the list
        data_dict['total'].append(total)

        try:
            #get the base price per night
            basePerNight=airSoup.find(class_='_pgfqnw').text
            #convert to integer
            basePerNight= int(basePerNight[1:].replace(',',''))
        except:
            basePerNight='null'
        data_dict['basePerNight'].append(basePerNight)

        try:
            # get the dates 
            dates= airSoup.findAll(class_='_1g8031c')
            ##get the start date and the end date from the list of items with the """date""" class
            startDate= dates[0].text
            endDate=dates[1].text
        except:
            startDate='null'
            endDate='null'

        data_dict['endDate'].append(endDate)

        data_dict['startDate'].append(startDate)

        try:
            ###calculate the numbert of nights use the end and start dates. uses datetime, I could use an alias for date time to make the prettier
            nights = int((datetime.datetime.strptime(endDate,'%m/%d/%Y')-datetime.datetime.strptime(startDate,'%m/%d/%Y')).days)
        except:
            nights='null'
        data_dict['nights'].append(nights)

        try:

            #use the base fee per night, number of nights, and total to calculate the 'other fees'
            extraFees = total - basePerNight*nights
        except:
            extraFees='null'
        data_dict['extraFees'].append(extraFees)

        try:
            ### get average review 
            averageRating = float(airSoup.find(class_='_12si43g').text)
        except:
            averageRating='null'

        data_dict['averageRating'].append(averageRating)

        try:
            # get the title
            title =airSoup.find(class_='_14i3z6h').text
        except:
            title='null'

        data_dict['title'].append(title)

        try:
            # get the number of ratings
            numOfRatings = int(airSoup.find(class_='_bq6krt').text[1:-1])
        except:
            numOfRatings='null'

        data_dict['numOfRatings'].append(numOfRatings)

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

        data_dict['rooms'].append(room)
        data_dict['beds'].append(bed)
        data_dict['baths'].append(bath)

        try:
            # get number of guests
            guests= int((airSoup.find(class_='_1ir6ymk').text).split(' ')[0])
        except:
            guests ='null'

        data_dict['guests'].append(guests)


        try:
            location = airSoup.find(class_='_169len4r').text
        except:
            location = 'null'

        data_dict['location'].append(location)

        try:
            data_dict['costPerPerson'].append((total/guests))
        except:
            data_dict['costPerPerson'].append('null')
 
    ## add the links to the data dictionary 
    data_dict['links']=links

    ## convert the dictionary into a datafram
    df = pd.DataFrame(data_dict)

    ## sort by cost per person
    # df =  df.sort_values(by=['costPerPerson']).reset_index(drop=True)

    print(df)

    # save results as a csv
    df.to_csv('results.csv',index=False)

    ### return the dataframe for later use
    return df



#### i set the functions up this way so I could easily change how i'm feeding the function links, possibly making the more dynamic
links = openLinks()

scrapeNsave(links)