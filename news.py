import streamlit as st
import requests

API_KEY = "268c814b5a844219a10161018252810"  
st.title("🌥️  Smart Weather Prediction App")

st.write(
    "Welcome to the Smart Weather Prediction App.\n\n"
    "Just type the name of any city and get the current weather conditions instantly.\n"
    "You will also receive a clear, human-friendly suggestion based on the live weather —"
    "so you know how to plan your day."
)

st.write("---")

def smart_suggestion(temp_c: float, condition: str, humidity: int) -> str:
    c = (condition or "").lower()

    # 🌧️ Rainy Conditions
    if "rain" in c or "drizzle" in c or "shower" in c:
        return (
            "🌧️ Looks like rain today!\n"
            "You may want to carry an umbrella or a light raincoat.\n"
            "Try not to stay outside for too long if possible.\n"
            "Drive safely — roads may get slippery."
        )

    # ❄️ Snowy Conditions
    if "snow" in c or "sleet" in c:
        return (
            "❄️ Snowy conditions ahead.\n"
            "Dress warmly in layers to stay comfortable.\n"
            "Walk carefully — surfaces can be slippery.\n"
            "Avoid driving if the roads look unsafe."
        )

    # 🌤️ Partly Cloudy (Custom Style)
    if "partly cloudy" in c:
        return (
            "🌤️ The sky is partly cloudy with a cool breeze.\n"
            "It’s a pleasant day — great for a morning walk or a relaxed outing.\n"
            "Clouds may move in and out, so light clothing works best.\n"
            "Keep an eye out — a drizzle could appear later in the evening."
        )

    # ☀️ Clear / Sunny
    if "clear" in c or "sun" in c:
        if temp_c >= 35:
            return (
                "☀️ It’s hot and sunny today!\n"
                "Stay hydrated and try to avoid direct sun for long.\n"
                "Use sunscreen if you go outside.\n"
                "Prefer shade or cooler places when possible."
            )
        if temp_c <= 5:
            return (
                "🌙 Clear but quite cold.\n"
                "Wear warm clothing to stay comfortable.\n"
                "Mornings and evenings may feel even colder.\n"
                "Limit outdoor time if you start feeling uncomfortable."
            )
        return (
            "🌤️ Clear and pleasant weather.\n"
            "Great time for outdoor plans or a walk.\n"
            "Light and comfortable clothing is enough.\n"
            "Enjoy the day and stay hydrated."
        )

    # ☁️ Cloudy / Overcast
    if "cloud" in c or "overcast" in c:
        return (
            "☁️ It's cloudy outside.\n"
            "A light layer of clothing should be fine.\n"
            "There might be a slight chance of drizzle.\n"
            "You can still go out and enjoy your day."
        )

    # 💧 Humid
    if humidity is not None and humidity >= 80:
        if temp_c >= 30:
            return (
                "💧 Warm and quite humid today.\n"
                "It may feel sticky or uncomfortable outdoors.\n"
                "Drink water regularly to stay hydrated.\n"
                "Avoid heavy physical activity outside."
            )
        return (
            "💧 Humidity is on the higher side.\n"
            "The air may feel a bit heavy and warm.\n"
            "Avoid too much exertion if you feel uneasy.\n"
            "Try to stay in cool or ventilated areas."
        )

    # 🌤️ Default
    return (
        "🌤️ Weather looks moderate.\n"
        "You don’t need any special preparation.\n"
        "Dress comfortably and continue your routine.\n"
        "Have a nice day ahead!"
    )


city = st.text_input("🏙️ Enter city name (e.g. London, Delhi, New York)")

if not city.strip():
    st.info("Please enter a city name to get the current weather.")

get = st.button("Get Weather")
if get:
    city_clean = city.strip()
    if not city_clean:
        st.warning("Please enter a city name.")
    else:
        url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city_clean}"
        try:
            res = requests.get(url, timeout=8)
            data = res.json()
        except requests.exceptions.RequestException:
            st.error("Network error while contacting the weather service. Please try again.")
        else:
            if "error" in data:
                st.error("Oops! Couldn’t find that city — please check the spelling and try again 😊")
            else:
                temp_c = data["current"].get("temp_c")
                condition = data["current"].get("condition", {}).get("text", "")
                humidity = data["current"].get("humidity")

                st.subheader(f"📍 Weather in {city_clean.title()}")
                st.write(f"**Temperature:** {temp_c} °C")
                st.write(f"**Condition:** {condition}")
                st.write(f"**Humidity:** {humidity}%")

                suggestion = smart_suggestion(temp_c, condition, humidity)
                st.success("📌 Suggested Plan:")
                for line in suggestion.split("\n"):
                    st.write(line)

                # ---------- Doctor Precautions ----------
                c = (condition or "").lower()
                risky = False
                if any(x in c for x in ["rain","drizzle","shower","snow","sleet","partly cloudy"]) or humidity>=80 or temp_c>=35 or temp_c<=5:
                    risky = True

                if risky:
                    st.warning("🩺 **Doctor's Precautions:**")
                    precautions = []

                    if "rain" in c or "drizzle" in c or "shower" in c:
                        precautions += [
                            "  Keep yourself dry to avoid catching cold.",
                            "  Wash hands after getting wet to reduce infections.",
                            "  Drink warm fluids like tea or soup.",
                        ]

                    if "snow" in c or "sleet" in c or temp_c<=5:
                        precautions += [
                            "  Wear warm layered clothing to prevent hypothermia.",
                            "  Avoid staying outside for long in freezing air.",
                            "  Walk carefully to avoid slips on icy surfaces.",
                        ]

                    if temp_c>=35:
                        precautions += [
                            "  Drink water frequently to avoid dehydration.",
                            "  Avoid direct sunlight during afternoon hours.",
                            "  Prefer light meals; avoid heavy oily food.",
                        ]

                    if humidity>=80:
                        precautions += [
                            "  Stay in ventilated or cool areas.",
                            "  Avoid heavy physical activity outdoors.",
                        ]

                    if "partly cloudy" in c:
                        precautions += [
                            "  If you have allergies, wear a mask — pollen may still circulate.",
                            "  Mild dust may cause sneezing — keep a handkerchief handy.",
                            "  Use moisturizer to prevent dry skin in breezy air.",
                            "  Stay hydrated even if weather feels cool.",
                            "  Protect your eyes from mild UV rays or dust with sunglasses.",
                        ]

                    for p in precautions[:5]:
                        st.write(p)
