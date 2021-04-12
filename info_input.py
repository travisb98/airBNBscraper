import datetime
# for normal usage
from formlayout import fedit



def dBox():


    ### maybe I could scrape to get a list of cities?
    location_list = [0,'Minneapolis St Paul (MSP)','Seattle (Any)','IllAddMoreCitiesLater']



    datalist=[
        ('Start', datetime.date(2010, 10, 10)),
        ('End',datetime.date(2020, 8, 10)),
        ('Home',location_list ),
        ('Destination', location_list)
        ]


    #### version without apply button or function
    response_dict=fedit( datalist, title="Date Range Selector",
                comment="Aye Homie, pick a date range.",
                cancel='Cancel',
                ok='Submit',
                result='dict',
                type='questions',
                scrollbar=True,
                background_color='#6c6',
                widget_color='#cf9')

    return response_dict