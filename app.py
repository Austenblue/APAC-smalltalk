import streamlit as st
import requests
from datetime import datetime
import pytz
import time

# List of APAC capital cities and their respective time zones
apac_capitals = {
    'Australia': ('Canberra', 'Australia/Sydney'),
    'Bangladesh': ('Dhaka', 'Asia/Dhaka'),
    'Brunei': ('Bandar Seri Begawan', 'Asia/Brunei'),
    'Cambodia': ('Phnom Penh', 'Asia/Phnom_Penh'),
    'China': ('Beijing', 'Asia/Shanghai'),
    'Fiji': ('Suva', 'Pacific/Fiji'),
    'India': ('New Delhi', 'Asia/Kolkata'),
    'Indonesia': ('Jakarta', 'Asia/Jakarta'),
    'Japan': ('Tokyo', 'Asia/Tokyo'),
    'Laos': ('Vientiane', 'Asia/Vientiane'),
    'Malaysia': ('Kuala Lumpur', 'Asia/Kuala_Lumpur'),
    'Maldives': ('Malé', 'Indian/Maldives'),
    'Mongolia': ('Ulaanbaatar', 'Asia/Ulaanbaatar'),
    'Myanmar': ('Naypyidaw', 'Asia/Yangon'),
    'Nepal': ('Kathmandu', 'Asia/Kathmandu'),
    'New Zealand': ('Wellington', 'Pacific/Auckland'),
    'Pakistan': ('Islamabad', 'Asia/Karachi'),
    'Papua New Guinea': ('Port Moresby', 'Pacific/Port_Moresby'),
    'Philippines': ('Manila', 'Asia/Manila'),
    'Singapore': ('Singapore', 'Asia/Singapore'),
    'South Korea': ('Seoul', 'Asia/Seoul'),
    'Sri Lanka': ('Sri Jayawardenepura Kotte', 'Asia/Colombo'),
    'Taiwan': ('Taipei', 'Asia/Taipei'),
    'Thailand': ('Bangkok', 'Asia/Bangkok'),
    'Vietnam': ('Hanoi', 'Asia/Ho_Chi_Minh')
}

# Function to get weather data
def get_weather(lat, lon):
    base_url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': lat,
        'longitude': lon,
        'current_weather': 'true'
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data

# Coordinates for the APAC capitals (latitude, longitude)
city_coordinates = {
    'Canberra': (-35.282, 149.128),
    'Dhaka': (23.8103, 90.4125),
    'Bandar Seri Begawan': (4.9031, 114.9398),
    'Phnom Penh': (11.5564, 104.9282),
    'Beijing': (39.9042, 116.4074),
    'Suva': (-18.1248, 178.4501),
    'New Delhi': (28.6139, 77.2090),
    'Jakarta': (-6.2088, 106.8456),
    'Tokyo': (35.6895, 139.6917),
    'Vientiane': (17.9757, 102.6331),
    'Kuala Lumpur': (3.1390, 101.6869),
    'Malé': (4.1755, 73.5093),
    'Ulaanbaatar': (47.8864, 106.9057),
    'Naypyidaw': (19.7633, 96.0785),
    'Kathmandu': (27.7172, 85.3240),
    'Wellington': (-41.2865, 174.7762),
    'Islamabad': (33.6844, 73.0479),
    'Port Moresby': (-9.4438, 147.1803),
    'Manila': (14.5995, 120.9842),
    'Singapore': (1.3521, 103.8198),
    'Seoul': (37.5665, 126.9780),
    'Sri Jayawardenepura Kotte': (6.9271, 79.8612),
    'Taipei': (25.0330, 121.5654),
    'Bangkok': (13.7563, 100.5018),
    'Hanoi': (21.0285, 105.8542)
}

# Streamlit app
st.title('Small Talk Dashboard')

# Dropdown to select a country
selected_country = st.selectbox('Select a country', list(apac_capitals.keys()))

if selected_country:
    city, timezone = apac_capitals[selected_country]
    st.header(f"{city}, {selected_country}")

    # Get current time
    tz = pytz.timezone(timezone)
    local_time = datetime.now(tz)
    formatted_date = local_time.strftime('%Y-%m-%d')
    formatted_time = local_time.strftime('%H:%M:%S')

    st.write(f"Local Date: {formatted_date}")
    st.write(f"Local Time: {formatted_time}")
    st.markdown(f"<h1>{local_time.strftime('%H:%M:%S')}</h1>", unsafe_allow_html=True)

    # Get weather data
    lat, lon = city_coordinates[city]
    weather_data = get_weather(lat, lon)
    if weather_data.get('current_weather'):
        temp = weather_data['current_weather']['temperature']
        weather_description = weather_data['current_weather']['weathercode']
        st.write(f"Temperature: {temp} °C")
        st.write(f"Weather: {weather_description}")
    else:
        st.write("Weather data not available")
