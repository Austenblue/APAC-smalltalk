import streamlit as st
import requests
from datetime import datetime
import pytz
from PIL import Image

# List of APAC capital cities, their respective time zones, and flags
apac_capitals = {
    'Australia': ('Canberra', 'Australia/Sydney', '🇦🇺'),
    'Bangladesh': ('Dhaka', 'Asia/Dhaka', '🇧🇩'),
    'Brunei': ('Bandar Seri Begawan', 'Asia/Brunei', '🇧🇳'),
    'Cambodia': ('Phnom Penh', 'Asia/Phnom_Penh', '🇰🇭'),
    'China': ('Beijing', 'Asia/Shanghai', '🇨🇳'),
    'Fiji': ('Suva', 'Pacific/Fiji', '🇫🇯'),
    'India': ('New Delhi', 'Asia/Kolkata', '🇮🇳'),
    'Indonesia': ('Jakarta', 'Asia/Jakarta', '🇮🇩'),
    'Japan': ('Tokyo', 'Asia/Tokyo', '🇯🇵'),
    'Laos': ('Vientiane', 'Asia/Vientiane', '🇱🇦'),
    'Malaysia': ('Kuala Lumpur', 'Asia/Kuala_Lumpur', '🇲🇾'),
    'Maldives': ('Malé', 'Indian/Maldives', '🇲🇻'),
    'Mongolia': ('Ulaanbaatar', 'Asia/Ulaanbaatar', '🇲🇳'),
    'Myanmar': ('Naypyidaw', 'Asia/Yangon', '🇲🇲'),
    'Nepal': ('Kathmandu', 'Asia/Kathmandu', '🇳🇵'),
    'New Zealand': ('Wellington', 'Pacific/Auckland', '🇳🇿'),
    'Pakistan': ('Islamabad', 'Asia/Karachi', '🇵🇰'),
    'Papua New Guinea': ('Port Moresby', 'Pacific/Port_Moresby', '🇵🇬'),
    'Philippines': ('Manila', 'Asia/Manila', '🇵🇭'),
    'Singapore': ('Singapore', 'Asia/Singapore', '🇸🇬'),
    'South Korea': ('Seoul', 'Asia/Seoul', '🇰🇷'),
    'Sri Lanka': ('Sri Jayawardenepura Kotte', 'Asia/Colombo', '🇱🇰'),
    'Taiwan': ('Taipei', 'Asia/Taipei', '🇹🇼'),
    'Thailand': ('Bangkok', 'Asia/Bangkok', '🇹🇭'),
    'Vietnam': ('Hanoi', 'Asia/Ho_Chi_Minh', '🇻🇳')
}

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

# Function to get weather emoji
def get_weather_emoji(weather_code):
    weather_emojis = {
        0: '☀️',  # Clear sky
        1: '🌤️',  # Mainly clear
        2: '⛅',  # Partly cloudy
        3: '☁️',  # Overcast
        45: '🌫️',  # Fog
        48: '🌫️',  # Depositing rime fog
        51: '🌦️',  # Drizzle: Light intensity
        53: '🌦️',  # Drizzle: Moderate intensity
        55: '🌦️',  # Drizzle: Dense intensity
        56: '🌦️',  # Freezing Drizzle: Light intensity
        57: '🌦️',  # Freezing Drizzle: Dense intensity
        61: '🌧️',  # Rain: Slight intensity
        63: '🌧️',  # Rain: Moderate intensity
        65: '🌧️',  # Rain: Heavy intensity
        66: '🌧️',  # Freezing Rain: Light intensity
        67: '🌧️',  # Freezing Rain: Heavy intensity
        71: '❄️',  # Snow fall: Slight intensity
        73: '❄️',  # Snow fall: Moderate intensity
        75: '❄️',  # Snow fall: Heavy intensity
        77: '❄️',  # Snow grains
        80: '🌨️',  # Rain showers: Slight intensity
        81: '🌨️',  # Rain showers: Moderate intensity
        82: '🌨️',  # Rain showers: Violent intensity
        85: '🌨️',  # Snow showers slight
        86: '🌨️',  # Snow showers heavy
        95: '⛈️',  # Thunderstorm: Slight or moderate
        96: '⛈️',  # Thunderstorm with slight hail
        99: '⛈️'   # Thunderstorm with heavy hail
    }
    return weather_emojis.get(weather_code, '')

# Streamlit app
st.title('Small Talk Dashboard')

# Sidebar to list all countries
st.sidebar.title("Countries in APAC")
selected_country = st.sidebar.selectbox('Select a country', list(apac_capitals.keys()))

if selected_country:
    city, timezone, flag = apac_capitals[selected_country]
    st.header(f"{flag} {city}, {selected_country}")

    # Get current time
    tz = pytz.timezone(timezone)
    local_time = datetime.now(tz)
    formatted_date = local_time.strftime('%Y-%m-%d')
    formatted_time = local_time.strftime('%I:%M:%S %p')
    formatted_day = local_time.strftime('%A')

    st.write(f"Date: {formatted_date}")
    st.write(f"Day: {formatted_day}")
    st.write(f"Time: {formatted_time}")

    # Get weather data
    lat, lon = city_coordinates[city]
    weather_data = get_weather(lat, lon)
    if weather_data.get('current_weather'):
        temp = weather_data['current_weather']['temperature']
        weather_code = weather_data['current_weather']['weathercode']
        weather_emoji = get_weather_emoji(weather_code)
        st.write(f"Temperature: {temp} °C {weather_emoji}")
    else:
        st.write("Weather data not available")
