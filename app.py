import streamlit as st
import datetime
import requests
import pytz
import numpy as np

'''
# NYC Taxifare Predictor
'''

st.markdown('''
## This app is designed to help you forecast the price of a taxi ride in NYC based on your location and pickup time
''')

#The code below handles the pick up date and time


d = st.date_input("Enter the date of your ride:",
                   datetime.date(2022, 1, 1))

t = st.time_input("Enter the time of your ride:",
                   datetime.time(10, 30))

combined=str(datetime.datetime.combine(d, t))
pickup_datetime = datetime.datetime.strptime(combined, "%Y-%m-%d %H:%M:%S")
eastern = pytz.timezone("US/Eastern")
localized_pickup_datetime = eastern.localize(pickup_datetime, is_dst=None)
utc_pickup_datetime = localized_pickup_datetime.astimezone(pytz.utc)
formatted_pickup_datetime = utc_pickup_datetime.strftime("%Y-%m-%d %H:%M:%S UTC")





#The code below handles the pick-up and drop-off coordinates


pick_up= st.text_input('Enter your pick up location', '844 AVENUE OF THE AMERICAS')
drop_off=st.text_input('Enter your drop off location', '1200 BROADWAY')


url = "https://maps.googleapis.com/maps/api/geocode/json"


params1 = {"address": pick_up,"key": key}
params2 = {"address": drop_off,"key": key}

response1 = requests.get(url,params1).json()
response2 = requests.get(url,params2).json()

pickup_longitude=response1["results"][0]["geometry"]["location"]["lng"]
pickup_latitude=response1["results"][0]["geometry"]["location"]["lat"]

dropoff_longitude=response2["results"][0]["geometry"]["location"]["lng"]
dropoff_latitude=response2["results"][0]["geometry"]["location"]["lat"]


#The code below handles the number of passengers

option = st.slider('Enter the number of passengers:', 1, 10, 3)

nb_passengers = int(option)


#The code below calls the API

if st.button('Predict'):

    url = 'https://taxifare.lewagon.ai/predict'

    params = {"pickup_datetime":formatted_pickup_datetime[:-4],
            "pickup_longitude":pickup_longitude,
            "pickup_latitude":pickup_latitude,
            "dropoff_longitude":dropoff_longitude,
            "dropoff_latitude":dropoff_latitude,
            "passenger_count": nb_passengers}


    response = requests.get(url,params)

    st.write("Your ride will cost you: ",str(np.round(response.json()["fare"])))
