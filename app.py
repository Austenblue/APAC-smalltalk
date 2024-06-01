import streamlit as st
import requests
from datetime import datetime
import pytz

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

# Fun facts and number of cities for each country
country_info = {
    'Australia': (
        [
            'Australia is home to the world\'s longest fence, the Dingo Fence.',
            'The Great Barrier Reef is the largest ecosystem in the world.',
            'Australia has over 60 separate wine regions.'
        ], 101),
    'Bangladesh': (
        [
            'Bangladesh is the world\'s second-largest producer of jute.',
            'The Royal Bengal Tiger is the national animal of Bangladesh.',
            'Dhaka is known as the city of mosques.'
        ], 570),
    'Brunei': (
        [
            'Brunei is one of the world\'s wealthiest nations due to its oil and gas reserves.',
            'Brunei has one of the highest rates of car ownership in the world.',
            'The country is known for its pristine rainforests.'
        ], 1),
    'Cambodia': (
        [
            'Cambodia is known for the famous Angkor Wat temple complex.',
            'Tonle Sap Lake in Cambodia is one of the largest freshwater lakes in Asia.',
            'Cambodia’s national flag is the only one in the world to feature a building.'
        ], 26),
    'China': (
        [
            'China is the world\'s most populous country.',
            'The Great Wall of China is one of the Seven Wonders of the World.',
            'China has the world\'s largest high-speed rail network.'
        ], 685),
    'Fiji': (
        [
            'Fiji is made up of over 330 islands.',
            'Fiji has a unique blend of cultures including Indian, Chinese, and European influences.',
            'Fiji is known for its crystal-clear waters and coral reefs.'
        ], 6),
    'India': (
        [
            'India is the largest democracy in the world.',
            'India has the world\'s second-largest population.',
            'The Indian film industry, known as Bollywood, produces the most films annually in the world.'
        ], 4000),
    'Indonesia': (
        [
            'Indonesia is made up of over 17,000 islands.',
            'Indonesia has the world\'s largest Muslim population.',
            'The Komodo dragon, the world\'s largest lizard, is native to Indonesia.'
        ], 93),
    'Japan': (
        [
            'Japan is home to the world\'s oldest company, Kongo Gumi, founded in 578 AD.',
            'Japan has more than 3,000 McDonald\'s restaurants, the largest number outside the US.',
            'The Japanese railway system is one of the most efficient in the world.'
        ], 780),
    'Laos': (
        [
            'Laos is the most heavily bombed country in history.',
            'Laos is known for its stunning waterfalls and rivers.',
            'The Plain of Jars in Laos is an archaeological wonder with thousands of large stone jars.'
        ], 3),
    'Malaysia': (
        [
            'Malaysia is known for its Petronas Twin Towers, once the tallest buildings in the world.',
            'Malaysia is a melting pot of different cultures and ethnicities.',
            'Malaysia is home to the world\'s largest cave chamber, the Sarawak Chamber.'
        ], 150),
    'Maldives': (
        [
            'Maldives is the flattest country in the world.',
            'Maldives is famous for its luxurious overwater bungalows.',
            'The Maldives has a 100% literacy rate among youth.'
        ], 1),
    'Mongolia': (
        [
            'Mongolia is the least densely populated country in the world.',
            'Mongolia is known for its vast steppes and nomadic culture.',
            'The Mongolian Empire was the largest contiguous empire in history.'
        ], 2),
    'Myanmar': (
        [
            'Myanmar is home to the world\'s largest book, the Kuthodaw Pagoda.',
            'Myanmar has some of the most beautiful and ancient pagodas and temples.',
            'Myanmar is known for its vibrant traditional festivals.'
        ], 330),
    'Nepal': (
        [
            'Nepal is home to eight of the world\'s ten highest peaks, including Mount Everest.',
            'Nepal is known for its rich cultural heritage and festivals.',
            'Nepal is the only country in the world with a non-rectangular flag.'
        ], 58),
    'New Zealand': (
        [
            'New Zealand was the first country to give women the right to vote.',
            'New Zealand has more sheep than people.',
            'The country is famous for its breathtaking landscapes and outdoor adventures.'
        ], 5),
    'Pakistan': (
        [
            'Pakistan has the world\'s largest ambulance network, the Edhi Foundation.',
            'Pakistan is home to some of the highest mountains in the world, including K2.',
            'Pakistan is known for its rich history and cultural heritage.'
        ], 625),
    'Papua New Guinea': (
        [
            'Papua New Guinea has over 800 indigenous languages.',
            'The country is one of the most culturally diverse in the world.',
            'Papua New Guinea is known for its unique wildlife and marine biodiversity.'
        ], 8),
    'Philippines': (
        [
            'The Philippines is the world\'s largest producer of coconuts.',
            'The Philippines consists of over 7,000 islands.',
            'The country is known for its beautiful beaches and vibrant festivals.'
        ], 146),
    'Singapore': (
        [
            'Singapore is one of only three surviving city-states in the world.',
            'Singapore is known for its cleanliness and green spaces.',
            'The country has a world-class education and healthcare system.'
        ], 1),
    'South Korea': (
        [
            'South Korea is known for its advanced technology and high-speed internet.',
            'K-pop and Korean dramas have a huge global following.',
            'South Korea is famous for its delicious cuisine, including kimchi and Korean BBQ.'
        ], 79),
    'Sri Lanka': (
        [
            'Sri Lanka is known as the Pearl of the Indian Ocean.',
            'Sri Lanka has a rich history of ancient civilizations and historical sites.',
            'The country is famous for its tea plantations and Ceylon tea.'
        ], 20),
    'Taiwan': (
        [
            'Taiwan is known for its night markets and street food.',
            'Taiwan has the highest density of convenience stores in the world.',
            'Taiwan is a leader in technology and innovation, especially in electronics.'
        ], 23),
    'Thailand': (
        [
            'Thailand is the only Southeast Asian country never to have been colonized by a European power.',
            'Thailand is known for its beautiful beaches and vibrant nightlife.',
            'The country is famous for its delicious cuisine, including Thai curry and pad Thai.'
        ], 117),
    'Vietnam': (
        [
            'Vietnam is the largest exporter of cashew nuts and black pepper in the world.',
            'Vietnam is known for its stunning landscapes, including Ha Long Bay.',
            'The country has a rich cultural heritage and history, including ancient temples and pagodas.'
        ], 85)
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

# Dropdown to select a country on the main page
selected_country = st.selectbox('Select a country', list(apac_capitals.keys()))

if selected_country:
    city, timezone, flag = apac_capitals[selected_country]
    st.header(f"{flag} {city}, {selected_country}")

    # Additional information
    fun_facts, num_cities = country_info[selected_country]
    st.write(f"**Capital City**: {city}")
    st.write(f"**Number of Cities**: {num_cities}")
    
    # Display fun facts
    st.write("**Fun Facts**:")
    for fact in fun_facts:
        st.write(f"- {fact}")

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
