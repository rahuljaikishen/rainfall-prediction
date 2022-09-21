import streamlit as st
import pandas as pd
import json
import requests
import datetime
from common.config import config

def get_rainfall_predictions(rainfall_data):
    files = {'upload_file': rainfall_data}
    res = requests.post(config['API']['URL']+'/predictions', files=files)
    data = []
    if res.status_code == 200:
        data = res.json()
    return data

def home_page():
    with st.form("my_form"):
        st.write("Inside the form")
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            pred = get_rainfall_predictions(uploaded_file.getvalue())
            if len(pred) > 0:
                data = pd.json_normalize(json.loads(pred))
            else:
                data = "Please try again after sometime"
        submitted = st.form_submit_button("Submit")
        if submitted and uploaded_file is None:
            st.error("Please enter a Vaild File")
        elif submitted and uploaded_file is not None:
            st.write(data)
    

m = st.markdown("""
<style>
.css-k008qs > div.stButton {
    display:flex;
    justify-content:center;
    align-items:center;
}
div.stButton > button:hover {
    transform:translateY(-5px);
    transition: 0.3s all ease-in-out;
    }
</style>""", unsafe_allow_html=True)


###################################
######### PAGE TWO ################
###################################


def get_rain_prediction(data):
    print(data)
    res = requests.post(config['API']['URL'] + '/predict_rain', data=json.dumps(data))
    if res.status_code == 200:
        return res.json()['msg']
    else:
        return "Please try again later"

def page_two():
    st.markdown("# Page 2 ❄️")
    with st.sidebar:
        st.sidebar.markdown("# Page 2 ❄️")
        
    with st.form("get_pred"):
        st.write("Inside the form")

        ###DATA VAR ##
        predict_date = st.date_input("When's your birthday",datetime.date(2022, 6, 21))
        
        locations = 'Albury', 'BadgerysCreek', 'Cobar', 'CoffsHarbour', 'Moree','Newcastle', 'NorahHead', 'NorfolkIsland', 'Penrith', 'Richmond','Sydney', 'SydneyAirport', 'WaggaWagga', 'Williamtown','Wollongong', 'Canberra', 'Tuggeranong', 'MountGinini', 'Ballarat','Bendigo', 'Sale', 'MelbourneAirport', 'Melbourne', 'Mildura','Nhil', 'Portland', 'Watsonia', 'Dartmoor', 'Brisbane', 'Cairns','GoldCoast', 'Townsville', 'Adelaide', 'MountGambier', 'Nuriootpa','Woomera', 'Albany', 'Witchcliffe', 'PearceRAAF', 'PerthAirport','Perth', 'SalmonGums', 'Walpole', 'Hobart', 'Launceston','AliceSprings', 'Darwin', 'Katherine', 'Uluru'
        windgustdir_sel = 'W', 'WNW', 'WSW', 'NE', 'NNW', 'N', 'NNE', 'SW', 'ENE','SSE', 'S', 'NW', 'SE', 'ESE', 'E', 'SSW'
        loc_selectbox = st.selectbox(
                        "Select Locations",
                        (locations)
                        )
        min_temp = st.slider('Min Temprature', -10.0, 35.0, 5.0, step=0.1)
        max_temp = st.slider('Max Temprature', -10.0, 50.0, 5.0, step=0.1)
        rainfall = st.number_input('Rainfall',min_value=0.0,max_value=371.0)
        windgustdir = st.selectbox(
                        "WindGustDir",
                        (windgustdir_sel)
                        )
        windgustspeed = st.number_input('WindGustSpeed',min_value=0.0,max_value=140.0)
        winddir9am = st.selectbox(
                        "WindDir9am",
                        (windgustdir_sel)
                        )
        winddir3am = st.selectbox(
                        "WindDir3am",
                        (windgustdir_sel)
                        )
        windspeed3pm = st.number_input('WindSpeed3pm',min_value=0.0,max_value=370.0)
        windspeed9am = st.number_input('WindSpeed9am',min_value=0.0,max_value=100.0)

        humidity3pm = st.number_input('Humidity3pm',min_value=0.0,max_value=100.0)
        humidity9am = st.number_input('Humidity9am',min_value=0.0,max_value=100.0)

        pressure3pm = st.number_input('Pressure3pm',min_value=0.0,max_value=1050.0)
        pressure9am = st.number_input('Pressure9am',min_value=0.0,max_value=1050.0)

        cloud3pm = st.slider('Cloud3pm', 0.0, 10.0, 1.0, step=1.0)
        cloud9am = st.slider('Cloud9am', 0.0, 10.0, 1.0, step=1.0)

        temp3pm = st.number_input('temp3pm',min_value=0.0,max_value=50.0)
        temp9am = st.number_input('temp9am',min_value=0.0,max_value=50.0)

        raintoday = st.selectbox(
                        "Rain Today",
                        ("No","Yes")
                        )

        #number = st.number_input('Insert a number',min_value=0.0,max_value=371.0)
        submitted = st.form_submit_button("Submit")
            
    if submitted is True:
        data = {
            "Date":predict_date.strftime("%Y-%m-%d"),
            "Location": loc_selectbox,
            "MinTemp": min_temp,
            "MaxTemp": max_temp,
            "Rainfall": rainfall,
            "WindGustDir":windgustdir,
            "WindGustSpeed":windgustspeed,
            "WindDir9am":winddir9am,
            "WindDir3pm":winddir3am,
            "WindSpeed3pm":windspeed3pm,
            "WindSpeed9am":windspeed9am,
            "Humidity3pm":humidity3pm,
            "Humidity9am":humidity9am,
            "Pressure3pm":pressure3pm,
            "Pressure9am":pressure9am,
            "Cloud3pm":cloud3pm,
            "Cloud9am":cloud9am,
            "Temp3pm":temp3pm,
            "Temp9am":temp9am,
            "RainToday":raintoday
        }
        res = get_rain_prediction(data)
        st.write(res)
    elif submitted is None:
        st.error("Error")            
        
    

################# DEF ###############
page_names_to_funcs = {
    "Main Page": home_page,
    "Page 2": page_two,
}


selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())


if __name__ == '__main__':
    page_names_to_funcs[selected_page]()
    