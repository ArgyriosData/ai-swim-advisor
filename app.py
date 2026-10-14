import streamlit as st
import requests
from datetime import datetime, timedelta
from google import genai

client = genai.Client()

st.title("🏊 AI Swim Advisor")

# if st.button("Can I swim tomorrow?"):
#     st.write("Checking conditions...")



def get_swim_conditions_tomorrow(latitude=40.58, longitude=22.94):

    target_time = (
        (datetime.now() + timedelta(days=1))
        .strftime("%Y-%m-%d") + "T11:00"
    )

    # Weather Forecast
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,wind_speed_10m,precipitation,cloud_cover"
    }

    weather_data = requests.get(
        weather_url,
        params=weather_params
    ).json()

    # Marine Forecast
    marine_url = "https://marine-api.open-meteo.com/v1/marine"

    marine_params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "sea_surface_temperature"
    }

    marine_data = requests.get(
        marine_url,
        params=marine_params
    ).json()

    idx_weather = weather_data["hourly"]["time"].index(target_time)
    idx_marine = marine_data["hourly"]["time"].index(target_time)

    air_temp = weather_data["hourly"]["temperature_2m"][idx_weather]
    wind_speed = weather_data["hourly"]["wind_speed_10m"][idx_weather]
    precipitation = weather_data["hourly"]["precipitation"][idx_weather]
    cloud_cover = weather_data["hourly"]["cloud_cover"][idx_weather]

    sea_temp = marine_data["hourly"]["sea_surface_temperature"][idx_marine]

    return (
        sea_temp,
        air_temp,
        wind_speed,
        precipitation,
        cloud_cover
    )

def get_swim_recommendation(prompt):
    # STEP 1: Try the best, modern free models first
    preferred_models = ["gemini-2.5-flash", "gemini-2.5-flash-lite"]

    for model in preferred_models:
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt
            )
            return response.text, model
        except Exception:
            continue  # If it fails, try the next preferred model

    # STEP 2: Ultimate Safety Net (Your original loop)
    # If the preferred models fail, search everything else available
    for model_info in client.models.list():
        model = model_info.name

        # Skip text-to-speech models and models we already tried
        if "tts" in model.lower() or model in preferred_models:
            continue

        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt
            )
            return response.text, model
        except Exception:
            continue

    return None, None



# --- User Interface ---
if st.button("Can I swim tomorrow?"):
    
    with st.spinner("🏊 Fetching live weather data and consulting the AI advisor..."):
        # 1. Fetch the data only when the button is actively clicked
        sea_temp, air_temp, wind_speed, precipitation, cloud_cover = get_swim_conditions_tomorrow()
        
        # 2. Build the prompt dynamically using the fetched data
        prompt = f"""
        You are an experienced sea swimming advisor.

        About Argyrios:
        - He regularly swims in the sea throughout the year.
        - Water temperatures above 20°C are considered comfortable.
        - Water temperatures between 17°C and 20°C are considered cool but enjoyable.
        - Water temperatures below 17°C are considered cold.
        - He is comfortable with colder water than the average swimmer.

        Forecast for tomorrow at 11:00:
        Sea temperature: {sea_temp}°C
        Air temperature: {air_temp}°C
        Wind speed: {wind_speed} km/h
        Precipitation: {precipitation} mm
        Cloud cover: {cloud_cover}%

        Evaluation guidelines:
        - Sea temperature is the most important factor.
        - Strong wind reduces comfort and may affect swimming conditions.
        - Rain reduces comfort.
        - Cloud cover has only a small impact on the recommendation.
        - Consider the overall swimming experience, not only safety.

        Return ONLY in the following format:

        Swim Score: X/10

        Recommendation: GO, MAYBE, or NO GO

        Reason:
        Provide a concise explanation in no more than 3 sentences.
        """
        
        # 3. Get LLM recommendation
        response_text, successful_model = get_swim_recommendation(prompt)
        
        # 4. Display Everything
        st.subheader("📊 Tomorrow's Forecast")
        st.write(f"🌊 Sea Temperature: {sea_temp}°C")
        st.write(f"🌡️ Air Temperature: {air_temp}°C")
        st.write(f"💨 Wind Speed: {wind_speed} km/h")
        st.write(f"🌧️ Precipitation: {precipitation} mm")
        st.write(f"☁️ Cloud Cover: {cloud_cover}%")
        
        st.subheader("🤖 Advisor Recommendation")
        st.write(response_text)
